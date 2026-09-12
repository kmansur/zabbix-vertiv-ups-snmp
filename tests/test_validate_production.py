from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_production_validator_passes():
    import sys

    sys.path.insert(0, str(ROOT / "tools"))
    import validate_production

    validate_production.run()


def test_no_private_control_or_test_start_objects_in_templates():
    for version in ("7.0", "8.0"):
        text = (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(
            encoding="utf-8"
        )
        assert "1.3.6.1.2.1.33.1.8" not in text
        assert "1.3.6.1.2.1.33.1.7.1.0" not in text  # upsTestId
        assert "1.3.6.1.2.1.33.1.7.2.0" not in text  # upsTestSpinLock


def test_alarm_discovery_is_diagnostic_not_trigger_spam():
    for version in ("7.0", "8.0"):
        data = yaml.safe_load(
            (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(
                encoding="utf-8"
            )
        )
        template = data["zabbix_export"]["templates"][0]
        rule = next(
            r for r in template["discovery_rules"] if r["key"] == "ups.alarm.discovery"
        )
        assert not rule.get("trigger_prototypes")
        for proto in rule["item_prototypes"]:
            assert not proto.get("trigger_prototypes")


def test_field_unsupported_rfc1628_battery_scalars_are_disabled():
    optional_keys = {"ups.battery.current", "ups.battery.temperature"}
    for version in ("7.0", "8.0"):
        data = yaml.safe_load(
            (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(
                encoding="utf-8"
            )
        )
        template = data["zabbix_export"]["templates"][0]
        items = {str(item.get("key")): item for item in template.get("items", [])}
        for key in optional_keys:
            assert items[key]["status"] == "DISABLED"
            assert not items[key].get("triggers")
            assert "noSuchObject" in items[key].get("description", "")


def test_dashboard_does_not_use_unsupported_battery_scalars():
    unsupported = {"ups.battery.current", "ups.battery.temperature"}
    for version in ("7.0", "8.0"):
        data = yaml.safe_load(
            (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(
                encoding="utf-8"
            )
        )
        template = data["zabbix_export"]["templates"][0]
        dashboard = next(
            dashboard
            for dashboard in template.get("dashboards", [])
            if dashboard.get("name") == "Vertiv UPS Overview"
        )
        item_keys = set()
        widget_names = set()
        for page in dashboard.get("pages", []):
            for widget in page.get("widgets", []):
                widget_names.add(str(widget.get("name", "")))
                for field in widget.get("fields", []):
                    if field.get("name") != "itemid.0":
                        continue
                    value = field.get("value") or {}
                    if value.get("key"):
                        item_keys.add(str(value["key"]))

        assert not (item_keys & unsupported)
        assert "vertiv.battery.current" in item_keys
        assert "ups.battery.status" in item_keys
        assert "Battery temperature" not in widget_names
