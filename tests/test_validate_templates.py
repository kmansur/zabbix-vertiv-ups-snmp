import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_templates


def test_version_is_semver():
    assert validate_templates.SEMVER_RE.fullmatch(validate_templates.load_version())


def test_zabbix_vendor_version_format():
    assert validate_templates.zabbix_vendor_version("1.1.0") == "1.1-0"


def test_versioned_templates_validate():
    version = validate_templates.load_version()
    stable_version = validate_templates.load_stable_version()
    allowed_vendor_versions = {validate_templates.zabbix_vendor_version(version)}
    if version != stable_version:
        allowed_vendor_versions.add(
            validate_templates.zabbix_vendor_version(stable_version)
        )

    loaded = {}
    for export_version, path in validate_templates.TEMPLATE_FILES.items():
        data = validate_templates.load_template(path)
        validate_templates.validate_one(
            export_version,
            data,
            allowed_vendor_versions,
        )
        loaded[export_version] = data
    validate_templates.validate_semantic_parity(loaded["7.0"], loaded["8.0"])


def test_template_is_read_only_for_known_control_branches():
    for path in validate_templates.TEMPLATE_FILES.values():
        text = path.read_text(encoding="utf-8")
        for prefix in validate_templates.FORBIDDEN_OID_PREFIXES:
            assert prefix not in text
