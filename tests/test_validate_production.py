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
