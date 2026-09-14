"""Validate documentation structure and parity against the Zabbix template."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
MACRO_RE = re.compile(r"\{\$[A-Z0-9_.]+\}")
TRIGGER_ROW_RE = re.compile(r"^\|\s*(UPS[^|]+?)\s*\|\s*(?:INFO|WARNING|AVERAGE|HIGH|DISASTER|NOT_CLASSIFIED)\s*\|", re.MULTILINE)

ROOT_PAIRS = [
    ("README.md", "README.pt-BR.md"),
    ("CHANGELOG.md", "CHANGELOG.pt-BR.md"),
    ("CONTRIBUTING.md", "CONTRIBUTING.pt-BR.md"),
    ("NOTICE.md", "NOTICE.pt-BR.md"),
    ("SECURITY.md", "SECURITY.pt-BR.md"),
]

DOC_BASENAMES = [
    "README.md",
    "compatibility.md",
    "configuration.md",
    "dashboard.md",
    "electrical-summary.md",
    "homologation-1.5.0.md",
    "installation.md",
    "license-attribution.md",
    "metrics.md",
    "mib-sources.md",
    "production-readiness.md",
    "project-status.md",
    "snmp.md",
    "synoptic-map.md",
    "triggers.md",
    "troubleshooting.md",
    "versioning.md",
    "zabbix-8.0.md",
]


class ValidationError(Exception):
    pass


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_template() -> dict[str, Any]:
    path = ROOT / "templates/7.0/vertiv-by-snmp.yaml"
    return yaml.safe_load(_read(path))["zabbix_export"]["templates"][0]


def _walk_triggers(template: dict[str, Any]) -> list[dict[str, Any]]:
    triggers: list[dict[str, Any]] = []
    for item in template.get("items", []):
        triggers.extend(item.get("triggers", []))
    for rule in template.get("discovery_rules", []):
        triggers.extend(rule.get("trigger_prototypes", []))
        for proto in rule.get("item_prototypes", []):
            triggers.extend(proto.get("trigger_prototypes", []))
    triggers.extend(template.get("triggers", []))
    return triggers


def validate_pairs() -> list[str]:
    errors: list[str] = []
    for en, pt in ROOT_PAIRS:
        if not (ROOT / en).is_file():
            errors.append(f"missing English root document: {en}")
        if not (ROOT / pt).is_file():
            errors.append(f"missing pt-BR root document: {pt}")

    for name in DOC_BASENAMES:
        for lang in ("en", "pt-BR"):
            path = ROOT / "docs" / lang / name
            if not path.is_file():
                errors.append(f"missing {lang} document: docs/{lang}/{name}")
    return errors


def validate_local_links() -> list[str]:
    errors: list[str] = []
    for path in sorted(ROOT.rglob("*.md")):
        text = _read(path)
        for target in LINK_RE.findall(text):
            target = target.strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            resolved = (path.parent / target_path).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(ROOT)} links outside repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)} has broken local link: {target}")
    return errors


def validate_version_mentions() -> list[str]:
    errors: list[str] = []
    candidate = _read(ROOT / "VERSION").strip()
    stable = _read(ROOT / "STABLE_VERSION").strip()
    for label, value in (("VERSION", candidate), ("STABLE_VERSION", stable)):
        if not VERSION_RE.fullmatch(value):
            errors.append(f"invalid {label}: {value!r}")
    if errors:
        return errors

    candidate_required = [
        "README.md",
        "README.pt-BR.md",
        "CHANGELOG.md",
        "CHANGELOG.pt-BR.md",
        "docs/en/README.md",
        "docs/pt-BR/README.md",
        "docs/en/versioning.md",
        "docs/pt-BR/versioning.md",
        "docs/en/project-status.md",
        "docs/pt-BR/project-status.md",
        "docs/en/homologation-1.5.0.md",
        "docs/pt-BR/homologation-1.5.0.md",
    ]
    stable_required = [
        "README.md",
        "README.pt-BR.md",
        "docs/en/README.md",
        "docs/pt-BR/README.md",
        "docs/en/versioning.md",
        "docs/pt-BR/versioning.md",
    ]
    for rel in candidate_required:
        if candidate not in _read(ROOT / rel):
            errors.append(f"{rel} does not mention candidate version {candidate}")
    for rel in stable_required:
        if stable not in _read(ROOT / rel):
            errors.append(f"{rel} does not mention stable version {stable}")
    return errors


def validate_trigger_docs() -> list[str]:
    template = _load_template()
    expected = {str(t.get("name")) for t in _walk_triggers(template) if t.get("name")}
    errors: list[str] = []
    for rel in ("docs/en/triggers.md", "docs/pt-BR/triggers.md"):
        text = _read(ROOT / rel)
        documented = set(TRIGGER_ROW_RE.findall(text))
        missing = sorted(expected - documented)
        extra = sorted(documented - expected)
        if missing:
            errors.append(f"{rel} is missing trigger rows: {missing}")
        if extra:
            errors.append(f"{rel} documents non-existent trigger rows: {extra}")
        count_text = f"{len(expected)} "
        if count_text not in text:
            errors.append(f"{rel} does not state the actual trigger count {len(expected)}")
    return errors


def validate_macro_docs() -> list[str]:
    template = _load_template()
    expected = {str(m.get("macro")) for m in template.get("macros", []) if m.get("macro")}
    errors: list[str] = []
    for rel in ("docs/en/configuration.md", "docs/pt-BR/configuration.md"):
        documented = set(MACRO_RE.findall(_read(ROOT / rel)))
        missing = sorted(expected - documented)
        extra = sorted(documented - expected)
        if missing:
            errors.append(f"{rel} is missing template macros: {missing}")
        if extra:
            errors.append(f"{rel} documents unknown template macros: {extra}")
    return errors


def validate_branch_policy_docs() -> list[str]:
    errors: list[str] = []
    checks = {
        "README.md": ("main", "tagged GitHub Release"),
        "README.pt-BR.md": ("main", "GitHub Release"),
        "docs/en/README.md": ("main", "tagged GitHub Release"),
        "docs/pt-BR/README.md": ("main", "GitHub Release"),
    }
    for rel, required in checks.items():
        text = _read(ROOT / rel)
        for phrase in required:
            if phrase not in text:
                errors.append(f"{rel} is missing branch/release policy phrase: {phrase!r}")

    for rel in ("CONTRIBUTING.md", "CONTRIBUTING.pt-BR.md"):
        text = _read(ROOT / rel)
        if "templates/7.0/" not in text or "templates/8.0/" not in text:
            errors.append(f"{rel} must document the real versioned template paths")
        if "templates/zabbix-<major.minor>/" in text:
            errors.append(f"{rel} still documents the obsolete template path convention")
    return errors


def run() -> None:
    errors: list[str] = []
    errors.extend(validate_pairs())
    errors.extend(validate_local_links())
    errors.extend(validate_version_mentions())
    errors.extend(validate_trigger_docs())
    errors.extend(validate_macro_docs())
    errors.extend(validate_branch_policy_docs())
    if errors:
        raise ValidationError("\n  - ".join([""] + errors))
    print("OK: bilingual docs, links, versions, triggers, macros and release policy validated")


if __name__ == "__main__":
    try:
        run()
    except ValidationError as exc:
        print(f"ERROR:{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
