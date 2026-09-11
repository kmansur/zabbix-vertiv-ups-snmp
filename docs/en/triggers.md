# Triggers

[Português (Brasil)](../pt-BR/triggers.md)

The template contains 26 trigger or trigger-prototype definitions.

| Trigger | Severity | Condition |
| --- | --- | --- |
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
| UPS battery temperature is high on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/vertiv.battery.temperature)>={$UPS.BATTERY.TEMP.WARN} and last(/VERTIV by SNMP/vertiv.battery.temperature)<{$UPS.BATTERY.TEMP.CRIT}` |
| UPS battery temperature is critically high on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.battery.temperature)>={$UPS.BATTERY.TEMP.CRIT}` |
| UPS battery self-test failed on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.battery.test.result)=2 or last(/VERTIV by SNMP/vertiv.battery.test.result)=4` |
| UPS registered a new battery discharge on {HOST.NAME} | INFO | `change(/VERTIV by SNMP/vertiv.battery.discharge.count)>0` |
| UPS detected a new bad input line event on {HOST.NAME} | WARNING | `change(/VERTIV by SNMP/ups.input.line.bads)>0` |
| UPS registered a new input blackout on {HOST.NAME} | WARNING | `change(/VERTIV by SNMP/vertiv.input.blackout.count)>0` |
| UPS registered a new input brownout on {HOST.NAME} | WARNING | `change(/VERTIV by SNMP/vertiv.input.brownout.count)>0` |
| UPS load is high on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/vertiv.output.load)>={$UPS.LOAD.WARN} and last(/VERTIV by SNMP/vertiv.output.load)<{$UPS.LOAD.CRIT}` |
| UPS load is critically high on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.output.load)>={$UPS.LOAD.CRIT}` |
| UPS inlet air temperature is high on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/vertiv.inlet.temperature)>={$UPS.INLET.TEMP.WARN} and last(/VERTIV by SNMP/vertiv.inlet.temperature)<{$UPS.INLET.TEMP.CRIT}` |
| UPS inlet air temperature is critically high on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/vertiv.inlet.temperature)>={$UPS.INLET.TEMP.CRIT}` |
| UPS output line {#SNMPINDEX} load is high on {HOST.NAME} | WARNING | `last(/VERTIV by SNMP/ups.output.load[{#SNMPINDEX}])>={$UPS.LOAD.WARN} and last(/VERTIV by SNMP/ups.output.load[{#SNMPINDEX}])<{$UPS.LOAD.CRIT}` |
| UPS output line {#SNMPINDEX} load is critically high on {HOST.NAME} | HIGH | `last(/VERTIV by SNMP/ups.output.load[{#SNMPINDEX}])>={$UPS.LOAD.CRIT}` |

## Design notes

- Warning and critical thresholds are intentionally non-overlapping.
- Battery runtime and charge thresholds are evaluated only while the UPS output source is `Battery`.
- Counter-based triggers use `change()` to report a newly registered blackout, brownout, battery discharge or bad-input event.
- System-status and output-source triggers rely on value maps for readable Latest data values.
- SNMP trap event parsing is not enabled by default because event OID names do not by themselves define the exact trap payload sent by every management card.
