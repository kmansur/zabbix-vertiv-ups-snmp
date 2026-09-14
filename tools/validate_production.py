"""Production-readiness validation for Vertiv by SNMP."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_FILES = (
    ROOT / "templates/7.0/vertiv-by-snmp.yaml",
    ROOT / "templates/8.0/vertiv-by-snmp.yaml",
)
REQUIRED_KEYS = {
    "ups.snmp.uptime",
    "ups.snmp.sysname",
    "ups.ident.manufacturer",
    "ups.ident.model",
    "ups.ident.ups.software",
    "ups.ident.agent.software",
    "ups.ident.name",
    "ups.battery.current",
    "ups.battery.temperature",
    "ups.test.results.summary",
    "ups.test.results.detail",
    "ups.test.start.time",
    "ups.test.elapsed.time",
}
DISABLED_EXPERIMENTAL_KEYS = {
    "vertiv.input.power.l1",
    "vertiv.input.power.l2",
    "vertiv.input.power.l3",
    "vertiv.input.power.total",
    "vertiv.battery.temperature",
}
DISABLED_OPTIONAL_STANDARD_KEYS = {
    "ups.battery.current",
    "ups.battery.temperature",
}
OBSOLETE_GRAPHS = {
    "UPS: Input phase power",
    "UPS: Power quality counters",
    "UPS: Temperatures",
}


class ProductionValidationError(Exception):
    pass


def _load(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(path: Path) -> None:
    data = _load(path)
    export = data["zabbix_export"]
    template = export["templates"][0]
    items = {str(item.get("key")): item for item in template.get("items", [])}
    errors: list[str] = []

    missing = sorted(REQUIRED_KEYS - set(items))
    if missing:
        errors.append(f"missing production/compatibility items: {missing}")

    uptime = items.get("ups.snmp.uptime", {})
    if any(
        p.get("type") == "DISCARD_UNCHANGED_HEARTBEAT"
        for p in uptime.get("preprocessing", [])
    ):
        errors.append("ups.snmp.uptime must not discard unchanged values")
    expressions = {str(t.get("expression")) for t in uptime.get("triggers", [])}
    if "nodata(/VERTIV by SNMP/ups.snmp.uptime,5m)=1" not in expressions:
        errors.append("missing five-minute SNMP nodata trigger")

    for key in DISABLED_EXPERIMENTAL_KEYS:
        item = items.get(key)
        if item is None:
            errors.append(f"missing retained experimental item {key}")
            continue
        if item.get("status") != "DISABLED":
            errors.append(f"experimental item must be disabled: {key}")
        if item.get("triggers"):
            errors.append(f"experimental item must not have triggers: {key}")

    # The field-validated ITA-20kVA management agent returns noSuchObject for
    # RFC1628 upsBatteryCurrent and upsBatteryTemperature. Keep these standard
    # objects available for other cards/firmwares, but never poll or alert on
    # them by default.
    for key in DISABLED_OPTIONAL_STANDARD_KEYS:
        item = items.get(key)
        if item is None:
            errors.append(f"missing retained optional RFC1628 item {key}")
            continue
        if item.get("status") != "DISABLED":
            errors.append(f"optional unsupported RFC1628 item must be disabled: {key}")
        if item.get("triggers"):
            errors.append(
                f"optional unsupported RFC1628 item must not have triggers: {key}"
            )

    if items.get("vertiv.output.load", {}).get("triggers"):
        errors.append("private aggregate output load must not drive triggers")

    rules = {str(rule.get("key")): rule for rule in template.get("discovery_rules", [])}
    alarm = rules.get("ups.alarm.discovery")
    if alarm is None:
        errors.append("missing RFC1628 active alarm discovery")
    else:
        if "33.1.6.2.1.2" not in str(alarm.get("snmp_oid")):
            errors.append("alarm discovery must use upsAlarmDescr")
        proto_keys = {str(i.get("key")) for i in alarm.get("item_prototypes", [])}
        if proto_keys != {
            "ups.alarm.descr[{#SNMPINDEX}]",
            "ups.alarm.time[{#SNMPINDEX}]",
        }:
            errors.append(f"unexpected alarm prototypes: {sorted(proto_keys)}")

    maps = {str(v.get("name")): v for v in template.get("valuemaps", [])}
    alarm_map = maps.get("UPS RFC1628 alarm description")
    fixture = json.loads(
        (ROOT / "tests/fixtures/rfc1628-alarm-oids.json").read_text(encoding="utf-8")
    )
    actual_map = {
        str(m.get("value")): str(m.get("newvalue"))
        for m in (alarm_map or {}).get("mappings", [])
    }
    if actual_map != fixture:
        errors.append("RFC1628 alarm value map differs from fixture")

    graph_names = {str(graph.get("name")) for graph in export.get("graphs", [])}
    leaked = sorted(graph_names & OBSOLETE_GRAPHS)
    if leaked:
        errors.append(f"obsolete graphs still exported: {leaked}")

    # The default dashboard may only reference battery telemetry confirmed on
    # the field device. Unsupported optional RFC1628 battery scalars must not
    # leak into widgets. Active-alarm count must not imply severity by count.
    dashboard = next(
        d
        for d in template.get("dashboards", [])
        if d.get("name") == "Vertiv UPS Overview"
    )
    dashboard_item_keys: list[str] = []
    alarm_thresholds = []
    for page in dashboard.get("pages", []):
        for widget in page.get("widgets", []):
            if widget.get("type") != "item":
                continue
            fields = widget.get("fields", [])
            for field in fields:
                if field.get("name") == "itemid.0":
                    ref = field.get("value") or {}
                    key = ref.get("key")
                    if key:
                        dashboard_item_keys.append(str(key))
            if widget.get("name") == "Active alarms":
                alarm_thresholds = [
                    f
                    for f in fields
                    if str(f.get("name", "")).startswith("thresholds.")
                ]

    leaked_optional = sorted(set(dashboard_item_keys) & DISABLED_OPTIONAL_STANDARD_KEYS)
    if leaked_optional:
        errors.append(
            f"unsupported optional RFC1628 battery items referenced by dashboard: {leaked_optional}"
        )
    if "vertiv.battery.current" not in dashboard_item_keys:
        errors.append("dashboard must retain field-validated Vertiv battery current")
    if "ups.battery.status" not in dashboard_item_keys:
        errors.append("dashboard must retain RFC1628 battery status")

    thresholds = {str(f.get("name")): str(f.get("value")) for f in alarm_thresholds}
    if thresholds != {"thresholds.0.color": "FFCDD2", "thresholds.0.threshold": "1"}:
        errors.append(
            f"active alarm card thresholds must be any-positive red: {thresholds}"
        )

    inventory_expected = {
        "ups.ident.manufacturer": "VENDOR",
        "vertiv.system.model": "MODEL",
        "vertiv.system.serial": "SERIALNO_A",
        "vertiv.system.firmware": "SOFTWARE",
        "ups.snmp.sysname": "NAME",
    }
    for key, expected in inventory_expected.items():
        if items.get(key, {}).get("inventory_link") != expected:
            errors.append(f"inventory link mismatch for {key}: expected {expected}")

    if items.get("vertiv.system.name", {}).get("inventory_link"):
        errors.append("private Vertiv system name must not populate inventory NAME")

    # Safety: no UPS control branch or Vertiv reboot OID can appear anywhere.
    serialized = path.read_text(encoding="utf-8")
    forbidden = ("1.3.6.1.2.1.33.1.8", "1.3.6.1.4.1.476.1.42.2.5.1")
    for oid in forbidden:
        if oid in serialized:
            errors.append(f"forbidden control OID present: {oid}")

    if errors:
        raise ProductionValidationError(f"{path}:\n- " + "\n- ".join(errors))


def run() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    parts = version.split(".")
    if len(parts) != 3 or not all(part.isdigit() for part in parts):
        raise ProductionValidationError(
            f"production candidate VERSION must be Semantic Versioning, got {version}"
        )
    for path in TEMPLATE_FILES:
        validate(path)
    print(
        f"OK: production-readiness validation passed for repository {version} "
        "and Zabbix 7.0/8.0 exports"
    )


if __name__ == "__main__":
    try:
        run()
    except ProductionValidationError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
