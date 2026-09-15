# Status do projeto

[English](../en/project-status.md)

**Prontidão do repositório: PASS**

**Validação de importação/upgrade no Zabbix 7.0: PASS**

**Homologação em campo: EM ANDAMENTO (pós-release)**

**Gate da última release de produção: PASS — 1.5.2**

**Versão atual do repositório: 1.5.3**

A versão **1.5.2** é a release estável atual. Ela alinha o licenciamento e a atribuição do repositório/template com a autorização direta para GPLv3 recebida do autor do Template Vertiv original. Itens, OIDs, chaves, triggers, macros e o comportamento somente leitura permanecem iguais aos da 1.5.1.

A versão **1.5.1** introduziu o gerador opcional de dashboard global, documentação bilíngue de implantação e testes automatizados de conversão/layout. O mantenedor validou seu fluxo `--dry-run` contra um ambiente Zabbix 7.0 real.

Este status deliberadamente **não** afirma que a combinação de nobreak/placa/firmware de referência concluiu todos os cenários de homologação em campo.

| Área | Status | Observações |
| --- | --- | --- |
| Estrutura do template Zabbix 7.0 | PASS | Validadores estruturais/do template passam |
| Importação nova e upgrade via API no Zabbix 7.0 | PASS | O CI importa o baseline estável e atualiza in-place para a release atual |
| Segurança somente leitura | PASS | Famílias conhecidas de OIDs de controle/escrita são proibidas pelos validadores/testes |
| Isolamento de métricas privadas/experimentais | PASS | Valores não validados não podem gerar alertas padrão de produção |
| Verificação semântica documentação/template | PASS | Versões, tabelas de triggers, macros, pares bilíngues e política de release são validados |
| Workflow CodeQL/segurança | PASS | A análise de segurança passa antes da promoção da release |
| Identificação, heartbeat, testes e diagnóstico de alarmes RFC1628 | PASS | Comportamento de produção estabelecido na 1.5.0 |
| Gerador de dashboard global | VALIDADO | Introduzido na 1.5.1; `--dry-run` validado pelo mantenedor em Zabbix 7.0 real |
| Licença e atribuição GPLv3 | PASS | O autor do template original autorizou diretamente o uso como base e a publicação sob GPLv3 em 14/09/2026 |
| Registro de compatibilidade em campo | EM ANDAMENTO | Há evidência real em um ambiente Vertiv ITA-20kVA / IS-UNITY-DP; cenários controlados de evento permanecem abertos |
| Zabbix 8.0 | PREVIEW | Apenas paridade de export; sem alegação de suporte de produção |
| Release de produção `v1.5.2` | PASS | Patch de licença/metadados; sem alteração da semântica de monitoramento da 1.5.1 |

## Modelo de branch/release

A `main` é a branch ativa de desenvolvimento. `VERSION` identifica a versão/candidata atual do repositório e `STABLE_VERSION` identifica a última release estável com tag. Para produção, utilize uma GitHub Release com tag, pois a `main` pode avançar depois que um novo ciclo de desenvolvimento começar.

Marcadores desta release:

```text
VERSION:        1.5.3
STABLE_VERSION: 1.5.3
```

## Decisão de release

`v1.5.2` é uma release patch de licenciamento, atribuição e metadados de release. Ela não introduz novo comportamento de monitoramento. A promoção exige os mesmos validadores do repositório, caminho de importação/upgrade no Zabbix 7.0 e checks de segurança usados pelo workflow de release do projeto.

Os checks controlados de campo restantes continuam registrados no [registro de campo da 1.5.0](homologation-1.5.0.md) e na issue correspondente. A conclusão desses testes poderá elevar a redação de compatibilidade para **homologada em campo**, mas eles não bloqueiam esta release patch de licença/metadados.
