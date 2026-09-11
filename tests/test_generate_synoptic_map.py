import base64
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from generate_synoptic_map import (
    ICON_OK,
    ICON_PROBLEM,
    build_export,
    render_yaml,
)


def test_map_export_for_zabbix_7():
    data = build_export("UPS-SRV01", "7.0")
    export = data["zabbix_export"]
    assert export["version"] == "7.0"
    assert export["maps"][0]["name"] == "VERTIV UPS Synoptic - UPS-SRV01"
    assert export["maps"][0]["selements"][0]["elements"] == [{"host": "UPS-SRV01"}]
    assert len(export["maps"][0]["lines"]) == 4
    assert {
        shape["text"].split("\n", 1)[0] for shape in export["maps"][0]["shapes"]
    } >= {
        "INPUT",
        "OUTPUT",
        "BYPASS",
        "BATTERY",
    }


def test_map_export_for_zabbix_8():
    data = build_export("UPS-SRV01", "8.0")
    assert data["zabbix_export"]["version"] == "8.0"


def test_embedded_icons_are_png():
    images = {
        image["name"]: image
        for image in build_export("UPS-SRV01")["zabbix_export"]["images"]
    }
    assert set(images) == {ICON_OK, ICON_PROBLEM}
    for image in images.values():
        decoded = base64.b64decode(image["encodedImage"])
        assert decoded.startswith(b"\x89PNG\r\n\x1a\n")
        assert len(decoded) > 100


def test_rendered_yaml_round_trip():
    rendered = render_yaml("UPS-SRV01", "7.0")
    data = yaml.safe_load(rendered)
    assert (
        data["zabbix_export"]["maps"][0]["selements"][0]["elements"][0]["host"]
        == "UPS-SRV01"
    )


def test_empty_host_is_rejected():
    with pytest.raises(ValueError, match="must not be empty"):
        build_export("   ")


def test_unsupported_version_is_rejected():
    with pytest.raises(ValueError, match="unsupported Zabbix version"):
        build_export("UPS-SRV01", "6.0")
