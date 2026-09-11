"""Validate the versioned VERTIV by SNMP Zabbix templates."""

from __future__ import annotations

import copy
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_FILES = {
    "7.0": ROOT / "templates" / "7.0" / "vertiv-by-snmp.yaml",
    "8.0": ROOT / "templates" / "8.0" / "vertiv-by-snmp.yaml",
}
TEMPLATE_NAME = "VERTIV by SNMP"
VENDOR_NAME = "Net Tech"
EXPECTED_GROUP = "Templates/Power"
UUID_RE = re.compile(r"^[0-9a-f]{32}$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
MACRO_RE = re.compile(r"\{\$[A-Z0-9_.]+\}")
ALLOWED_PRIORITIES = {
    "NOT_CLASSIFIED",
    "INFO",
    "WARNING",
    "AVERAGE",
    "HIGH",
    "DISASTER",
}

REQUIRED_PHASE1_KEYS = {
    "ups.output.frequency",
    "vertiv.input.voltage.l1n",
    "vertiv.input.voltage.l12",
    "vertiv.input.power.l1",
    "vertiv.input.power.l2",
    "vertiv.input.power.l3",
    "vertiv.input.power.total",
    "vertiv.bypass.voltage.l1n",
    "vertiv.bypass.voltage.l12",
    "vertiv.output.voltage.l1n",
    "vertiv.output.voltage.l12",
    "vertiv.output.current.l1",
    "vertiv.output.pf.l1",
    "vertiv.output.load.l1",
    "vertiv.output.power.l1",
    "vertiv.output.apparent.power.l1",
    "vertiv.battery.cabinet.type",
    "vertiv.battery.test.interval",
}
UNVALIDATED_EVENT_BRANCH = "1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.100."

# Consequential control branches/OIDs intentionally excluded from this project.
FORBIDDEN_OID_PREFIXES = (
    "1.3.6.1.2.1.33.1.8",  # UPS-MIB shutdown/control group
    "1.3.6.1.4.1.476.1.42.2.5.1",  # Vertiv/Liebert agent reboot
)


class ValidationError(Exception):
    """Raised when repository template validation fails."""


def load_version() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(version):
        raise ValidationError(f"VERSION is not Semantic Versioning: {version!r}")
    return version


def zabbix_vendor_version(project_version: str) -> str:
    """Convert project SemVer X.Y.Z to Zabbix vendor version X.Y-Z."""
    major, minor, patch = project_version.split(".")
    return f"{major}.{minor}-{patch}"


def load_template(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValidationError(f"Missing template: {path.relative_to(ROOT)}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValidationError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"Template root must be a mapping: {path}")
    return data


def walk_objects(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_objects(child)


def collect_uuids(data: dict[str, Any]) -> list[str]:
    uuids: list[str] = []
    for obj in walk_objects(data):
        if "uuid" in obj:
            uuids.append(str(obj["uuid"]))
    return uuids


def collect_trigger_objects(template: dict[str, Any]) -> list[dict[str, Any]]:
    triggers: list[dict[str, Any]] = []
    for item in template.get("items", []):
        triggers.extend(item.get("triggers", []))
    for rule in template.get("discovery_rules", []):
        for proto in rule.get("item_prototypes", []):
            triggers.extend(proto.get("trigger_prototypes", []))
        triggers.extend(rule.get("trigger_prototypes", []))
    triggers.extend(template.get("triggers", []))
    return triggers


def collect_item_keys(template: dict[str, Any]) -> tuple[list[str], list[str]]:
    fixed = [str(item["key"]) for item in template.get("items", [])]
    prototypes: list[str] = []
    for rule in template.get("discovery_rules", []):
        prototypes.extend(str(item["key"]) for item in rule.get("item_prototypes", []))
    return fixed, prototypes


def validate_one(
    export_version: str, data: dict[str, Any], project_version: str
) -> None:
    errors: list[str] = []

    export = data.get("zabbix_export")
    if not isinstance(export, dict):
        errors.append("missing zabbix_export mapping")
        export = {}

    if str(export.get("version")) != export_version:
        errors.append(
            f"zabbix_export.version={export.get('version')!r}; expected {export_version!r}"
        )

    templates = export.get("templates", [])
    if not isinstance(templates, list) or len(templates) != 1:
        errors.append("export must contain exactly one template")
        template = {}
    else:
        template = templates[0]

    if template.get("template") != TEMPLATE_NAME:
        errors.append(f"technical template name must be {TEMPLATE_NAME!r}")
    if template.get("name") != TEMPLATE_NAME:
        errors.append(f"visible template name must be {TEMPLATE_NAME!r}")

    vendor = template.get("vendor", {})
    if vendor.get("name") != VENDOR_NAME:
        errors.append(f"vendor.name must be {VENDOR_NAME!r}")
    expected_vendor_version = zabbix_vendor_version(project_version)
    if str(vendor.get("version")) != expected_vendor_version:
        errors.append(
            f"vendor.version={vendor.get('version')!r}; expected {expected_vendor_version!r}"
        )

    groups = {str(g.get("name")) for g in template.get("groups", [])}
    if EXPECTED_GROUP not in groups:
        errors.append(f"template must belong to {EXPECTED_GROUP!r}")

    export_groups = {str(g.get("name")) for g in export.get("template_groups", [])}
    if EXPECTED_GROUP not in export_groups:
        errors.append(f"export must define template group {EXPECTED_GROUP!r}")

    uuids = collect_uuids(data)
    invalid_uuids = [uuid for uuid in uuids if not UUID_RE.fullmatch(uuid)]
    if invalid_uuids:
        errors.append(f"invalid UUIDs: {invalid_uuids[:5]}")
    duplicates = sorted({uuid for uuid in uuids if uuids.count(uuid) > 1})
    if duplicates:
        errors.append(f"duplicate UUIDs inside export: {duplicates[:5]}")

    fixed_keys, prototype_keys = collect_item_keys(template)
    missing_phase1 = sorted(REQUIRED_PHASE1_KEYS - set(fixed_keys))
    if missing_phase1:
        errors.append(f"missing required phase-1 item keys: {missing_phase1}")

    for label, keys in (("item", fixed_keys), ("item prototype", prototype_keys)):
        dup = sorted({key for key in keys if keys.count(key) > 1})
        if dup:
            errors.append(f"duplicate {label} keys: {dup}")

    declared_macros = {str(m.get("macro")) for m in template.get("macros", [])}
    for trigger in collect_trigger_objects(template):
        priority = trigger.get("priority", "NOT_CLASSIFIED")
        if priority not in ALLOWED_PRIORITIES:
            errors.append(
                f"invalid trigger priority {priority!r} in {trigger.get('name')!r}"
            )
        expr = str(trigger.get("expression", ""))
        for macro in MACRO_RE.findall(expr):
            if macro not in declared_macros:
                errors.append(
                    f"undeclared macro {macro} in trigger {trigger.get('name')!r}"
                )

    value_map_names = {str(v.get("name")) for v in template.get("valuemaps", [])}
    for item in template.get("items", []):
        valuemap = item.get("valuemap")
        if valuemap:
            name = str(valuemap.get("name"))
            if name not in value_map_names:
                errors.append(
                    f"item {item.get('key')!r} references missing value map {name!r}"
                )

    # Read-only / OID-family checks.
    for obj in walk_objects(template):
        if "snmp_oid" not in obj:
            continue
        oid = str(obj["snmp_oid"])
        if UNVALIDATED_EVENT_BRANCH in oid:
            errors.append(
                f"unvalidated Vertiv event-state OID is not allowed yet: {oid}"
            )
        if "1.3.6.1.4.1.6302" in oid:
            errors.append(
                f"legacy rectifier OID tree is not allowed in UPS template: {oid}"
            )
        for prefix in FORBIDDEN_OID_PREFIXES:
            if prefix in oid:
                errors.append(f"forbidden control OID/branch in template: {oid}")

    # Ensure graphs reference existing fixed items on this template.
    fixed_key_set = set(fixed_keys)
    for graph in export.get("graphs", []):
        for graph_item in graph.get("graph_items", []):
            ref = graph_item.get("item", {})
            if ref.get("host") != TEMPLATE_NAME:
                errors.append(
                    f"graph {graph.get('name')!r} references unexpected host "
                    f"{ref.get('host')!r}"
                )
            key = str(ref.get("key"))
            if key not in fixed_key_set:
                errors.append(
                    f"graph {graph.get('name')!r} references missing item key {key!r}"
                )

    trap_items = [
        item for item in template.get("items", []) if item.get("type") == "SNMP_TRAP"
    ]
    for item in trap_items:
        if item.get("status") != "DISABLED":
            errors.append(
                f"SNMP trap item must remain disabled by default: {item.get('key')}"
            )

    if errors:
        joined = "\n  - ".join(errors)
        raise ValidationError(
            f"Zabbix {export_version} template validation failed:\n  - {joined}"
        )


def semantic_copy(data: dict[str, Any]) -> dict[str, Any]:
    normalized = copy.deepcopy(data)
    export = normalized["zabbix_export"]
    export["version"] = "<version>"
    template = export["templates"][0]
    description = str(template.get("description", ""))
    description = re.sub(
        r"\n\nExport target: Zabbix (?:7\.0|8\.0)\.\s*$", "", description
    )
    template["description"] = description
    return normalized


def validate_semantic_parity(v7: dict[str, Any], v8: dict[str, Any]) -> None:
    if semantic_copy(v7) != semantic_copy(v8):
        raise ValidationError(
            "Zabbix 7.0 and 8.0 templates differ beyond the export-version marker"
        )


def run() -> None:
    project_version = load_version()
    loaded = {version: load_template(path) for version, path in TEMPLATE_FILES.items()}
    for version, data in loaded.items():
        validate_one(version, data, project_version)
    validate_semantic_parity(loaded["7.0"], loaded["8.0"])
    print(f"OK: validated VERTIV by SNMP {project_version} for Zabbix 7.0 and 8.0")


if __name__ == "__main__":
    try:
        run()
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
