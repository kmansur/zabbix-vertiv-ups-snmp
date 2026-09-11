# Changelog

[English](CHANGELOG.md) | **Português (Brasil)**

Todas as alterações relevantes deste projeto são documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto utiliza [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Planejado

- Validar modelos adicionais de nobreaks Vertiv/Liebert e firmwares de placas de gerenciamento.
- Adicionar processamento específico de traps SNMP após a captura e documentação de payloads reais.
- Revalidar o export Zabbix 8.0 contra builds RC/final.

## [1.5.0] - Não lançado (candidata para homologação)

### Adicionado

- Heartbeat SNMP dedicado por `sysUpTime.0`, trigger de indisponibilidade por `nodata(5m)` e aviso de reset do agente.
- Identificação RFC1628, corrente/temperatura de bateria padronizadas e resultados somente leitura de testes diagnósticos.
- Descoberta de `upsAlarmTable` com value map dos 24 alarmes conhecidos da RFC1628.
- Proveniência MIB/OID, matriz de compatibilidade e checklist de homologação de produção.
- Validador específico de produção e teste CI de importação via API em Zabbix 7 real.

### Alterado

- Alertas de temperatura de bateria passam a usar `upsBatteryTemperature` RFC1628.
- Alertas de carga permanecem nos protótipos `upsOutputPercentLoad` RFC1628; o agregado privado deixa de gerar trigger.
- Card de alarmes fica vermelho para qualquer quantidade positiva, evitando sugerir severidade pela contagem.

### Segurança / confiabilidade

- Potência privada de entrada e temperatura privada de bateria ficam desabilitadas por padrão.
- Gráficos legados baseados em métricas experimentais/contadores cumulativos foram removidos.
- Nenhum OID de controle/escrita foi adicionado.

## [1.4.1] - 2026-09-11

### Corrigido

- Reorganizado o dashboard após a remoção das métricas privadas de potência de entrada não validadas, eliminando grandes áreas vazias.
- Autonomia exibida em horas por um item calculado de apresentação, mantendo o item RFC1628 original em minutos para triggers e diagnóstico.
- O gráfico de bateria passa a usar horas, evitando a apresentação `Kmin` do frontend.
- Contadores cumulativos de blackout, brownout e linha inválida deixam de ocupar um gráfico de tendência no dashboard e passam a cards numéricos na página Electrical.
- O gráfico padrão de ambiente passa a mostrar somente a temperatura de entrada; a temperatura privada da bateria continua coletada e disponível, mas não distorce mais a escala do gráfico quando a própria placa informa valores sentinela como `-0.1 °C`.
- O gráfico de carga por fase ocupa a largura da página Electrical e os cards elétricos foram redistribuídos.
- Contadores de descargas e eventos são exibidos sem casas decimais.

### Observação de campo

No equipamento Vertiv ITA-20kVA validado, a própria interface web do nobreak informa `4320 min` de autonomia e `-0.1 °C` de temperatura de bateria. A 1.4.1 não altera esses dados de origem: apenas apresenta a autonomia como horas e evita tratar a temperatura privada da bateria como referência ambiental padrão.

## [1.4.0] - 2026-09-11

### Adicionado

- Documentação do status/maturidade do projeto com pontuação explícita de **85%** e trabalhos de validação restantes.
- Monitoramento de dependências Python pelo Dependabot, além das GitHub Actions.
- Testes de higiene do repositório para empacotamento de release e baseline dos workflows.

### Alterado

- Nome visível do template alterado para **Vertiv by SNMP**. O identificador técnico permanece `VERTIV by SNMP` intencionalmente para permitir atualização in-place sem criar um template duplicado.
- Dashboard nativo renomeado para **Vertiv UPS Overview**.
- Cards de status com cores por criticidade finalizados usando value map nativo e zero casas decimais para enums compactos.
- GitHub Actions checkout/setup-python atualizadas para v7.
- Valores privados de potência de entrada continuam disponíveis para troubleshooting, mas deixam de ser destacados no dashboard até a validação da escala específica do fabricante.

### Corrigido

- Validador do template alinhado à configuração final de tipografia/cores do dashboard.
- Removido texto obsoleto do preview de macros nos metadados do template.
- Empacotamento de release agora usa nomes exclusivos para assets Zabbix 7.0/8.0, inclui o gerador/ferramentas do mapa sinótico e publica checksums SHA-256.
- Removida a documentação exclusiva do preview do dashboard no projeto final.

## [1.3.3] - 2026-09-11

### Alterado

- Ajustado o tamanho dos valores dos cards do dashboard para evitar truncamento.
- Valores de estado/value map usam 24%; valores numéricos usam 27%.
- Casas decimais e unidades usam 16%.
- Removidos os indicadores de mudança dos cards compactos, preservando espaço para valores como `Normal operation`, `External` e `8 weeks`.
- Mantidos layout, gráficos, itens, triggers e coleta SNMP sem alterações funcionais.

## [1.3.2] - 2026-09-11

### Corrigido

- Normalização dos enums privados Vertiv que algumas placas retornam como `STRING` em vez de valores numéricos SNMP.
- Os dez itens de estado/configuração afetados agora aceitam tanto o texto retornado pela placa quanto o enum numérico canônico.
- Mantidos os tipos `Numeric (unsigned)`, value maps e triggers numéricos, preservando compatibilidade entre diferentes placas/firmwares.
- Mapeamentos validados em equipamento real para `Normal Operation`, `on`, `off`, `Online`, `None`, `fully charged`, `Passed`, `disabled`, `8 weeks` e `External`.
- Validador do repositório reforçado para exigir o pré-processamento de normalização nesses itens.

## [1.3.1] - 2026-09-11

### Corrigido

- Corrigido o UUID do dashboard nativo do template para um UUID versão 4 RFC 4122 válido, como exigido pela validação de importação do Zabbix 7.0.
- Reforçada a validação do repositório para exigir UUIDv4 em todo campo `uuid` exportado, evitando a recorrência do erro `UUIDv4 is expected`.

## [1.3.0] - 2026-09-11

### Adicionado

- Gerador opcional de mapa sinótico de rede do Zabbix para um host Vertiv UPS.
- Ícones próprios de estado normal/problema incorporados ao YAML gerado.
- Blocos esquemáticos de entrada, bypass, saída e bateria com destaque dinâmico do elemento central do host.
- Testes automatizados do formato do mapa, referências de host e imagens PNG incorporadas.
- Documentação bilíngue de geração e importação do mapa.

### Segurança / compatibilidade

- O mapa não adiciona OIDs SNMP de escrita ou controle.
- O host referenciado precisa existir antes da importação do mapa.
- Os blocos periféricos permanecem estáticos para evitar a criação de vínculos dinâmicos não suportados pelo formato genérico de importação.

## [1.2.0] - 2026-09-11

### Adicionado

- Dashboard nativo de template **Vertiv UPS Overview**.
- Páginas Overview, Electrical e Battery & Environment.
- Cards de estado do nobreak, fonte da saída, alarmes, carga/autonomia da bateria e principais valores elétricos.
- Integração do dashboard com os seis gráficos nativos do template.
- Documentação bilíngue do dashboard.

## [1.1.0] - 2026-09-11

### Adicionado

- Item de frequência de saída pela RFC 1628 com escala padronizada de `0,1 Hz`.
- Itens fixos Vertiv de tensão L-N/L-L para entrada, saída e bypass, preparados para dashboards.
- Itens fixos por fase de corrente, fator de potência e potência real de entrada.
- Itens fixos por fase de corrente, fator de potência, percentual de carga, potência real e potência aparente de saída.
- Potência total de entrada calculada a partir das três potências de fase Vertiv.
- Itens/value maps para tipo de gabinete de bateria e intervalo do teste automático de bateria.
- Gráficos de potência de entrada por fase e carga de saída por fase.
- Documentação bilíngue do resumo elétrico.

### Segurança / validação

- Nenhum multiplicador foi presumido para os novos OIDs elétricos privados Vertiv porque a lista de parâmetros SNMP fornecida não define a escala numérica desses objetos.
- Os OIDs de condição Vertiv `.2.100.*` continuam intencionalmente fora do polling/triggers ativos até validarmos a codificação dos estados em equipamento real.
- Nenhum OID SNMP de escrita/controle foi adicionado.

## [1.0.0] - 2026-09-10

### Adicionado

- Primeira release mantida do **Vertiv by SNMP**.
- Export versionado para Zabbix 7.0.
- Export de compatibilidade com Zabbix 8.0.
- Monitoramento pela RFC 1628 UPS-MIB para bateria, entrada, saída, bypass e configuração nominal.
- Monitoramento privado Vertiv/Liebert para status do sistema, detalhes de bateria, qualidade de energia, energia, temperaturas e identificação.
- LLD para tabelas de linhas de entrada, saída e bypass.
- Macros configuráveis para limites de autonomia, carga da bateria, carga do nobreak e temperatura.
- Value maps para os principais estados do nobreak e da Vertiv.
- Quatro gráficos nativos para bateria/autonomia, temperaturas, potência de saída e contadores de qualidade de energia.
- Item opcional e desabilitado para traps SNMP da árvore privada Vertiv.
- Documentação bilíngue em inglês e português do Brasil.
- Validadores de template/documentação, testes e CI no GitHub Actions.
- Workflows de release e CodeQL.
- Licenciamento MIT para as contribuições originais do repositório.
- Atribuição explícita à referência histórica `Template Vertiv` de Mihguel da Silva Santos Tavares de Araujo.

### Alterado em relação à referência histórica

- O modelo de monitoramento foi refeito da estrutura original orientada a retificadores `1.3.6.1.4.1.6302...` para objetos de UPS da RFC 1628 e Vertiv/Liebert `1.3.6.1.4.1.476.1.42`.
- Alarmes fixos de percentual de bateria foram substituídos por triggers contextuais de autonomia/carga avaliadas quando o nobreak está em bateria.
- Premissas fixas de fases foram substituídas por LLD.
- Macros/value maps não relacionados e operações de escrita/controle foram removidos.
