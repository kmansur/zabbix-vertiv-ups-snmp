# Compatibility matrix

[Português (Brasil)](../pt-BR/compatibility.md)

This matrix distinguishes **engineering compatibility** from **field homologation**. A template export can pass structural/import validation without proving every OID on every firmware. The 1.5.0 homologation uses real device behavior to define safe template defaults.

| UPS / card | Zabbix | Status | Notes |
| --- | --- | --- | --- |
| Vertiv `ITA-20k00AL3A02E00` (20 kVA), UPS firmware `V220` / `IS-UNITY-DP` card, firmware `8.5.1.0` (`IS-UNITY_8.5.1.0_00173`) | 7.0 | 1.5.0 homologation in progress | Core states, electrical values, enum strings and dashboard behavior were observed on real hardware. `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) and `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) return `noSuchObject` on this card/firmware. The exact Zabbix version still needs to be recorded. |
| Other Vertiv/Liebert UPS/card firmware | 7.0 | Compatible by RFC1628 design; not field-certified | UPS-MIB implementation can be partial. Optional standard objects must be confirmed on the target device; private OIDs must be compared with the local UPS UI. |
| Vertiv/Liebert | 8.0 development | Export/semantic parity only | Not a production support claim until a real 8.0 build is imported and run. |

## Field identification

The management card identified itself as vendor `Vertiv`, model `IS-UNITY-DP`, firmware `8.5.1.0`, build `IS-UNITY_8.5.1.0_00173`, with `sysObjectID` `.1.3.6.1.4.1.476.1.42`. The UPS reported model `ITA-20k00AL3A02E00` and firmware `V220`. Serial numbers are intentionally not published in this matrix.

## Field result — RFC1628 battery group

The management card used for homologation implements only part of the UPS-MIB battery group. Observed behavior:

- `upsBatteryStatus` (`.1.3.6.1.2.1.33.1.2.1.0`) — **supported**;
- `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) — **unsupported**, returns `No Such Object available on this agent at this OID`;
- `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) — **unsupported**, returns the same `noSuchObject` response.

Therefore, the 1.5.0 candidate retains the RFC1628 current and temperature objects only as optional items **disabled by default**. They do not participate in the production dashboard or triggers and should only be enabled on another card/firmware after support is confirmed.

On the validated device, battery current continues to use the Vertiv private OID `...1.2.1.4149` (`vertiv.battery.current`), which has been observed in the field. Private instance `...1.2.1.4156` returned `-0.1 °C`, inconsistent with the observed environment, so it remains disabled and has no production trigger. The same walk exposed a second instance, `...1.2.2.4156`, returning `31.8 °C`; this is physically plausible, but the physical identity of that second instance still needs to be confirmed in the UPS UI/LCD before it can be used as production battery temperature. The environmental graph continues to use only the validated inlet temperature.

This is an important compatibility rule: implementing parts of RFC1628 **does not imply that every UPS-MIB scalar is implemented** by an SNMP agent.

## Field result — private input power

Private OIDs `6318`, `6319`, and `6320` returned `1.6`, `1.5`, and `1.5`. At the same capture, input voltage/current/power-factor values (`209.3 V / 7.9 A / 0.99`, `212.7 V / 7.6 A / 0.99`, `209.5 V / 7.5 A / 0.99`) imply approximately `4.8 kW` total input power, while the three private objects sum to `4.6`. This is strong evidence that these objects are expressed in **kW per phase**, not watts, but direct confirmation against the UPS LCD/web UI is still required before enabling them by default.

## Field result — events and alarms

With the UPS in normal state, `upsAlarmsPresent` returned `0` and `upsAlarmTable` contained no rows, which is the expected behavior. The observed private `.2.100.*` event objects returned the text `Inactive Event`, confirming the inactive-state encoding for this card/firmware. The text/encoding of the **active** state still needs to be captured during a real event before private event-specific triggers can be implemented.

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
