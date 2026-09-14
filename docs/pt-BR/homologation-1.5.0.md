# Registro de homologação em campo — candidata 1.5.0

[English](../en/homologation-1.5.0.md)

**Candidata:** 1.5.0  
**Data do registro:** 14/09/2026  
**Status geral:** **EM ANDAMENTO / RELEASE BLOQUEADA**

Este registro separa a evidência já coletada em hardware real dos checks que ainda exigem uma ação controlada em campo. Um check de campo pendente nunca é convertido em PASS apenas com base em evidência de repositório/CI.

## Ambiente de referência

| Componente | Valor observado |
| --- | --- |
| Nobreak | Vertiv `ITA-20k00AL3A02E00`, 20 kVA |
| Firmware do nobreak | `V220` |
| Placa de gerenciamento | `IS-UNITY-DP` |
| Firmware da placa | `8.5.1.0` / `IS-UNITY_8.5.1.0_00173` |
| sysObjectID | `.1.3.6.1.4.1.476.1.42` |
| Zabbix Server | `7.0.30` |
| Template candidato | `1.5.0` / `vendor.version: 1.5-0` |

Números de série e credenciais são intencionalmente omitidos.

## Evidência já coletada

| Check | Status | Evidência/observações |
| --- | --- | --- |
| Identificação do equipamento/placa | PASS | Fabricante, placa, firmware e modelo do nobreak observados em hardware real |
| Cobertura de identificação RFC1628 | PASS | Objetos de identificação presentes; `sysName.0` escolhido para NAME do inventário porque os objetos de nome do nobreak retornaram valores placeholder |
| Status/carga/autonomia/tensão da bateria via RFC1628 | PASS | Status suportado; autonomia observada em 4320 min, carga 100%, tensão 544,0 V após escala RFC |
| Corrente da bateria RFC1628 | EXCEÇÃO DE COMPATIBILIDADE | `upsBatteryCurrent` retornou `noSuchObject`; item permanece desabilitado por padrão |
| Temperatura da bateria RFC1628 | EXCEÇÃO DE COMPATIBILIDADE | `upsBatteryTemperature` retornou `noSuchObject`; item permanece desabilitado por padrão |
| Corrente privada da bateria Vertiv | PASS | OID privado final `4149` observado funcionando e mantido no dashboard de produção |
| Temperatura privada da bateria Vertiv | REJEITADA PARA PRODUÇÃO | OID privado final `4156` retornou aproximadamente `-0,1 °C`; desabilitado e sem trigger |
| Valores elétricos de entrada/saída RFC1628 | PASS | Valores trifásicos observados e coerentes com o ambiente do nobreak |
| Caracterização da escala de potência privada de entrada | PASS | Valores privados 1,6/1,5/1,5 correlacionados com os valores padrão 1600/1500/1500 W; itens privados continuam desabilitados porque RFC1628 é preferido |
| Comportamento normal da tabela de alarmes | PASS | `upsAlarmsPresent=0`; `upsAlarmTable` vazia em estado normal, como esperado |
| Estado inativo dos eventos privados | PASS (somente inativo) | Objetos `.2.100.*` retornaram `Inactive Event`; a codificação do estado ativo permanece desconhecida |
| Objetos de resultado de teste RFC1628 presentes | PASS | Objetos de resultado/tempo observados; o template apenas lê resultados |
| Validação estrutural/somente leitura do repositório | PASS | Validadores automatizados proíbem OIDs conhecidos de controle e caminhos de alerta padrão não suportados |
| Importação nova / upgrade no Zabbix 7.0 | PASS (CI) | CI importa a baseline estável e atualiza para a candidata pela API do Zabbix |

## Checks obrigatórios ainda pendentes

Os checks abaixo exigem acesso controlado ao ambiente real de monitoramento e são **bloqueadores da release**:

- [ ] Confirmar que `ups.snmp.uptime` atualiza a cada minuto no host de produção/homologação.
- [ ] Em janela controlada, interromper o acesso SNMP tempo suficiente para validar o problema `nodata()` após cinco minutos e a recuperação automática.
- [ ] Confirmar o evento informativo de reset do uptime do agente com um restart conhecido da placa/agente, ou documentar método alternativo aceito de verificação.
- [ ] Gerar ou aguardar um alarme real seguro do nobreak e confirmar que `upsAlarmTable` cria as linhas esperadas de descrição/tempo e as remove após a recuperação.
- [ ] Observar uma transição segura de resultado de teste diagnóstico/bateria e confirmar os itens/triggers somente leitura. O próprio template não deve iniciar o teste.
- [ ] Revisar as três páginas do dashboard em janela normal e em pelo menos uma janela representativa de incidente/evento.
- [ ] Registrar a versão/nível de segurança SNMP utilizado no ambiente de homologação.
- [ ] Confirmar que nenhum item inesperadamente unsupported permanece habilitado por padrão nessa combinação exata de placa/firmware.
- [ ] Registrar aprovação final do operador e data de homologação.

## Decisão de promoção

**Decisão atual: NÃO CRIAR A TAG `v1.5.0`.**

A promoção só é permitida depois que todos os checkboxes obrigatórios acima estiverem concluídos ou que uma exceção não bloqueante esteja explicitamente aprovada e documentada. Ao fechar o gate:

1. alterar este registro para **PASS** e incluir data/aprovação final;
2. atualizar a matriz de compatibilidade para `1.5.0 homologada em campo`;
3. datar a entrada 1.5.0 do changelog;
4. atualizar `STABLE_VERSION` para `1.5.0`;
5. criar tag/release `v1.5.0` somente após sucesso do CI de release.
