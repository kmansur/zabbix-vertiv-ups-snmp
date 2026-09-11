# Vertiv by SNMP

[![CI](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) | **Português (Brasil)**

Template Zabbix para monitoramento **somente leitura de nobreaks Vertiv/Liebert via SNMP**. Ele combina a UPS-MIB padrão da RFC 1628 com OIDs privados Vertiv/Liebert para monitorar fonte de alimentação, bateria, entrada/saída elétrica, bypass, ambiente, contadores de qualidade de energia, autoteste e identificação do equipamento.

## Preview do dashboard

<p align="center">
  <a href="docs/pt-BR/dashboard.md">
    <img src="docs/images/dashboard-overview.png" alt="Dashboard Vertiv UPS Overview" width="100%">
  </a>
</p>

<p align="center"><strong>Overview</strong> — saúde operacional, bateria, potência de saída e carga por fase em uma única visão.</p>

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/pt-BR/dashboard.md#electrical">
        <img src="docs/images/dashboard-electrical.png" alt="Dashboard elétrico do Vertiv UPS" width="100%">
      </a>
      <br>
      <sub><strong>Electrical</strong> — medições de entrada, saída e bypass, frequência, topologia e contadores de qualidade de energia.</sub>
    </td>
    <td width="50%" valign="top">
      <a href="docs/pt-BR/dashboard.md#battery--environment">
        <img src="docs/images/dashboard-battery-environment.png" alt="Dashboard de bateria e ambiente do Vertiv UPS" width="100%">
      </a>
      <br>
      <sub><strong>Battery &amp; Environment</strong> — carga, autonomia, estado da bateria, teste/configuração e temperatura de entrada.</sub>
    </td>
  </tr>
</table>

<p align="center">📖 <a href="docs/pt-BR/dashboard.md"><strong>Leia o guia de interpretação do dashboard</strong></a> — o que cada gráfico significa, como é o comportamento normal e o que investigar durante um incidente.</p>

## Compatibilidade

| Zabbix | Template | Status |
| --- | --- | --- |
| 7.0 | `templates/7.0/vertiv-by-snmp.yaml` | Export suportado; valide os OIDs específicos no nobreak utilizado |
| 8.0 | `templates/8.0/vertiv-by-snmp.yaml` | Export de compatibilidade preliminar para builds de desenvolvimento do Zabbix 8.0; ainda requer validação em execução |

O Zabbix 8.0 é atualmente documentado pela Zabbix como versão em desenvolvimento. Consulte [docs/pt-BR/zabbix-8.0.md](docs/pt-BR/zabbix-8.0.md).

## Status do projeto

Versão atual: **1.4.1**

**Maturidade de engenharia: 85%** — consulte o [status e os trabalhos restantes](docs/pt-BR/project-status.md).

## O que o template monitora

- identificação do nobreak e da placa/agente de gerenciamento;
- estado global do nobreak e fonte da saída;
- quantidade de alarmes ativos;
- estado, carga, autonomia, tensão, corrente e temperatura da bateria;
- resultado do teste da bateria, quantidade de descargas e tempo de aviso de bateria baixa;
- contadores de qualidade da entrada, incluindo linha inválida, blackout e brownout;
- carga, potência real e potência aparente da saída;
- energia de entrada e saída;
- temperatura do ar de entrada e tempo total de operação;
- configuração elétrica nominal;
- linhas/fases de entrada, saída e bypass por descoberta de baixo nível (LLD);
- métricas fixas L-N/L-L de entrada, saída e bypass para dashboards determinísticos;
- corrente, fator de potência, carga e potência fixos por fase;
- potência total de entrada calculada e metadados de gabinete/intervalo de teste da bateria;
- coleta opcional de traps SNMP da árvore privada Vertiv.

Um mapa sinótico de rede do Zabbix pode ser gerado opcionalmente para cada host de nobreak com `tools/generate_synoptic_map.py`.

O template é intencionalmente **somente leitura**. Operações de reboot, shutdown, controle de tomadas e outras escritas SNMP não estão incluídas.

## Estrutura do repositório

```text
.github/                 GitHub Actions, modelos de issue e PR
docs/
├── en/                  Documentação em inglês
├── images/              Screenshots do dashboard usados na documentação
└── pt-BR/               Documentação em português do Brasil
templates/
├── 7.0/                 Export para Zabbix 7.0
└── 8.0/                 Export para Zabbix 8.0
tests/                   Testes dos validadores
tools/                   Validadores dos templates e documentação
```

## Início rápido

1. Configure SNMP na placa de gerenciamento do nobreak Vertiv/Liebert. Prefira SNMPv3 quando suportado.
2. No Zabbix, crie ou selecione o host do nobreak e configure sua interface SNMP.
3. Importe o YAML correspondente à sua versão do Zabbix.
4. Vincule **Vertiv by SNMP** ao host.
5. Verifique **Monitoring → Latest data** e compare os valores com o LCD/interface web do nobreak.
6. Ajuste as macros do template conforme a autonomia, carga e temperatura esperadas.

Instruções detalhadas: [docs/pt-BR/installation.md](docs/pt-BR/installation.md).

## Limites padrão

| Macro | Padrão | Finalidade |
| --- | ---: | --- |
| `{$UPS.RUNTIME.WARN}` | 10 min | Aviso de autonomia baixa |
| `{$UPS.RUNTIME.CRIT}` | 5 min | Autonomia crítica |
| `{$UPS.BATTERY.CHARGE.WARN}` | 40% | Carga baixa da bateria enquanto em bateria |
| `{$UPS.BATTERY.CHARGE.CRIT}` | 20% | Carga crítica da bateria enquanto em bateria |
| `{$UPS.LOAD.WARN}` | 80% | Carga elevada do nobreak |
| `{$UPS.LOAD.CRIT}` | 95% | Carga crítica do nobreak |
| `{$UPS.BATTERY.TEMP.WARN}` | 35 °C | Temperatura elevada da bateria |
| `{$UPS.BATTERY.TEMP.CRIT}` | 40 °C | Temperatura crítica da bateria |
| `{$UPS.INLET.TEMP.WARN}` | 30 °C | Temperatura elevada do ar de entrada |
| `{$UPS.INLET.TEMP.CRIT}` | 35 °C | Temperatura crítica do ar de entrada |

## Documentação

Português (Brasil):

- [Visão geral](docs/pt-BR/README.md)
- [Instalação](docs/pt-BR/installation.md)
- [Configuração e macros](docs/pt-BR/configuration.md)
- [Métricas e OIDs](docs/pt-BR/metrics.md)
- [Resumo elétrico](docs/pt-BR/electrical-summary.md)
- [Dashboard nativo](docs/pt-BR/dashboard.md)
- [Mapa sinótico opcional](docs/pt-BR/synoptic-map.md)
- [Triggers](docs/pt-BR/triggers.md)
- [Arquitetura SNMP](docs/pt-BR/snmp.md)
- [Troubleshooting](docs/pt-BR/troubleshooting.md)
- [Compatibilidade com Zabbix 8.0](docs/pt-BR/zabbix-8.0.md)
- [Versionamento](docs/pt-BR/versioning.md)
- [Licença e atribuição](docs/pt-BR/license-attribution.md)

A documentação em inglês está disponível em [docs/en/](docs/en/README.md).

## Desenvolvimento e validação

Instale as dependências de desenvolvimento:

```sh
python -m pip install -r requirements-dev.txt
```

Execute:

```sh
python -m compileall -q tools tests
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
```

Consulte [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md).

## Versionamento

Versão atual do projeto: **1.4.1**. O projeto utiliza Versionamento Semântico.

As releases do projeto usam `X.Y.Z`, enquanto o `vendor.version` do template Zabbix segue a convenção `X.Y-Z`. Portanto a versão `1.4.1` do projeto é exportada como `vendor.version: 1.4-1`.

```text
VERSION / tag Git / GitHub Release: X.Y.Z
Zabbix vendor.version: X.Y-Z
```

## Licença e atribuição

O trabalho original deste repositório é distribuído sob a **Licença MIT**.

Este projeto credita o **Template Vertiv** original de **Mihguel da Silva Santos Tavares de Araujo** como referência estrutural e histórica:

https://github.com/Mihguel-Araujo/Template-Zabbix/blob/main/Template%20Vertiv

Nenhuma licença explícita foi encontrada no repositório referenciado no momento da revisão; por isso o arquivo original não é redistribuído aqui e não é relicenciado por este projeto.

Consulte [LICENSE](LICENSE), [NOTICE.pt-BR.md](NOTICE.pt-BR.md) e [docs/pt-BR/license-attribution.md](docs/pt-BR/license-attribution.md).

Mantido por **Karim Mansur / Net Tech**.
