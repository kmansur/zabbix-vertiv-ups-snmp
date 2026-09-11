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
| {$UPS.LOAD.WARN} | 80 | UPS load warning threshold, percent. |
| {$UPS.LOAD.CRIT} | 95 | UPS load critical threshold, percent. |
| {$UPS.BATTERY.TEMP.WARN} | 35 | Battery temperature warning threshold, degrees Celsius. |
| {$UPS.BATTERY.TEMP.CRIT} | 40 | Battery temperature critical threshold, degrees Celsius. |
| {$UPS.INLET.TEMP.WARN} | 30 | UPS inlet air temperature warning threshold, degrees Celsius. |
| {$UPS.INLET.TEMP.CRIT} | 35 | UPS inlet air temperature critical threshold, degrees Celsius. |

## Recommended tuning workflow

1. Observe normal values for several days.
2. Confirm the expected UPS load under normal and degraded conditions.
3. Confirm the autonomy required by the site.
4. Adjust warning and critical battery-runtime limits.
5. Adjust temperature thresholds according to the battery/UPS manufacturer's operating limits and the room design.
6. Override macros at host level when UPS models or battery banks differ.

## Threshold behavior

Battery runtime and battery charge triggers are evaluated only while `UPS: Output source` reports **Battery**. This prevents normal charging or maintenance states from generating low-battery incidents.

Load and temperature warning triggers use non-overlapping ranges so the warning event does not remain active when the critical threshold is reached.

## SNMP credentials

Credentials are not stored in the template. Configure them on the Zabbix SNMP interface or through the standard Zabbix macro/credential strategy used in your environment.

Prefer SNMPv3 authentication and privacy when available.
