import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_docs


def test_bilingual_pairs_exist():
    assert validate_docs.validate_pairs() == []


def test_local_markdown_links():
    assert validate_docs.validate_local_links() == []


def test_version_mentions():
    assert validate_docs.validate_version_mentions() == []


def test_trigger_documentation_matches_template():
    assert validate_docs.validate_trigger_docs() == []


def test_macro_documentation_matches_template():
    assert validate_docs.validate_macro_docs() == []


def test_branch_and_release_policy_is_documented():
    assert validate_docs.validate_branch_policy_docs() == []
