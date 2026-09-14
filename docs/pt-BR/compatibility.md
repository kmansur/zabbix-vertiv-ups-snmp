# Matriz de compatibilidade

[English](../en/compatibility.md)

Esta matriz separa **compatibilidade de engenharia** de **homologação em campo**. Um export pode passar na validação estrutural/importação sem comprovar cada OID em todos os firmwares. A homologação 1.5.0 usa o comportamento real do equipamento para definir os defaults seguros do template.

| Nobreak / placa | Zabbix | Status | Observações |
| --- | --- | --- | --- |
| Vertiv `ITA-20k00AL3A02E00` (20 kVA), firmware UPS `V220` / placa `IS-UNITY-DP`, firmware `8.5.1.0` (`IS-UNITY_8.5.1.0_00173`) | 7.0 | Homologação 1.5.0 em andamento | Estados principais, valores elétricos, enums textuais e dashboard foram observados em hardware real. `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) e `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) retornam `noSuchObject` nesta placa/firmware. A versão exata do Zabbix ainda deve ser registrada. |
| Outros Vertiv/Liebert / firmwares de placa | 7.0 | Compatível por projeto RFC1628; não certificado em campo | A implementação de UPS-MIB pode ser parcial. Objetos padrão opcionais devem ser confirmados no equipamento; OIDs privados precisam ser comparados com a UI local do nobreak. |
| Vertiv/Liebert | 8.0 desenvolvimento | Apenas export/paridade semântica | Não é alegação de suporte de produção até importação e execução em uma build 8.0 real. |

## Identificação observada em campo

A placa respondeu como fabricante `Vertiv`, modelo `IS-UNITY-DP`, firmware `8.5.1.0`, build `IS-UNITY_8.5.1.0_00173` e `sysObjectID` `.1.3.6.1.4.1.476.1.42`. O nobreak reportou modelo `ITA-20k00AL3A02E00` e firmware `V220`. Números de série não são publicados nesta matriz.

## Resultado de campo — grupo de bateria RFC1628

A placa usada na homologação implementa apenas parte do grupo UPS-MIB de bateria. Foram observados:

- `upsBatteryStatus` (`.1.3.6.1.2.1.33.1.2.1.0`) — **suportado**;
- `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) — **não suportado**, retorna `No Such Object available on this agent at this OID`;
- `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) — **não suportado**, retorna a mesma resposta `noSuchObject`.

Por isso, a candidata 1.5.0 mantém corrente e temperatura RFC1628 no template apenas como itens opcionais **desabilitados por padrão**. Eles não participam de dashboard nem triggers de produção e só devem ser habilitados em outra placa/firmware depois de confirmar suporte.

No equipamento validado, a corrente de bateria continua sendo coletada pelo OID privado Vertiv `...1.2.1.4149` (`vertiv.battery.current`), que já foi observado em campo. A instância privada `...1.2.1.4156` retornou `-0,1 °C`, valor incompatível com o ambiente observado, e permanece desabilitada e sem trigger de produção. O mesmo walk revelou uma segunda instância `...1.2.2.4156` retornando `31,8 °C`; esse valor é plausível, mas a identidade física dessa segunda instância ainda precisa ser confirmada na interface/LCD antes de ser usada como temperatura de bateria de produção. O gráfico ambiental continua usando apenas a temperatura de entrada validada.

Esse comportamento é um exemplo importante: conformidade com partes da RFC1628 **não implica implementação de todos os escalares do UPS-MIB** pelo agente SNMP.

## Resultado de campo — potência de entrada privada

Os OIDs privados `6318`, `6319` e `6320` retornaram respectivamente `1,6`, `1,5` e `1,5`. No mesmo instante, as tensões/correntes/fatores de potência de entrada (`209,3 V / 7,9 A / 0,99`, `212,7 V / 7,6 A / 0,99`, `209,5 V / 7,5 A / 0,99`) implicam aproximadamente `4,8 kW` no total, enquanto a soma dos três objetos privados é `4,6`. Isso é forte evidência de que esses objetos usam **kW por fase**, e não watts, mas a confirmação final contra LCD/interface web continua obrigatória antes de habilitá-los por padrão.

## Resultado de campo — eventos e alarmes

Com o equipamento em estado normal, `upsAlarmsPresent` retornou `0` e a `upsAlarmTable` não apresentou linhas, comportamento esperado. Os objetos privados `.2.100.*` observados retornaram o texto `Inactive Event`; esse estado inativo está portanto confirmado para esta placa/firmware. O texto/encoding do estado **ativo** ainda precisa ser capturado em um evento real antes de criar triggers privados específicos.

## Registro de homologação

Para cada novo equipamento certificado, registre:

- modelo e capacidade nominal do nobreak;
- modelo da placa de gerenciamento;
- firmware do nobreak e da placa;
- versão exata do Zabbix;
- versão/nível de segurança SNMP;
- suporte real aos objetos RFC1628 de identificação, bateria, tabela de alarmes e resultado de testes;
- comparação dos valores privados exibidos com LCD/interface web;
- variantes de enums/traps observadas.
