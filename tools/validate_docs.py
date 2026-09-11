"""Validate bilingual documentation parity and local Markdown links."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")

ROOT_PAIRS = [
    ("README.md", "README.pt-BR.md"),
    ("CHANGELOG.md", "CHANGELOG.pt-BR.md"),
    ("CONTRIBUTING.md", "CONTRIBUTING.pt-BR.md"),
    ("NOTICE.md", "NOTICE.pt-BR.md"),
    ("SECURITY.md", "SECURITY.pt-BR.md"),
]

DOC_BASENAMES = [
    "README.md",
    "installation.md",
    "configuration.md",
    "metrics.md",
    "electrical-summary.md",
    "triggers.md",
    "snmp.md",
    "troubleshooting.md",
    "zabbix-8.0.md",
    "versioning.md",
    "license-attribution.md",
]


class ValidationError(Exception):
    pass


def validate_pairs() -> list[str]:
    errors: list[str] = []
    for en, pt in ROOT_PAIRS:
        if not (ROOT / en).is_file():
            errors.append(f"missing English root document: {en}")
        if not (ROOT / pt).is_file():
            errors.append(f"missing pt-BR root document: {pt}")

    for name in DOC_BASENAMES:
        if not (ROOT / "docs" / "en" / name).is_file():
            errors.append(f"missing English document: docs/en/{name}")
        if not (ROOT / "docs" / "pt-BR" / name).is_file():
            errors.append(f"missing pt-BR document: docs/pt-BR/{name}")
    return errors


def validate_local_links() -> list[str]:
    errors: list[str] = []
    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
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
                errors.append(
                    f"{path.relative_to(ROOT)} links outside repository: {target}"
                )
                continue
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)} has broken local link: {target}"
                )
    return errors


def validate_version_mentions() -> list[str]:
    errors: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        errors.append(f"invalid VERSION: {version!r}")
        return errors
    required = [
        ROOT / "README.md",
        ROOT / "README.pt-BR.md",
        ROOT / "CHANGELOG.md",
        ROOT / "CHANGELOG.pt-BR.md",
        ROOT / "docs/en/versioning.md",
        ROOT / "docs/pt-BR/versioning.md",
    ]
    for path in required:
        if version not in path.read_text(encoding="utf-8"):
            errors.append(
                f"{path.relative_to(ROOT)} does not mention current version {version}"
            )
    return errors


def run() -> None:
    errors = []
    errors.extend(validate_pairs())
    errors.extend(validate_local_links())
    errors.extend(validate_version_mentions())
    if errors:
        raise ValidationError("\n  - ".join([""] + errors))
    print("OK: bilingual documentation parity and local links validated")


if __name__ == "__main__":
    try:
        run()
    except ValidationError as exc:
        print(f"ERROR:{exc}", file=sys.stderr)
        raise SystemExit(1) from exc
