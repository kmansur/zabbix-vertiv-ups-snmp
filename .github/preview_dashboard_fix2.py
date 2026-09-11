from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path.cwd()
DASHBOARD_NAME = "VERTIV UPS Overview"

STATUS_KEYS = {
    "vertiv.system.status",
    "ups.output.source",
    "ups.battery.status",
    "vertiv.battery.test.result",
    "vertiv.shutdown.reason",
    "vertiv.eco.status",
    "vertiv.topology",
    "vertiv.battery.cabinet.type",
    "vertiv.battery.test.interval",
}

NUMERIC_KEYS = {
    "ups.alarms.present",
    "ups.battery.charge",
    "ups.battery.runtime",
}


def widget_item_key(widget: dict) -> str:
    for field in widget.get("fields", []):
        if field.get("type") == "ITEM" and field.get("name") == "itemid.0":
            value = field.get("value")
            if isinstance(value, dict):
                return str(value.get("key", ""))
    return ""


def set_field(fields: list[dict], field_type: str, name: str, value: int | str) -> None:
    fields[:] = [field for field in fields if field.get("name") != name]
    fields.append({"type": field_type, "name": name, "value": str(value)})


def remove_fields(fields: list[dict], names: set[str]) -> None:
    fields[:] = [field for field in fields if str(field.get("name", "")) not in names]


def style_status_widget(widget: dict) -> None:
    fields = widget.setdefault("fields", [])
    remove_fields(
        fields,
        {
            "description",
            "desc_size",
            "desc_h_pos",
            "desc_v_pos",
            "desc_bold",
            "desc_color",
        },
    )
    fields[:] = [
        field
        for field in fields
        if not str(field.get("name", "")).startswith("show.")
    ]
    set_field(fields, "INTEGER", "show.0", 2)
    set_field(fields, "INTEGER", "value_size", 21)
    set_field(fields, "INTEGER", "value_h_pos", 1)
    set_field(fields, "INTEGER", "value_v_pos", 1)
    set_field(fields, "INTEGER", "value_bold", 1)
    set_field(fields, "STRING", "value_color", "263238")
    set_field(fields, "INTEGER", "decimal_places", 0)


def style_numeric_widget(widget: dict) -> None:
    fields = widget.setdefault("fields", [])
    key = widget_item_key(widget)
    if key == "ups.alarms.present":
        set_field(fields, "INTEGER", "decimal_places", 0)
    elif key == "ups.battery.runtime":
        set_field(fields, "INTEGER", "decimal_places", 0)
        set_field(fields, "INTEGER", "value_size", 24)
    elif key == "ups.battery.charge":
        set_field(fields, "INTEGER", "value_size", 26)


def tune_overview_layout(page: dict) -> None:
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
        current
        for current in template.get("dashboards", [])
        if current.get("name") == DASHBOARD_NAME
    )

    seen: set[str] = set()
    for page in dashboard.get("pages", []):
        if page.get("name") == "Overview":
            tune_overview_layout(page)
        for widget in page.get("widgets", []):
            if widget.get("type") != "item":
                continue
            key = widget_item_key(widget)
            if key in STATUS_KEYS:
                style_status_widget(widget)
                seen.add(key)
            elif key in NUMERIC_KEYS:
                style_numeric_widget(widget)
                seen.add(key)

    required = {
        "vertiv.system.status",
        "ups.output.source",
        "ups.battery.status",
        "vertiv.battery.test.result",
        "vertiv.shutdown.reason",
        "vertiv.eco.status",
        "vertiv.battery.cabinet.type",
        "vertiv.battery.test.interval",
        "ups.alarms.present",
        "ups.battery.charge",
        "ups.battery.runtime",
    }
    missing = sorted(required - seen)
    if missing:
        raise RuntimeError(f"missing expected widgets in Zabbix {version}: {missing}")

    header = (
        "# SPDX-License-Identifier: MIT\n"
        "# Copyright (C) 2026 Karim Mansur / Net Tech\n"
        "# See NOTICE.md for attribution to the original Vertiv template reference.\n"
    )
    path.write_text(
        header
        + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )


def write_docs() -> None:
    (ROOT / "docs/en/dashboard-status-preview.md").write_text(
        """# Dashboard status-card preview

[Português (Brasil)](../pt-BR/dashboard-status-preview.md)

This provisional branch keeps the dynamic pastel backgrounds and returns status cards to the native **Item value** rendering after the description-macro experiment proved unreliable on the tested Zabbix 7 frontend.

## Current preview behavior

- Status cards keep dynamic green/yellow/orange/red backgrounds based on the original numeric item and thresholds.
- Status text is rendered natively through the existing value map.
- Status/enum cards use zero decimal places, so mapped values render with a shorter raw suffix such as `(1)` instead of `(1.00)`.
- Long cards retain the widened layout introduced by the previous preview.
- Active alarms are rendered as an integer.
- Battery charge and runtime keep their dynamic severity backgrounds.

## Confirmed limitation

The attempt to strip the parenthesized numeric suffix by rendering a macro/regular expression in the widget Description field produced broken strings such as `\\1`, `\\3`, and `\\0` on the tested Zabbix 7 frontend. This branch intentionally removes that experiment.

The main branch remains unchanged while this visual behavior is evaluated.
""",
        encoding="utf-8",
    )
    (ROOT / "docs/pt-BR/dashboard-status-preview.md").write_text(
        """# Preview dos cards de status do dashboard

[English](../en/dashboard-status-preview.md)

Este branch provisório mantém os fundos dinâmicos em tons suaves e volta os cards de status para a renderização nativa do **Item value**, depois que o experimento com macro no campo Description se mostrou pouco confiável no frontend Zabbix 7 testado.

## Comportamento atual do preview

- Os cards de status mantêm fundos dinâmicos em verde/amarelo/laranja/vermelho usando o item numérico original e seus thresholds.
- O texto de status é renderizado nativamente pelo value map já existente.
- Cards de status/enum usam zero casas decimais, deixando o sufixo bruto mais curto, por exemplo `(1)` em vez de `(1.00)`.
- Cards com textos longos mantêm a largura ampliada criada no preview anterior.
- Active alarms é exibido como inteiro.
- Battery charge e Runtime remaining mantêm os fundos dinâmicos por criticidade.

## Limitação confirmada

A tentativa de remover o sufixo numérico entre parênteses usando macro/expressão regular no campo Description produziu strings quebradas como `\\1`, `\\3` e `\\0` no frontend Zabbix 7 testado. Este branch remove intencionalmente esse experimento.

O branch main permanece inalterado enquanto este comportamento visual é avaliado.
""",
        encoding="utf-8",
    )


def validate_preview() -> None:
    for version in ("7.0", "8.0"):
        path = ROOT / "templates" / version / "vertiv-by-snmp.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        template = data["zabbix_export"]["templates"][0]
        dashboard = next(
            current
            for current in template["dashboards"]
            if current["name"] == DASHBOARD_NAME
        )
        widgets = [
            widget
            for page in dashboard["pages"]
            for widget in page["widgets"]
            if widget.get("type") == "item"
        ]
        by_key = {widget_item_key(widget): widget for widget in widgets}

        for key in STATUS_KEYS:
            if key not in by_key:
                continue
            fields = {field["name"]: field for field in by_key[key]["fields"]}
            if "description" in fields:
                raise RuntimeError(f"{version}: description macro still present on {key}")
            if fields["show.0"]["value"] != "2":
                raise RuntimeError(f"{version}: {key} is not using native value rendering")
            if fields["decimal_places"]["value"] != "0":
                raise RuntimeError(f"{version}: {key} must use zero decimal places")
            if "bg_color" not in fields:
                raise RuntimeError(f"{version}: {key} lost its background color")

        for key in NUMERIC_KEYS:
            fields = {field["name"]: field for field in by_key[key]["fields"]}
            if "bg_color" not in fields:
                raise RuntimeError(f"{version}: {key} lost its background color")
            if not any(name.startswith("thresholds.") for name in fields):
                raise RuntimeError(f"{version}: {key} lost its thresholds")

        if by_key["vertiv.system.status"].get("width") != "16":
            raise RuntimeError(f"{version}: System status width must remain 16")


def main() -> None:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != "1.3.3":
        raise RuntimeError("preview fix must start from project version 1.3.3")
    for version in ("7.0", "8.0"):
        update_template(version)
    write_docs()
    validate_preview()


if __name__ == "__main__":
    main()
