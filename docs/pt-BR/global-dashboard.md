# Dashboard global

[English](../en/global-dashboard.md)

**Introduzido na candidata do repositório:** `1.5.1`  
**Última release estável enquanto esta candidata está em revisão:** `1.5.0`

O template já inclui o dashboard nativo de template **Vertiv UPS Overview**. Esse dashboard acompanha automaticamente o contexto do host quando o template é vinculado a um nobreak.

Um **dashboard global** do Zabbix é um objeto diferente. A exportação de template não promove automaticamente um dashboard de template para **Monitoring → Dashboards**. Por isso, este projeto fornece `tools/create_global_dashboard.py`, que usa o próprio dashboard nativo como fonte de verdade e cria ou atualiza com segurança um dashboard global pela API do Zabbix para um host real já monitorado.

O mantenedor validou com sucesso o gerador em modo `--dry-run` contra um ambiente Zabbix 7.0 real antes da finalização da documentação da candidata 1.5.1. Isso confirma, no fluxo de referência, a detecção da versão da API, descoberta do host de destino, resolução de itens/gráficos e geração do payload; a criação/atualização efetiva do dashboard continua sendo uma ação explícita do operador.

## Por que usar o gerador

O gerador evita manter uma segunda definição de dashboard escrita manualmente. Ele:

- detecta a versão major/minor do Zabbix conectado;
- carrega `templates/<major.minor>/vertiv-by-snmp.yaml`;
- localiza o dashboard nativo `Vertiv UPS Overview`;
- resolve as chaves dos itens do template para os IDs dos itens no host escolhido;
- resolve os nomes dos gráficos para os IDs dos gráficos no host escolhido;
- preserva páginas, posições, dimensões, títulos, thresholds, cores e demais campos suportados dos widgets;
- cria um novo dashboard usando `dashboard.create`;
- quando `--replace` é informado explicitamente, atualiza in-place exatamente um dashboard editável de mesmo nome usando `dashboard.update`.

O utilitário nunca usa `dashboard.delete`. Assim, a substituição é fail-safe: o objeto existente não é removido antes de o Zabbix aceitar a atualização.

## Requisitos

- Zabbix 7.0 ou 8.0 correspondente a uma exportação existente neste repositório;
- template Vertiv já importado e vinculado ao host do nobreak;
- Python 3.9+;
- PyYAML (`pip install -r requirements-dev.txt` é suficiente);
- token de API do Zabbix cujo usuário tenha permissão para ler host/itens/gráficos e criar ou editar dashboards conforme necessário.

## Faça primeiro um dry-run

A partir da raiz do repositório:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --dry-run
```

Esse comando resolve todas as referências e mostra o payload do dashboard sem criar ou atualizar nada.

Para um endpoint interno de laboratório ou gerenciamento que utilize deliberadamente um certificado não confiável, acrescente `--insecure`. Essa opção não deve ser o padrão normal de produção.

## Criar o dashboard

Depois de revisar a saída do dry-run:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01"
```

Nome padrão:

```text
Vertiv UPS - <nome visível do host>
```

Para escolher outro nome:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --dashboard-name "Vertiv UPS - Datacenter"
```

## Privado ou público

Por padrão, o dashboard global é criado como privado. Para criá-lo como público, ou para marcar como público o dashboard selecionado durante uma atualização explícita, adicione `--public`:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --public
```

O compartilhamento com usuários ou grupos específicos deve seguir a política de acesso do ambiente Zabbix.

## Atualizar com segurança um dashboard existente

O utilitário se recusa a sobrescrever um dashboard editável de mesmo nome sem que `--replace` seja informado explicitamente.

Depois de revisar o `--dry-run`, use:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --replace
```

A substituição é deliberadamente conservadora:

- a descoberta usa `dashboard.get` com `editable=true`, portanto dashboards que o usuário da API não pode editar não são alvos de substituição;
- se não existir dashboard editável com o nome exato, um novo é criado;
- se existir exatamente um dashboard editável com o nome exato, `dashboard.update` atualiza suas propriedades/páginas geradas in-place;
- se existirem dois ou mais dashboards editáveis com o mesmo nome exato, o utilitário interrompe a execução sem modificar nada porque o alvo é ambíguo;
- `dashboard.delete` nunca é chamado.

Como o dashboard existente é atualizado in-place, sua identidade é preservada. O utilitário não envia `users` nem `userGroups` durante a atualização, portanto as definições de compartilhamento existentes não são deliberadamente substituídas pela ferramenta. As páginas/layout derivados do template são substituídos; consequentemente, edições manuais de widgets/layout feitas diretamente no dashboard global podem ser sobrescritas. Sempre que possível, mantenha as alterações de layout no dashboard do template.

## TLS

A validação do certificado TLS fica habilitada por padrão. A opção `--insecure` existe apenas para laboratórios controlados com certificado não confiável e não deve ser o modo normal de produção.

## Zabbix 7.0 e 8.0

O utilitário escolhe automaticamente a exportação do repositório correspondente à versão major/minor informada pela API do servidor. Atualmente o projeto contém exportações para Zabbix 7.0 e 8.0.

Se não existir `templates/<major.minor>/vertiv-by-snmp.yaml` para a versão encontrada, a execução é interrompida em vez de tentar uma conversão entre versões sem validação.

## Dashboard de template x dashboard global

| Característica | Dashboard de template | Dashboard global gerado |
|---|---|---|
| Localização | Contexto do host/template | Monitoring → Dashboards |
| Associação ao host | Contexto automático | Associado ao host selecionado na geração |
| Vem junto com a importação do template | Sim | Não |
| Criado pelo utilitário do projeto | Não | Sim |
| Melhor uso | Troubleshooting individual | Entrada operacional/NOC e navegação compartilhada |

O dashboard global gerado fica propositalmente associado a um único host, porque os widgets de item e gráfico precisam de IDs reais. Para vários nobreaks, gere um dashboard por host ou construa separadamente um dashboard de frota/NOC baseado em padrões de host ou widgets de navegação.

## Observação de versionamento

A candidata `1.5.1` introduz esta ferramenta auxiliar e sua documentação sem alterar a semântica de monitoramento do template estável `1.5.0`. Por isso, `VERSION` pode estar em `1.5.1` enquanto `STABLE_VERSION` e o `vendor.version` do template não alterado permanecem em `1.5.0` / `1.5-0` até uma promoção explícita de release. Consulte [Versionamento](versioning.md).

## Segurança

- Utilize um token de API com o menor privilégio prático.
- Nunca grave o token de API no repositório.
- Revogue/rotacione imediatamente um token caso ele seja exposto em histórico de shell, chat, logs ou outro local não controlado.
- A substituição é fail-closed: múltiplos dashboards editáveis de mesmo nome fazem a execução falhar antes de qualquer escrita.
- Dashboards existentes são atualizados in-place; esta ferramenta não chama `dashboard.delete`.
- Nenhuma operação SNMP de escrita é adicionada por esta funcionalidade.
