from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path.cwd()
TEMPLATE_ID = "VERTIV by SNMP"
DASHBOARD = "Vertiv UPS Overview"
PROJECT_VERSION = "1.4.1"
VENDOR_VERSION = "1.4-1"
RUNTIME_HOURS_UUID = "77cb62fff87e4a5e99f9a3b178d1db91"
INLET_GRAPH_UUID = "f5ede3274cfa45d18dd0ffd571f93725"


def item_widget(name: str, key: str, x: int, y: int, width: int = 12, *, integer: bool = False) -> dict:
    fields = [
        {"type": "ITEM", "name": "itemid.0", "value": {"host": TEMPLATE_ID, "key": key}},
        {"type": "INTEGER", "name": "show.0", "value": "2"},
        {"type": "INTEGER", "name": "value_size", "value": "27"},
        {"type": "INTEGER", "name": "decimal_size", "value": "16"},
        {"type": "INTEGER", "name": "units_size", "value": "16"},
        {"type": "INTEGER", "name": "value_h_pos", "value": "1"},
        {"type": "INTEGER", "name": "value_v_pos", "value": "1"},
    ]
    if integer:
        fields.append({"type": "INTEGER", "name": "decimal_places", "value": "0"})
    return {"type": "item", "name": name, "x": str(x), "y": str(y), "width": str(width), "height": "2", "fields": fields}


def graph_widget(name: str, graph_name: str, ref: str, x: int, y: int, width: int, height: int = 6) -> dict:
    return {
        "type": "graph",
        "name": name,
        "x": str(x),
        "y": str(y),
        "width": str(width),
        "height": str(height),
        "fields": [
            {"type": "GRAPH", "name": "graphid.0", "value": {"host": TEMPLATE_ID, "name": graph_name}},
            {"type": "STRING", "name": "reference", "value": ref},
        ],
    }


def widget_key(widget: dict) -> str:
    for field in widget.get("fields", []):
        if field.get("type") == "ITEM" and field.get("name") == "itemid.0":
            value = field.get("value")
            if isinstance(value, dict):
                return str(value.get("key", ""))
    return ""


def set_field(widget: dict, field_type: str, name: str, value: str | int | float) -> None:
    fields = widget.setdefault("fields", [])
    fields[:] = [f for f in fields if f.get("name") != name]
    fields.append({"type": field_type, "name": name, "value": str(value)})


def find_page(dashboard: dict, name: str) -> dict:
    return next(page for page in dashboard.get("pages", []) if page.get("name") == name)


def ensure_runtime_hours(template: dict) -> None:
    items = template.setdefault("items", [])
    if any(item.get("key") == "ups.battery.runtime.hours" for item in items):
        return
    raw_index = next(i for i, item in enumerate(items) if item.get("key") == "ups.battery.runtime")
    runtime_hours = {
        "uuid": RUNTIME_HOURS_UUID,
        "name": "UPS: Estimated runtime remaining (hours)",
        "type": "CALCULATED",
        "key": "ups.battery.runtime.hours",
        "delay": "30s",
        "history": "90d",
        "value_type": "FLOAT",
        "units": "h",
        "params": "last(//ups.battery.runtime)/60",
        "description": "Display-oriented conversion of RFC1628 upsEstimatedMinutesRemaining from minutes to hours. The raw minutes item remains authoritative for triggers.",
        "tags": [{"tag": "component", "value": "battery"}],
    }
    items.insert(raw_index + 1, runtime_hours)


def fix_overview(page: dict) -> None:
    item_widgets = [w for w in page.get("widgets", []) if w.get("type") == "item"]
    page["widgets"] = item_widgets + [
        graph_widget("Battery charge and runtime", "UPS: Battery charge and runtime", "A0000", 0, 2, 24),
        graph_widget("Output power", "UPS: Output power", "A0001", 24, 2, 24),
        graph_widget("Output phase load", "UPS: Output phase load", "A0002", 48, 2, 24),
    ]
    for widget in item_widgets:
        if widget_key(widget) == "ups.battery.runtime":
            for field in widget.get("fields", []):
                if field.get("type") == "ITEM" and field.get("name") == "itemid.0":
                    field["value"]["key"] = "ups.battery.runtime.hours"
            set_field(widget, "INTEGER", "decimal_places", 1)
            set_field(widget, "INTEGER", "value_size", 24)
            fields = widget.setdefault("fields", [])
            fields[:] = [f for f in fields if not str(f.get("name", "")).startswith("thresholds.") and f.get("name") != "bg_color"]
            fields.extend([
                {"type": "STRING", "name": "bg_color", "value": "FFCDD2"},
                {"type": "STRING", "name": "thresholds.0.color", "value": "FFE0B2"},
                {"type": "STRING", "name": "thresholds.0.threshold", "value": "0.083333"},
                {"type": "STRING", "name": "thresholds.1.color", "value": "FFF3CD"},
                {"type": "STRING", "name": "thresholds.1.threshold", "value": "0.166667"},
                {"type": "STRING", "name": "thresholds.2.color", "value": "C8E6C9"},
                {"type": "STRING", "name": "thresholds.2.threshold", "value": "0.5"},
            ])


def fix_electrical(page: dict) -> None:
    widgets = page.get("widgets", [])
    existing_items = {widget_key(w): w for w in widgets if w.get("type") == "item"}
    wanted = [
        ("vertiv.output.power", "Output power", 0),
        ("vertiv.output.apparent.power", "Output apparent power", 12),
        ("ups.output.frequency", "Output frequency", 24),
        ("vertiv.input.frequency", "Input frequency", 36),
        ("ups.bypass.frequency", "Bypass frequency", 48),
        ("vertiv.topology", "Topology", 60),
    ]
    for key, name, x in wanted:
        widget = existing_items.get(key)
        if widget is None:
            widget = item_widget(name, key, x, 2)
            widgets.append(widget)
            existing_items[key] = widget
        widget["name"], widget["x"], widget["y"], widget["width"], widget["height"] = name, str(x), "2", "12", "2"
    counters = [
        ("vertiv.input.blackout.count", "Input blackouts", 0),
        ("vertiv.input.brownout.count", "Input brownouts", 12),
        ("ups.input.line.bads", "Bad input lines", 24),
    ]
    for key, name, x in counters:
        widget = existing_items.get(key)
        if widget is None:
            widget = item_widget(name, key, x, 4, integer=True)
            widgets.append(widget)
            existing_items[key] = widget
        widget["name"], widget["x"], widget["y"], widget["width"], widget["height"] = name, str(x), "4", "12", "2"
        set_field(widget, "INTEGER", "decimal_places", 0)
    widgets[:] = [w for w in widgets if not (w.get("type") == "graph" and w.get("name") == "Output phase load")]
    widgets.append(graph_widget("Output phase load", "UPS: Output phase load", "C0001", 0, 6, 72))


def fix_battery(page: dict) -> None:
    widgets = page.get("widgets", [])
    for widget in widgets:
        key = widget_key(widget)
        if key == "ups.battery.runtime":
            for field in widget.get("fields", []):
                if field.get("type") == "ITEM" and field.get("name") == "itemid.0":
                    field["value"]["key"] = "ups.battery.runtime.hours"
            set_field(widget, "INTEGER", "decimal_places", 1)
            set_field(widget, "INTEGER", "value_size", 24)
            fields = widget.setdefault("fields", [])
            fields[:] = [f for f in fields if not str(f.get("name", "")).startswith("thresholds.") and f.get("name") != "bg_color"]
            fields.extend([
                {"type": "STRING", "name": "bg_color", "value": "FFCDD2"},
                {"type": "STRING", "name": "thresholds.0.color", "value": "FFE0B2"},
                {"type": "STRING", "name": "thresholds.0.threshold", "value": "0.083333"},
                {"type": "STRING", "name": "thresholds.1.color", "value": "FFF3CD"},
                {"type": "STRING", "name": "thresholds.1.threshold", "value": "0.166667"},
                {"type": "STRING", "name": "thresholds.2.color", "value": "C8E6C9"},
                {"type": "STRING", "name": "thresholds.2.threshold", "value": "0.5"},
            ])
        elif key == "vertiv.battery.discharge.count":
            set_field(widget, "INTEGER", "decimal_places", 0)
    widgets[:] = [w for w in widgets if w.get("type") != "graph"]
    widgets.extend([
        graph_widget("Battery charge and runtime", "UPS: Battery charge and runtime", "D0000", 0, 4, 36),
        graph_widget("Inlet temperature", "UPS: Inlet temperature", "D0001", 36, 4, 36),
    ])


def fix_graphs(export: dict) -> None:
    graphs = export.setdefault("graphs", [])
    battery_graph = next(g for g in graphs if g.get("name") == "UPS: Battery charge and runtime")
    for graph_item in battery_graph.get("graph_items", []):
        item = graph_item.get("item", {})
        if item.get("key") == "ups.battery.runtime":
            item["key"] = "ups.battery.runtime.hours"
    if not any(g.get("name") == "UPS: Inlet temperature" for g in graphs):
        graphs.append({
            "uuid": INLET_GRAPH_UUID,
            "name": "UPS: Inlet temperature",
            "graph_items": [{
                "sortorder": "0",
                "color": "F63100",
                "item": {"host": TEMPLATE_ID, "key": "vertiv.inlet.temperature"},
            }],
            "show_work_period": "NO",
        })


def update_template(version: str) -> None:
    path = ROOT / "templates" / version / "vertiv-by-snmp.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    export = data["zabbix_export"]
    template = export["templates"][0]
    template["vendor"]["version"] = VENDOR_VERSION
    ensure_runtime_hours(template)
    dashboard = next(d for d in template.get("dashboards", []) if d.get("name") == DASHBOARD)
    fix_overview(find_page(dashboard, "Overview"))
    fix_electrical(find_page(dashboard, "Electrical"))
    fix_battery(find_page(dashboard, "Battery & Environment"))
    fix_graphs(export)
    desc = str(template.get("description", ""))
    if "Version 1.4.1" not in desc:
        marker = f"\n\nExport target: Zabbix {version}."
        desc = desc.replace(marker, "\n\nVersion 1.4.1 fixes the field dashboard layout, displays runtime in hours while preserving raw RFC1628 minutes for triggers, replaces cumulative-counter graphs with readable counter cards, and separates inlet temperature from the raw battery-temperature trend.\n" + marker)
        template["description"] = desc
    header = "# SPDX-License-Identifier: MIT\n# Copyright (C) 2026 Karim Mansur / Net Tech\n# See NOTICE.md for attribution to the original Vertiv template reference.\n"
    path.write_text(header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000), encoding="utf-8")


def replace_version(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = text.replace("1.4.0\n```", "1.4.1\n```")
    text = text.replace("project version `1.4.0` is exported as `vendor.version: 1.4-0`", "project version `1.4.1` is exported as `vendor.version: 1.4-1`")
    text = text.replace("versão `1.4.0` do projeto é exportada como `vendor.version: 1.4-0`", "versão `1.4.1` do projeto é exportada como `vendor.version: 1.4-1`")
    path.write_text(text, encoding="utf-8")


def add_changelog(path: Path, portuguese: bool) -> None:
    text = path.read_text(encoding="utf-8")
    if "## [1.4.1] - 2026-09-11" in text:
        return
    if portuguese:
        section = """## [1.4.1] - 2026-09-11

### Corrigido

- Reorganizado o dashboard após a remoção das métricas privadas de potência de entrada não validadas, eliminando grandes áreas vazias.
- Autonomia exibida em horas por um item calculado de apresentação, mantendo o item RFC1628 original em minutos para triggers e diagnóstico.
- O gráfico de bateria passa a usar horas, evitando a apresentação `Kmin` do frontend.
- Contadores cumulativos de blackout, brownout e linha inválida deixam de ocupar um gráfico de tendência no dashboard e passam a cards numéricos na página Electrical.
- O gráfico padrão de ambiente passa a mostrar somente a temperatura de entrada; a temperatura privada da bateria continua coletada e disponível, mas não distorce mais a escala do gráfico quando a própria placa informa valores sentinela como `-0.1 °C`.
- O gráfico de carga por fase ocupa a largura da página Electrical e os cards elétricos foram redistribuídos.
- Contadores de descargas e eventos são exibidos sem casas decimais.

### Observação de campo

No equipamento Vertiv ITA-20kVA validado, a própria interface web do nobreak informa `4320 min` de autonomia e `-0.1 °C` de temperatura de bateria. A 1.4.1 não altera esses dados de origem: apenas apresenta a autonomia como horas e evita tratar a temperatura privada da bateria como referência ambiental padrão.

"""
    else:
        section = """## [1.4.1] - 2026-09-11

### Fixed

- Reflowed the dashboard after removing unvalidated private input-power metrics, eliminating large empty regions.
- Runtime is displayed in hours through a presentation calculated item while the original RFC1628 minutes item remains authoritative for triggers and troubleshooting.
- The battery graph now uses hours, avoiding the frontend `Kmin` representation.
- Cumulative blackout, brownout and bad-line counters are no longer used as a dashboard trend graph and are shown as numeric cards on the Electrical page.
- The default environment graph now shows inlet temperature only; private battery temperature remains collected and available without distorting the default graph when the management card reports sentinel-like values such as `-0.1 °C`.
- Output phase load now spans the Electrical page and electrical cards were reflowed.
- Discharge/event counters are displayed without decimal places.

### Field note

On the validated Vertiv ITA-20kVA device, the UPS web interface itself reports `4320 min` runtime and `-0.1 °C` battery temperature. Version 1.4.1 does not rewrite those source values; it converts runtime to hours for presentation and keeps the private battery-temperature value out of the default environmental trend.

"""
    text = text.replace("## [1.4.0] - 2026-09-11", section + "## [1.4.0] - 2026-09-11", 1)
    path.write_text(text, encoding="utf-8")


def update_dashboard_docs(path: Path, portuguese: bool) -> None:
    text = path.read_text(encoding="utf-8")
    if "1.4.1" in text:
        return
    if portuguese:
        extra = """

## Ajustes de campo na versão 1.4.1

A página **Overview** usa três gráficos principais em uma única linha: carga/autonomia da bateria, potência de saída e carga de saída por fase. O antigo gráfico de contadores cumulativos foi retirado do dashboard porque uma linha crescente/cumulativa não representa bem eventos operacionais.

A página **Electrical** apresenta blackout, brownout e linhas inválidas como cards de contadores e usa o gráfico de carga por fase em largura total. A página **Battery & Environment** exibe autonomia em horas e usa um gráfico dedicado de temperatura de entrada.

O item bruto `ups.battery.runtime` permanece em minutos para preservar a semântica RFC1628 e as triggers. O item calculado `ups.battery.runtime.hours` existe apenas para apresentação. A temperatura privada de bateria continua disponível em Latest data e no gráfico legado `UPS: Temperatures`, mas não é usada no gráfico ambiental padrão porque alguns firmwares podem expor valores não físicos/sentinela quando não há sensor útil.
"""
    else:
        extra = """

## Field refinements in version 1.4.1

The **Overview** page uses three primary graphs in one row: battery charge/runtime, output power and output phase load. The cumulative-counter graph was removed from the dashboard because cumulative lines are not a useful operational event visualization.

The **Electrical** page shows blackout, brownout and bad-line values as counter cards and gives the output phase-load graph the full page width. **Battery & Environment** displays runtime in hours and uses a dedicated inlet-temperature graph.

The raw `ups.battery.runtime` item remains in minutes to preserve RFC1628 semantics and trigger behavior. The calculated `ups.battery.runtime.hours` item is presentation-only. Private battery temperature remains available in Latest data and in the legacy `UPS: Temperatures` graph, but is not used by the default environmental graph because some firmware can expose non-physical/sentinel-like values when no useful battery-temperature sensor is present.
"""
    path.write_text(text + extra, encoding="utf-8")


def update_validator() -> None:
    path = ROOT / "tools/validate_templates.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace('    "vertiv.battery.test.interval",\n}', '    "vertiv.battery.test.interval",\n    "ups.battery.runtime.hours",\n}')
    text = text.replace('"ups.battery.runtime": "24",', '"ups.battery.runtime.hours": "24",')
    marker = '    fixed_keys, prototype_keys = collect_item_keys(template)\n'
    block = '''    runtime_hours = item_by_key.get("ups.battery.runtime.hours")
    if runtime_hours is None:
        errors.append("missing calculated runtime-hours display item")
    else:
        if runtime_hours.get("type") != "CALCULATED":
            errors.append("ups.battery.runtime.hours must be CALCULATED")
        if str(runtime_hours.get("params")) != "last(//ups.battery.runtime)/60":
            errors.append("ups.battery.runtime.hours must derive from raw RFC1628 minutes / 60")
        if str(runtime_hours.get("units")) != "h":
            errors.append("ups.battery.runtime.hours must use h units")

    main_dashboard = next((d for d in dashboards if d.get("name") == REQUIRED_DASHBOARD_NAME), None)
    if main_dashboard:
        pages = {str(p.get("name")): p for p in main_dashboard.get("pages", [])}
        overview_graphs = {str(w.get("name")) for w in pages.get("Overview", {}).get("widgets", []) if w.get("type") == "graph"}
        if overview_graphs != {"Battery charge and runtime", "Output power", "Output phase load"}:
            errors.append(f"unexpected Overview graph set: {sorted(overview_graphs)}")
        electrical_keys = {
            str(field.get("value", {}).get("key"))
            for w in pages.get("Electrical", {}).get("widgets", [])
            if w.get("type") == "item"
            for field in w.get("fields", [])
            if field.get("type") == "ITEM" and isinstance(field.get("value"), dict)
        }
        for required in ("vertiv.input.blackout.count", "vertiv.input.brownout.count", "ups.input.line.bads"):
            if required not in electrical_keys:
                errors.append(f"Electrical page is missing counter card {required}")
        battery_graphs = {str(w.get("name")) for w in pages.get("Battery & Environment", {}).get("widgets", []) if w.get("type") == "graph"}
        if battery_graphs != {"Battery charge and runtime", "Inlet temperature"}:
            errors.append(f"unexpected Battery & Environment graph set: {sorted(battery_graphs)}")

'''
    if block not in text:
        text = text.replace(marker, block + marker, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != "1.4.0":
        raise RuntimeError("1.4.1 fix must start from project version 1.4.0")
    for version in ("7.0", "8.0"):
        update_template(version)
    (ROOT / "VERSION").write_text(PROJECT_VERSION + "\n", encoding="utf-8")
    for path in (ROOT / "docs/en/versioning.md", ROOT / "docs/pt-BR/versioning.md"):
        replace_version(path)
    add_changelog(ROOT / "CHANGELOG.md", False)
    add_changelog(ROOT / "CHANGELOG.pt-BR.md", True)
    update_dashboard_docs(ROOT / "docs/en/dashboard.md", False)
    update_dashboard_docs(ROOT / "docs/pt-BR/dashboard.md", True)
    update_validator()


if __name__ == "__main__":
    main()
