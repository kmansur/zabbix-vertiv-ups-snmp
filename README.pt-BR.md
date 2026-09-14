# Vertiv by SNMP

[![CI](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

[English](README.md) | **Português (Brasil)**

Template Zabbix para monitoramento **somente leitura de nobreaks Vertiv/Liebert via SNMP**. Ele combina a UPS-MIB padrão da RFC 1628 com OIDs privados Vertiv/Liebert para monitorar fonte de alimentação, bateria, entrada/saída elétrica, bypass, alarmes, ambiente, contadores de qualidade de energia, teste diagnóstico/autoteste e identificação do equipamento.

## Status das versões

- **Última versão estável:** `1.5.2`
- **Versão atual do repositório:** `1.5.3`
- **Escopo da candidata 1.5.3:** manutenção orientada pela validação em campo; a LLD de alarmes ativos passa de 1m para 30s para melhorar a captura de linhas transitórias RFC1628
- **Homologação estendida em campo:** em andamento após a release

A versão `1.5.0` foi aprovada para release pelo mantenedor após aprovação da validação do repositório, CodeQL, importação nova no Zabbix 7.0 e upgrade in-place de `1.4.1` para `1.5.0`. Os cenários controlados restantes em hardware continuam sendo acompanhados separadamente e **não devem ser interpretados como certificação de campo concluída**.

A release `1.5.1` adicionou o gerador opcional de dashboard global e sua documentação/testes bilíngues. A release `1.5.2` regulariza o licenciamento e a atribuição do repositório/template sob GPLv3 com autorização do autor do template original. A candidata `1.5.3` aplica uma melhoria de cadência de descoberta de alarmes baseada em evidência de campo, enquanto o `STABLE_VERSION` permanece `1.5.2` até a promoção.

A branch `main` é a branch ativa de desenvolvimento. **Em produção, utilize uma GitHub Release com tag**, pois a `main` pode avançar além da última release estável quando um novo ciclo de desenvolvimento começar.

Consulte [status do projeto](docs/pt-BR/project-status.md), [prontidão para produção](docs/pt-BR/production-readiness.md) e [versionamento](docs/pt-BR/versioning.md).

## Preview do dashboard

<p align="center">
  <a href="docs/pt-BR/dashboard.md">
    <img src="docs/images/dashboard-overview.png" alt="Dashboard Vertiv UPS Overview" width="100%">
  </a>
</p>

Guia detalhado de interpretação: [docs/pt-BR/dashboard.md](docs/pt-BR/dashboard.md).  
Geração do dashboard global: [docs/pt-BR/global-dashboard.md](docs/pt-BR/global-dashboard.md).

## Compatibilidade

| Zabbix | Template | Status |
| --- | --- | --- |
| 7.0 | `templates/7.0/vertiv-by-snmp.yaml` | Candidata 1.5.3; descoberta de alarmes ativos em 30s baseada em validação de campo, mantendo 1.5.2 como estável até a promoção |
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

A placa de referência/teste usada durante o desenvolvimento implementa apenas parte da RFC1628. `upsBatteryCurrent` e `upsBatteryTemperature` retornam `noSuchObject` nesse conjunto placa/firmware e, por isso, permanecem **desabilitados por padrão** para compatibilidade com outros equipamentos.

O objeto privado Vertiv de temperatura da bateria também retornou valor não confiável/semelhante a sentinela no equipamento de teste. Portanto, **não existe trigger padrão de temperatura da bateria na release 1.5.0**. As macros de temperatura da bateria permanecem reservadas por compatibilidade/futuros perfis, mas não habilitam alertamento sozinhas.

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

### Teste de desenvolvimento

Os arquivos em `templates/` na `main` representam o estado atual de desenvolvimento e podem ficar mais novos que a última release estável. Use uma GitHub Release com tag em produção e utilize a `main` apenas quando a intenção for testar alterações de desenvolvimento.

O gerador de dashboard global introduzido na 1.5.1 pode ser testado independentemente do template de monitoramento usando `--dry-run` antes da criação do dashboard.

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
- [Gerador de dashboard global](docs/pt-BR/global-dashboard.md)
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

As releases usam Versionamento Semântico `X.Y.Z`. O `vendor.version` do Zabbix usa a representação equivalente `X.Y-Z` para o artefato de monitoramento do template.

```text
VERSION / tag Git / GitHub Release: X.Y.Z
Zabbix vendor.version: X.Y-Z
```

A versão atual do repositório e a release estável são `1.5.2`, com metadados do template `vendor.version: 1.5-2`. A validação de release exige que `VERSION`, `STABLE_VERSION`, a tag Git e os metadados de vendor correspondam à versão promovida.

## Licença e atribuição

Este repositório é distribuído sob a **GNU General Public License v3.0 somente (`GPL-3.0-only`)**.

Este projeto é baseado no **Template Vertiv** original de **Mihguel da Silva Santos Tavares de Araujo**:

https://github.com/Mihguel-Araujo/Template-Zabbix/blob/main/Template%20Vertiv

O repositório original não possuía uma licença explícita quando foi revisado em 10/09/2026. Em 14/09/2026, o autor original forneceu ao mantenedor autorização direta e por escrito para utilizar seu template como base deste projeto e publicar o projeto comunitário resultante sob GPLv3.

Por cautela e para não atribuir à autorização um alcance maior do que o efetivamente concedido, este repositório utiliza o identificador SPDX **`GPL-3.0-only`**. Este projeto não afirma alterar a licença do repositório original separado do autor.

Consulte [LICENSE](LICENSE), [NOTICE.pt-BR.md](NOTICE.pt-BR.md) e [docs/pt-BR/license-attribution.md](docs/pt-BR/license-attribution.md).

Modificações mantidas e organização do repositório: **Karim Mansur / Net Tech**.
