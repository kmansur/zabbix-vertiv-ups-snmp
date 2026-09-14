# Revisão PDCA — release 1.5.1

[English](../en/pdca-1.5.1.md)

**Data da revisão:** 2026-09-14  
**Escopo:** release `1.5.1`, PR #16 e gerador de dashboard global  
**Baseline estável:** `1.5.0`  
**Alvo da promoção:** `1.5.1`

## Avaliação executiva

A release 1.5.1 é uma release de manutenção focada em ferramenta/documentação. Ela não adiciona operações SNMP de escrita nem altera a semântica de monitoramento introduzida pelo template estável 1.5.0. Sua principal nova superfície é `tools/create_global_dashboard.py`, que converte o dashboard nativo do template em um dashboard global associado a um host pela API do Zabbix.

O ciclo PDCA encontrou dois problemas relevantes de confiabilidade na primeira implementação do `--replace`: dashboards com o mesmo nome podiam ser tratados como identidade única e o fluxo anterior excluía dashboards existentes antes de criar o substituto. Ambos os achados foram corrigidos. A substituição agora é fail-closed e in-place: apenas dashboards editáveis com nome exato são considerados, mais de um resultado interrompe a execução sem alteração, exatamente um resultado é atualizado com `dashboard.update` e a ferramenta nunca chama `dashboard.delete`.

Os metadados do repositório foram promovidos para a release: `VERSION=1.5.1`, `STABLE_VERSION=1.5.1` e ambos os exports Zabbix usam `vendor.version: 1.5-1`. A semântica de monitoramento continua igual à 1.5.0; o bump de metadados mantém a release com tag internamente consistente.

## PLAN

### Objetivos

1. Gerar um dashboard global reproduzível sem manter um segundo layout independente.
2. Manter `Vertiv UPS Overview` como única fonte de verdade.
3. Suportar os exports do repositório para Zabbix 7.0 e 8.0 sem adivinhar conversões entre versões.
4. Resolver referências de itens e gráficos do host antes de qualquer escrita.
5. Tornar a substituição segura diante de falhas da API, nomes duplicados e permissões restritas.
6. Preservar o modelo de segurança SNMP somente leitura.
7. Manter documentação EN/PT-BR, testes e versionamento sincronizados.
8. Promover metadados de release somente depois que a implementação corrigida passar pelos gates do repositório.

### Critérios de aceitação

- `--dry-run` não realiza nenhuma escrita de dashboard.
- A criação usa `dashboard.create` somente após resolver as referências.
- `--replace` considera apenas dashboards editáveis com nome exato.
- Zero resultados editáveis cria; um resultado atualiza in-place; múltiplos resultados interrompem a operação.
- Dashboards existentes nunca são excluídos antecipadamente.
- O gerador não contém chamada `dashboard.delete`.
- Testes cobrem criação, atualização, recusa sem `--replace`, filtro de editabilidade e ambiguidade.
- Python 3.9/3.13/3.14, Ruff, pytest, validadores do repositório, importação/upgrade Zabbix 7.0 e CodeQL devem passar.
- `VERSION`, `STABLE_VERSION` e `vendor.version` do template devem estar consistentes com a release antes da criação da tag.

## DO

Implementado na 1.5.1:

- gerador de dashboard global orientado pelo dashboard nativo do template;
- detecção automática da versão major/minor do servidor e seleção do YAML correspondente;
- resolução de chaves de itens e nomes de gráficos para IDs concretos do host;
- suporte a `--dry-run`, `--public`, nome personalizado, validação TLS e `--insecure` controlado;
- substituição segura usando `dashboard.update` em vez de excluir/recriar;
- busca via `dashboard.get` restrita com `editable=true`;
- rejeição explícita de múltiplos dashboards editáveis com o mesmo nome exato;
- payload de atualização não envia `users` nem `userGroups`, evitando substituir deliberadamente as definições de compartilhamento;
- testes de regressão para todas as invariantes de segurança da substituição;
- documentação bilíngue do dashboard global e relatório PDCA bilíngue;
- promoção da release para `VERSION=1.5.1`, `STABLE_VERSION=1.5.1` e `vendor.version: 1.5-1` nos dois exports Zabbix.

O mantenedor também executou com sucesso o `--dry-run` contra um ambiente Zabbix 7.0 real, validando detecção da versão da API, descoberta do host, resolução de itens/gráficos e geração do payload. A criação/atualização real do dashboard nesse endpoint permanece uma ação explícita do operador e não é apresentada aqui como homologação de campo.

## CHECK

### Resultado da validação

A implementação corrigida passou por:

- Python 3.9 — compilação, Ruff lint/format, pytest e validadores do repositório;
- Python 3.13 — compilação, Ruff lint/format, pytest e validadores do repositório;
- Python 3.14 — compilação, Ruff lint/format, pytest e validadores do repositório;
- validação dos templates Zabbix;
- validação da documentação bilíngue;
- validação de prontidão para produção;
- importação do baseline estável em Zabbix 7.0 descartável e upgrade in-place para a candidata;
- análise CodeQL para Python.

Os dois achados de revisão estão resolvidos na PR:

1. **P2 — substituição ambígua por nome duplicado:** corrigida com busca apenas por editáveis e rejeição de múltiplos resultados.
2. **P1 — janela de perda por delete antes do create:** corrigida com `dashboard.update` in-place; `dashboard.delete` não é usado.

É necessário um último ciclo de CI/CodeQL no head promovido da release antes do merge/tag.

### Pontos fortes confirmados

- O monitoramento permanece somente leitura; nenhum OID SNMP de controle/escrita foi adicionado.
- O dashboard global é gerado a partir de uma única fonte de verdade.
- A substituição falha de forma segura quando a identidade do alvo é ambígua.
- A atualização in-place elimina a antiga janela de perda do fluxo delete/create.
- A identidade do dashboard existente é preservada.
- Testes unitários verificam que o caminho de substituição segura nunca exclui um dashboard.
- Os metadados da release estão alinhados em 1.5.1.

### Riscos residuais / lacunas

| Área | Estado | Avaliação |
| --- | --- | --- |
| Zabbix 7.0 real com `--dry-run` | Validado | Descoberta via API e resolução de referências confirmadas pelo mantenedor. |
| Importação/upgrade do template Zabbix 7.0 no CI | Aprovado antes da promoção; novo ciclo exigido no head final | Importação do baseline estável e upgrade in-place para a candidata concluídos com sucesso. |
| Create/update de dashboard contra Zabbix descartável real | Melhoria aberta | Comportamento da API coberto por testes unitários; teste de integração dedicado aumentaria a confiança. |
| Paridade semântica do export Zabbix 8.0 | Coberta pelo validador | Validação real de API/import/runtime ainda pendente. |
| Outros modelos/firmwares Vertiv | Trabalho de campo aberto | Subconjuntos da MIB podem variar. |
| Homologação estendida do hardware de referência | Em andamento | Separada da correção do repositório/ferramenta. |
| Proteção/ruleset da `main` | Recomendado | Exigir checks obrigatórios reduziria risco de processo. |

## ACT

### Decisão de merge e release

O mantenedor aprovou a promoção da 1.5.1 e solicitou merge mais criação da tag. Os metadados de release foram promovidos antes do merge para que o workflow existente disparado por tag valide um estado consistente do repositório.

A PR só deve ser mergeada depois que o head promovido final passar por CI e CodeQL. A tag `v1.5.1` deve apontar para o commit final mergeado da release.

### Prioridades para o próximo PDCA

1. Adicionar, se viável, cobertura de integração com Zabbix descartável para `dashboard.create` / `dashboard.update`.
2. Realizar validação real de importação/API/runtime no Zabbix 8.0.
3. Concluir os cenários controlados restantes no hardware de referência.
4. Aplicar proteção/ruleset na branch para exigir CI, importação e análise de segurança.

## Conclusão

A implementação corrigida da 1.5.1 é materialmente mais segura que o desenho inicial: a substituição agora é restrita por identidade editável, fail-closed e não destrutiva. Os metadados da release foram promovidos de forma consistente e o merge/tag final foi autorizado pelo mantenedor, condicionado apenas à aprovação do head promovido nos gates configurados de CI e CodeQL.
