"""Create a global Zabbix dashboard from the native template dashboard.

The script keeps the template dashboard as the single source of truth. It reads
its pages/widgets from the repository YAML, resolves template item/graph
references against a real monitored host, and creates a global dashboard via
the Zabbix API.
"""

from __future__ import annotations

import argparse
import json
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

FIELD_TYPES = {
    "INTEGER": 0,
    "STRING": 1,
    "HOST_GROUP": 2,
    "HOST": 3,
    "ITEM": 4,
    "ITEM_PROTOTYPE": 5,
    "GRAPH": 6,
    "GRAPH_PROTOTYPE": 7,
    "MAP": 8,
    "SERVICE": 9,
    "SLA": 10,
    "USER": 11,
    "ACTION": 12,
    "MEDIA_TYPE": 13,
}


class ZabbixAPIError(RuntimeError):
    pass


class ZabbixAPI:
    def __init__(self, url: str, token: str, verify_tls: bool = True) -> None:
        base = url.rstrip("/")
        self.url = (
            base if base.endswith("api_jsonrpc.php") else f"{base}/api_jsonrpc.php"
        )
        self.token = token
        self.context = None if verify_tls else ssl._create_unverified_context()
        self.request_id = 0

    def call(self, method: str, params: Any, authenticated: bool = True) -> Any:
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.request_id,
        }
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json-rpc"}
        if authenticated:
            headers["Authorization"] = f"Bearer {self.token}"

        request = urllib.request.Request(
            self.url, data=data, headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(
                request, context=self.context, timeout=30
            ) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise ZabbixAPIError(f"API connection failed: {exc}") from exc

        if "error" in result:
            error = result["error"]
            raise ZabbixAPIError(
                f"{method} failed: {error.get('message', 'API error')} - "
                f"{error.get('data', '')}"
            )
        return result["result"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a global dashboard from the Vertiv template dashboard."
    )
    parser.add_argument(
        "--url",
        required=True,
        help="Zabbix frontend URL, e.g. https://zabbix.example.com",
    )
    parser.add_argument("--token", required=True, help="Zabbix API token")
    parser.add_argument(
        "--host",
        required=True,
        help="Technical or visible name of the monitored UPS host",
    )
    parser.add_argument(
        "--dashboard-name",
        default=None,
        help="Global dashboard name (default: 'Vertiv UPS - <host>')",
    )
    parser.add_argument(
        "--template-dashboard",
        default="Vertiv UPS Overview",
        help="Native template dashboard name to clone",
    )
    parser.add_argument(
        "--template-file",
        type=Path,
        default=None,
        help=(
            "Override template YAML path; normally selected from the server "
            "major.minor version"
        ),
    )
    parser.add_argument(
        "--public", action="store_true", help="Create a public dashboard"
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete an existing dashboard with the same name",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve references and print the API payload only",
    )
    parser.add_argument(
        "--insecure", action="store_true", help="Disable TLS certificate validation"
    )
    return parser.parse_args()


def repository_root() -> Path:
    return Path(__file__).resolve().parents[1]


def select_template_file(server_version: str, override: Path | None) -> Path:
    if override:
        return override
    parts = server_version.split(".")
    if len(parts) < 2:
        raise RuntimeError(f"Unexpected Zabbix version: {server_version}")
    version = f"{parts[0]}.{parts[1]}"
    candidate = repository_root() / "templates" / version / "vertiv-by-snmp.yaml"
    if not candidate.exists():
        supported = sorted(
            p.parent.name
            for p in (repository_root() / "templates").glob(
                "*/vertiv-by-snmp.yaml"
            )
        )
        raise RuntimeError(
            f"No template export for Zabbix {version}. "
            f"Available exports: {', '.join(supported)}"
        )
    return candidate


def load_template_dashboard(path: Path, dashboard_name: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        document = yaml.safe_load(handle)

    templates = document.get("zabbix_export", {}).get("templates", [])
    for template in templates:
        for dashboard in template.get("dashboards", []):
            if dashboard.get("name") == dashboard_name:
                return dashboard
    raise RuntimeError(f"Template dashboard '{dashboard_name}' was not found in {path}")


def resolve_host(api: ZabbixAPI, host_name: str) -> dict[str, str]:
    hosts = api.call(
        "host.get",
        {
            "output": ["hostid", "host", "name"],
            "filter": {"host": [host_name]},
        },
    )
    if not hosts:
        hosts = api.call(
            "host.get",
            {
                "output": ["hostid", "host", "name"],
                "filter": {"name": [host_name]},
            },
        )
    if len(hosts) != 1:
        raise RuntimeError(
            f"Expected exactly one host matching '{host_name}', found {len(hosts)}"
        )
    return hosts[0]


def load_item_index(api: ZabbixAPI, hostid: str) -> dict[str, str]:
    items = api.call(
        "item.get",
        {
            "output": ["itemid", "key_"],
            "hostids": [hostid],
            "webitems": True,
        },
    )
    return {item["key_"]: item["itemid"] for item in items}


def load_graph_index(api: ZabbixAPI, hostid: str) -> dict[str, str]:
    graphs = api.call(
        "graph.get",
        {
            "output": ["graphid", "name"],
            "hostids": [hostid],
        },
    )
    return {graph["name"]: graph["graphid"] for graph in graphs}


def convert_field(
    field: dict[str, Any], item_index: dict[str, str], graph_index: dict[str, str]
) -> dict[str, Any]:
    raw_type = field["type"]
    field_type = FIELD_TYPES.get(raw_type, raw_type)
    value = field.get("value")

    if field_type == 4 and isinstance(value, dict):
        key = value.get("key")
        if not key or key not in item_index:
            raise RuntimeError(f"Unable to resolve item key '{key}' on target host")
        value = item_index[key]
    elif field_type == 6 and isinstance(value, dict):
        name = value.get("name")
        if not name or name not in graph_index:
            raise RuntimeError(f"Unable to resolve graph '{name}' on target host")
        value = graph_index[name]
    elif isinstance(value, dict):
        raise RuntimeError(
            "Unsupported structured field reference: "
            f"type={raw_type}, name={field.get('name')}, value={value}"
        )

    return {"type": int(field_type), "name": field["name"], "value": value}


def build_dashboard_payload(
    source: dict[str, Any],
    dashboard_name: str,
    private: int,
    item_index: dict[str, str],
    graph_index: dict[str, str],
) -> dict[str, Any]:
    pages: list[dict[str, Any]] = []
    for source_page in source.get("pages", []):
        page: dict[str, Any] = {"name": source_page.get("name", "")}
        widgets: list[dict[str, Any]] = []
        for source_widget in source_page.get("widgets", []):
            widget: dict[str, Any] = {
                "type": source_widget["type"],
                "x": int(source_widget.get("x", 0)),
                "y": int(source_widget.get("y", 0)),
                "width": int(source_widget.get("width", 1)),
                "height": int(source_widget.get("height", 1)),
                "view_mode": int(source_widget.get("view_mode", 0)),
                "fields": [
                    convert_field(field, item_index, graph_index)
                    for field in source_widget.get("fields", [])
                ],
            }
            if source_widget.get("name"):
                widget["name"] = source_widget["name"]
            widgets.append(widget)
        page["widgets"] = widgets
        pages.append(page)

    return {
        "name": dashboard_name,
        "private": private,
        "display_period": 30,
        "auto_start": 0,
        "pages": pages,
    }


def find_dashboard(api: ZabbixAPI, name: str) -> list[dict[str, str]]:
    return api.call(
        "dashboard.get",
        {
            "output": ["dashboardid", "name"],
            "filter": {"name": [name]},
        },
    )


def main() -> int:
    args = parse_args()
    api = ZabbixAPI(args.url, args.token, verify_tls=not args.insecure)

    server_version = api.call("apiinfo.version", {}, authenticated=False)
    template_file = select_template_file(server_version, args.template_file)
    source = load_template_dashboard(template_file, args.template_dashboard)
    host = resolve_host(api, args.host)
    item_index = load_item_index(api, host["hostid"])
    graph_index = load_graph_index(api, host["hostid"])
    dashboard_name = args.dashboard_name or f"Vertiv UPS - {host['name']}"

    payload = build_dashboard_payload(
        source,
        dashboard_name,
        0 if args.public else 1,
        item_index,
        graph_index,
    )

    if args.dry_run:
        print(
            json.dumps(
                {
                    "server_version": server_version,
                    "template_file": str(template_file),
                    "dashboard": payload,
                },
                indent=2,
            )
        )
        return 0

    existing = find_dashboard(api, dashboard_name)
    if existing and not args.replace:
        raise RuntimeError(
            f"Dashboard '{dashboard_name}' already exists. "
            "Use --replace to recreate it explicitly."
        )
    if existing:
        api.call("dashboard.delete", [entry["dashboardid"] for entry in existing])

    result = api.call("dashboard.create", payload)
    dashboard_ids = result.get("dashboardids", [])
    print(
        f"Created global dashboard '{dashboard_name}' for host '{host['name']}' "
        f"on Zabbix {server_version}: {', '.join(dashboard_ids)}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, ZabbixAPIError, OSError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
