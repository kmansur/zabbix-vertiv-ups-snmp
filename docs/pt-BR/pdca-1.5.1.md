# Revisão PDCA — candidata 1.5.1

[English](../en/pdca-1.5.1.md)

**Data da revisão:** 2026-09-14  
**Escopo:** candidata `1.5.1` do repositório, PR #16 e gerador de dashboard global  
**Baseline estável:** `1.5.0`  
**Head pós-correção validado:** `7ee4bd0d41abd32ab67d28edbef91f3d1298c65e`

## Avaliação executiva

A candidata 1.5.1 é uma release de manutenção focada em ferramenta/documentação. Ela não adiciona operações SNMP de escrita nem altera a semântica de monitoramento do template estável 1.5.0. Sua principal nova superfície é `tools/create_global_dashboard.py`, que converte o dashboard nativo do template em um dashboard global associado a um host pela API do Zabbix.

O ciclo PDCA encontrou dois problemas relevantes de confiabilidade na primeira implementação do `--replace`: dashboards com o mesmo nome podiam ser tratados como uma identidade única e o fluxo anterior excluía dashboards existentes antes de criar o substituto. Ambos os achados foram corrigidos. A substituição agora é fail-closed e in-place: apenas dashboards editáveis com nome exato são considerados, mais de um resultado interrompe a execução sem alteração, exatamente um resultado é atualizado com `dashboard.update` e a ferramenta nunca chama `dashboard.delete`.

O head pós-correção passou por todos os gates configurados de CI e CodeQL. A PR continua sendo uma candidata; a promoção para release estável é uma decisão separada do mantenedor.

## PLAN

### Objetivos

1. Gerar um dashboard global reproduzível sem manter um segundo layout independente.
2. Manter `Vertiv UPS Overview` como única fonte de verdade.
3. Suportar os exports do repositório para Zabbix 7.0 e 8.0 sem adivinhar conversões entre versões.
4. Resolver referências de itens e gráficos do host antes de qualquer escrita.
5. Tornar a substituição segura diante de falhas da API, nomes duplicados e permissões restritas.
6. Preservar o modelo de segurança SNMP somente leitura.
7. Manter documentação EN/PT-BR, testes e versionamento sincronizados.

### Critérios de aceitação

- `--dry-run` não realiza nenhuma escrita de dashboard.
- A criação usa `dashboard.create` somente após resolver as referências.
- `--replace` considera apenas dashboards editáveis com nome exato.
- Zero resultados editáveis cria; um resultado atualiza in-place; múltiplos resultados interrompem a operação.
- Dashboards existentes nunca são excluídos antecipadamente.
- O gerador não contém chamada `dashboard.delete`.
- Testes cobrem criação, atualização, recusa sem `--replace`, filtro de editabilidade e ambiguidade.
- Python 3.9/3.13/3.14, Ruff, pytest, validadores do repositório, importação/upgrade Zabbix 7.0 e CodeQL devem passar.

## DO

Implementado na candidata 1.5.1:

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
- `VERSION=1.5.1`, mantendo `STABLE_VERSION=1.5.0` até promoção explícita da release.

O mantenedor também executou com sucesso o `--dry-run` contra um ambiente Zabbix 7.0 real, validando detecção da versão da API, descoberta do host, resolução de itens/gráficos e geração do payload. A criação/atualização real do dashboard nesse endpoint permanece uma ação explícita do operador e não é apresentada aqui como homologação de campo.

## CHECK

### Resultado final da validação

O head pós-correção `7ee4bd0d41abd32ab67d28edbef91f3d1298c65e` passou por:

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

### Pontos fortes confirmados

- O monitoramento permanece somente leitura; nenhum OID SNMP de controle/escrita foi adicionado.
- O dashboard global é gerado a partir de uma única fonte de verdade.
- A substituição falha de forma segura quando a identidade do alvo é ambígua.
- A atualização in-place elimina a antiga janela de perda do fluxo delete/create.
- A identidade do dashboard existente é preservada.
- Testes unitários verificam que o caminho de substituição segura nunca exclui um dashboard.
- A separação entre candidata e estável permanece explícita: repositório `1.5.1`, marcador estável `1.5.0`.

### Riscos residuais / lacunas

| Área | Estado | Avaliação |
| --- | --- | --- |
| Zabbix 7.0 real com `--dry-run` | Validado | Descoberta via API e resolução de referências confirmadas pelo mantenedor. |
| Importação/upgrade do template Zabbix 7.0 no CI | Aprovado | Importação do baseline estável e upgrade in-place para a candidata concluídos com sucesso. |
| Create/update de dashboard contra Zabbix descartável real | Melhoria aberta | Comportamento da API coberto por testes unitários; teste de integração dedicado aumentaria a confiança. |
| Paridade semântica do export Zabbix 8.0 | Coberta pelo validador | Validação real de API/import/runtime ainda pendente. |
| Outros modelos/firmwares Vertiv | Trabalho de campo aberto | Subconjuntos da MIB podem variar. |
| Homologação estendida do hardware de referência | Em andamento | Separada da correção do repositório/ferramenta. |
| Proteção/ruleset da `main` | Recomendado | Exigir checks obrigatórios reduziria risco de processo. |

## ACT

### Decisão de merge

Os gates de engenharia da PR #16 estão atendidos e os threads de revisão estão resolvidos. A candidata está tecnicamente apta para merge na `main`. Fazer o merge **não** transforma automaticamente a 1.5.1 em release estável.

### Antes da promoção para release estável

- Decidir explicitamente quando a candidata 1.5.1 será considerada estável.
- Promover metadados/tag somente pelo workflow existente de release e pelos gates de versão.
- Preferir um teste controlado de criação e atualização in-place do dashboard em uma instância Zabbix não crítica antes de uso operacional amplo.

### Prioridades para o próximo PDCA

1. Adicionar, se viável, cobertura de integração com Zabbix descartável para `dashboard.create` / `dashboard.update`.
2. Realizar validação real de importação/API/runtime no Zabbix 8.0.
3. Concluir os cenários controlados restantes no hardware de referência.
4. Aplicar proteção/ruleset na branch para exigir CI, importação e análise de segurança.

## Conclusão

A implementação corrigida da 1.5.1 é materialmente mais segura que o desenho inicial: a substituição agora é restrita por identidade editável, fail-closed e não destrutiva. Os gates completos pós-correção de CI, importação/upgrade Zabbix 7.0 e CodeQL passaram, e os dois achados de revisão foram resolvidos. A PR #16 está tecnicamente pronta para merge, enquanto a promoção para 1.5.1 estável permanece uma ação separada do mantenedor.
