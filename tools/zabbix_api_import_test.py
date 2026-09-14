#!/usr/bin/env python3
"""Import a template into a running Zabbix frontend through the JSON-RPC API."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


def call_api(url: str, method: str, params: Any, token: str | None = None) -> Any:
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json-rpc"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))
    if "error" in result:
        raise RuntimeError(
            f"Zabbix API {method} failed: {json.dumps(result['error'], sort_keys=True)}"
        )
    return result.get("result")


def wait_for_api(url: str, timeout: int) -> None:
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            version = call_api(url, "apiinfo.version", [])
            print(f"Zabbix API ready: {version}")
            return
        except (OSError, RuntimeError, urllib.error.URLError) as exc:
            last_error = exc
            time.sleep(3)
    raise RuntimeError(
        f"Zabbix API did not become ready within {timeout}s: {last_error}"
    )


def import_template(
    url: str, template_path: Path, username: str, password: str
) -> None:
    token = call_api(url, "user.login", {"username": username, "password": password})
    rules = {
        "template_groups": {"createMissing": True, "updateExisting": True},
        "templates": {"createMissing": True, "updateExisting": True},
        "items": {"createMissing": True, "updateExisting": True, "deleteMissing": True},
        "discoveryRules": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True,
        },
        "triggers": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True,
        },
        "graphs": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True,
        },
        "valueMaps": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True,
        },
        "templateDashboards": {
            "createMissing": True,
            "updateExisting": True,
            "deleteMissing": True,
        },
        "templateLinkage": {"createMissing": True, "deleteMissing": False},
    }
    source = template_path.read_text(encoding="utf-8")
    result = call_api(
        url,
        "configuration.import",
        {"format": "yaml", "rules": rules, "source": source},
        token,
    )
    if result is not True:
        raise RuntimeError(
            f"configuration.import returned unexpected result: {result!r}"
        )
    templates = call_api(
        url,
        "template.get",
        {
            "output": ["templateid", "host", "name"],
            "filter": {"host": ["VERTIV by SNMP"]},
        },
        token,
    )
    if len(templates) != 1 or templates[0].get("name") != "Vertiv by SNMP":
        raise RuntimeError(f"imported template verification failed: {templates!r}")
    print(f"Imported and verified template: {templates[0]}")
    call_api(url, "user.logout", [], token)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8080/api_jsonrpc.php")
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--username", default="Admin")
    parser.add_argument("--password", default="zabbix")
    parser.add_argument("--wait", type=int, default=180)
    args = parser.parse_args()
    wait_for_api(args.url, args.wait)
    import_template(args.url, args.template, args.username, args.password)


if __name__ == "__main__":
    main()
