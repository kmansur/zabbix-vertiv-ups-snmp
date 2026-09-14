# Triggers

[Português (Brasil)](../pt-BR/triggers.md)

The template contains 26 trigger or trigger-prototype definitions in the 1.5.0 candidate.

| Trigger | Severity | Condition |
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

## Design notes

- Warning and critical thresholds are intentionally non-overlapping.
- Battery runtime and charge thresholds are evaluated only while `UPS: Output source` reports **Battery**.
- Counter-based triggers use `change()` to report a newly registered blackout, brownout, battery discharge or bad-input event.
- Load alerting is based on standardized RFC1628 `upsOutputPercentLoad` discovery prototypes. The private aggregate `vertiv.output.load` item does not drive triggers in the 1.5.0 candidate.
- No default battery-temperature trigger is present. On the homologation device, RFC1628 `upsBatteryTemperature` is unsupported and the Vertiv private battery-temperature object produced an invalid/sentinel-like value; both remain outside default production alerting.
- The dedicated `sysUpTime.0` heartbeat generates an availability alert after five minutes without data and an informational event when management-agent uptime decreases.
- RFC1628 diagnostic-test objects are read-only in this project; the two diagnostic-test triggers only observe the result summary and never start or abort a test.
- System-status and output-source triggers rely on value maps for readable Latest data values.
- SNMP trap event parsing is not enabled by default because event OID names do not by themselves define the exact trap payload sent by every management card.
