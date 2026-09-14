# Configuration and macros

[Português (Brasil)](../pt-BR/configuration.md)

The template does not require custom scripts. All monitoring is performed through the host SNMP interface.

## User macros

| Macro | Default | Description |
| --- | --- | --- |
| {$UPS.RUNTIME.WARN} | 10 | Battery runtime warning threshold, minutes. |
| {$UPS.RUNTIME.CRIT} | 5 | Battery runtime critical threshold, minutes. |
| {$UPS.BATTERY.CHARGE.WARN} | 40 | Battery charge warning threshold, percent. Applied while UPS is on battery. |
| {$UPS.BATTERY.CHARGE.CRIT} | 20 | Battery charge critical threshold, percent. Applied while UPS is on battery. |
| {$UPS.LOAD.WARN} | 80 | Output-line load warning threshold, percent. Used by RFC1628 LLD trigger prototypes. |
| {$UPS.LOAD.CRIT} | 95 | Output-line load critical threshold, percent. Used by RFC1628 LLD trigger prototypes. |
| {$UPS.BATTERY.TEMP.WARN} | 35 | Reserved battery-temperature warning threshold. No default 1.5.0 production trigger currently uses it. |
| {$UPS.BATTERY.TEMP.CRIT} | 40 | Reserved battery-temperature critical threshold. No default 1.5.0 production trigger currently uses it. |
| {$UPS.INLET.TEMP.WARN} | 30 | UPS inlet air temperature warning threshold, degrees Celsius. |
| {$UPS.INLET.TEMP.CRIT} | 35 | UPS inlet air temperature critical threshold, degrees Celsius. |

The battery-temperature macros are intentionally retained for backward compatibility and future device profiles. They do **not** enable battery-temperature alerting by themselves. On the current homologation device, RFC1628 `upsBatteryTemperature` is unsupported and the private Vertiv battery-temperature value is not reliable enough for default production alerting.

## Recommended tuning workflow

1. Observe normal values for several days.
2. Confirm the expected UPS load under normal and degraded conditions.
3. Confirm the autonomy required by the site.
4. Adjust warning and critical battery-runtime limits.
5. Adjust inlet-temperature thresholds according to the UPS/environment design.
6. Override macros at host level when UPS models or battery banks differ.
7. Do not build battery-temperature alerting from the reserved macros until a trustworthy sensor/OID is confirmed on the target card/firmware.

## Threshold behavior

Battery runtime and battery charge triggers are evaluated only while `UPS: Output source` reports **Battery**. This prevents normal charging or maintenance states from generating low-battery incidents.

Load warning/critical triggers use RFC1628 output-line discovery (`upsOutputPercentLoad`). The private aggregate `vertiv.output.load` item does not drive default production triggers.

Inlet-temperature warning/critical triggers use non-overlapping ranges so the warning event does not remain active when the critical threshold is reached.

## SNMP credentials

Credentials are not stored in the template. Configure them on the Zabbix SNMP interface or through the standard Zabbix macro/credential strategy used in your environment.

Prefer SNMPv3 authentication and privacy when available.
