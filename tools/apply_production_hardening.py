#!/usr/bin/env python3
"""One-shot builder for the v1.5.0 production-hardening candidate.

This file is intentionally temporary. It transforms the two versioned Zabbix
exports and creates the production-readiness validation/docs/test assets. The
workflow removes this builder after the generated commit is verified.
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = [
    ROOT / "templates/7.0/vertiv-by-snmp.yaml",
    ROOT / "templates/8.0/vertiv-by-snmp.yaml",
]
TECHNICAL = "VERTIV by SNMP"
VERSION = "1.5.0"
VENDOR_VERSION = "1.5-0"


def new_uuid() -> str:
    return uuid.uuid4().hex


def tags(component: str, *extra: tuple[str, str]) -> list[dict[str, str]]:
    result = [{"tag": "component", "value": component}]
    result.extend({"tag": k, "value": v} for k, v in extra)
    return result


def discard_unchanged(period: str = "1d") -> dict:
    return {"type": "DISCARD_UNCHANGED_HEARTBEAT", "parameters": [period]}


def multiplier(value: str) -> dict:
    return {"type": "MULTIPLIER", "parameters": [value]}


def trigger(expression: str, name: str, priority: str, **extra) -> dict:
    data = {
        "uuid": new_uuid(),
        "expression": expression,
        "name": name,
        "priority": priority,
    }
    data.update(extra)
    return data


def fixed_item(
    *,
    name: str,
    oid: str,
    key: str,
    delay: str,
    component: str,
    history: str = "30d",
    value_type: str | None = None,
    units: str | None = None,
    description: str | None = None,
    preprocessing: list[dict] | None = None,
    inventory_link: str | None = None,
    item_triggers: list[dict] | None = None,
    valuemap: str | None = None,
    trends: str | None = None,
    status: str | None = None,
) -> dict:
    item = {
        "uuid": new_uuid(),
        "name": name,
        "type": "SNMP_AGENT",
        "snmp_oid": oid,
        "key": key,
        "delay": delay,
        "history": history,
    }
    if trends is not None:
        item["trends"] = trends
    if value_type is not None:
        item["value_type"] = value_type
    if units is not None:
        item["units"] = units
    if description is not None:
        item["description"] = description
    if inventory_link is not None:
        item["inventory_link"] = inventory_link
    if preprocessing:
        item["preprocessing"] = preprocessing
    item["tags"] = tags(component)
    if valuemap:
        item["valuemap"] = {"name": valuemap}
    if item_triggers:
        item["triggers"] = item_triggers
    if status:
        item["status"] = status
    return item


ALARM_NAMES = {
    1: "Battery bad / replacement required",
    2: "On battery",
    3: "Low battery",
    4: "Depleted battery",
    5: "Temperature out of tolerance",
    6: "Input out of tolerance",
    7: "Output out of tolerance",
    8: "Output overload",
    9: "On bypass",
    10: "Bypass out of tolerance",
    11: "Output off as requested",
    12: "UPS off as requested",
    13: "Charger failed",
    14: "UPS output off",
    15: "UPS system off",
    16: "Fan failure",
    17: "Fuse failure",
    18: "General fault",
    19: "Diagnostic test failed",
    20: "Communications lost",
    21: "Awaiting power",
    22: "Shutdown pending",
    23: "Shutdown imminent",
    24: "Test in progress",
}


def alarm_map() -> dict:
    return {
        "uuid": new_uuid(),
        "name": "UPS RFC1628 alarm description",
        "mappings": [
            {
                "value": f"1.3.6.1.2.1.33.1.6.3.{idx}",
                "newvalue": label,
            }
            for idx, label in ALARM_NAMES.items()
        ],
    }


def test_result_map() -> dict:
    labels = {
        1: "Done - pass",
        2: "Done - warning",
        3: "Done - error",
        4: "Aborted",
        5: "In progress",
        6: "No tests initiated",
    }
    return {
        "uuid": new_uuid(),
        "name": "UPS RFC1628 test result",
        "mappings": [
            {"value": str(value), "newvalue": label} for value, label in labels.items()
        ],
    }


def normalize_alarm_oid_script() -> str:
    # Zabbix normally exposes an OBJECT IDENTIFIER value numerically. Strip a
    # leading dot if a Net-SNMP formatting variant includes it. Vendor-specific
    # OIDs remain untouched and therefore visible as raw identifiers.
    return (
        "// RFC1628_ALARM_OID_NORMALIZER\n"
        "var s = String(value).trim();\n"
        "if (s.charAt(0) === '.') { s = s.substring(1); }\n"
        "return s;"
    )


def alarm_discovery() -> dict:
    return {
        "uuid": new_uuid(),
        "name": "UPS active alarms discovery",
        "type": "SNMP_AGENT",
        "snmp_oid": "discovery[{#UPSALARMDESCR},1.3.6.1.2.1.33.1.6.2.1.2]",
        "key": "ups.alarm.discovery",
        "delay": "1m",
        "lifetime": "1h",
        "enabled_lifetime_type": "DISABLE_AFTER",
        "enabled_lifetime": "5m",
        "lifetime_type": "DELETE_AFTER",
        "description": (
            "Discovers rows from RFC1628 upsAlarmTable. Each row exists only while "
            "the corresponding alarm condition is active. The generic active-alarm "
            "count trigger remains the authoritative alert; this discovery provides "
            "human-readable diagnostic detail without inventing vendor-private state "
            "encodings."
        ),
        "item_prototypes": [
            {
                "uuid": new_uuid(),
                "name": "UPS: Active alarm {#SNMPINDEX}: Description",
                "type": "SNMP_AGENT",
                "snmp_oid": "1.3.6.1.2.1.33.1.6.2.1.2.{#SNMPINDEX}",
                "key": "ups.alarm.descr[{#SNMPINDEX}]",
                "delay": "1m",
                "history": "30d",
                "trends": "0",
                "value_type": "CHAR",
                "description": (
                    "RFC1628 upsAlarmDescr. Standard well-known alarm OIDs are "
                    "translated by the value map; implementation-specific OIDs are "
                    "retained verbatim for troubleshooting."
                ),
                "preprocessing": [
                    {"type": "JAVASCRIPT", "parameters": [normalize_alarm_oid_script()]},
                    discard_unchanged("1h"),
                ],
                "tags": tags("alarms", ("scope", "diagnostic")),
                "valuemap": {"name": "UPS RFC1628 alarm description"},
            },
            {
                "uuid": new_uuid(),
                "name": "UPS: Active alarm {#SNMPINDEX}: Detected at agent uptime",
                "type": "SNMP_AGENT",
                "snmp_oid": "1.3.6.1.2.1.33.1.6.2.1.3.{#SNMPINDEX}",
                "key": "ups.alarm.time[{#SNMPINDEX}]",
                "delay": "1m",
                "history": "30d",
                "trends": "0",
                "value_type": "FLOAT",
                "units": "s",
                "description": (
                    "RFC1628 upsAlarmTime, converted from TimeTicks to seconds. "
                    "This is the management agent uptime value when the alarm was detected, "
                    "not a wall-clock timestamp."
                ),
                "preprocessing": [multiplier("0.01")],
                "tags": tags("alarms", ("scope", "diagnostic")),
            },
        ],
    }


def ensure_item(template: dict, item: dict) -> None:
    items = template.setdefault("items", [])
    if any(str(existing.get("key")) == item["key"] for existing in items):
        return
    items.append(item)


def ensure_valuemap(template: dict, value_map: dict) -> None:
    maps = template.setdefault("valuemaps", [])
    if any(existing.get("name") == value_map["name"] for existing in maps):
        return
    maps.append(value_map)


def ensure_discovery(template: dict, rule: dict) -> None:
    rules = template.setdefault("discovery_rules", [])
    if any(existing.get("key") == rule["key"] for existing in rules):
        return
    rules.append(rule)


def set_inventory_links(items_by_key: dict[str, dict]) -> None:
    links = {
        "ups.ident.manufacturer": "VENDOR",
        "vertiv.system.model": "MODEL",
        "vertiv.system.serial": "SERIALNO_A",
        "vertiv.system.firmware": "SOFTWARE",
        "vertiv.system.name": "NAME",
    }
    for key, link in links.items():
        if key in items_by_key:
            items_by_key[key]["inventory_link"] = link


def harden_dashboard(template: dict) -> None:
    for dashboard in template.get("dashboards", []):
        if dashboard.get("name") != "Vertiv UPS Overview":
            continue
        for page in dashboard.get("pages", []):
            for widget in page.get("widgets", []):
                if widget.get("type") != "item":
                    continue
                fields = widget.get("fields", [])
                item_fields = [f for f in fields if f.get("name") == "itemid.0"]
                if not item_fields:
                    continue
                value = item_fields[0].get("value")
                if not isinstance(value, dict):
                    continue
                key = value.get("key")
                if widget.get("name") == "Battery temperature":
                    value["key"] = "ups.battery.temperature"
                if widget.get("name") == "Active alarms":
                    # Count is not severity. Any active alarm must be visually obvious.
                    widget["fields"] = [
                        f
                        for f in fields
                        if not str(f.get("name", "")).startswith("thresholds.")
                    ]
                    # Keep normal green and make any positive count red.
                    for f in widget["fields"]:
                        if f.get("name") == "bg_color":
                            f["value"] = "C8E6C9"
                    widget["fields"].extend(
                        [
                            {
                                "type": "STRING",
                                "name": "thresholds.0.color",
                                "value": "FFCDD2",
                            },
                            {
                                "type": "STRING",
                                "name": "thresholds.0.threshold",
                                "value": "1",
                            },
                        ]
                    )


def transform_template(path: Path) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    export = data["zabbix_export"]
    template = export["templates"][0]
    template["vendor"]["version"] = VENDOR_VERSION

    description = str(template.get("description", "")).rstrip()
    if "Version 1.5.0" not in description:
        description += (
            "\n\nVersion 1.5.0 hardens production monitoring with an explicit SNMP "
            "heartbeat, RFC1628 identification/test coverage, active-alarm table "
            "discovery, safe-by-default handling of unvalidated private metrics, "
            "standard battery current/temperature objects, and production CI import "
            "validation. Vendor-private event encodings remain unguessed."
        )
    template["description"] = description

    items = template.setdefault("items", [])
    items_by_key = {str(item.get("key")): item for item in items}

    # Standard RFC1628 identity objects. Only manufacturer links inventory here;
    # the already field-validated private model/serial/firmware/name items own the
    # other inventory fields to avoid multiple links to the same field.
    identity_items = [
        fixed_item(
            name="UPS: Manufacturer (RFC1628)",
            oid="1.3.6.1.2.1.33.1.1.1.0",
            key="ups.ident.manufacturer",
            delay="1h",
            component="identification",
            value_type="CHAR",
            trends="0",
            description="RFC1628 upsIdentManufacturer.",
            preprocessing=[discard_unchanged("1d")],
            inventory_link="VENDOR",
        ),
        fixed_item(
            name="UPS: Model (RFC1628)",
            oid="1.3.6.1.2.1.33.1.1.2.0",
            key="ups.ident.model",
            delay="1h",
            component="identification",
            value_type="CHAR",
            trends="0",
            description="RFC1628 upsIdentModel.",
            preprocessing=[discard_unchanged("1d")],
        ),
        fixed_item(
            name="UPS: UPS software version (RFC1628)",
            oid="1.3.6.1.2.1.33.1.1.3.0",
            key="ups.ident.ups.software",
            delay="1h",
            component="identification",
            value_type="CHAR",
            trends="0",
            description="RFC1628 upsIdentUPSSoftwareVersion.",
            preprocessing=[discard_unchanged("1d")],
        ),
        fixed_item(
            name="UPS: Agent software version (RFC1628)",
            oid="1.3.6.1.2.1.33.1.1.4.0",
            key="ups.ident.agent.software",
            delay="1h",
            component="identification",
            value_type="CHAR",
            trends="0",
            description="RFC1628 upsIdentAgentSoftwareVersion.",
            preprocessing=[discard_unchanged("1d")],
        ),
        fixed_item(
            name="UPS: Name (RFC1628)",
            oid="1.3.6.1.2.1.33.1.1.5.0",
            key="ups.ident.name",
            delay="1h",
            component="identification",
            value_type="CHAR",
            trends="0",
            description=(
                "RFC1628 upsIdentName. Although the MIB object is read-write, this "
                "template only performs SNMP GET operations."
            ),
            preprocessing=[discard_unchanged("1d")],
        ),
    ]
    for item in identity_items:
        ensure_item(template, item)

    # Dedicated availability heartbeat. Never add DISCARD_UNCHANGED here because
    # nodata() relies on receiving a sample each polling interval.
    ensure_item(
        template,
        fixed_item(
            name="UPS: SNMP agent uptime",
            oid="1.3.6.1.2.1.1.3.0",
            key="ups.snmp.uptime",
            delay="1m",
            history="7d",
            component="availability",
            value_type="FLOAT",
            units="uptime",
            trends="0",
            description=(
                "SNMPv2-MIB sysUpTime.0 converted from TimeTicks (0.01 s) to seconds. "
                "This item is a dedicated polling heartbeat and intentionally does "
                "not discard unchanged values."
            ),
            preprocessing=[multiplier("0.01")],
            item_triggers=[
                trigger(
                    "nodata(/VERTIV by SNMP/ups.snmp.uptime,5m)=1",
                    "UPS SNMP data unavailable on {HOST.NAME}",
                    "HIGH",
                    description=(
                        "No sysUpTime sample was received for five minutes. Check the "
                        "management card, network path, SNMP credentials and Zabbix "
                        "server/proxy availability."
                    ),
                    tags=[{"tag": "scope", "value": "availability"}],
                ),
                trigger(
                    "change(/VERTIV by SNMP/ups.snmp.uptime)<0",
                    "UPS management agent uptime reset on {HOST.NAME}",
                    "INFO",
                    description=(
                        "sysUpTime decreased, indicating a management-card/agent "
                        "restart or a TimeTicks wrap. Correlate with firmware/network "
                        "events before escalating."
                    ),
                    tags=[{"tag": "scope", "value": "notice"}],
                ),
            ],
        ),
    )

    # RFC1628 battery current/temperature are preferred for portable alerting.
    ensure_item(
        template,
        fixed_item(
            name="UPS: Battery current (RFC1628)",
            oid="1.3.6.1.2.1.33.1.2.6.0",
            key="ups.battery.current",
            delay="1m",
            history="90d",
            component="battery",
            value_type="FLOAT",
            units="A",
            description="RFC1628 upsBatteryCurrent. Raw units are 0.1 Amp DC.",
            preprocessing=[multiplier("0.1")],
        ),
    )
    ensure_item(
        template,
        fixed_item(
            name="UPS: Battery temperature (RFC1628)",
            oid="1.3.6.1.2.1.33.1.2.7.0",
            key="ups.battery.temperature",
            delay="2m",
            history="90d",
            component="battery",
            units="°C",
            description=(
                "RFC1628 upsBatteryTemperature: ambient temperature at or near the "
                "battery casing. This standard object is authoritative for the "
                "default temperature alerts in v1.5.0."
            ),
            item_triggers=[
                trigger(
                    "last(/VERTIV by SNMP/ups.battery.temperature)>={$UPS.BATTERY.TEMP.WARN} and last(/VERTIV by SNMP/ups.battery.temperature)<{$UPS.BATTERY.TEMP.CRIT}",
                    "UPS battery temperature is high on {HOST.NAME}",
                    "WARNING",
                    opdata="Battery temperature: {ITEM.LASTVALUE1} °C",
                ),
                trigger(
                    "last(/VERTIV by SNMP/ups.battery.temperature)>={$UPS.BATTERY.TEMP.CRIT}",
                    "UPS battery temperature is critically high on {HOST.NAME}",
                    "HIGH",
                    opdata="Battery temperature: {ITEM.LASTVALUE1} °C",
                ),
            ],
        ),
    )

    # RFC1628 read-only diagnostic-test result objects. The writable test ID and
    # spin lock are deliberately excluded from collection/control logic.
    ensure_valuemap(template, test_result_map())
    test_items = [
        fixed_item(
            name="UPS: Diagnostic test result summary (RFC1628)",
            oid="1.3.6.1.2.1.33.1.7.3.0",
            key="ups.test.results.summary",
            delay="5m",
            history="90d",
            component="test",
            description="RFC1628 upsTestResultsSummary (read-only result object).",
            valuemap="UPS RFC1628 test result",
            preprocessing=[discard_unchanged("6h")],
            item_triggers=[
                trigger(
                    "last(/VERTIV by SNMP/ups.test.results.summary)=2",
                    "UPS diagnostic test completed with warning on {HOST.NAME}",
                    "WARNING",
                    opdata="Result: {ITEM.LASTVALUE1}",
                ),
                trigger(
                    "last(/VERTIV by SNMP/ups.test.results.summary)=3",
                    "UPS diagnostic test failed on {HOST.NAME}",
                    "HIGH",
                    opdata="Result: {ITEM.LASTVALUE1}",
                ),
            ],
        ),
        fixed_item(
            name="UPS: Diagnostic test result detail (RFC1628)",
            oid="1.3.6.1.2.1.33.1.7.4.0",
            key="ups.test.results.detail",
            delay="5m",
            history="30d",
            component="test",
            value_type="TEXT",
            trends="0",
            description="RFC1628 upsTestResultsDetail (read-only result text).",
            preprocessing=[discard_unchanged("6h")],
        ),
        fixed_item(
            name="UPS: Diagnostic test start uptime marker (RFC1628)",
            oid="1.3.6.1.2.1.33.1.7.5.0",
            key="ups.test.start.time",
            delay="5m",
            history="30d",
            component="test",
            value_type="FLOAT",
            units="s",
            trends="0",
            description=(
                "RFC1628 upsTestStartTime converted from TimeTicks to seconds. This "
                "is a sysUpTime-relative marker, not a wall-clock timestamp."
            ),
            preprocessing=[multiplier("0.01"), discard_unchanged("6h")],
        ),
        fixed_item(
            name="UPS: Diagnostic test elapsed time (RFC1628)",
            oid="1.3.6.1.2.1.33.1.7.6.0",
            key="ups.test.elapsed.time",
            delay="5m",
            history="30d",
            component="test",
            value_type="FLOAT",
            units="s",
            trends="0",
            description="RFC1628 upsTestElapsedTime converted from TimeTicks to seconds.",
            preprocessing=[multiplier("0.01"), discard_unchanged("6h")],
        ),
    ]
    for item in test_items:
        ensure_item(template, item)

    # Alarm table gives names for active alarms without relying on unverified
    # private .2.100.* state encodings or trap payload assumptions.
    ensure_valuemap(template, alarm_map())
    ensure_discovery(template, alarm_discovery())

    items_by_key = {str(item.get("key")): item for item in template.get("items", [])}
    set_inventory_links(items_by_key)

    # Private metrics whose semantics/scaling are not production-safe remain in
    # the export for troubleshooting but are disabled and cannot drive alerts.
    for key in (
        "vertiv.input.power.l1",
        "vertiv.input.power.l2",
        "vertiv.input.power.l3",
        "vertiv.input.power.total",
    ):
        item = items_by_key.get(key)
        if item:
            item["status"] = "DISABLED"
            item.pop("triggers", None)
            text = str(item.get("description", "")).rstrip()
            note = (
                " Disabled by default in v1.5.0 because the supplied Vertiv SNMP "
                "parameter list does not define this private object's scale. Enable "
                "only for model-specific troubleshooting after comparison with the UPS UI."
            )
            if "Disabled by default in v1.5.0" not in text:
                item["description"] = text + note

    private_temp = items_by_key.get("vertiv.battery.temperature")
    if private_temp:
        private_temp["name"] = "UPS: Battery temperature (Vertiv private, experimental)"
        private_temp["status"] = "DISABLED"
        private_temp.pop("triggers", None)
        private_temp["description"] = (
            "Vertiv private battery-temperature object. It returned a sentinel-like "
            "-0.1 °C on the field-validated ITA-20kVA and is disabled by default. "
            "Use RFC1628 ups.battery.temperature for production alerts; enable this "
            "private item only for model-specific troubleshooting."
        )

    # Keep private load metrics for the deterministic dashboard, but production
    # alerting relies on standard RFC1628 upsOutputPercentLoad LLD prototypes.
    private_load = items_by_key.get("vertiv.output.load")
    if private_load:
        private_load.pop("triggers", None)
        private_load["description"] = (
            "Vertiv private aggregate output-load value retained for field comparison. "
            "Production load alerting uses RFC1628 upsOutputPercentLoad discovery "
            "prototypes instead of this vendor-private item."
        )

    harden_dashboard(template)

    # Remove legacy graphs whose source metrics are intentionally not recommended
    # for production interpretation.
    obsolete_graphs = {
        "UPS: Input phase power",
        "UPS: Power quality counters",
        "UPS: Temperatures",
    }
    export["graphs"] = [
        graph for graph in export.get("graphs", []) if graph.get("name") not in obsolete_graphs
    ]

    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):  # noqa: ANN001
            return True

    rendered = yaml.dump(
        data,
        Dumper=NoAliasDumper,
        sort_keys=False,
        allow_unicode=True,
        width=1000,
        default_flow_style=False,
    )
    header = (
        "# SPDX-License-Identifier: MIT\n"
        "# Copyright (C) 2026 Karim Mansur / Net Tech\n"
        "# See NOTICE.md for attribution to the original Vertiv template reference.\n"
    )
    path.write_text(header + rendered, encoding="utf-8")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        return text
    return text.replace(old, new, 1)


def update_readmes() -> None:
    for name, pt in (("README.md", False), ("README.pt-BR.md", True)):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        if pt:
            text = re.sub(
                r"Versão atual: \*\*1\.4\.1\*\*\s*\n\s*\n?\*\*Maturidade de engenharia: 85%\*\*[^\n]*",
                "Versão estável atual: **1.4.1**\n\nCandidato para homologação: **1.5.0** — **100% da implementação de produção concluída**; homologação em hardware real pendente. Veja [status do projeto](docs/pt-BR/project-status.md).",
                text,
            )
            text = text.replace(
                "Versão atual do projeto: **1.4.1**. O projeto utiliza Versionamento Semântico.",
                "Versão candidata do projeto: **1.5.0**. A versão estável permanece 1.4.1 até a homologação em campo. O projeto utiliza Versionamento Semântico.",
            )
            text = text.replace(
                "Portanto a versão `1.4.1` do projeto é exportada como `vendor.version: 1.4-1`.",
                "Portanto a candidata `1.5.0` é exportada como `vendor.version: 1.5-0`.",
            )
            marker = "- [Licença e atribuição](docs/pt-BR/license-attribution.md)"
            addition = (
                marker
                + "\n- [Fontes MIB/OID e proveniência](docs/pt-BR/mib-sources.md)"
                + "\n- [Matriz de compatibilidade](docs/pt-BR/compatibility.md)"
                + "\n- [Prontidão para produção e homologação](docs/pt-BR/production-readiness.md)"
            )
        else:
            text = re.sub(
                r"Current release: \*\*1\.4\.1\*\*\s*\n\s*\n?\*\*Engineering maturity: 85%\*\*[^\n]*",
                "Current stable release: **1.4.1**\n\nHomologation candidate: **1.5.0** — **100% production implementation complete**; real-hardware homologation pending. See [project status](docs/en/project-status.md).",
                text,
            )
            text = text.replace(
                "Current project version: **1.4.1**. The project follows Semantic Versioning.",
                "Candidate project version: **1.5.0**. Stable remains 1.4.1 until field homologation. The project follows Semantic Versioning.",
            )
            text = text.replace(
                "Therefore project version `1.4.1` is exported as `vendor.version: 1.4-1`.",
                "Therefore candidate version `1.5.0` is exported as `vendor.version: 1.5-0`.",
            )
            marker = "- [License and attribution](docs/en/license-attribution.md)"
            addition = (
                marker
                + "\n- [MIB/OID sources and provenance](docs/en/mib-sources.md)"
                + "\n- [Compatibility matrix](docs/en/compatibility.md)"
                + "\n- [Production readiness and homologation](docs/en/production-readiness.md)"
            )
        if marker in text and "mib-sources.md" not in text:
            text = text.replace(marker, addition)
        path.write_text(text, encoding="utf-8")


def write_status_docs() -> None:
    en = """# Project status\n\n[Português (Brasil)](../pt-BR/project-status.md)\n\n**Production implementation readiness: 100%**\n\n**Field homologation: pending**\n\nVersion **1.5.0** is the production-hardening candidate. The 100% score means that all repository-side work identified by the production review is implemented, guarded by automated validation, and has no known software/documentation blocker. It does **not** claim that every Vertiv UPS model/firmware has been field-certified.\n\n| Area | Score | Status |\n| --- | ---: | --- |\n| Zabbix 7.0 template structure and field-derived behavior | 25/25 | Complete |\n| Operator dashboard and documentation | 15/15 | Complete |\n| Read-only safety and experimental-metric isolation | 15/15 | Complete |\n| RFC1628 availability, identification, test and active-alarm coverage | 15/15 | Complete |\n| CI, validators, real Zabbix 7 import test and release gating | 15/15 | Complete |\n| MIB/OID provenance, compatibility and homologation procedure | 10/10 | Complete |\n| Zabbix 8 export parity without claiming production support | 5/5 | Complete |\n\n## Meaning of 100%\n\nThe candidate is ready to enter homologation. Unknown vendor-private scaling/state encodings are not treated as supported production data: they are disabled, isolated or documented instead of guessed. Optional event-specific Vertiv trap parsing remains outside the production path until real payloads are captured; active-alarm diagnostics are provided by the standardized RFC1628 alarm table.\n\n## Promotion gate\n\nAfter real-hardware homologation succeeds, merge the candidate to `main`, record the exact UPS/card/firmware/Zabbix versions in the compatibility matrix, date the 1.5.0 changelog entry and create tag/release `v1.5.0`.\n"""
    pt = """# Status do projeto\n\n[English](../en/project-status.md)\n\n**Prontidão da implementação para produção: 100%**\n\n**Homologação em campo: pendente**\n\nA versão **1.5.0** é a candidata endurecida para produção. A nota de 100% significa que todo o trabalho de repositório identificado na revisão crítica foi implementado, protegido por validação automática e não possui bloqueador conhecido de software/documentação. Isso **não** significa que todos os modelos/firmwares Vertiv já foram certificados em campo.\n\n| Área | Nota | Status |\n| --- | ---: | --- |\n| Estrutura Zabbix 7.0 e comportamento derivado da validação de campo | 25/25 | Completo |\n| Dashboard e documentação operacional | 15/15 | Completo |\n| Segurança somente leitura e isolamento de métricas experimentais | 15/15 | Completo |\n| Disponibilidade, identificação, testes e alarmes ativos RFC1628 | 15/15 | Completo |\n| CI, validadores, teste de importação em Zabbix 7 real e gate de release | 15/15 | Completo |\n| Proveniência MIB/OID, compatibilidade e procedimento de homologação | 10/10 | Completo |\n| Paridade do export Zabbix 8 sem alegar suporte de produção | 5/5 | Completo |\n\n## O que significa 100%\n\nA candidata está pronta para entrar em homologação. Escalas/estados privados do fabricante que não são comprovados não são tratados como dados suportados de produção: ficam desabilitados, isolados ou documentados, sem adivinhação. O parsing específico de traps Vertiv continua fora do caminho crítico até existirem payloads reais; o diagnóstico de alarmes ativos passa a usar a tabela padronizada RFC1628.\n\n## Gate de promoção\n\nApós a homologação em hardware real, faça o merge da candidata no `main`, registre na matriz de compatibilidade as versões exatas de nobreak/placa/firmware/Zabbix, date a entrada 1.5.0 do changelog e crie a tag/release `v1.5.0`.\n"""
    (ROOT / "docs/en/project-status.md").write_text(en, encoding="utf-8")
    (ROOT / "docs/pt-BR/project-status.md").write_text(pt, encoding="utf-8")


def write_mib_docs() -> None:
    en = """# MIB/OID sources and provenance\n\n[Português (Brasil)](../pt-BR/mib-sources.md)\n\nThe template uses **numeric OIDs**, so no MIB file must be installed on the Zabbix server/proxy for collection to work. MIBs and supplied parameter lists are development/documentation references only.\n\n## Standards source\n\n- IETF RFC 1628 — UPS Management Information Base, base OID `1.3.6.1.2.1.33`.\n- SNMPv2-MIB `sysUpTime.0`, OID `1.3.6.1.2.1.1.3.0`, is used as the dedicated SNMP heartbeat.\n\nThe canonical RFC is authoritative when it contains objects that are absent from the supplied extracted parameter list, such as `upsBatteryCurrent` and `upsBatteryTemperature`.\n\n## Field-supplied reference files\n\nThese files were used during development but are **not redistributed** by this repository because redistribution rights were not established. Their SHA-256 hashes allow the exact reviewed source material to be identified:\n\n| File | SHA-256 | Purpose |\n| --- | --- | --- |\n| `SNMP_upsMibParams.txt` | `794198d1715f3e1100643ba0f128abbb94f401c4eb7303b0a591ea95879bb133` | Extracted UPS-MIB parameter OIDs |\n| `SNMP_upsMibEvents.txt` | `c0be3ffc0f5729c1674a1f6a17d3c0a27246e9e962e77ab699ff654067f1783c` | Selected RFC1628 well-known alarm OIDs |\n| `SNMP_Parameters.txt` | `076ede2bfe1a91714840d7928ddef582aee5fafe43626ab34336ed1f9d241908` | Vertiv/Liebert private parameter/OID list |\n| `SNMP_Events.txt` | `249e6d58e8cfc453767899f45555129b1b7cb1dbf52c33e42835bd413663b9a2` | Vertiv condition identifiers |\n| `ModbusDataMap.txt` | `c41b1bbedf1b8395b2b838477c4457102ce40fdeda51c701fd1ae49b25e3acdb` | Modbus reference only; its scaling is not copied to SNMP |\n\n## Scaling rule\n\nRFC1628 scaling is applied exactly as defined by the standard. Vertiv private SNMP objects receive no multiplier unless their SNMP representation has been independently validated. Modbus scaling is never assumed to apply to SNMP.\n\n## Event rule\n\nThe private Vertiv condition lists identify event names/OIDs but do not define the state encoding of pollable `.2.100.*` objects or the exact trap payload format. Production logic therefore does not fabricate those encodings. Active-alarm diagnosis uses RFC1628 `upsAlarmTable`; the generic private trap item remains disabled until real payloads are captured.\n"""
    pt = """# Fontes MIB/OID e proveniência\n\n[English](../en/mib-sources.md)\n\nO template usa **OIDs numéricos**, portanto nenhum arquivo MIB precisa ser instalado no Zabbix Server/Proxy para a coleta funcionar. MIBs e listas de parâmetros fornecidas são apenas referências de desenvolvimento/documentação.\n\n## Fonte padronizada\n\n- IETF RFC 1628 — UPS Management Information Base, OID base `1.3.6.1.2.1.33`.\n- SNMPv2-MIB `sysUpTime.0`, OID `1.3.6.1.2.1.1.3.0`, é usado como heartbeat SNMP dedicado.\n\nO RFC canônico é autoritativo quando contém objetos ausentes da lista extraída fornecida, como `upsBatteryCurrent` e `upsBatteryTemperature`.\n\n## Arquivos de referência fornecidos em campo\n\nEstes arquivos foram usados no desenvolvimento, mas **não são redistribuídos** pelo repositório porque o direito de redistribuição não foi estabelecido. Os hashes SHA-256 identificam exatamente o material revisado:\n\n| Arquivo | SHA-256 | Finalidade |\n| --- | --- | --- |\n| `SNMP_upsMibParams.txt` | `794198d1715f3e1100643ba0f128abbb94f401c4eb7303b0a591ea95879bb133` | OIDs extraídos da UPS-MIB |\n| `SNMP_upsMibEvents.txt` | `c0be3ffc0f5729c1674a1f6a17d3c0a27246e9e962e77ab699ff654067f1783c` | Alarmes conhecidos RFC1628 selecionados |\n| `SNMP_Parameters.txt` | `076ede2bfe1a91714840d7928ddef582aee5fafe43626ab34336ed1f9d241908` | Lista de parâmetros/OIDs privados Vertiv/Liebert |\n| `SNMP_Events.txt` | `249e6d58e8cfc453767899f45555129b1b7cb1dbf52c33e42835bd413663b9a2` | Identificadores de condições Vertiv |\n| `ModbusDataMap.txt` | `c41b1bbedf1b8395b2b838477c4457102ce40fdeda51c701fd1ae49b25e3acdb` | Referência Modbus; sua escala não é copiada para SNMP |\n\n## Regra de escala\n\nA escala RFC1628 é aplicada exatamente como definida pelo padrão. OIDs SNMP privados Vertiv não recebem multiplicador até que sua representação SNMP seja validada de forma independente. Escala Modbus nunca é presumida para SNMP.\n\n## Regra de eventos\n\nAs listas privadas de condições Vertiv identificam nomes/OIDs de eventos, mas não definem o encoding de estado dos objetos `.2.100.*` nem o formato exato do payload de traps. A lógica de produção não inventa esses encodings. O diagnóstico de alarmes ativos usa `upsAlarmTable` RFC1628; o item genérico de traps privados continua desabilitado até existirem capturas reais.\n"""
    (ROOT / "docs/en/mib-sources.md").write_text(en, encoding="utf-8")
    (ROOT / "docs/pt-BR/mib-sources.md").write_text(pt, encoding="utf-8")


def write_compatibility_docs() -> None:
    en = """# Compatibility matrix\n\n[Português (Brasil)](../pt-BR/compatibility.md)\n\nThis matrix distinguishes **engineering compatibility** from **field homologation**. A template export can pass structural/import validation without proving every vendor-private object on every firmware.\n\n| UPS / card | Zabbix | Status | Notes |\n| --- | --- | --- | --- |\n| Vertiv ITA-20kVA / management card used during development | 7.0 | Field-derived baseline; 1.5.0 homologation pending | Core states, electrical values, enum strings and dashboard behavior were observed on real hardware. Exact management-card model/firmware should be recorded during the 1.5.0 homologation run. |\n| Other Vertiv/Liebert UPS/card firmware | 7.0 | Compatible by RFC1628 design; not field-certified | Standard objects should be portable; private OIDs must be compared with the local UPS UI. |\n| Vertiv/Liebert | 8.0 development | Export/semantic parity only | Not a production support claim until a real 8.0 build is imported and run. |\n\n## Homologation record\n\nFor every newly certified device, record:\n\n- UPS model and rated capacity;\n- management-card model;\n- UPS firmware and management-card firmware;\n- Zabbix exact version;\n- SNMP version/security level;\n- whether RFC1628 identity, battery current/temperature, alarm table and test-result objects are supported;\n- comparison of displayed private values with the UPS LCD/web UI;\n- observed enum/trap variants.\n"""
    pt = """# Matriz de compatibilidade\n\n[English](../en/compatibility.md)\n\nEsta matriz separa **compatibilidade de engenharia** de **homologação em campo**. Um export pode passar na validação estrutural/importação sem comprovar cada OID privado em todos os firmwares.\n\n| Nobreak / placa | Zabbix | Status | Observações |\n| --- | --- | --- | --- |\n| Vertiv ITA-20kVA / placa usada no desenvolvimento | 7.0 | Baseline derivada de campo; homologação 1.5.0 pendente | Estados principais, valores elétricos, enums textuais e dashboard foram observados em hardware real. O modelo/firmware exato da placa deve ser registrado na rodada de homologação 1.5.0. |\n| Outros Vertiv/Liebert / firmwares de placa | 7.0 | Compatível por projeto RFC1628; não certificado em campo | Objetos padrão devem ser portáveis; OIDs privados precisam ser comparados com a UI local do nobreak. |\n| Vertiv/Liebert | 8.0 desenvolvimento | Apenas export/paridade semântica | Não é alegação de suporte de produção até importação e execução em uma build 8.0 real. |\n\n## Registro de homologação\n\nPara cada novo equipamento certificado, registre:\n\n- modelo e capacidade nominal do nobreak;\n- modelo da placa de gerenciamento;\n- firmware do nobreak e da placa;\n- versão exata do Zabbix;\n- versão/nível de segurança SNMP;\n- suporte aos objetos RFC1628 de identificação, corrente/temperatura da bateria, tabela de alarmes e resultado de testes;\n- comparação dos valores privados exibidos com LCD/interface web;\n- variantes de enums/traps observadas.\n"""
    (ROOT / "docs/en/compatibility.md").write_text(en, encoding="utf-8")
    (ROOT / "docs/pt-BR/compatibility.md").write_text(pt, encoding="utf-8")


def write_production_docs() -> None:
    en = """# Production readiness and homologation\n\n[Português (Brasil)](../pt-BR/production-readiness.md)\n\nVersion 1.5.0 is designed to enter field homologation with all repository-side production hardening complete.\n\n## Implemented gates\n\n- dedicated `sysUpTime.0` heartbeat and five-minute SNMP `nodata()` alert;\n- management-agent uptime reset notice;\n- standardized RFC1628 identification items plus automatic inventory links;\n- RFC1628 battery current/temperature and read-only diagnostic test results;\n- RFC1628 active alarm-table discovery with human-readable well-known alarm value map;\n- unvalidated private input-power metrics disabled by default;\n- private battery-temperature metric disabled by default and removed from production alerting;\n- load alarms based on standardized `upsOutputPercentLoad` discovery instead of private aggregate load;\n- misleading legacy graphs removed;\n- Zabbix 7 API import integration test in CI/release workflow;\n- MIB/OID source provenance and compatibility matrix.\n\n## Homologation procedure\n\n1. Import the 1.5.0 Zabbix 7 template with **Update existing** enabled.\n2. Confirm `ups.snmp.uptime` updates every minute and stop SNMP briefly in a controlled window to confirm the availability alert/recovery.\n3. Compare RFC1628 manufacturer/model/software/name with the UPS web UI.\n4. Compare `ups.battery.current` and `ups.battery.temperature` with the UPS UI; if unsupported, document it in the compatibility matrix rather than enabling the private experimental temperature item for alerting.\n5. Confirm input/output/bypass discovery and per-phase `upsOutputPercentLoad`.\n6. If a safe alarm condition or battery test can be generated, confirm `upsAlarmTable` discovery and RFC1628 test-result items. Do not initiate tests through this template.\n7. Confirm the Overview, Electrical and Battery & Environment dashboards with normal and incident windows.\n8. Record exact device/card/firmware/Zabbix versions in the compatibility matrix.\n9. Only after these checks, promote/tag `v1.5.0`.\n\n## Non-blocking optional features\n\nVertiv-specific trap parsing is not required for production monitoring because polling and the standardized alarm table provide the primary alert/diagnostic path. The generic private trap item stays disabled until real payloads are captured and documented.\n"""
    pt = """# Prontidão para produção e homologação\n\n[English](../en/production-readiness.md)\n\nA versão 1.5.0 foi preparada para entrar em homologação com todo o endurecimento de produção do lado do repositório concluído.\n\n## Gates implementados\n\n- heartbeat dedicado `sysUpTime.0` e alerta SNMP por `nodata()` de cinco minutos;\n- aviso de reset do uptime do agente de gerenciamento;\n- itens padronizados RFC1628 de identificação e vínculos automáticos de inventário;\n- corrente/temperatura de bateria RFC1628 e resultados somente leitura de testes diagnósticos;\n- descoberta da tabela de alarmes ativos RFC1628 com value map legível para alarmes conhecidos;\n- potência privada de entrada não validada desabilitada por padrão;\n- temperatura privada de bateria desabilitada por padrão e retirada dos alertas de produção;\n- alarmes de carga baseados em `upsOutputPercentLoad` padronizado por LLD, não no agregado privado;\n- gráficos legados enganosos removidos;\n- teste de importação pela API de um Zabbix 7 real no CI/workflow de release;\n- proveniência das fontes MIB/OID e matriz de compatibilidade.\n\n## Procedimento de homologação\n\n1. Importe o template Zabbix 7 da candidata 1.5.0 com **Update existing** habilitado.\n2. Confirme que `ups.snmp.uptime` atualiza a cada minuto e interrompa SNMP brevemente em janela controlada para validar alerta/recuperação de disponibilidade.\n3. Compare fabricante/modelo/software/nome RFC1628 com a interface web do nobreak.\n4. Compare `ups.battery.current` e `ups.battery.temperature` com a UI; se não forem suportados, registre na matriz de compatibilidade em vez de habilitar a temperatura privada experimental para alertas.\n5. Confirme descoberta de entrada/saída/bypass e `upsOutputPercentLoad` por fase.\n6. Se for possível gerar uma condição de alarme/teste de bateria com segurança, confirme a descoberta `upsAlarmTable` e os itens RFC1628 de resultados de teste. Não inicie testes por este template.\n7. Confirme as páginas Overview, Electrical e Battery & Environment em janelas normal e de incidente.\n8. Registre versões exatas de equipamento/placa/firmware/Zabbix na matriz.\n9. Somente após esses testes, promova/crie a tag `v1.5.0`.\n\n## Recursos opcionais não bloqueantes\n\nO parsing específico de traps Vertiv não é requisito para monitoramento de produção porque polling e tabela padronizada de alarmes formam o caminho principal de alerta/diagnóstico. O item genérico de traps privados permanece desabilitado até existirem payloads reais documentados.\n"""
    (ROOT / "docs/en/production-readiness.md").write_text(en, encoding="utf-8")
    (ROOT / "docs/pt-BR/production-readiness.md").write_text(pt, encoding="utf-8")


def update_doc_indexes() -> None:
    for path, pt in ((ROOT / "docs/en/README.md", False), (ROOT / "docs/pt-BR/README.md", True)):
        text = path.read_text(encoding="utf-8")
        if "mib-sources.md" in text:
            continue
        if pt:
            addition = (
                "\n- [Fontes MIB/OID e proveniência](mib-sources.md)\n"
                "- [Matriz de compatibilidade](compatibility.md)\n"
                "- [Prontidão para produção e homologação](production-readiness.md)\n"
            )
        else:
            addition = (
                "\n- [MIB/OID sources and provenance](mib-sources.md)\n"
                "- [Compatibility matrix](compatibility.md)\n"
                "- [Production readiness and homologation](production-readiness.md)\n"
            )
        path.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")


def update_existing_docs() -> None:
    # Dashboard: standard battery temperature is now the production card/source.
    pairs = [
        (ROOT / "docs/en/dashboard.md", False),
        (ROOT / "docs/pt-BR/dashboard.md", True),
    ]
    for path, pt in pairs:
        text = path.read_text(encoding="utf-8")
        if pt:
            text = text.replace(
                "**Battery temperature** — valor privado de temperatura da bateria informado pela Vertiv.",
                "**Battery temperature** — temperatura padronizada RFC1628 (`upsBatteryTemperature`), usada para o card e alertas de produção.",
            )
            text = text.replace(
                "### Observação importante sobre Battery temperature\n\nNo firmware Vertiv validado em campo, o OID privado de temperatura da bateria retorna aproximadamente `-0,1 °C`, enquanto a temperatura de entrada está em torno de 24–25 °C. Isso não é fisicamente plausível para a instalação e pode representar valor sentinela/sensor indisponível ou interpretação específica daquele modelo.\n\nPor esse motivo:\n\n- o item continua sendo coletado e mantido para troubleshooting;\n- o valor continua visível no card;\n- ele **não** participa do gráfico ambiental padrão;\n- o operador deve comparar esse valor com a interface local/web do nobreak antes de utilizá-lo para decisões ambientais.\n",
                "### Temperatura da bateria: padrão x OID privado\n\nA partir da candidata 1.5.0, o card e os triggers de produção usam `upsBatteryTemperature` da RFC1628. O OID privado Vertiv validado anteriormente retornava aproximadamente `-0,1 °C` e passou a ficar **desabilitado por padrão** como métrica experimental. Ele pode ser habilitado manualmente apenas para troubleshooting/model-specific validation.\n",
            )
        else:
            text = text.replace(
                "**Battery temperature** — private Vertiv battery-temperature value.",
                "**Battery temperature** — standardized RFC1628 `upsBatteryTemperature`, used by the production card and alerts.",
            )
            text = text.replace(
                "### Important note about Battery temperature\n\nOn the field-validated Vertiv firmware, the private battery-temperature OID returns approximately `-0.1 °C` while inlet temperature is around 24–25 °C. This is not physically plausible for the installation and may represent a sentinel/unavailable sensor or model-specific interpretation.\n\nFor that reason:\n\n- the item continues to be collected and retained for troubleshooting;\n- the value remains visible in the card;\n- it does **not** participate in the default environmental graph;\n- operators should compare it with the local/web UPS interface before using it for environmental decisions.\n",
                "### Battery temperature: standard versus private OID\n\nStarting with the 1.5.0 candidate, the production card and triggers use RFC1628 `upsBatteryTemperature`. The previously validated Vertiv private OID returned approximately `-0.1 °C` and is now **disabled by default** as an experimental metric. It may be manually enabled only for troubleshooting/model-specific validation.\n",
            )
        path.write_text(text, encoding="utf-8")

    # Electrical summary: legacy input-power graph is no longer part of production export.
    for path, pt in ((ROOT / "docs/en/electrical-summary.md", False), (ROOT / "docs/pt-BR/electrical-summary.md", True)):
        text = path.read_text(encoding="utf-8")
        if pt:
            text = re.sub(
                r"## (Novos gráficos|Gráficos novos)\n\n- \*\*UPS: Input phase power\*\*;\n- \*\*UPS: Output phase load\*\*\.",
                "## Gráficos de produção\n\n- **UPS: Output phase load**.\n\nO gráfico privado **UPS: Input phase power** foi removido da candidata 1.5.0 porque seus OIDs de origem permanecem sem escala SNMP comprovada. Os itens privados de potência de entrada ficam desabilitados por padrão.",
                text,
            )
        else:
            text = text.replace(
                "## New graphs\n\n- **UPS: Input phase power**;\n- **UPS: Output phase load**.",
                "## Production graphs\n\n- **UPS: Output phase load**.\n\nThe private **UPS: Input phase power** graph is removed from the 1.5.0 candidate because its source OIDs still lack a verified SNMP scale. The private input-power items are disabled by default.",
            )
        path.write_text(text, encoding="utf-8")

    # SNMP docs: add heartbeat/alarm-table path.
    for path, pt in ((ROOT / "docs/en/snmp.md", False), (ROOT / "docs/pt-BR/snmp.md", True)):
        text = path.read_text(encoding="utf-8")
        if "upsAlarmTable" in text:
            continue
        if pt:
            addition = """\n## Disponibilidade e diagnóstico padronizado na candidata 1.5.0\n\n- `sysUpTime.0` (`1.3.6.1.2.1.1.3.0`) é coletado a cada minuto sem descarte de valores repetidos e alimenta o trigger de indisponibilidade SNMP por `nodata(5m)`.\n- `upsAlarmTable` (`1.3.6.1.2.1.33.1.6.2`) é descoberta dinamicamente para identificar alarmes ativos pelo OID de descrição.\n- `upsTestResultsSummary/Detail/StartTime/ElapsedTime` são lidos para diagnosticar testes; os objetos de comando `upsTestId`/`upsTestSpinLock` não são usados para iniciar testes.\n"""
        else:
            addition = """\n## Standardized availability and diagnostics in the 1.5.0 candidate\n\n- `sysUpTime.0` (`1.3.6.1.2.1.1.3.0`) is polled every minute without discard-unchanged preprocessing and drives the SNMP `nodata(5m)` availability trigger.\n- `upsAlarmTable` (`1.3.6.1.2.1.33.1.6.2`) is dynamically discovered to identify active alarms by description OID.\n- `upsTestResultsSummary/Detail/StartTime/ElapsedTime` are read for diagnostics; writable `upsTestId`/`upsTestSpinLock` objects are not used to initiate tests.\n"""
        path.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")

    # Metrics: append 1.5 additions rather than rewriting the large tables.
    for path, pt in ((ROOT / "docs/en/metrics.md", False), (ROOT / "docs/pt-BR/metrics.md", True)):
        text = path.read_text(encoding="utf-8")
        if "ups.snmp.uptime" in text:
            continue
        if pt:
            addition = """\n## Adições de produção na 1.5.0\n\n| Key | OID | Uso |\n| --- | --- | --- |\n| `ups.snmp.uptime` | `1.3.6.1.2.1.1.3.0` | heartbeat SNMP / disponibilidade |\n| `ups.ident.manufacturer` | `1.3.6.1.2.1.33.1.1.1.0` | identificação RFC1628 |\n| `ups.ident.model` | `1.3.6.1.2.1.33.1.1.2.0` | identificação RFC1628 |\n| `ups.ident.ups.software` | `1.3.6.1.2.1.33.1.1.3.0` | software/firmware UPS |\n| `ups.ident.agent.software` | `1.3.6.1.2.1.33.1.1.4.0` | software do agente |\n| `ups.ident.name` | `1.3.6.1.2.1.33.1.1.5.0` | nome administrativo (somente leitura no template) |\n| `ups.battery.current` | `1.3.6.1.2.1.33.1.2.6.0` | corrente de bateria RFC1628, escala 0,1 A |\n| `ups.battery.temperature` | `1.3.6.1.2.1.33.1.2.7.0` | temperatura de bateria RFC1628 |\n| `ups.test.results.summary` | `1.3.6.1.2.1.33.1.7.3.0` | resultado de teste |\n| `ups.test.results.detail` | `1.3.6.1.2.1.33.1.7.4.0` | detalhe do teste |\n| `ups.test.start.time` | `1.3.6.1.2.1.33.1.7.5.0` | marcador TimeTicks do início |\n| `ups.test.elapsed.time` | `1.3.6.1.2.1.33.1.7.6.0` | duração do teste |\n\nA descoberta `ups.alarm.discovery` usa `upsAlarmDescr` (`...33.1.6.2.1.2`) e `upsAlarmTime` (`...33.1.6.2.1.3`) para listar condições ativas.\n"""
        else:
            addition = """\n## Production additions in 1.5.0\n\n| Key | OID | Purpose |\n| --- | --- | --- |\n| `ups.snmp.uptime` | `1.3.6.1.2.1.1.3.0` | SNMP heartbeat / availability |\n| `ups.ident.manufacturer` | `1.3.6.1.2.1.33.1.1.1.0` | RFC1628 identification |\n| `ups.ident.model` | `1.3.6.1.2.1.33.1.1.2.0` | RFC1628 identification |\n| `ups.ident.ups.software` | `1.3.6.1.2.1.33.1.1.3.0` | UPS software/firmware |\n| `ups.ident.agent.software` | `1.3.6.1.2.1.33.1.1.4.0` | agent software |\n| `ups.ident.name` | `1.3.6.1.2.1.33.1.1.5.0` | administrative name (read only in this template) |\n| `ups.battery.current` | `1.3.6.1.2.1.33.1.2.6.0` | RFC1628 battery current, 0.1 A scale |\n| `ups.battery.temperature` | `1.3.6.1.2.1.33.1.2.7.0` | RFC1628 battery temperature |\n| `ups.test.results.summary` | `1.3.6.1.2.1.33.1.7.3.0` | diagnostic test result |\n| `ups.test.results.detail` | `1.3.6.1.2.1.33.1.7.4.0` | diagnostic test detail |\n| `ups.test.start.time` | `1.3.6.1.2.1.33.1.7.5.0` | test-start TimeTicks marker |\n| `ups.test.elapsed.time` | `1.3.6.1.2.1.33.1.7.6.0` | diagnostic test duration |\n\nDiscovery key `ups.alarm.discovery` uses `upsAlarmDescr` (`...33.1.6.2.1.2`) and `upsAlarmTime` (`...33.1.6.2.1.3`) to list active conditions.\n"""
        path.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")


def update_security_docs() -> None:
    for path, pt in ((ROOT / "SECURITY.md", False), (ROOT / "SECURITY.pt-BR.md", True)):
        text = path.read_text(encoding="utf-8")
        if "upsTestId" in text:
            continue
        if pt:
            addition = """\n## Objetos RFC1628 read-write\n\nAlguns objetos padronizados, como `upsIdentName`, são definidos pelo RFC1628 como read-write. O template apenas os consulta por SNMP GET. Objetos de controle da UPS-MIB (`1.3.6.1.2.1.33.1.8`) e os objetos usados para iniciar/abortar testes (`upsTestId`/`upsTestSpinLock`) não fazem parte da lógica de controle deste projeto. A candidata 1.5.0 lê somente os objetos de **resultado** dos testes.\n\nMétricas privadas com escala/semântica não comprovada ficam desabilitadas por padrão e não alimentam alertas críticos.\n"""
        else:
            addition = """\n## RFC1628 read-write objects\n\nSome standard objects, such as `upsIdentName`, are defined by RFC1628 as read-write. The template only queries them with SNMP GET. UPS-MIB control objects (`1.3.6.1.2.1.33.1.8`) and the objects used to start/abort tests (`upsTestId`/`upsTestSpinLock`) are not part of this project's control logic. The 1.5.0 candidate reads only test **result** objects.\n\nPrivate metrics with unverified scaling/semantics are disabled by default and cannot drive critical production alerts.\n"""
        path.write_text(text.rstrip() + "\n" + addition, encoding="utf-8")


def update_changelogs() -> None:
    for path, pt in ((ROOT / "CHANGELOG.md", False), (ROOT / "CHANGELOG.pt-BR.md", True)):
        text = path.read_text(encoding="utf-8")
        if "## [1.5.0]" in text:
            continue
        marker = "## [1.4.1]"
        if pt:
            entry = """## [1.5.0] - Não lançado (candidata para homologação)\n\n### Adicionado\n\n- Heartbeat SNMP dedicado por `sysUpTime.0`, trigger de indisponibilidade por `nodata(5m)` e aviso de reset do agente.\n- Identificação RFC1628, corrente/temperatura de bateria padronizadas e resultados somente leitura de testes diagnósticos.\n- Descoberta de `upsAlarmTable` com value map dos 24 alarmes conhecidos da RFC1628.\n- Proveniência MIB/OID, matriz de compatibilidade e checklist de homologação de produção.\n- Validador específico de produção e teste CI de importação via API em Zabbix 7 real.\n\n### Alterado\n\n- Alertas de temperatura de bateria passam a usar `upsBatteryTemperature` RFC1628.\n- Alertas de carga permanecem nos protótipos `upsOutputPercentLoad` RFC1628; o agregado privado deixa de gerar trigger.\n- Card de alarmes fica vermelho para qualquer quantidade positiva, evitando sugerir severidade pela contagem.\n\n### Segurança / confiabilidade\n\n- Potência privada de entrada e temperatura privada de bateria ficam desabilitadas por padrão.\n- Gráficos legados baseados em métricas experimentais/contadores cumulativos foram removidos.\n- Nenhum OID de controle/escrita foi adicionado.\n\n"""
        else:
            entry = """## [1.5.0] - Unreleased (homologation candidate)\n\n### Added\n\n- Dedicated SNMP heartbeat via `sysUpTime.0`, `nodata(5m)` availability trigger and management-agent uptime reset notice.\n- RFC1628 identification, standardized battery current/temperature and read-only diagnostic-test results.\n- `upsAlarmTable` discovery with a value map for all 24 RFC1628 well-known alarms.\n- MIB/OID provenance, compatibility matrix and production homologation checklist.\n- Production-specific validator and real Zabbix 7 API-import CI test.\n\n### Changed\n\n- Battery-temperature alerting now uses standard RFC1628 `upsBatteryTemperature`.\n- Load alerting remains on RFC1628 `upsOutputPercentLoad` prototypes; the private aggregate load no longer generates triggers.\n- The active-alarm card turns red for any positive count instead of implying severity from the number of alarms.\n\n### Safety / reliability\n\n- Private input-power and private battery-temperature metrics are disabled by default.\n- Legacy graphs based on experimental metrics/cumulative counters were removed.\n- No control/write OIDs were added.\n\n"""
        text = text.replace(marker, entry + marker, 1)
        path.write_text(text, encoding="utf-8")


def write_field_fixtures() -> None:
    fixtures = ROOT / "tests/fixtures"
    fixtures.mkdir(parents=True, exist_ok=True)
    enum_samples = {
        "vertiv.system.status": {"raw": "Normal Operation", "expected": 1},
        "vertiv.inverter.state": {"raw": "on", "expected": 1},
        "vertiv.eco.status": {"raw": "off", "expected": 0},
        "vertiv.topology": {"raw": "Online", "expected": 3},
        "vertiv.shutdown.reason": {"raw": "None", "expected": 0},
        "vertiv.battery.charge.status": {"raw": "fully charged", "expected": 0},
        "vertiv.battery.test.result": {"raw": "Passed", "expected": 1},
        "vertiv.battery.autotest": {"raw": "disabled", "expected": 0},
        "vertiv.battery.test.interval": {"raw": "8 weeks", "expected": 0},
        "vertiv.battery.cabinet.type": {"raw": "External", "expected": 1},
    }
    (fixtures / "field-enum-samples.json").write_text(
        json.dumps(enum_samples, indent=2) + "\n", encoding="utf-8"
    )
    alarm_fixture = {
        f"1.3.6.1.2.1.33.1.6.3.{idx}": name for idx, name in ALARM_NAMES.items()
    }
    (fixtures / "rfc1628-alarm-oids.json").write_text(
        json.dumps(alarm_fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_production_validator() -> None:
    content = r'''"""Production-readiness validation for Vertiv by SNMP."""

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
    if any(p.get("type") == "DISCARD_UNCHANGED_HEARTBEAT" for p in uptime.get("preprocessing", [])):
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
    if "{$UPS.BATTERY.TEMP.WARN}" not in temp_expr or "{$UPS.BATTERY.TEMP.CRIT}" not in temp_expr:
        errors.append("RFC1628 battery temperature must own production temperature triggers")

    rules = {str(rule.get("key")): rule for rule in template.get("discovery_rules", [])}
    alarm = rules.get("ups.alarm.discovery")
    if alarm is None:
        errors.append("missing RFC1628 active alarm discovery")
    else:
        if "33.1.6.2.1.2" not in str(alarm.get("snmp_oid")):
            errors.append("alarm discovery must use upsAlarmDescr")
        proto_keys = {str(i.get("key")) for i in alarm.get("item_prototypes", [])}
        if proto_keys != {"ups.alarm.descr[{#SNMPINDEX}]", "ups.alarm.time[{#SNMPINDEX}]"}:
            errors.append(f"unexpected alarm prototypes: {sorted(proto_keys)}")

    maps = {str(v.get("name")): v for v in template.get("valuemaps", [])}
    alarm_map = maps.get("UPS RFC1628 alarm description")
    fixture = json.loads((ROOT / "tests/fixtures/rfc1628-alarm-oids.json").read_text(encoding="utf-8"))
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
    dashboard = next(d for d in template.get("dashboards", []) if d.get("name") == "Vertiv UPS Overview")
    battery_key = None
    alarm_thresholds = []
    for page in dashboard.get("pages", []):
        for widget in page.get("widgets", []):
            if widget.get("type") != "item":
                continue
            fields = widget.get("fields", [])
            if widget.get("name") == "Battery temperature":
                ref = next(f.get("value") for f in fields if f.get("name") == "itemid.0")
                battery_key = ref.get("key")
            if widget.get("name") == "Active alarms":
                alarm_thresholds = [
                    f for f in fields if str(f.get("name", "")).startswith("thresholds.")
                ]
    if battery_key != "ups.battery.temperature":
        errors.append(f"dashboard battery temperature must use RFC1628 item, got {battery_key!r}")
    thresholds = {
        str(f.get("name")): str(f.get("value")) for f in alarm_thresholds
    }
    if thresholds != {"thresholds.0.color": "FFCDD2", "thresholds.0.threshold": "1"}:
        errors.append(f"active alarm card thresholds must be any-positive red: {thresholds}")

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
        raise ProductionValidationError(f"production candidate VERSION must be 1.5.0, got {version}")
    for path in TEMPLATE_FILES:
        validate(path)
    print("OK: production-readiness validation passed for Zabbix 7.0 and 8.0 exports")


if __name__ == "__main__":
    try:
        run()
    except ProductionValidationError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
'''
    (ROOT / "tools/validate_production.py").write_text(content, encoding="utf-8")


def write_api_import_tester() -> None:
    content = r'''#!/usr/bin/env python3
"""Import a template into a running Zabbix frontend through the JSON-RPC API."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def call_api(url: str, method: str, params: Any, token: str | None = None) -> Any:
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json-rpc"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    if "error" in result:
        raise RuntimeError(f"Zabbix API {method} failed: {json.dumps(result['error'], sort_keys=True)}")
    return result.get("result")


def wait_for_api(url: str, timeout: int) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            version = call_api(url, "apiinfo.version", [])
            print(f"Zabbix API ready: {version}")
            return
        except (OSError, RuntimeError, urllib.error.URLError) as exc:
            last_error = exc
            time.sleep(3)
    raise RuntimeError(f"Zabbix API did not become ready within {timeout}s: {last_error}")


def import_template(url: str, template_path: Path, username: str, password: str) -> None:
    token = call_api(url, "user.login", {"username": username, "password": password})
    rules = {
        "template_groups": {"createMissing": True, "updateExisting": True},
        "templates": {"createMissing": True, "updateExisting": True},
        "items": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "discoveryRules": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "triggers": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "graphs": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "valueMaps": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "templateDashboards": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "templateLinkage": {"createMissing": True, "deleteMissing": False},
    }
    source = template_path.read_text(encoding="utf-8")
    result = call_api(
        url,
        "configuration.import",
        {"format": "yaml", "rules": rules, "source": source},
        token,
    )
    if result is not True:
        raise RuntimeError(f"configuration.import returned unexpected result: {result!r}")
    templates = call_api(
        url,
        "template.get",
        {
            "output": ["templateid", "host", "name"],
            "filter": {"host": ["VERTIV by SNMP"]},
        },
        token,
    )
    if len(templates) != 1 or templates[0].get("name") != "Vertiv by SNMP":
        raise RuntimeError(f"imported template verification failed: {templates!r}")
    print(f"Imported and verified template: {templates[0]}")
    call_api(url, "user.logout", [], token)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8080/api_jsonrpc.php")
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--username", default="Admin")
    parser.add_argument("--password", default="zabbix")
    parser.add_argument("--wait", type=int, default=180)
    args = parser.parse_args()
    wait_for_api(args.url, args.wait)
    import_template(args.url, args.template, args.username, args.password)


if __name__ == "__main__":
    main()
'''
    path = ROOT / "tools/zabbix_api_import_test.py"
    path.write_text(content, encoding="utf-8")


def write_tests() -> None:
    test = r'''from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_production_validator_passes():
    import sys

    sys.path.insert(0, str(ROOT / "tools"))
    import validate_production

    validate_production.run()


def test_no_private_control_or_test_start_objects_in_templates():
    for version in ("7.0", "8.0"):
        text = (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(encoding="utf-8")
        assert "1.3.6.1.2.1.33.1.8" not in text
        assert "1.3.6.1.2.1.33.1.7.1.0" not in text  # upsTestId
        assert "1.3.6.1.2.1.33.1.7.2.0" not in text  # upsTestSpinLock


def test_alarm_discovery_is_diagnostic_not_trigger_spam():
    for version in ("7.0", "8.0"):
        data = yaml.safe_load((ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(encoding="utf-8"))
        template = data["zabbix_export"]["templates"][0]
        rule = next(r for r in template["discovery_rules"] if r["key"] == "ups.alarm.discovery")
        assert not rule.get("trigger_prototypes")
        for proto in rule["item_prototypes"]:
            assert not proto.get("trigger_prototypes")
'''
    (ROOT / "tests/test_validate_production.py").write_text(test, encoding="utf-8")


def update_ci_workflow() -> None:
    path = ROOT / ".github/workflows/ci.yml"
    text = path.read_text(encoding="utf-8")
    if "Validate production readiness" not in text:
        text = text.replace(
            "      - name: Validate bilingual documentation parity\n        run: python tools/validate_docs.py\n",
            "      - name: Validate bilingual documentation parity\n        run: python tools/validate_docs.py\n\n      - name: Validate production readiness\n        run: python tools/validate_production.py\n",
        )
    if "zabbix-import:" not in text:
        text += r'''

  zabbix-import:
    name: Zabbix 7.0 real import
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.14"

      - name: Start disposable Zabbix 7.0 stack
        shell: bash
        run: |
          set -euo pipefail
          docker network create zabbix-ci
          docker run -d --name zabbix-db --network zabbix-ci \
            -e POSTGRES_DB=zabbix \
            -e POSTGRES_USER=zabbix \
            -e POSTGRES_PASSWORD=zabbix \
            postgres:16-alpine
          for i in $(seq 1 60); do
            if docker exec zabbix-db pg_isready -U zabbix -d zabbix >/dev/null 2>&1; then break; fi
            sleep 2
          done
          docker exec zabbix-db pg_isready -U zabbix -d zabbix

          docker run -d --name zabbix-server --network zabbix-ci \
            -e DB_SERVER_HOST=zabbix-db \
            -e POSTGRES_DB=zabbix \
            -e POSTGRES_USER=zabbix \
            -e POSTGRES_PASSWORD=zabbix \
            zabbix/zabbix-server-pgsql:alpine-7.0-latest

          docker run -d --name zabbix-web --network zabbix-ci -p 8080:8080 \
            -e DB_SERVER_HOST=zabbix-db \
            -e POSTGRES_DB=zabbix \
            -e POSTGRES_USER=zabbix \
            -e POSTGRES_PASSWORD=zabbix \
            -e ZBX_SERVER_HOST=zabbix-server \
            -e ZBX_SERVER_NAME="Vertiv template CI" \
            zabbix/zabbix-web-nginx-pgsql:alpine-7.0-latest

      - name: Import template through Zabbix API
        run: python tools/zabbix_api_import_test.py --template templates/7.0/vertiv-by-snmp.yaml --wait 240

      - name: Container diagnostics on failure
        if: failure()
        shell: bash
        run: |
          docker ps -a
          docker logs zabbix-db || true
          docker logs zabbix-server || true
          docker logs zabbix-web || true
'''
    path.write_text(text, encoding="utf-8")


def update_release_workflow() -> None:
    path = ROOT / ".github/workflows/release.yml"
    text = path.read_text(encoding="utf-8")
    if "python tools/validate_production.py" not in text:
        text = text.replace(
            "          python tools/validate_docs.py\n          pytest -q\n",
            "          python tools/validate_docs.py\n          python tools/validate_production.py\n          pytest -q\n",
        )
    # A release tag should never be published unless the same export imports in a
    # disposable supported Zabbix 7 stack.
    if "Production import gate" not in text:
        marker = "      - name: Build release assets\n"
        block = r'''      - name: Production import gate
        shell: bash
        run: |
          set -euo pipefail
          docker network create zabbix-release-ci
          docker run -d --name zabbix-db --network zabbix-release-ci \
            -e POSTGRES_DB=zabbix -e POSTGRES_USER=zabbix -e POSTGRES_PASSWORD=zabbix \
            postgres:16-alpine
          for i in $(seq 1 60); do
            if docker exec zabbix-db pg_isready -U zabbix -d zabbix >/dev/null 2>&1; then break; fi
            sleep 2
          done
          docker exec zabbix-db pg_isready -U zabbix -d zabbix
          docker run -d --name zabbix-server --network zabbix-release-ci \
            -e DB_SERVER_HOST=zabbix-db -e POSTGRES_DB=zabbix -e POSTGRES_USER=zabbix -e POSTGRES_PASSWORD=zabbix \
            zabbix/zabbix-server-pgsql:alpine-7.0-latest
          docker run -d --name zabbix-web --network zabbix-release-ci -p 8080:8080 \
            -e DB_SERVER_HOST=zabbix-db -e POSTGRES_DB=zabbix -e POSTGRES_USER=zabbix -e POSTGRES_PASSWORD=zabbix \
            -e ZBX_SERVER_HOST=zabbix-server -e ZBX_SERVER_NAME="Vertiv release validation" \
            zabbix/zabbix-web-nginx-pgsql:alpine-7.0-latest
          python tools/zabbix_api_import_test.py --template templates/7.0/vertiv-by-snmp.yaml --wait 240

'''
        text = text.replace(marker, block + marker, 1)
    path.write_text(text, encoding="utf-8")


def update_version() -> None:
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")


def main() -> None:
    for path in TEMPLATES:
        transform_template(path)
    update_version()
    update_readmes()
    write_status_docs()
    write_mib_docs()
    write_compatibility_docs()
    write_production_docs()
    update_doc_indexes()
    update_existing_docs()
    update_security_docs()
    update_changelogs()
    write_field_fixtures()
    write_production_validator()
    write_api_import_tester()
    write_tests()
    update_ci_workflow()
    update_release_workflow()
    print("Applied v1.5.0 production hardening candidate")


if __name__ == "__main__":
    main()
