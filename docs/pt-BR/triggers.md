# Triggers

[English](../en/triggers.md)

O template contém 26 definições de trigger ou protótipo de trigger.

| Trigger | Severidade | Condição |
| --- | --- | --- |
| UPS has a warning on {HOST.NAME} | WARNING | `last(/Vertiv by SNMP/vertiv.system.status)=8` |
| UPS has an active alarm on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/vertiv.system.status)=16` |
| UPS abnormal operation on {HOST.NAME} | DISASTER | `last(/Vertiv by SNMP/vertiv.system.status)=32` |
| UPS output is OFF on {HOST.NAME} | DISASTER | `last(/Vertiv by SNMP/ups.output.source)=2` |
| UPS is operating on bypass on {HOST.NAME} | AVERAGE | `last(/Vertiv by SNMP/ups.output.source)=4` |
| UPS is operating on battery on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/ups.output.source)=5` |
| UPS reports active alarm(s) on {HOST.NAME} | AVERAGE | `last(/Vertiv by SNMP/ups.alarms.present)>0` |
| UPS battery is low on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/ups.battery.status)=3` |
| UPS battery is depleted on {HOST.NAME} | DISASTER | `last(/Vertiv by SNMP/ups.battery.status)=4` |
| UPS battery runtime is low on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/ups.output.source)=5 and last(/Vertiv by SNMP/ups.battery.runtime)<{$UPS.RUNTIME.WARN} and last(/Vertiv by SNMP/ups.battery.runtime)>={$UPS.RUNTIME.CRIT}` |
| UPS battery runtime is critically low on {HOST.NAME} | DISASTER | `last(/Vertiv by SNMP/ups.output.source)=5 and last(/Vertiv by SNMP/ups.battery.runtime)<{$UPS.RUNTIME.CRIT}` |
| UPS battery charge is low on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/ups.output.source)=5 and last(/Vertiv by SNMP/ups.battery.charge)<{$UPS.BATTERY.CHARGE.WARN} and last(/Vertiv by SNMP/ups.battery.charge)>={$UPS.BATTERY.CHARGE.CRIT}` |
| UPS battery charge is critically low on {HOST.NAME} | DISASTER | `last(/Vertiv by SNMP/ups.output.source)=5 and last(/Vertiv by SNMP/ups.battery.charge)<{$UPS.BATTERY.CHARGE.CRIT}` |
| UPS battery temperature is high on {HOST.NAME} | WARNING | `last(/Vertiv by SNMP/vertiv.battery.temperature)>={$UPS.BATTERY.TEMP.WARN} and last(/Vertiv by SNMP/vertiv.battery.temperature)<{$UPS.BATTERY.TEMP.CRIT}` |
| UPS battery temperature is critically high on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/vertiv.battery.temperature)>={$UPS.BATTERY.TEMP.CRIT}` |
| UPS battery self-test failed on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/vertiv.battery.test.result)=2 or last(/Vertiv by SNMP/vertiv.battery.test.result)=4` |
| UPS registered a new battery discharge on {HOST.NAME} | INFO | `change(/Vertiv by SNMP/vertiv.battery.discharge.count)>0` |
| UPS detected a new bad input line event on {HOST.NAME} | WARNING | `change(/Vertiv by SNMP/ups.input.line.bads)>0` |
| UPS registered a new input blackout on {HOST.NAME} | WARNING | `change(/Vertiv by SNMP/vertiv.input.blackout.count)>0` |
| UPS registered a new input brownout on {HOST.NAME} | WARNING | `change(/Vertiv by SNMP/vertiv.input.brownout.count)>0` |
| UPS load is high on {HOST.NAME} | WARNING | `last(/Vertiv by SNMP/vertiv.output.load)>={$UPS.LOAD.WARN} and last(/Vertiv by SNMP/vertiv.output.load)<{$UPS.LOAD.CRIT}` |
| UPS load is critically high on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/vertiv.output.load)>={$UPS.LOAD.CRIT}` |
| UPS inlet air temperature is high on {HOST.NAME} | WARNING | `last(/Vertiv by SNMP/vertiv.inlet.temperature)>={$UPS.INLET.TEMP.WARN} and last(/Vertiv by SNMP/vertiv.inlet.temperature)<{$UPS.INLET.TEMP.CRIT}` |
| UPS inlet air temperature is critically high on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/vertiv.inlet.temperature)>={$UPS.INLET.TEMP.CRIT}` |
| UPS output line {#SNMPINDEX} load is high on {HOST.NAME} | WARNING | `last(/Vertiv by SNMP/ups.output.load[{#SNMPINDEX}])>={$UPS.LOAD.WARN} and last(/Vertiv by SNMP/ups.output.load[{#SNMPINDEX}])<{$UPS.LOAD.CRIT}` |
| UPS output line {#SNMPINDEX} load is critically high on {HOST.NAME} | HIGH | `last(/Vertiv by SNMP/ups.output.load[{#SNMPINDEX}])>={$UPS.LOAD.CRIT}` |

## Notas de projeto

- Os limites de aviso e crítico são deliberadamente configurados sem sobreposição.
- Os limites de autonomia e carga da bateria são avaliados somente quando a fonte da saída do nobreak é `Battery`.
- Triggers baseadas em contadores usam `change()` para informar um novo blackout, brownout, descarga de bateria ou evento de entrada inválida.
- As triggers de status do sistema e fonte da saída utilizam value maps para exibir valores legíveis em Latest data.
- A interpretação de eventos via trap SNMP não é habilitada por padrão porque os nomes dos OIDs de evento, isoladamente, não definem o payload exato enviado por cada placa de gerenciamento.
