from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_visible_and_technical_template_names_are_intentional():
    for version in ("7.0", "8.0"):
        data = yaml.safe_load(
            (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(
                encoding="utf-8"
            )
        )
        template = data["zabbix_export"]["templates"][0]
        assert template["template"] == "VERTIV by SNMP"
        assert template["name"] == "Vertiv by SNMP"
        assert template["dashboards"][0]["name"] == "Vertiv UPS Overview"


def test_trigger_docs_use_the_stable_technical_identifier():
    for path in (ROOT / "docs/en/triggers.md", ROOT / "docs/pt-BR/triggers.md"):
        text = path.read_text(encoding="utf-8")
        assert "/VERTIV by SNMP/" in text
        assert "/Vertiv by SNMP/" not in text


def test_release_assets_have_unique_names_checksums_and_stable_marker():
    text = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "vertiv-by-snmp-zabbix-7.0.yaml" in text
    assert "vertiv-by-snmp-zabbix-8.0.yaml" in text
    assert "SHA256SUMS" in text
    assert "cp -r templates docs tools" in text
    assert "STABLE_VERSION" in text
    assert 'stable_version="$(tr -d' in text
    assert 'stable_version" != "$tag_version' in text


def test_candidate_and_stable_versions_are_explicit_and_ordered():
    candidate = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    stable = (ROOT / "STABLE_VERSION").read_text(encoding="utf-8").strip()

    def semver_tuple(value: str) -> tuple[int, int, int]:
        parts = value.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)
        return tuple(int(part) for part in parts)

    candidate_version = semver_tuple(candidate)
    stable_version = semver_tuple(stable)
    assert stable_version <= candidate_version


def test_workflows_use_current_action_major():
    for name in ("ci.yml", "security.yml", "release.yml"):
        text = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
        assert "actions/checkout@v6" not in text
        assert "actions/setup-python@v6" not in text
        assert "actions/checkout@v7" in text


def test_preview_only_docs_are_not_part_of_release_tree():
    assert not (ROOT / "docs/en/dashboard-status-preview.md").exists()
    assert not (ROOT / "docs/pt-BR/dashboard-status-preview.md").exists()
