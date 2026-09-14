# Triggers

[English](../en/triggers.md)

O template contém 26 definições de trigger ou protótipo de trigger na candidata 1.5.0.

| Trigger | Severidade | Condição |
| --- | --- | --- |
| UPS SNMP data unavailable on {HOST.NAME} | HIGH | `nodata(/VERTIV by SNMP/ups.snmp.uptime,5m)=1` |
| UPS management agent uptime reset on {HOST.NAME} | INFO | `change(/VERTIV by SNMP/ups.snmp.uptime)<0` |
| UPS has a warning on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/vertiv.system.status)=8` |
| UPS has an active alarm on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.system.status)=16` |
| UPS abnormal operation on {HOST.NAME} | DISASTER | `last(/VERTIV by SNMP/vertiv.system.status)=32` |
| UPS output is OFF on {HOST.NAME} | DISASTER | `last(/VERTIV by SNMP/ups.output.source)=2` |
| UPS is operating on bypass on {HOST.NAME} | AVERAGE | `last(/VERTIV by SNMP/ups.output.source)=4` |
| UPS is operating on battery on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.output.source)=5` |
| UPS reports active alarm(s) on {HOST.NAME} | AVERAGE | `last(/VERTIV by SNMP/ups.alarms.present)>0` |
| UPS battery is low on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.battery.status)=3` |
| UPS battery is depleted on {HOST.NAME} | DISASTER | `last(/VERTIV by SNMP/ups.battery.status)=4` |
| UPS battery runtime is low on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.output.source)=5 and last(/VERTIV by SNMP/ups.battery.runtime)<{$UPS.RUNTIME.WARN} and last(/VERTIV by SNMP/ups.battery.runtime)>={$UPS.RUNTIME.CRIT}` |
| UPS battery runtime is critically low on {HOST.NAME} | DISASTER | `last(/VERTIV by SNMP/ups.output.source)=5 and last(/VERTIV by SNMP/ups.battery.runtime)<{$UPS.RUNTIME.CRIT}` |
| UPS battery charge is low on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.output.source)=5 and last(/VERTIV by SNMP/ups.battery.charge)<{$UPS.BATTERY.CHARGE.WARN} and last(/VERTIV by SNMP/ups.battery.charge)>={$UPS.BATTERY.CHARGE.CRIT}` |
| UPS battery charge is critically low on {HOST.NAME} | DISASTER | `last(/VERTIV by SNMP/ups.output.source)=5 and last(/VERTIV by SNMP/ups.battery.charge)<{$UPS.BATTERY.CHARGE.CRIT}` |
| UPS battery self-test failed on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.battery.test.result)=2 or last(/VERTIV by SNMP/vertiv.battery.test.result)=4` |
| UPS diagnostic test completed with warning on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/ups.test.results.summary)=2` |
| UPS diagnostic test failed on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.test.results.summary)=3` |
| UPS registered a new battery discharge on {HOST.NAME} | INFO | `change(/VERTIV by SNMP/vertiv.battery.discharge.count)>0` |
| UPS detected a new bad input line event on {HOST.NAME} | WARNING | `change(/VERTIV by SNMP/ups.input.line.bads)>0` |
| UPS registered a new input blackout on {HOST.NAME} | WARNING | `change(/VERTIV by SNMP/vertiv.input.blackout.count)>0` |
| UPS registered a new input brownout on {HOST.NAME} | WARNING | `change(/VERTIV by SNMP/vertiv.input.brownout.count)>0` |
| UPS inlet air temperature is high on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/vertiv.inlet.temperature)>={$UPS.INLET.TEMP.WARN} and last(/VERTIV by SNMP/vertiv.inlet.temperature)<{$UPS.INLET.TEMP.CRIT}` |
| UPS inlet air temperature is critically high on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.inlet.temperature)>={$UPS.INLET.TEMP.CRIT}` |
| UPS output line {#SNMPINDEX} load is high on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/ups.output.load[{#SNMPINDEX}])>={$UPS.LOAD.WARN} and last(/VERTIV by SNMP/ups.output.load[{#SNMPINDEX}])<{$UPS.LOAD.CRIT}` |
| UPS output line {#SNMPINDEX} load is critically high on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.output.load[{#SNMPINDEX}])>={$UPS.LOAD.CRIT}` |

## Notas de projeto

- Os limites de aviso e crítico são deliberadamente configurados sem sobreposição.
- Os limites de autonomia e carga da bateria são avaliados somente quando a fonte da saída do nobreak é `Battery`.
- Triggers baseadas em contadores usam `change()` para informar um novo blackout, brownout, descarga de bateria ou evento de entrada inválida.
- Os alertas de carga usam os protótipos padronizados RFC1628 `upsOutputPercentLoad`. O item privado agregado `vertiv.output.load` não gera triggers na candidata 1.5.0.
- Não existe trigger padrão de temperatura da bateria. No equipamento de homologação, o objeto RFC1628 `upsBatteryTemperature` não é suportado e o objeto privado de temperatura da bateria retornou valor inválido/semelhante a sentinela; ambos permanecem fora do alertamento padrão de produção.
- O heartbeat dedicado baseado em `sysUpTime.0` gera alerta após cinco minutos sem dados e um evento informativo quando o uptime do agente de gerenciamento diminui.
- Os objetos de teste diagnóstico RFC1628 são somente leitura neste projeto; as duas triggers de resultado apenas observam o resumo do teste e nunca iniciam ou interrompem testes.
- As triggers de status do sistema e fonte da saída utilizam value maps para exibir valores legíveis em Latest data.
- A interpretação de eventos via trap SNMP não é habilitada por padrão porque os nomes dos OIDs de evento, isoladamente, não definem o payload exato enviado por cada placa de gerenciamento.
