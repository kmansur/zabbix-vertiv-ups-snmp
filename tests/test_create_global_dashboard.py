from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from create_global_dashboard import build_dashboard_payload, convert_field, load_template_dashboard  # noqa: E402


def test_template_dashboard_exists_in_both_exports():
    for version in ("7.0", "8.0"):
        dashboard = load_template_dashboard(
            ROOT / "templates" / version / "vertiv-by-snmp.yaml",
            "Vertiv UPS Overview",
        )
        assert dashboard["name"] == "Vertiv UPS Overview"
        assert [page["name"] for page in dashboard["pages"]] == [
            "Overview",
            "Electrical",
            "Battery & Environment",
        ]


def test_convert_item_and_graph_references():
    item = convert_field(
        {
            "type": "ITEM",
            "name": "itemid.0",
            "value": {"host": "VERTIV by SNMP", "key": "ups.battery.charge"},
        },
        {"ups.battery.charge": "12345"},
        {},
    )
    assert item == {"type": 4, "name": "itemid.0", "value": "12345"}

    graph = convert_field(
        {
            "type": "GRAPH",
            "name": "graphid.0",
            "value": {"host": "VERTIV by SNMP", "name": "UPS: Output power"},
        },
        {},
        {"UPS: Output power": "67890"},
    )
    assert graph == {"type": 6, "name": "graphid.0", "value": "67890"}


def test_build_payload_preserves_layout_and_converts_scalar_types():
    source = {
        "pages": [
            {
                "name": "Overview",
                "widgets": [
                    {
                        "type": "item",
                        "name": "Battery charge",
                        "x": "50",
                        "y": "0",
                        "width": "11",
                        "height": "2",
                        "fields": [
                            {
                                "type": "ITEM",
                                "name": "itemid.0",
                                "value": {"host": "VERTIV by SNMP", "key": "ups.battery.charge"},
                            },
                            {"type": "INTEGER", "name": "value_size", "value": "26"},
                        ],
                    }
                ],
            }
        ]
    }
    payload = build_dashboard_payload(
        source,
        "Vertiv UPS - Test",
        1,
        {"ups.battery.charge": "12345"},
        {},
    )
    widget = payload["pages"][0]["widgets"][0]
    assert payload["name"] == "Vertiv UPS - Test"
    assert payload["private"] == 1
    assert (widget["x"], widget["y"], widget["width"], widget["height"]) == (50, 0, 11, 2)
    assert widget["fields"][0] == {"type": 4, "name": "itemid.0", "value": "12345"}
    assert widget["fields"][1] == {"type": 0, "name": "value_size", "value": "26"}
