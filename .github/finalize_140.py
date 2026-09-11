from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path.cwd()
PROJECT_VERSION = "1.4.0"
VENDOR_VERSION = "1.4-0"
TECHNICAL_NAME = "VERTIV by SNMP"
DISPLAY_NAME = "Vertiv by SNMP"
DASHBOARD_NAME = "Vertiv UPS Overview"
PROJECT_MATURITY = 85

STATUS_CARD_KEYS = {
    "vertiv.system.status",
    "ups.output.source",
    "ups.battery.status",
    "vertiv.topology",
    "vertiv.battery.test.result",
    "vertiv.shutdown.reason",
    "vertiv.eco.status",
    "vertiv.battery.cabinet.type",
    "vertiv.battery.test.interval",
}
DYNAMIC_STATUS_CARD_KEYS = {
    "vertiv.system.status",
    "ups.output.source",
    "ups.battery.status",
    "vertiv.battery.test.result",
    "vertiv.shutdown.reason",
    "vertiv.eco.status",
}


def dump_template(path: Path, data: dict) -> None:
    header = (
        "# SPDX-License-Identifier: MIT\n"
        "# Copyright (C) 2026 Karim Mansur / Net Tech\n"
        "# See NOTICE.md for attribution to the original Vertiv template reference.\n"
    )
    path.write_text(
        header + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000),
        encoding="utf-8",
    )


def item_key(widget: dict) -> str:
    for field in widget.get("fields", []):
        if field.get("type") == "ITEM" and field.get("name") == "itemid.0":
            value = field.get("value")
            if isinstance(value, dict):
                return str(value.get("key", ""))
    return ""


def update_template(export_version: str) -> None:
    path = ROOT / "templates" / export_version / "vertiv-by-snmp.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    export = data["zabbix_export"]
    template = export["templates"][0]
    if template.get("template") != TECHNICAL_NAME:
        raise RuntimeError(f"unexpected technical template name in {path}")

    # Keep the technical identifier stable so existing installations update in place.
    template["name"] = DISPLAY_NAME
    template["vendor"]["version"] = VENDOR_VERSION

    description = str(template.get("description", ""))
    description = description.replace("VERTIV by SNMP", DISPLAY_NAME)
    description = description.replace("VERTIV UPS Overview", DASHBOARD_NAME)
    description = re.sub(r"\n\nPreview branch:.*$", "", description, flags=re.S)
    description = re.sub(
        r"\n\nExport target: Zabbix (?:7\.0|8\.0)\.\s*$", "", description
    )
    if "Version 1.4.0" not in description:
        description += (
            "\n\nVersion 1.4.0 finalizes severity-colored dashboard cards, keeps native "
            "value-map rendering for reliable status text, changes the visible template name "
            "to Vertiv by SNMP while preserving the technical identifier for in-place upgrades, "
            "and removes unvalidated private input-power values from prominent dashboard views."
        )
    description += f"\n\nExport target: Zabbix {export_version}."
    template["description"] = description

    dashboards = template.get("dashboards", [])
    if len(dashboards) != 1:
        raise RuntimeError(f"expected one dashboard in {path}")
    dashboard = dashboards[0]
    dashboard["name"] = DASHBOARD_NAME

    # Private input-power scaling is not defined by the supplied SNMP documentation.
    # Keep the items/graph for troubleshooting, but do not feature them in the main dashboard.
    for page in dashboard.get("pages", []):
        widgets = page.get("widgets", [])
        page["widgets"] = [
            widget
            for widget in widgets
            if item_key(widget) != "vertiv.input.power.total"
            and widget.get("name") != "Input phase power"
        ]

    dump_template(path, data)


def replace_visible_product_name() -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        text = text.replace("VERTIV by SNMP", DISPLAY_NAME)
        text = text.replace("VERTIV UPS Overview", DASHBOARD_NAME)
        text = text.replace("VERTIV UPS", "Vertiv UPS")
        path.write_text(text, encoding="utf-8")

    generator = ROOT / "tools/generate_synoptic_map.py"
    text = generator.read_text(encoding="utf-8")
    text = text.replace("VERTIV by SNMP", DISPLAY_NAME)
    text = text.replace("VERTIV UPS", "Vertiv UPS")
    generator.write_text(text, encoding="utf-8")

    test_map = ROOT / "tests/test_generate_synoptic_map.py"
    text = test_map.read_text(encoding="utf-8")
    text = text.replace("VERTIV UPS", "Vertiv UPS")
    test_map.write_text(text, encoding="utf-8")


def update_versions() -> None:
    (ROOT / "VERSION").write_text(PROJECT_VERSION + "\n", encoding="utf-8")
    targets = [
        ROOT / "README.md",
        ROOT / "README.pt-BR.md",
        ROOT / "docs/en/versioning.md",
        ROOT / "docs/pt-BR/versioning.md",
    ]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        text = text.replace("1.3.3", PROJECT_VERSION)
        text = text.replace("1.3-3", VENDOR_VERSION)
        path.write_text(text, encoding="utf-8")


def add_project_status_docs() -> None:
    en = f'''# Project status\n\n[Português (Brasil)](../pt-BR/project-status.md)\n\n**Current project maturity: {PROJECT_MATURITY}%**\n\nThis percentage is a maintained engineering maturity score, not an uptime/SLA metric. It reflects the state of the template, field validation, automation and documentation.\n\n| Area | Score | Notes |\n| --- | ---: | --- |\n| Zabbix 7.0 core template and real-device validation | 30/30 | Import, collection, enum normalization and dashboard validated on real Vertiv hardware |\n| Dashboard and operator usability | 15/15 | Native dashboard, severity colors, readable mapped statuses and trend graphs |\n| Documentation, versioning, CI and security automation | 20/20 | Bilingual docs, validators, pytest, Ruff, CodeQL and release automation |\n| Read-only safety and control-OID exclusion | 10/10 | Consequential write/control branches are explicitly excluded and validated |\n| Private electrical scaling validation | 5/10 | Most displayed values are plausible; private input-power scale still requires confirmation |\n| Model/firmware coverage | 3/5 | One production device/card behavior has been validated in depth; broader coverage is pending |\n| Event-specific SNMP trap processing | 0/5 | Waiting for real trap payload capture before creating event-specific parsers/triggers |\n| Zabbix 8.0 runtime validation | 2/5 | Export parity is automated, but import/runtime testing against an actual Zabbix 8 build is pending |\n\n## Main remaining work\n\n1. Validate private input-power OID scaling against the UPS web/LCD values before using those metrics for alerting.\n2. Capture real Vertiv trap payloads and implement event-specific trap processing only from verified encodings.\n3. Validate additional UPS models and management-card firmware.\n4. Import and runtime-test the 8.0 export on an actual Zabbix 8 environment.\n5. Validate the optional synoptic map import on production-like Zabbix 7/8 instances.\n'''
    pt = f'''# Status do projeto\n\n[English](../en/project-status.md)\n\n**Maturidade atual do projeto: {PROJECT_MATURITY}%**\n\nEsse percentual é uma pontuação mantida de maturidade de engenharia, e não uma métrica de disponibilidade/SLA. Ele reflete o estado do template, validação em campo, automação e documentação.\n\n| Área | Pontuação | Observações |\n| --- | ---: | --- |\n| Template principal Zabbix 7.0 e validação em equipamento real | 30/30 | Importação, coleta, normalização de enums e dashboard validados em hardware Vertiv real |\n| Dashboard e usabilidade operacional | 15/15 | Dashboard nativo, cores por criticidade, estados mapeados legíveis e gráficos de tendência |\n| Documentação, versionamento, CI e automação de segurança | 20/20 | Documentação bilíngue, validadores, pytest, Ruff, CodeQL e automação de release |\n| Segurança somente leitura e exclusão de OIDs de controle | 10/10 | Ramos/OIDs de escrita consequencial são explicitamente excluídos e validados |\n| Validação de escala elétrica privada | 5/10 | A maioria dos valores exibidos é coerente; a escala da potência privada de entrada ainda precisa de confirmação |\n| Cobertura de modelos/firmwares | 3/5 | Um equipamento/placa de produção foi validado em profundidade; falta ampliar a cobertura |\n| Processamento específico de traps SNMP | 0/5 | Aguardando captura de payloads reais antes de criar parsers/triggers específicos |\n| Validação em execução no Zabbix 8.0 | 2/5 | A paridade do export é automatizada, mas ainda falta testar importação/execução em um Zabbix 8 real |\n\n## Principais trabalhos restantes\n\n1. Validar a escala dos OIDs privados de potência de entrada contra a interface web/LCD do nobreak antes de usar essas métricas em alertas.\n2. Capturar traps Vertiv reais e implementar processamento específico somente a partir de codificações confirmadas.\n3. Validar modelos adicionais de nobreak e firmwares de placas de gerenciamento.\n4. Importar e testar em execução o export 8.0 em um ambiente Zabbix 8 real.\n5. Validar a importação do mapa sinótico opcional em ambientes Zabbix 7/8 semelhantes à produção.\n'''
    (ROOT / "docs/en/project-status.md").write_text(en, encoding="utf-8")
    (ROOT / "docs/pt-BR/project-status.md").write_text(pt, encoding="utf-8")

    for path, anchor, line in (
        (
            ROOT / "README.md",
            "## What the template monitors\n",
            f"## Project status\n\n**Engineering maturity: {PROJECT_MATURITY}%** — see [project status and remaining work](docs/en/project-status.md).\n\n## What the template monitors\n",
        ),
        (
            ROOT / "README.pt-BR.md",
            "## O que o template monitora\n",
            f"## Status do projeto\n\n**Maturidade de engenharia: {PROJECT_MATURITY}%** — consulte o [status e os trabalhos restantes](docs/pt-BR/project-status.md).\n\n## O que o template monitora\n",
        ),
    ):
        text = path.read_text(encoding="utf-8")
        if "Engineering maturity:" not in text and "Maturidade de engenharia:" not in text:
            text = text.replace(anchor, line, 1)
        path.write_text(text, encoding="utf-8")

    for path, anchor, line in (
        (
            ROOT / "README.md",
            "- [Native dashboard](docs/en/dashboard.md)\n",
            "- [Native dashboard](docs/en/dashboard.md)\n- [Project status](docs/en/project-status.md)\n",
        ),
        (
            ROOT / "README.pt-BR.md",
            "- [Dashboard nativo](docs/pt-BR/dashboard.md)\n",
            "- [Dashboard nativo](docs/pt-BR/dashboard.md)\n- [Status do projeto](docs/pt-BR/project-status.md)\n",
        ),
    ):
        text = path.read_text(encoding="utf-8")
        if "project-status.md" not in text:
            text = text.replace(anchor, line, 1)
        path.write_text(text, encoding="utf-8")


def update_dashboard_docs() -> None:
    en = ROOT / "docs/en/dashboard.md"
    text = en.read_text(encoding="utf-8")
    text += '''\n## Version 1.4.0 status-card behavior\n\nThe finalized dashboard uses the native mapped **Item value** rendering for status cards. This keeps Zabbix value maps reliable across frontends while dynamic thresholds color the card background. Enum/status cards use zero decimal places, so mapped values render with compact raw suffixes such as `Normal (3)` instead of `Normal (3.00)`.\n\nSeverity colors use soft backgrounds: green for normal, yellow for attention, orange for degraded/alarm states and red for critical states. Static informational/configuration cards use a neutral or light-blue background.\n\nThe private calculated input-power card and input-phase-power graph are intentionally not featured on the dashboard because the supplied Vertiv SNMP documentation does not define the scale of those private OIDs. The underlying items remain available for field validation and troubleshooting.\n'''
    en.write_text(text, encoding="utf-8")

    pt = ROOT / "docs/pt-BR/dashboard.md"
    text = pt.read_text(encoding="utf-8")
    text += '''\n## Comportamento dos cards de status na versão 1.4.0\n\nO dashboard final utiliza a renderização nativa mapeada do **Item value** nos cards de status. Isso mantém os value maps do Zabbix confiáveis entre diferentes frontends, enquanto thresholds dinâmicos definem a cor de fundo do card. Cards de enum/status usam zero casas decimais, portanto valores mapeados aparecem com sufixos compactos como `Normal (3)` em vez de `Normal (3.00)`.\n\nAs cores de criticidade usam fundos suaves: verde para normal, amarelo para atenção, laranja para estados degradados/alarme e vermelho para estados críticos. Cards informativos/de configuração usam fundo neutro ou azul-claro.\n\nO card calculado de potência de entrada e o gráfico de potência de entrada por fase não são mais destacados no dashboard porque a documentação SNMP Vertiv fornecida não define a escala desses OIDs privados. Os itens continuam disponíveis para validação em campo e troubleshooting.\n'''
    pt.write_text(text, encoding="utf-8")


def update_electrical_docs() -> None:
    for path, note in (
        (
            ROOT / "docs/en/electrical-summary.md",
            "\n## Known scale limitation\n\nThe private Vertiv input-power OIDs (`6318`-`6320`) are retained for troubleshooting, but their numeric scale is not defined by the supplied SNMP parameter list. On the currently tested device, the calculated total did not match the expected magnitude from the UPS web interface. For that reason the input-power card/graph is not featured in the native dashboard and no trigger should rely on these values until the scale is confirmed on the target firmware.\n",
        ),
        (
            ROOT / "docs/pt-BR/electrical-summary.md",
            "\n## Limitação conhecida de escala\n\nOs OIDs privados Vertiv de potência de entrada (`6318`-`6320`) são mantidos para troubleshooting, mas a escala numérica não é definida pela lista de parâmetros SNMP fornecida. No equipamento atualmente testado, o total calculado não apresentou magnitude compatível com a interface web do nobreak. Por isso o card/gráfico de potência de entrada não é destacado no dashboard nativo e nenhum trigger deve depender desses valores até que a escala seja confirmada no firmware alvo.\n",
        ),
    ):
        text = path.read_text(encoding="utf-8")
        if "Known scale limitation" not in text and "Limitação conhecida de escala" not in text:
            text += note
        path.write_text(text, encoding="utf-8")


def update_changelogs() -> None:
    entries = {
        ROOT / "CHANGELOG.md": '''## [1.4.0] - 2026-09-11\n\n### Added\n\n- Project maturity/status documentation with an explicit **85%** engineering-maturity score and remaining validation work.\n- Dependency monitoring for Python packages in addition to GitHub Actions.\n- Repository hygiene tests for release packaging and workflow baselines.\n\n### Changed\n\n- Visible template name changed to **Vertiv by SNMP**. The technical template identifier remains `VERTIV by SNMP` intentionally so existing installations can update in place without creating a duplicate template.\n- Native dashboard renamed to **Vertiv UPS Overview**.\n- Finalized severity-colored status cards using native value-map rendering and zero decimal places for compact mapped enum values.\n- Updated GitHub Actions checkout/setup-python actions to v7.\n- Private input-power values remain available for troubleshooting but are no longer featured in the dashboard until their vendor-specific scale is validated.\n\n### Fixed\n\n- Aligned the template validator with the finalized dashboard typography/color configuration.\n- Removed stale preview-only macro-rendering text from template metadata.\n- Release packaging now uses unique Zabbix 7.0/8.0 asset filenames, includes the synoptic-map generator/tools, and publishes SHA-256 checksums.\n- Removed preview-only dashboard documentation from the finalized project.\n\n''',
        ROOT / "CHANGELOG.pt-BR.md": '''## [1.4.0] - 2026-09-11\n\n### Adicionado\n\n- Documentação do status/maturidade do projeto com pontuação explícita de **85%** e trabalhos de validação restantes.\n- Monitoramento de dependências Python pelo Dependabot, além das GitHub Actions.\n- Testes de higiene do repositório para empacotamento de release e baseline dos workflows.\n\n### Alterado\n\n- Nome visível do template alterado para **Vertiv by SNMP**. O identificador técnico permanece `VERTIV by SNMP` intencionalmente para permitir atualização in-place sem criar um template duplicado.\n- Dashboard nativo renomeado para **Vertiv UPS Overview**.\n- Cards de status com cores por criticidade finalizados usando value map nativo e zero casas decimais para enums compactos.\n- GitHub Actions checkout/setup-python atualizadas para v7.\n- Valores privados de potência de entrada continuam disponíveis para troubleshooting, mas deixam de ser destacados no dashboard até a validação da escala específica do fabricante.\n\n### Corrigido\n\n- Validador do template alinhado à configuração final de tipografia/cores do dashboard.\n- Removido texto obsoleto do preview de macros nos metadados do template.\n- Empacotamento de release agora usa nomes exclusivos para assets Zabbix 7.0/8.0, inclui o gerador/ferramentas do mapa sinótico e publica checksums SHA-256.\n- Removida a documentação exclusiva do preview do dashboard no projeto final.\n\n''',
    }
    for path, entry in entries.items():
        text = path.read_text(encoding="utf-8")
        if "## [1.4.0]" not in text:
            marker = "## [1.3.3] - 2026-09-11"
            text = text.replace(marker, entry + marker, 1)
        path.write_text(text, encoding="utf-8")


def update_versioning_docs() -> None:
    notes = {
        ROOT / "docs/en/versioning.md": "\n## Stable technical identifier\n\nStarting with 1.4.0 the visible template name is **Vertiv by SNMP**, while the technical export identifier remains `VERTIV by SNMP`. Keeping the technical identifier stable is deliberate: it allows imports to update existing installations instead of creating a second template only because capitalization changed.\n",
        ROOT / "docs/pt-BR/versioning.md": "\n## Identificador técnico estável\n\nA partir da 1.4.0 o nome visível do template é **Vertiv by SNMP**, enquanto o identificador técnico do export permanece `VERTIV by SNMP`. Manter o identificador técnico estável é intencional: isso permite atualizar instalações existentes sem criar um segundo template apenas por causa da capitalização.\n",
    }
    for path, note in notes.items():
        text = path.read_text(encoding="utf-8")
        if "Stable technical identifier" not in text and "Identificador técnico estável" not in text:
            text += note
        path.write_text(text, encoding="utf-8")


def update_docs_validator() -> None:
    path = ROOT / "tools/validate_docs.py"
    text = path.read_text(encoding="utf-8")
    if '"project-status.md"' not in text:
        text = text.replace('    "dashboard.md",\n', '    "dashboard.md",\n    "project-status.md",\n', 1)
    path.write_text(text, encoding="utf-8")


def update_template_validator() -> None:
    path = ROOT / "tools/validate_templates.py"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        'TEMPLATE_NAME = "VERTIV by SNMP"\n',
        'TEMPLATE_TECHNICAL_NAME = "VERTIV by SNMP"\nTEMPLATE_DISPLAY_NAME = "Vertiv by SNMP"\n',
        1,
    )
    text = text.replace("TEMPLATE_NAME", "TEMPLATE_TECHNICAL_NAME")
    text = text.replace(
        'REQUIRED_DASHBOARD_NAME = "VERTIV UPS Overview"',
        'REQUIRED_DASHBOARD_NAME = "Vertiv UPS Overview"',
    )
    text = text.replace(
        'if template.get("name") != TEMPLATE_TECHNICAL_NAME:\n        errors.append(f"visible template name must be {TEMPLATE_TECHNICAL_NAME!r}")',
        'if template.get("name") != TEMPLATE_DISPLAY_NAME:\n        errors.append(f"visible template name must be {TEMPLATE_DISPLAY_NAME!r}")',
        1,
    )

    start = text.index('                if widget.get("type") == "item":')
    end = text.index('    groups = {str(g.get("name")) for g in template.get("groups", [])}', start)
    block = '''                if widget.get("type") == "item":\n                    fields_by_name = {\n                        str(field.get("name")): field\n                        for field in widget.get("fields", [])\n                    }\n                    item_field = fields_by_name.get("itemid.0", {})\n                    item_ref = item_field.get("value", {})\n                    item_key = (\n                        str(item_ref.get("key", ""))\n                        if isinstance(item_ref, dict)\n                        else ""\n                    )\n                    shown = {\n                        str(field.get("value"))\n                        for name, field in fields_by_name.items()\n                        if name.startswith("show.")\n                    }\n                    if shown != {"2"}:\n                        errors.append(\n                            f"dashboard item widget requires value-only display: {widget.get('name')!r}"\n                        )\n                    for field_name in ("value_h_pos", "value_v_pos"):\n                        actual = str(fields_by_name.get(field_name, {}).get("value", ""))\n                        if actual != "1":\n                            errors.append(\n                                f"dashboard item widget alignment mismatch: {widget.get('name')!r} "\n                                f"{field_name}={actual!r}; expected '1'"\n                            )\n\n                    if item_key in DASHBOARD_STATUS_VALUE_KEYS:\n                        if str(fields_by_name.get("value_size", {}).get("value", "")) != "21":\n                            errors.append(\n                                f"dashboard status card value_size must be 21: {widget.get('name')!r}"\n                            )\n                        if str(fields_by_name.get("decimal_places", {}).get("value", "")) != "0":\n                            errors.append(\n                                f"dashboard status card decimal_places must be 0: {widget.get('name')!r}"\n                            )\n                        if "description" in fields_by_name:\n                            errors.append(\n                                f"dashboard status card must use native value rendering: {widget.get('name')!r}"\n                            )\n                        if "bg_color" not in fields_by_name:\n                            errors.append(\n                                f"dashboard status card is missing background color: {widget.get('name')!r}"\n                            )\n                    else:\n                        expected_size = {\n                            "ups.battery.charge": "26",\n                            "ups.battery.runtime": "24",\n                        }.get(item_key, "27")\n                        actual_size = str(fields_by_name.get("value_size", {}).get("value", ""))\n                        if actual_size != expected_size:\n                            errors.append(\n                                f"dashboard numeric card value_size mismatch: {widget.get('name')!r} "\n                                f"{actual_size!r}; expected {expected_size!r}"\n                            )\n                        for field_name in ("decimal_size", "units_size"):\n                            actual = str(fields_by_name.get(field_name, {}).get("value", ""))\n                            if actual != "16":\n                                errors.append(\n                                    f"dashboard numeric card typography mismatch: {widget.get('name')!r} "\n                                    f"{field_name}={actual!r}; expected '16'"\n                                )\n                        if item_key in {"ups.alarms.present", "ups.battery.runtime"}:\n                            if str(fields_by_name.get("decimal_places", {}).get("value", "")) != "0":\n                                errors.append(\n                                    f"dashboard numeric card decimal_places must be 0: {widget.get('name')!r}"\n                                )\n\n'''
    text = text[:start] + block + text[end:]

    set_start = text.index("DASHBOARD_TEXT_VALUE_KEYS = {")
    set_end = text.index("}\nUUID_RE", set_start) + 2
    new_set = '''DASHBOARD_STATUS_VALUE_KEYS = {\n    "vertiv.system.status",\n    "ups.output.source",\n    "ups.battery.status",\n    "vertiv.topology",\n    "vertiv.battery.test.result",\n    "vertiv.shutdown.reason",\n    "vertiv.eco.status",\n    "vertiv.battery.cabinet.type",\n    "vertiv.battery.test.interval",\n}\n'''
    text = text[:set_start] + new_set + text[set_end:]
    path.write_text(text, encoding="utf-8")


def write_release_workflow() -> None:
    content = '''name: Release\n\non:\n  push:\n    tags:\n      - "v*"\n\npermissions:\n  contents: write\n\njobs:\n  release:\n    runs-on: ubuntu-latest\n\n    steps:\n      - name: Checkout repository\n        uses: actions/checkout@v7\n\n      - name: Set up Python\n        uses: actions/setup-python@v7\n        with:\n          python-version: "3.14"\n\n      - name: Install validation dependencies\n        run: python -m pip install -r requirements-dev.txt\n\n      - name: Validate tag and project version\n        shell: bash\n        run: |\n          set -euo pipefail\n          project_version="$(tr -d '\\r\\n' < VERSION)"\n          tag_version="${GITHUB_REF_NAME#v}"\n          if [[ "$project_version" != "$tag_version" ]]; then\n            echo "VERSION ($project_version) does not match tag ($tag_version)" >&2\n            exit 1\n          fi\n          python tools/validate_templates.py\n          python tools/validate_docs.py\n          pytest -q\n\n      - name: Build release assets\n        shell: bash\n        run: |\n          set -euo pipefail\n          version="$(tr -d '\\r\\n' < VERSION)"\n          package="zabbix-vertiv-ups-snmp-${version}"\n          mkdir -p "dist/${package}"\n          cp -r templates docs tools "dist/${package}/"\n          cp README.md README.pt-BR.md \\\n             CHANGELOG.md CHANGELOG.pt-BR.md \\\n             CONTRIBUTING.md CONTRIBUTING.pt-BR.md \\\n             SECURITY.md SECURITY.pt-BR.md \\\n             LICENSE NOTICE.md NOTICE.pt-BR.md VERSION requirements-dev.txt \\\n             "dist/${package}/"\n          cp templates/7.0/vertiv-by-snmp.yaml "dist/vertiv-by-snmp-zabbix-7.0.yaml"\n          cp templates/8.0/vertiv-by-snmp.yaml "dist/vertiv-by-snmp-zabbix-8.0.yaml"\n          (cd dist && zip -r "${package}.zip" "${package}")\n          (cd dist && sha256sum \\\n            vertiv-by-snmp-zabbix-7.0.yaml \\\n            vertiv-by-snmp-zabbix-8.0.yaml \\\n            "${package}.zip" > SHA256SUMS)\n\n      - name: Create GitHub Release\n        env:\n          GH_TOKEN: ${{ github.token }}\n        run: |\n          version="$(tr -d '\\r\\n' < VERSION)"\n          gh release create "${GITHUB_REF_NAME}" \\\n            "dist/vertiv-by-snmp-zabbix-7.0.yaml" \\\n            "dist/vertiv-by-snmp-zabbix-8.0.yaml" \\\n            "dist/zabbix-vertiv-ups-snmp-${version}.zip" \\\n            "dist/SHA256SUMS" \\\n            --title "Vertiv by SNMP ${GITHUB_REF_NAME}" \\\n            --generate-notes\n'''
    (ROOT / ".github/workflows/release.yml").write_text(content, encoding="utf-8")


def update_workflows_and_dependabot() -> None:
    for name in ("ci.yml", "security.yml"):
        path = ROOT / ".github/workflows" / name
        text = path.read_text(encoding="utf-8")
        text = text.replace("actions/checkout@v6", "actions/checkout@v7")
        text = text.replace("actions/setup-python@v6", "actions/setup-python@v7")
        path.write_text(text, encoding="utf-8")

    path = ROOT / ".github/dependabot.yml"
    text = path.read_text(encoding="utf-8")
    if "package-ecosystem: pip" not in text:
        text += '''\n  - package-ecosystem: pip\n    directory: "/"\n    schedule:\n      interval: monthly\n    labels:\n      - dependencies\n'''
    path.write_text(text, encoding="utf-8")


def write_hygiene_test() -> None:
    content = '''from pathlib import Path\n\nimport yaml\n\nROOT = Path(__file__).resolve().parents[1]\n\n\ndef test_visible_and_technical_template_names_are_intentional():\n    for version in ("7.0", "8.0"):\n        data = yaml.safe_load((ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(encoding="utf-8"))\n        template = data["zabbix_export"]["templates"][0]\n        assert template["template"] == "VERTIV by SNMP"\n        assert template["name"] == "Vertiv by SNMP"\n        assert template["dashboards"][0]["name"] == "Vertiv UPS Overview"\n\n\ndef test_release_assets_have_unique_names_and_checksums():\n    text = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")\n    assert "vertiv-by-snmp-zabbix-7.0.yaml" in text\n    assert "vertiv-by-snmp-zabbix-8.0.yaml" in text\n    assert "SHA256SUMS" in text\n    assert "cp -r templates docs tools" in text\n\n\ndef test_workflows_use_current_action_major():\n    for name in ("ci.yml", "security.yml", "release.yml"):\n        text = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")\n        assert "actions/checkout@v6" not in text\n        assert "actions/setup-python@v6" not in text\n        assert "actions/checkout@v7" in text\n\n\ndef test_preview_only_docs_are_not_part_of_release_tree():\n    assert not (ROOT / "docs/en/dashboard-status-preview.md").exists()\n    assert not (ROOT / "docs/pt-BR/dashboard-status-preview.md").exists()\n'''
    (ROOT / "tests/test_repository_hygiene.py").write_text(content, encoding="utf-8")


def remove_preview_docs() -> None:
    for path in (
        ROOT / "docs/en/dashboard-status-preview.md",
        ROOT / "docs/pt-BR/dashboard-status-preview.md",
    ):
        if path.exists():
            path.unlink()


def final_self_checks() -> None:
    for version in ("7.0", "8.0"):
        data = yaml.safe_load(
            (ROOT / "templates" / version / "vertiv-by-snmp.yaml").read_text(encoding="utf-8")
        )
        template = data["zabbix_export"]["templates"][0]
        assert template["template"] == TECHNICAL_NAME
        assert template["name"] == DISPLAY_NAME
        assert template["vendor"]["version"] == VENDOR_VERSION
        dashboard = template["dashboards"][0]
        assert dashboard["name"] == DASHBOARD_NAME
        keys = {item_key(w) for p in dashboard["pages"] for w in p.get("widgets", [])}
        assert "vertiv.input.power.total" not in keys
        assert all(
            w.get("name") != "Input phase power"
            for p in dashboard["pages"]
            for w in p.get("widgets", [])
        )


if __name__ == "__main__":
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != "1.3.3":
        raise RuntimeError("1.4.0 finalization must start from project version 1.3.3")

    for export_version in ("7.0", "8.0"):
        update_template(export_version)
    replace_visible_product_name()
    update_versions()
    add_project_status_docs()
    update_dashboard_docs()
    update_electrical_docs()
    update_changelogs()
    update_versioning_docs()
    update_docs_validator()
    update_template_validator()
    write_release_workflow()
    update_workflows_and_dependabot()
    write_hygiene_test()
    remove_preview_docs()
    final_self_checks()
