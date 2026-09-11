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


def test_release_assets_have_unique_names_and_checksums():
    text = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
    assert "vertiv-by-snmp-zabbix-7.0.yaml" in text
    assert "vertiv-by-snmp-zabbix-8.0.yaml" in text
    assert "SHA256SUMS" in text
    assert "cp -r templates docs tools" in text


def test_workflows_use_current_action_major():
    for name in ("ci.yml", "security.yml", "release.yml"):
        text = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
        assert "actions/checkout@v6" not in text
        assert "actions/setup-python@v6" not in text
        assert "actions/checkout@v7" in text


def test_preview_only_docs_are_not_part_of_release_tree():
    assert not (ROOT / "docs/en/dashboard-status-preview.md").exists()
    assert not (ROOT / "docs/pt-BR/dashboard-status-preview.md").exists()
