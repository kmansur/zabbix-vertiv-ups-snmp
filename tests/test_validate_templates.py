from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_templates  # noqa: E402


def test_version_is_semver():
    assert validate_templates.SEMVER_RE.fullmatch(validate_templates.load_version())


def test_versioned_templates_validate():
    version = validate_templates.load_version()
    loaded = {}
    for export_version, path in validate_templates.TEMPLATE_FILES.items():
        data = validate_templates.load_template(path)
        validate_templates.validate_one(export_version, data, version)
        loaded[export_version] = data
    validate_templates.validate_semantic_parity(
        loaded["7.0"], loaded["8.0"]
    )


def test_template_is_read_only_for_known_control_branches():
    for path in validate_templates.TEMPLATE_FILES.values():
        text = path.read_text(encoding="utf-8")
        for prefix in validate_templates.FORBIDDEN_OID_PREFIXES:
            assert prefix not in text
