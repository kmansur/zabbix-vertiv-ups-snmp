# Vertiv by SNMP

[![CI](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) | **Português (Brasil)**

Template Zabbix para monitoramento **somente leitura de nobreaks Vertiv/Liebert via SNMP**. Ele combina a UPS-MIB padrão da RFC 1628 com OIDs privados Vertiv/Liebert para monitorar fonte de alimentação, bateria, entrada/saída elétrica, bypass, alarmes, ambiente, contadores de qualidade de energia, teste diagnóstico/autoteste e identificação do equipamento.

## Status das versões

- **Última versão estável:** `1.4.1`
- **Candidata atual do repositório:** `1.5.0`
- **Homologação em campo:** em andamento

A branch `main` é a branch ativa de desenvolvimento/candidato. **Em produção, utilize uma GitHub Release com tag**, e não assuma que o conteúdo atual da `main` representa a última versão estável. A candidata 1.5.0 precisa passar pelo gate de homologação em campo documentado antes de receber uma tag estável.

Consulte [status do projeto](docs/pt-BR/project-status.md), [prontidão para produção](docs/pt-BR/production-readiness.md) e [versionamento](docs/pt-BR/versioning.md).

## Preview do dashboard

<p align="center">
  <a href="docs/pt-BR/dashboard.md">
    <img src="docs/images/dashboard-overview.png" alt="Dashboard Vertiv UPS Overview" width="100%">
  </a>
</p>

Guia detalhado de interpretação: [docs/pt-BR/dashboard.md](docs/pt-BR/dashboard.md).

## Compatibilidade

| Zabbix | Template | Status |
| --- | --- | --- |
| 7.0 | `templates/7.0/vertiv-by-snmp.yaml` | O export candidato é testado por importação no CI; OIDs específicos ainda precisam ser validados no nobreak alvo |
| 8.0 | `templates/8.0/vertiv-by-snmp.yaml` | Export preliminar de compatibilidade; a equivalência semântica é verificada, mas ainda falta validação real de importação/execução |

Consulte a [matriz de compatibilidade](docs/pt-BR/compatibility.md).

## Cobertura de monitoramento

- identificação do nobreak e da placa/agente de gerenciamento;
- heartbeat SNMP dedicado e aviso de reinicialização do agente de gerenciamento;
- estado global do nobreak e fonte da saída;
- quantidade de alarmes ativos e descoberta da tabela RFC1628 de alarmes ativos;
- estado, carga, autonomia, tensão e corrente privada validada da bateria;
- observação de resultado de teste diagnóstico RFC1628, somente leitura;
- metadados de teste da bateria, número de descargas e tempo de bateria baixa;
- descoberta de entrada/saída/bypass via LLD RFC1628;
- valores elétricos fixos para dashboards determinísticos;
- alertas padronizados de carga por linha de saída;
- contadores de qualidade da entrada, incluindo linha inválida, blackout e brownout;
- potência real/aparente de saída e contadores de energia;
- temperatura do ar de entrada e tempo de operação;
- configuração elétrica nominal;
- coleta opcional de traps SNMP Vertiv, desabilitada por padrão.

O template é intencionalmente **somente leitura**. Operações de reboot, shutdown, controle de tomadas, início de testes e outras escritas/controles SNMP não estão incluídas.

## Comportamento importante em produção

A placa usada durante a homologação implementa apenas parte da RFC1628. `upsBatteryCurrent` e `upsBatteryTemperature` retornam `noSuchObject` nesse conjunto placa/firmware e, por isso, permanecem **desabilitados por padrão** para compatibilidade com outros equipamentos.

O objeto privado Vertiv de temperatura da bateria também retornou valor não confiável/semelhante a sentinela no equipamento de teste. Portanto, **não existe trigger padrão de temperatura da bateria na candidata 1.5.0**. As macros de temperatura da bateria permanecem reservadas por compatibilidade/futuros perfis, mas não habilitam alertamento sozinhas.

Os alertas de carga usam os protótipos RFC1628 `upsOutputPercentLoad`; o item privado agregado `vertiv.output.load` não gera triggers padrão de produção.

## Início rápido

### Produção

1. Abra a página **Releases** do repositório e baixe a última versão estável com tag.
2. Configure SNMP na placa de gerenciamento Vertiv/Liebert; prefira SNMPv3 quando suportado.
3. No Zabbix, crie/selecione o host do nobreak e configure a interface SNMP.
4. Importe o YAML da release correspondente à versão do Zabbix.
5. Vincule **Vertiv by SNMP** ao host.
6. Verifique **Monitoring → Latest data** e compare os valores com o LCD/interface web do nobreak.
7. Ajuste os limites de autonomia, carga, carga por linha e temperatura de entrada para o local.

### Teste da candidata/desenvolvimento

Os arquivos em `templates/` na `main` representam a candidata atual do repositório e podem ser mais novos que a última release estável. Use-os somente quando a intenção for testar a candidata.

Instruções detalhadas: [docs/pt-BR/installation.md](docs/pt-BR/installation.md).

## Limites padrão e reservados

| Macro | Padrão | Finalidade |
| --- | ---: | --- |
| `{$UPS.RUNTIME.WARN}` | 10 min | Aviso de autonomia baixa |
| `{$UPS.RUNTIME.CRIT}` | 5 min | Autonomia crítica |
| `{$UPS.BATTERY.CHARGE.WARN}` | 40% | Carga baixa enquanto em bateria |
| `{$UPS.BATTERY.CHARGE.CRIT}` | 20% | Carga crítica enquanto em bateria |
| `{$UPS.LOAD.WARN}` | 80% | Aviso de carga da linha de saída RFC1628 |
| `{$UPS.LOAD.CRIT}` | 95% | Carga crítica da linha de saída RFC1628 |
| `{$UPS.INLET.TEMP.WARN}` | 30 °C | Temperatura elevada do ar de entrada |
| `{$UPS.INLET.TEMP.CRIT}` | 35 °C | Temperatura crítica do ar de entrada |
| `{$UPS.BATTERY.TEMP.WARN}` | 35 °C | Reservada; não usada por trigger padrão de produção na 1.5.0 |
| `{$UPS.BATTERY.TEMP.CRIT}` | 40 °C | Reservada; não usada por trigger padrão de produção na 1.5.0 |

Consulte [configuração e macros](docs/pt-BR/configuration.md).

## Estrutura do repositório

```text
.github/                 GitHub Actions, modelos de issue e PR
docs/
├── en/                  Documentação em inglês
├── images/              Screenshots do dashboard
└── pt-BR/               Documentação em português do Brasil
templates/
├── 7.0/                 Export para Zabbix 7.0
└── 8.0/                 Export preliminar para Zabbix 8.0
tests/                   Testes dos validadores
tools/                   Validadores e ferramentas auxiliares
```

## Desenvolvimento e validação

```sh
python -m pip install -r requirements-dev.txt
python -m compileall -q tools tests
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
python tools/validate_production.py
```

O CI também executa teste real de importação/upgrade pela API do Zabbix 7.0. Consulte [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md).

## Documentação

- [Visão geral](docs/pt-BR/README.md)
- [Instalação](docs/pt-BR/installation.md)
- [Configuração e macros](docs/pt-BR/configuration.md)
- [Métricas e OIDs](docs/pt-BR/metrics.md)
- [Resumo elétrico](docs/pt-BR/electrical-summary.md)
- [Dashboard](docs/pt-BR/dashboard.md)
- [Triggers](docs/pt-BR/triggers.md)
- [Arquitetura SNMP](docs/pt-BR/snmp.md)
- [Troubleshooting](docs/pt-BR/troubleshooting.md)
- [Matriz de compatibilidade](docs/pt-BR/compatibility.md)
- [Prontidão para produção/homologação](docs/pt-BR/production-readiness.md)
- [Fontes MIB/OID e proveniência](docs/pt-BR/mib-sources.md)
- [Versionamento](docs/pt-BR/versioning.md)
- [Licença e atribuição](docs/pt-BR/license-attribution.md)

A documentação em inglês está disponível em [docs/en/](docs/en/README.md).

## Versionamento

As releases usam Versionamento Semântico `X.Y.Z`. O `vendor.version` do Zabbix usa a representação equivalente `X.Y-Z`.

```text
VERSION / tag Git / GitHub Release: X.Y.Z
Zabbix vendor.version: X.Y-Z
```

A candidata `1.5.0` é exportada como `vendor.version: 1.5-0`.

## Licença e atribuição

O trabalho original deste repositório é distribuído sob a **Licença MIT**.

Este projeto credita o **Template Vertiv** original de **Mihguel da Silva Santos Tavares de Araujo** como referência estrutural e histórica:

https://github.com/Mihguel-Araujo/Template-Zabbix/blob/main/Template%20Vertiv

Nenhuma licença explícita foi encontrada no repositório referenciado no momento da revisão; por isso o arquivo original não é redistribuído aqui e não é relicenciado por este projeto.

Consulte [LICENSE](LICENSE), [NOTICE.pt-BR.md](NOTICE.pt-BR.md) e [docs/pt-BR/license-attribution.md](docs/pt-BR/license-attribution.md).

Mantido por **Karim Mansur / Net Tech**.
