# Revisão PDCA — candidata 1.5.1

[English](../en/pdca-1.5.1.md)

**Data da revisão:** 2026-09-14  
**Escopo:** candidata `1.5.1` do repositório, PR #16 e gerador de dashboard global  
**Baseline estável:** `1.5.0`

## Avaliação executiva

A candidata 1.5.1 é uma release de manutenção focada em ferramenta/documentação. Ela não adiciona operações SNMP de escrita nem altera a semântica de monitoramento do template estável 1.5.0. A principal nova superfície é `tools/create_global_dashboard.py`, que converte o dashboard nativo do template em um dashboard global associado a um host pela API do Zabbix.

A revisão identificou um risco relevante de confiabilidade na primeira implementação do `--replace`: dashboards com o mesmo nome podiam ser tratados como uma identidade única e o fluxo anterior excluía o dashboard existente antes de criar o substituto. A correção muda a substituição para um modelo fail-closed com atualização in-place. Apenas dashboards editáveis com nome exato são considerados, mais de um resultado interrompe a operação sem alteração e a ferramenta nunca chama `dashboard.delete`.

## PLAN

### Objetivos

1. Oferecer um dashboard global reproduzível sem manter um segundo layout independente.
2. Manter o dashboard nativo `Vertiv UPS Overview` como única fonte de verdade.
3. Suportar os exports Zabbix 7.0 e 8.0 do repositório sem adivinhar conversões entre versões.
4. Resolver itens e gráficos para IDs reais do host selecionado antes de qualquer escrita.
5. Tornar a substituição segura diante de erros de API, nomes duplicados e permissões restritas.
6. Preservar o modelo de segurança SNMP somente leitura do projeto.
7. Manter documentação EN/PT-BR, testes, versionamento e política de release sincronizados.

### Critérios de aceitação

- `--dry-run` não realiza nenhuma escrita de dashboard.
- A criação de um novo dashboard usa `dashboard.create` somente após resolver todas as referências.
- `--replace` considera apenas dashboards editáveis com nome exato.
- Zero resultados editáveis cria um novo dashboard; um resultado atualiza in-place; múltiplos resultados interrompem a operação.
- Dashboards existentes nunca são excluídos antecipadamente.
- Não existe chamada `dashboard.delete` no gerador.
- Testes automatizados cobrem criação, atualização, recusa sem `--replace`, filtro de editabilidade e ambiguidade.
- O CI deve passar Python 3.9/3.13/3.14, Ruff, pytest, validadores do repositório e importação/upgrade Zabbix 7.0.
- CodeQL deve passar antes do merge.

## DO

Implementado na candidata 1.5.1:

- gerador de dashboard global baseado no dashboard nativo do template;
- detecção automática da versão major/minor do servidor e seleção do YAML versionado correspondente;
- resolução de chaves de itens e nomes de gráficos para IDs concretos do host;
- suporte a `--dry-run`, `--public`, nome personalizado, validação TLS e `--insecure` controlado;
- substituição segura usando `dashboard.update` em vez de excluir/recriar;
- busca via `dashboard.get` restrita com `editable=true`;
- rejeição explícita quando há mais de um dashboard editável com o mesmo nome exato;
- payload de atualização não envia `users` nem `userGroups`, evitando substituir deliberadamente as definições de compartilhamento;
- testes para as invariantes de segurança da substituição;
- documentação operacional bilíngue e validação automática da presença dos documentos EN/PT-BR;
- versão candidata do repositório avançada para `1.5.1`, mantendo `STABLE_VERSION=1.5.0` até promoção explícita.

O mantenedor também executou com sucesso o gerador em `--dry-run` contra um ambiente Zabbix 7.0 real, validando detecção da versão da API, descoberta do host, resolução de itens/gráficos e geração do payload. A criação/atualização real nesse endpoint permanece uma ação explícita do operador e não é apresentada neste relatório como homologação de campo.

## CHECK

### Pontos fortes confirmados

- O template de monitoramento permanece somente leitura e nenhum OID SNMP de controle/escrita foi introduzido.
- O dashboard global é gerado a partir de uma única fonte de verdade, evitando manter uma cópia manual paralela.
- A substituição agora falha de forma segura quando a identidade do alvo é ambígua.
- A atualização in-place elimina a janela anterior em que uma falha no `create` poderia deixar o operador sem o dashboard antigo.
- A identidade do dashboard existente é preservada durante a atualização.
- Testes unitários verificam diretamente que não ocorre exclusão no caminho de substituição segura.
- A separação entre versão candidata e estável permanece explícita: `VERSION=1.5.1` e `STABLE_VERSION=1.5.0` até promoção de release.

### Riscos residuais / lacunas

| Área | Estado | Avaliação |
| --- | --- | --- |
| Zabbix 7.0 real com `--dry-run` | Validado | Descoberta via API e resolução de referências confirmadas pelo mantenedor. |
| Importação/upgrade do template Zabbix 7.0 no CI | Gate obrigatório | Deve permanecer verde no head final da PR. |
| Create/update de dashboard contra Zabbix descartável real | Melhoria aberta | Comportamento da API coberto por testes unitários; teste de integração dedicado aumentaria a confiança. |
| Paridade semântica do export Zabbix 8.0 | Coberta pelo validador | Validação real de API/import/runtime ainda pendente. |
| Outros modelos/firmwares Vertiv | Trabalho de campo aberto | Subconjuntos da MIB podem variar. |
| Homologação estendida do hardware de referência | Em andamento | Separada da correção do repositório/ferramenta. |
| Proteção/ruleset da `main` | Recomendado | Exigir checks obrigatórios reduziria risco de processo. |

### Achados críticos tratados neste ciclo

1. **Substituição ambígua por nome duplicado:** corrigida com busca apenas por editáveis e rejeição de múltiplos resultados.
2. **Janela de perda por delete antes do create:** corrigida com `dashboard.update` in-place; `dashboard.delete` não é usado.

## ACT

### Antes do merge

- Exigir sucesso do CI final e CodeQL no head pós-correção da PR.
- Manter a PR #16 sem merge se qualquer teste Python, validador, importação/upgrade ou análise de segurança falhar.
- Não promover `STABLE_VERSION` apenas porque a branch é mergeável.

### Depois do merge / antes da promoção da release

- Decidir explicitamente quando a candidata 1.5.1 será considerada estável.
- Promover metadados/tag somente pelo workflow existente de release e pelos gates de versão.
- Preferir um teste controlado de criação e atualização in-place do dashboard global em uma instância Zabbix não crítica antes de uso operacional amplo.

### Prioridades para o próximo PDCA

1. Adicionar, se viável, cobertura de integração com Zabbix descartável para `dashboard.create` / `dashboard.update`.
2. Realizar validação real de importação/API/runtime no Zabbix 8.0.
3. Concluir os cenários controlados restantes no hardware de referência.
4. Aplicar proteção/ruleset na branch para exigir CI, importação e análise de segurança.

## Conclusão

O desenho corrigido da 1.5.1 é materialmente mais seguro que a implementação inicial porque a substituição agora é restrita por identidade editável, fail-closed e não destrutiva. Do ponto de vista do processo de engenharia, a candidata só deve ser mergeada após o head final da PR passar por todos os gates configurados de CI e CodeQL. A promoção para release estável permanece uma decisão separada do mantenedor.
