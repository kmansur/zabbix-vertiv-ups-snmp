# Status do projeto

[English](../en/project-status.md)

**Prontidão do repositório: PASS**

**Validação de importação/upgrade no Zabbix 7.0: PASS**

**Homologação em campo: EM ANDAMENTO (pós-release)**

**Gate de release para produção: PASS — mantenedor aprovou a 1.5.0 em 14/09/2026**

A versão **1.5.0** é a release estável atual. Os controles estruturais, de segurança, documentação, CI e segurança de código do repositório foram aprovados, incluindo importação nova em Zabbix 7.0 e upgrade in-place da 1.4.1 para a 1.5.0. O mantenedor aceitou esse conjunto de evidências para a release 1.5.0, mantendo os cenários controlados restantes em hardware como validação de campo pós-release.

Este status deliberadamente **não** afirma que a combinação de nobreak/placa/firmware de referência concluiu todos os cenários de homologação em campo.

| Área | Status | Observações |
| --- | --- | --- |
| Estrutura do template Zabbix 7.0 | PASS | Validadores estruturais/do template passam |
| Importação nova e upgrade via API no Zabbix 7.0 | PASS | O CI importa a 1.4.1 e atualiza in-place para a 1.5.0 |
| Segurança somente leitura | PASS | Famílias conhecidas de OIDs de controle/escrita são proibidas pelos validadores/testes |
| Isolamento de métricas privadas/experimentais | PASS | Valores não validados não podem gerar alertas padrão de produção |
| Verificação semântica documentação/template | PASS | Versões, tabelas de triggers, macros, pares bilíngues e política de release são validados |
| Workflow CodeQL/segurança | PASS | A branch de release só é promovida após sucesso do workflow de segurança |
| Identificação, heartbeat, testes e diagnóstico de alarmes RFC1628 | PASS | Incluídos na release 1.5.0 |
| Registro de compatibilidade em campo | EM ANDAMENTO | Há evidência real em um ambiente Vertiv ITA-20kVA / IS-UNITY-DP; cenários controlados de evento permanecem abertos |
| Zabbix 8.0 | PREVIEW | Apenas paridade de export; sem alegação de suporte de produção |
| Release de produção `v1.5.0` | PASS | Aprovada pelo mantenedor com base nos gates de repositório/CI/segurança e evidência de campo já coletada |

## Modelo de branch/release

A `main` é a branch ativa de desenvolvimento. `VERSION` identifica a versão/candidata atual do repositório e `STABLE_VERSION` identifica a última release estável com tag. Para produção, utilize uma GitHub Release com tag, pois a `main` pode avançar depois que um novo ciclo de desenvolvimento começar.

Para a release 1.5.0, os dois marcadores de versão estão em `1.5.0`.

## Decisão de release

O mantenedor aprovou `v1.5.0` para release em **14/09/2026** depois que:

1. os validadores de repositório/template/documentação passaram;
2. os jobs de CI com Python 3.9, 3.13 e 3.14 passaram;
3. o CodeQL passou;
4. a importação nova em um Zabbix 7.0 real passou;
5. o upgrade in-place pela API do Zabbix de 1.4.1 para 1.5.0 passou;
6. a evidência já coletada em hardware real confirmou os defaults seguros utilizados pelo template.

Os checks controlados de campo restantes continuam registrados no [registro de campo da 1.5.0](homologation-1.5.0.md) e na issue correspondente. A conclusão desses testes poderá elevar a redação de compatibilidade para **homologada em campo**, mas eles não bloqueiam mais a publicação da release de software 1.5.0.
