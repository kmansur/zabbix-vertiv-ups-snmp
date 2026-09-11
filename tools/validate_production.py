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
        errors.append(f"missing production items: {missing}")

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

    if items.get("vertiv.output.load", {}).get("triggers"):
        errors.append("private aggregate output load must not drive triggers")

    temp = items.get("ups.battery.temperature", {})
    temp_expr = " ".join(str(t.get("expression")) for t in temp.get("triggers", []))
    if (
        "{$UPS.BATTERY.TEMP.WARN}" not in temp_expr
        or "{$UPS.BATTERY.TEMP.CRIT}" not in temp_expr
    ):
        errors.append(
            "RFC1628 battery temperature must own production temperature triggers"
        )

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

    # Dashboard must use standard battery temperature and count must not imply
    # severity by multiple count thresholds.
    dashboard = next(
        d
        for d in template.get("dashboards", [])
        if d.get("name") == "Vertiv UPS Overview"
    )
    battery_key = None
    alarm_thresholds = []
    for page in dashboard.get("pages", []):
        for widget in page.get("widgets", []):
            if widget.get("type") != "item":
                continue
            fields = widget.get("fields", [])
            if widget.get("name") == "Battery temperature":
                ref = next(
                    f.get("value") for f in fields if f.get("name") == "itemid.0"
                )
                battery_key = ref.get("key")
            if widget.get("name") == "Active alarms":
                alarm_thresholds = [
                    f
                    for f in fields
                    if str(f.get("name", "")).startswith("thresholds.")
                ]
    if battery_key != "ups.battery.temperature":
        errors.append(
            f"dashboard battery temperature must use RFC1628 item, got {battery_key!r}"
        )
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
        "vertiv.system.name": "NAME",
    }
    for key, expected in inventory_expected.items():
        if items.get(key, {}).get("inventory_link") != expected:
            errors.append(f"inventory link mismatch for {key}: expected {expected}")

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
    if version != "1.5.0":
        raise ProductionValidationError(
            f"production candidate VERSION must be 1.5.0, got {version}"
        )
    for path in TEMPLATE_FILES:
        validate(path)
    print("OK: production-readiness validation passed for Zabbix 7.0 and 8.0 exports")


if __name__ == "__main__":
    try:
        run()
    except ProductionValidationError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
