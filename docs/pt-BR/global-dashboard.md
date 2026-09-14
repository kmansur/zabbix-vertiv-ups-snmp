# Dashboard global

[English](../en/global-dashboard.md)

O template já inclui o dashboard nativo de template **Vertiv UPS Overview**. Esse dashboard acompanha automaticamente o contexto do host quando o template é vinculado a um nobreak.

Um **dashboard global** do Zabbix é um objeto diferente. A exportação de template não promove automaticamente um dashboard de template para **Monitoring → Dashboards**. Por isso, este projeto fornece `tools/create_global_dashboard.py`, que usa o próprio dashboard nativo como fonte de verdade e o recria pela API do Zabbix para um host real já monitorado.

## Por que usar o gerador

O gerador evita manter uma segunda definição de dashboard escrita manualmente. Ele:

- detecta a versão major/minor do Zabbix conectado;
- carrega `templates/<major.minor>/vertiv-by-snmp.yaml`;
- localiza o dashboard nativo `Vertiv UPS Overview`;
- resolve as chaves dos itens do template para os IDs dos itens no host escolhido;
- resolve os nomes dos gráficos para os IDs dos gráficos no host escolhido;
- preserva páginas, posições, dimensões, títulos, thresholds, cores e demais campos suportados dos widgets;
- cria o objeto final usando `dashboard.create`.

Assim, alterações futuras feitas no dashboard nativo do template podem ser refletidas no dashboard global sem manter dois layouts independentes.

## Requisitos

- Zabbix 7.0 ou 8.0 correspondente a uma exportação existente neste repositório;
- template Vertiv já importado e vinculado ao host do nobreak;
- Python 3.9+;
- PyYAML (`pip install -r requirements-dev.txt` é suficiente);
- token de API do Zabbix cujo usuário tenha permissão para ler o host, itens e gráficos e criar dashboards.

## Faça primeiro um dry-run

A partir da raiz do repositório:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --dry-run
```

Esse comando resolve todas as referências e mostra o payload exato que seria enviado ao `dashboard.create`, sem criar nada.

## Criar o dashboard

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

Por padrão, o dashboard global é criado como privado. Para criá-lo como público, adicione `--public`:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --public
```

O compartilhamento com usuários ou grupos específicos deve ser configurado depois da criação, de acordo com a política de acesso do ambiente Zabbix.

## Recriar um dashboard existente

O utilitário se recusa a sobrescrever silenciosamente um dashboard com o mesmo nome. Isso é proposital.

Depois de revisar o `--dry-run`, use `--replace` para excluir e recriar explicitamente o dashboard existente:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.exemplo.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --replace
```

Como `--replace` recria o objeto, compartilhamentos personalizados e edições manuais feitas diretamente no dashboard global precisarão ser reaplicados. O modelo recomendado é fazer alterações de layout no dashboard do template e depois gerar novamente o global.

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

## Segurança

- Utilize um token de API com o menor privilégio prático.
- Nunca grave o token de API no repositório.
- O utilitário faz leituras para descobrir host, itens e gráficos e cria um dashboard. Ele somente exclui um dashboard quando `--replace` é informado explicitamente.
- Nenhuma operação SNMP de escrita é adicionada por esta funcionalidade.
