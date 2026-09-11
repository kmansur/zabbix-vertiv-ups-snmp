from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import validate_docs  # noqa: E402


def test_bilingual_pairs_exist():
    assert validate_docs.validate_pairs() == []


def test_local_markdown_links():
    assert validate_docs.validate_local_links() == []


def test_version_mentions():
    assert validate_docs.validate_version_mentions() == []
