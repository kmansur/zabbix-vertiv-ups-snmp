# Registro de validação em campo — release 1.5.0

[English](../en/homologation-1.5.0.md)

**Release:** 1.5.0  
**Data do registro:** 14/09/2026  
**Status da release de software:** **APROVADA**  
**Status da validação estendida em campo:** **EM ANDAMENTO**

Este registro separa a evidência já coletada em hardware real dos cenários controlados que ainda exigem ação em campo. O mantenedor aprovou a release de software 1.5.0 depois que passaram a validação do repositório, o CodeQL, a importação nova no Zabbix 7.0 e o upgrade in-place 1.4.1 → 1.5.0. Checks de campo pendentes não são convertidos em PASS com base em CI, e o hardware de referência ainda não é descrito como totalmente homologado em campo.

A candidata de repositório **1.5.1** adiciona apenas ferramenta/documentação de dashboard global e não altera a semântica de monitoramento da 1.5.0 nem invalida este registro de campo. O `--dry-run` do gerador foi validado com sucesso pelo mantenedor contra um ambiente Zabbix 7.0 real.

## Ambiente de referência

| Componente | Valor observado |
| --- | --- |
| Nobreak | Vertiv `ITA-20k00AL3A02E00`, 20 kVA |
| Firmware do nobreak | `V220` |
| Placa de gerenciamento | `IS-UNITY-DP` |
| Firmware da placa | `8.5.1.0` / `IS-UNITY_8.5.1.0_00173` |
| sysObjectID | `.1.3.6.1.4.1.476.1.42` |
| Zabbix Server | `7.0.30` |
| Release do template | `1.5.0` / `vendor.version: 1.5-0` |

Números de série e credenciais são intencionalmente omitidos.

## Evidência já coletada

| Check | Status | Evidência/observações |
| --- | --- | --- |
| Identificação do equipamento/placa | PASS | Fabricante, placa, firmware e modelo do nobreak observados em hardware real |
| Cobertura de identificação RFC1628 | PASS | Objetos de identificação presentes; `sysName.0` escolhido para NAME do inventário porque os objetos de nome do nobreak retornaram valores placeholder |
| Status/carga/autonomia/tensão da bateria via RFC1628 | PASS | Status suportado; autonomia observada em 4320 min, carga 100%, tensão 544,0 V após escala RFC |
| Corrente da bateria RFC1628 | EXCEÇÃO DE COMPATIBILIDADE | `upsBatteryCurrent` retornou `noSuchObject`; item da release permanece desabilitado por padrão |
| Temperatura da bateria RFC1628 | EXCEÇÃO DE COMPATIBILIDADE | `upsBatteryTemperature` retornou `noSuchObject`; item da release permanece desabilitado por padrão |
| Corrente privada da bateria Vertiv | PASS | OID privado final `4149` observado funcionando e mantido no dashboard de produção |
| Temperatura privada da bateria Vertiv | REJEITADA PARA PRODUÇÃO | OID privado final `4156` retornou aproximadamente `-0,1 °C`; desabilitado e sem trigger |
| Valores elétricos de entrada/saída RFC1628 | PASS | Valores trifásicos observados e coerentes com o ambiente do nobreak |
| Caracterização da escala de potência privada de entrada | PASS | Valores privados 1,6/1,5/1,5 correlacionados com os valores padrão 1600/1500/1500 W; itens privados continuam desabilitados porque RFC1628 é preferido |
| Comportamento normal da tabela de alarmes | PASS | `upsAlarmsPresent=0`; `upsAlarmTable` vazia em estado normal, como esperado |
| Estado inativo dos eventos privados | PASS (somente inativo) | Objetos `.2.100.*` retornaram `Inactive Event`; a codificação do estado ativo permanece desconhecida |
| Objetos de resultado de teste RFC1628 presentes | PASS | Objetos de resultado/tempo observados; o template apenas lê resultados |
| Validação estrutural/somente leitura do repositório | PASS | Validadores automatizados proíbem OIDs conhecidos de controle e caminhos de alerta padrão não suportados |
| Importação nova no Zabbix 7.0 | PASS (CI) | O export da release importa pela API do Zabbix |
| Upgrade in-place no Zabbix 7.0 | PASS (CI) | A 1.4.1 estável importa e atualiza in-place para a 1.5.0 pela API do Zabbix |
| CodeQL | PASS | A análise de segurança foi concluída com sucesso antes da promoção |

## Checks de campo pós-release ainda pendentes

Os checks abaixo exigem acesso controlado ao ambiente real de monitoramento. Eles **não são bloqueadores da release de software**, mas continuam obrigatórios antes de descrever essa combinação exata de hardware como totalmente homologada em campo:

- [x] Confirmar que `ups.snmp.uptime` atualiza a cada minuto no host de produção/homologação.
- [x] Em janela controlada, interromper o acesso SNMP tempo suficiente para validar o problema `nodata()` após cinco minutos e a recuperação automática.
- [ ] Confirmar o evento informativo de reset do uptime do agente com um restart conhecido da placa/agente, ou documentar método alternativo aceito de verificação.
- [ ] Gerar ou aguardar um alarme real seguro do nobreak e confirmar que `upsAlarmTable` cria as linhas esperadas de descrição/tempo e as remove após a recuperação.
- [ ] Observar uma transição segura de resultado de teste diagnóstico/bateria e confirmar os itens/triggers somente leitura. O próprio template não deve iniciar o teste.
- [x] Revisar as três páginas do dashboard em janela normal e em pelo menos uma janela representativa de incidente/evento.
- [x] Registrar a versão/nível de segurança SNMP utilizado no ambiente de referência.
- [x] Confirmar que nenhum item inesperadamente unsupported permanece habilitado por padrão nessa combinação exata de placa/firmware.
- [ ] Registrar aprovação final do operador e data da homologação em campo.

## Evidência de validação em campo coletada em 14/09/2026

- `ups.snmp.uptime` foi observado atualizando no intervalo configurado de 1 minuto.
- Uma interrupção controlada de UDP/161 no lado do monitoramento gerou o evento HIGH esperado `UPS SNMP data unavailable` após cinco minutos e recuperou automaticamente após a restauração do SNMP.
- O filtro `Not supported` do Zabbix não retornou nenhum item padrão/habilitado no host de referência.
- O ambiente de referência usa SNMPv2c em UDP/161 monitorado diretamente pelo Zabbix Server; o segredo da community é intencionalmente omitido deste registro.
- Os dashboards Overview, Electrical e Battery & Environment renderizaram corretamente em operação normal; as lacunas no histórico correspondem à interrupção SNMP intencional.
- Eventos reais de 12/09/2026 confirmaram triggers de alarme ativo, operação em bateria, warning, contador de blackout e contador de descarga da bateria com recuperação automática. O alarme ativo durou 30 segundos.
- `upsAlarmsPresent` e o comportamento normal de `upsAlarmTable` vazia estão validados. Como o alarme real de 30 segundos foi menor que a cadência atual de 1 minuto da LLD, não é afirmada a captura individual da linha; a candidata 1.5.3 reduz a descoberta para 30 segundos.
- `UPS: Battery test result` é coletado e mapeado como `Passed`; nenhuma transição de estado foi observada no histórico retido, portanto a transição permanece pendente de observação natural.
- Um restart real da placa de gerenciamento ocorreu anteriormente e reiniciou somente a placa, mas o trigger de reset de uptime do Zabbix não ficou retido como evidência direta; o restart não será repetido apenas para validação.

## Decisão de release

**Decisão do mantenedor: APROVADO CRIAR/PUBLICAR `v1.5.0` em 14/09/2026.**

A decisão de release é baseada nos gates de repositório, CI, segurança e evidência já coletada em hardware real. Essa aprovação altera apenas o gate da release de software; ela não marca os checkboxes de hardware pendentes como concluídos.

Quando todos os checks de campo pós-release acima forem concluídos:

1. alterar o status da validação estendida em campo para **PASS** e incluir data/aprovação final;
2. atualizar a matriz de compatibilidade para `1.5.0 homologada em campo` para essa combinação exata de hardware;
3. fechar a issue de acompanhamento da validação de campo pós-release.

## Contexto das releases posteriores

Este documento permanece como registro de validação em campo da release de monitoramento 1.5.0. A candidata atual do repositório é **1.5.3** e a última release estável permanece **1.5.2**. A candidata 1.5.3 incorpora evidência de validação em campo e reduz a cadência da LLD de alarmes ativos de 1m para 30s, sem introduzir operações de escrita/controle.
