import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from create_global_dashboard import (
    apply_dashboard,
    build_dashboard_payload,
    convert_field,
    find_editable_dashboards,
    load_template_dashboard,
)


class FakeAPI:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def call(self, method, params, authenticated=True):
        self.calls.append((method, params, authenticated))
        response = self.responses[method]
        return response(params) if callable(response) else response


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
                                "value": {
                                    "host": "VERTIV by SNMP",
                                    "key": "ups.battery.charge",
                                },
                            },
                            {
                                "type": "INTEGER",
                                "name": "value_size",
                                "value": "26",
                            },
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
    assert (widget["x"], widget["y"], widget["width"], widget["height"]) == (
        50,
        0,
        11,
        2,
    )
    assert widget["fields"][0] == {
        "type": 4,
        "name": "itemid.0",
        "value": "12345",
    }
    assert widget["fields"][1] == {
        "type": 0,
        "name": "value_size",
        "value": "26",
    }


def test_find_dashboard_only_requests_editable_exact_name():
    api = FakeAPI({"dashboard.get": []})
    assert find_editable_dashboards(api, "Vertiv UPS - Test") == []
    method, params, authenticated = api.calls[0]
    assert method == "dashboard.get"
    assert authenticated is True
    assert params["filter"] == {"name": ["Vertiv UPS - Test"]}
    assert params["editable"] is True


def test_apply_dashboard_creates_when_no_editable_match_exists():
    payload = {"name": "Vertiv UPS - Test", "pages": []}
    api = FakeAPI(
        {
            "dashboard.get": [],
            "dashboard.create": {"dashboardids": ["101"]},
        }
    )

    action, ids = apply_dashboard(api, payload, replace=False)

    assert action == "Created"
    assert ids == ["101"]
    assert [call[0] for call in api.calls] == ["dashboard.get", "dashboard.create"]


def test_apply_dashboard_refuses_existing_without_replace():
    payload = {"name": "Vertiv UPS - Test", "pages": []}
    api = FakeAPI(
        {"dashboard.get": [{"dashboardid": "101", "name": "Vertiv UPS - Test"}]}
    )

    with pytest.raises(RuntimeError, match="Use --replace"):
        apply_dashboard(api, payload, replace=False)

    assert [call[0] for call in api.calls] == ["dashboard.get"]


def test_apply_dashboard_updates_single_match_in_place():
    payload = {
        "name": "Vertiv UPS - Test",
        "private": 1,
        "pages": [{"name": "Overview", "widgets": []}],
    }
    api = FakeAPI(
        {
            "dashboard.get": [{"dashboardid": "101", "name": "Vertiv UPS - Test"}],
            "dashboard.update": {"dashboardids": ["101"]},
        }
    )

    action, ids = apply_dashboard(api, payload, replace=True)

    assert action == "Updated"
    assert ids == ["101"]
    assert [call[0] for call in api.calls] == ["dashboard.get", "dashboard.update"]
    update_payload = api.calls[1][1]
    assert update_payload["dashboardid"] == "101"
    assert update_payload["pages"] == payload["pages"]
    assert "users" not in update_payload
    assert "userGroups" not in update_payload
    assert all(call[0] != "dashboard.delete" for call in api.calls)


def test_apply_dashboard_rejects_ambiguous_editable_matches_without_mutation():
    payload = {"name": "Vertiv UPS - Test", "pages": []}
    api = FakeAPI(
        {
            "dashboard.get": [
                {"dashboardid": "101", "name": "Vertiv UPS - Test"},
                {"dashboardid": "202", "name": "Vertiv UPS - Test"},
            ]
        }
    )

    with pytest.raises(RuntimeError, match="Multiple editable dashboards"):
        apply_dashboard(api, payload, replace=True)

    assert [call[0] for call in api.calls] == ["dashboard.get"]
