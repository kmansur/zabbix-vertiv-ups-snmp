# Compatibility matrix

[Português (Brasil)](../pt-BR/compatibility.md)

This matrix distinguishes **engineering compatibility** from **field homologation**. A template export can pass structural/import validation without proving every OID on every firmware. The 1.5.0 homologation uses real device behavior to define safe template defaults.

| UPS / card | Zabbix | Status | Notes |
| --- | --- | --- | --- |
| Vertiv ITA-20kVA / management card used during development | 7.0 | 1.5.0 homologation in progress | Core states, electrical values, enum strings and dashboard behavior were observed on real hardware. `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) and `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) return `noSuchObject` on this card/firmware. Exact management-card model/firmware still needs to be recorded. |
| Other Vertiv/Liebert UPS/card firmware | 7.0 | Compatible by RFC1628 design; not field-certified | UPS-MIB implementation can be partial. Optional standard objects must be confirmed on the target device; private OIDs must be compared with the local UPS UI. |
| Vertiv/Liebert | 8.0 development | Export/semantic parity only | Not a production support claim until a real 8.0 build is imported and run. |

## Field result — RFC1628 battery group

The management card used for homologation implements only part of the UPS-MIB battery group. Observed behavior:

- `upsBatteryStatus` (`.1.3.6.1.2.1.33.1.2.1.0`) — **supported**;
- `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) — **unsupported**, returns `No Such Object available on this agent at this OID`;
- `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) — **unsupported**, returns the same `noSuchObject` response.

Therefore, the 1.5.0 candidate retains the RFC1628 current and temperature objects only as optional items **disabled by default**. They do not participate in the production dashboard or triggers and should only be enabled on another card/firmware after support is confirmed.

On the validated device, battery current continues to use the Vertiv private OID `...1.2.1.4149` (`vertiv.battery.current`), which has been observed in the field. The Vertiv private battery-temperature object `...4156` returned approximately `-0.1 °C`, inconsistent with the observed environment, so it also remains disabled and has no production trigger. The environmental graph uses only the validated inlet temperature.

This is an important compatibility rule: implementing parts of RFC1628 **does not imply that every UPS-MIB scalar is implemented** by an SNMP agent.

## Homologation record

For every newly certified device, record:

- UPS model and rated capacity;
- management-card model;
- UPS firmware and management-card firmware;
- Zabbix exact version;
- SNMP version/security level;
- actual support for RFC1628 identification, battery, alarm-table and test-result objects;
- comparison of displayed private values with the UPS LCD/web UI;
- observed enum/trap variants.
