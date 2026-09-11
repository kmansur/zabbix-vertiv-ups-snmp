from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path.cwd()
DASHBOARD_NAME = "VERTIV UPS Overview"

GREEN = "C8E6C9"
YELLOW = "FFF3CD"
ORANGE = "FFE0B2"
RED = "FFCDD2"
BLUE = "E3F2FD"
GRAY = "ECEFF1"
DARK = "263238"

# Item-value widget description macro. {ITEM.LASTVALUE} is value-map aware in Zabbix;
# the regexp additionally strips a trailing raw value if the frontend/server renders one.
CLEAN_MAPPED_VALUE = r'{{ITEM.LASTVALUE}.regsub("^(.+?)(?:\\s+\\([^)]*\\))?$","\\1")}'

STATUS_RULES: dict[str, dict] = {
    "vertiv.system.status": {
        "base": GRAY,
        "thresholds": [(1, GREEN), (2, YELLOW), (8, YELLOW), (16, ORANGE), (32, RED)],
    },
    "ups.output.source": {
        "base": GRAY,
        "thresholds": [(1, YELLOW), (2, RED), (3, GREEN), (4, YELLOW), (5, ORANGE), (6, YELLOW), (7, YELLOW)],
    },
    "ups.battery.status": {
        "base": GRAY,
        "thresholds": [(1, YELLOW), (2, GREEN), (3, ORANGE), (4, RED)],
    },
    "vertiv.battery.test.result": {
        "base": GRAY,
        "thresholds": [(0, YELLOW), (1, GREEN), (2, RED), (3, YELLOW), (4, RED), (5, ORANGE)],
    },
    "vertiv.shutdown.reason": {
        "base": GRAY,
        "thresholds": [(0, GREEN), (1, RED), (2, RED), (3, RED), (4, RED), (5, ORANGE), (6, RED), (7, ORANGE), (8, ORANGE), (9, RED), (10, ORANGE)],
    },
    "vertiv.eco.status": {
        "base": GRAY,
        "thresholds": [(0, GREEN), (1, GREEN)],
    },
    "vertiv.topology": {"base": BLUE, "thresholds": []},
    "vertiv.battery.cabinet.type": {"base": BLUE, "thresholds": []},
    "vertiv.battery.test.interval": {"base": BLUE, "thresholds": []},
}

NUMERIC_RULES: dict[str, dict] = {
    "ups.alarms.present": {
        "base": GREEN,
        "thresholds": [(1, YELLOW), (2, ORANGE), (3, RED)],
    },
    "ups.battery.charge": {
        "base": RED,
        "thresholds": [(20, ORANGE), (40, YELLOW), (80, GREEN)],
    },
    "ups.battery.runtime": {
        "base": RED,
        "thresholds": [(5, ORANGE), (10, YELLOW), (30, GREEN)],
    },
}


def set_field(fields: list[dict], field_type: str, name: str, value: str) -> None:
    fields[:] = [field for field in fields if field.get("name") != name]
    fields.append({"type": field_type, "name": name, "value": value})


def remove_fields(fields: list[dict], prefixes: tuple[str, ...], names: set[str]) -> None:
    fields[:] = [
        field
        for field in fields
        if not any(str(field.get("name", "")).startswith(prefix) for prefix in prefixes)
        and str(field.get("name", "")) not in names
    ]


def widget_item_key(widget: dict) -> str:
    for field in widget.get("fields", []):
        if field.get("type") == "ITEM" and field.get("name") == "itemid.0":
            value = field.get("value")
            if isinstance(value, dict):
                return str(value.get("key", ""))
    return ""


def apply_thresholds(fields: list[dict], base: str, thresholds: list[tuple[int, str]]) -> None:
    remove_fields(fields, ("thresholds.",), {"bg_color"})
    set_field(fields, "STRING", "bg_color", base)
    for index, (threshold, color) in enumerate(thresholds):
        set_field(fields, "STRING", f"thresholds.{index}.color", color)
        set_field(fields, "STRING", f"thresholds.{index}.threshold", str(threshold))


def style_status_card(widget: dict, rule: dict) -> None:
    fields = widget.setdefault("fields", [])
    remove_fields(
        fields,
        ("show.", "thresholds."),
        {
            "bg_color",
            "value_size",
            "decimal_size",
            "units_size",
            "value_h_pos",
            "value_v_pos",
            "value_bold",
            "value_color",
            "description",
            "desc_size",
            "desc_h_pos",
            "desc_v_pos",
            "desc_bold",
            "desc_color",
        },
    )
    # Show Description only. The description macro expands the mapped latest value,
    # which removes the raw numeric suffix from cards such as "Normal operation (1.00)".
    set_field(fields, "INTEGER", "show.0", "1")
    set_field(fields, "STRING", "description", CLEAN_MAPPED_VALUE)
    set_field(fields, "INTEGER", "desc_size", "18")
    set_field(fields, "INTEGER", "desc_h_pos", "1")
    set_field(fields, "INTEGER", "desc_v_pos", "1")
    set_field(fields, "INTEGER", "desc_bold", "1")
    set_field(fields, "STRING", "desc_color", DARK)
    apply_thresholds(fields, rule["base"], rule["thresholds"])


def style_numeric_card(widget: dict, rule: dict) -> None:
    fields = widget.setdefault("fields", [])
    remove_fields(fields, ("thresholds.",), {"bg_color"})
    # Retain the 1.3.3 value-only typography and add only dynamic background colors.
    apply_thresholds(fields, rule["base"], rule["thresholds"])


def tune_overview_layout(page: dict) -> None:
    # Give System status extra width; keep the row at the native 72-column dashboard width.
    layout = {
        "System status": (0, 16),
        "Output source": (16, 12),
        "Active alarms": (28, 10),
        "Battery status": (38, 12),
        "Battery charge": (50, 11),
        "Runtime remaining": (61, 11),
    }
    for widget in page.get("widgets", []):
        if widget.get("name") in layout and str(widget.get("y")) == "0":
            x, width = layout[widget["name"]]
            widget["x"] = str(x)
            widget["width"] = str(width)


def update_template(version: str) -> None:
    path = ROOT / "templates" / version / "vertiv-by-snmp.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    template = data["zabbix_export"]["templates"][0]
    dashboard = next(
        dashboard
        for dashboard in template.get("dashboards", [])
        if dashboard.get("name") == DASHBOARD_NAME
    )

    status_seen: set[str] = set()
    numeric_seen: set[str] = set()
    for page in dashboard.get("pages", []):
        if page.get("name") == "Overview":
            tune_overview_layout(page)
        for widget in page.get("widgets", []):
            if widget.get("type") != "item":
                continue
            key = widget_item_key(widget)
            if key in STATUS_RULES:
                style_status_card(widget, STATUS_RULES[key])
                status_seen.add(key)
            elif key in NUMERIC_RULES:
                style_numeric_card(widget, NUMERIC_RULES[key])
                numeric_seen.add(key)

    missing_status = sorted(set(STATUS_RULES) - status_seen)
    # Some informational status keys are not present on every dashboard page; that is fine.
    required_status = {
        "vertiv.system.status",
        "ups.output.source",
        "ups.battery.status",
        "vertiv.battery.test.result",
        "vertiv.shutdown.reason",
        "vertiv.eco.status",
        "vertiv.battery.cabinet.type",
        "vertiv.battery.test.interval",
    }
    missing_required = sorted(required_status - status_seen)
    if missing_required:
        raise RuntimeError(f"Missing required preview status widgets in {path}: {missing_required}")
    if set(NUMERIC_RULES) - numeric_seen:
        raise RuntimeError(f"Missing numeric preview widgets in {path}: {sorted(set(NUMERIC_RULES) - numeric_seen)}")

    description = str(template.get("description", ""))
    preview_note = (
        "\n\nPreview branch: status cards render the value-map-aware {ITEM.LASTVALUE} "
        "as the widget description, suppressing raw numeric suffixes, while numeric "
        "thresholds drive pastel green/yellow/orange/red backgrounds."
    )
    if "Preview branch: status cards" not in description:
        description += preview_note
        template["description"] = description

    header = (
        "# SPDX-License-Identifier: MIT\n"
        "# Copyright (C) 2026 Karim Mansur / Net Tech\n"
        "# See NOTICE.md for attribution to the original Vertiv template reference.\n"
    )
    path.write_text(
        header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )


def write_docs() -> None:
    en = ROOT / "docs/en/dashboard-status-preview.md"
    pt = ROOT / "docs/pt-BR/dashboard-status-preview.md"
    en.write_text(
        """# Dashboard status-card preview

[Português (Brasil)](../pt-BR/dashboard-status-preview.md)

This provisional branch experiments with cleaner and more operational UPS status cards without changing SNMP collection, triggers, or the project version.

## What changes

- Status/value-map cards show only the mapped text (for example `Normal operation`, `Normal`, `Passed`, `External`, `8 weeks`).
- The raw numeric suffix normally rendered by the Item value widget is suppressed by showing a value-map-aware `{ITEM.LASTVALUE}` macro in the widget Description field.
- Numeric thresholds continue to use the original numeric item, so background colors can change dynamically.
- Pastel colors are used for readability: green = normal, yellow = attention, orange = alarm/degraded, red = critical, blue = informational/configuration.
- System status receives additional width in the Overview row.
- Active alarms, battery charge, and remaining runtime receive numeric threshold backgrounds.

This is a preview only. The main branch remains unchanged until the visual result is approved.
""",
        encoding="utf-8",
    )
    pt.write_text(
        """# Preview dos cards de status do dashboard

[English](../en/dashboard-status-preview.md)

Este branch provisório testa cards de status do nobreak mais limpos e operacionais sem alterar a coleta SNMP, triggers ou a versão do projeto.

## O que muda

- Cards de status/value map mostram somente o texto mapeado (por exemplo `Normal operation`, `Normal`, `Passed`, `External`, `8 weeks`).
- O sufixo numérico bruto normalmente exibido pelo widget Item value é ocultado mostrando uma macro `{ITEM.LASTVALUE}` consciente de value map no campo Description do widget.
- Os thresholds continuam usando o item numérico original, portanto a cor de fundo pode mudar dinamicamente.
- São usadas cores em tons suaves para manter legibilidade: verde = normal, amarelo = atenção, laranja = alarme/degradado, vermelho = crítico, azul = informativo/configuração.
- O card System status recebe largura adicional na linha Overview.
- Active alarms, Battery charge e Runtime remaining recebem fundos dinâmicos por threshold numérico.

Este é apenas um preview. O branch main permanece inalterado até a aprovação visual.
""",
        encoding="utf-8",
    )


def validate_preview() -> None:
    for version in ("7.0", "8.0"):
        path = ROOT / "templates" / version / "vertiv-by-snmp.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        template = data["zabbix_export"]["templates"][0]
        dashboard = next(d for d in template["dashboards"] if d["name"] == DASHBOARD_NAME)
        widgets = [w for p in dashboard["pages"] for w in p["widgets"] if w.get("type") == "item"]
        by_key = {widget_item_key(w): w for w in widgets}

        for key in {
            "vertiv.system.status",
            "ups.output.source",
            "ups.battery.status",
            "vertiv.battery.test.result",
            "vertiv.shutdown.reason",
            "vertiv.eco.status",
            "vertiv.battery.cabinet.type",
            "vertiv.battery.test.interval",
        }:
            widget = by_key[key]
            fields = {f["name"]: f for f in widget["fields"]}
            shown = {str(f["value"]) for name, f in fields.items() if name.startswith("show.")}
            if shown != {"1"}:
                raise RuntimeError(f"{version}: {key} must be description-only")
            if fields["description"]["value"] != CLEAN_MAPPED_VALUE:
                raise RuntimeError(f"{version}: {key} missing clean mapped-value macro")
            if "bg_color" not in fields:
                raise RuntimeError(f"{version}: {key} missing background color")

        system = by_key["vertiv.system.status"]
        if system.get("width") != "16":
            raise RuntimeError(f"{version}: System status width is not 16")

        for key in NUMERIC_RULES:
            fields = {f["name"]: f for f in by_key[key]["fields"]}
            if "bg_color" not in fields or not any(name.startswith("thresholds.") for name in fields):
                raise RuntimeError(f"{version}: {key} missing numeric background thresholds")


def main() -> None:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != "1.3.3":
        raise RuntimeError("Preview must start from project version 1.3.3")
    for version in ("7.0", "8.0"):
        update_template(version)
    write_docs()
    validate_preview()


if __name__ == "__main__":
    main()
