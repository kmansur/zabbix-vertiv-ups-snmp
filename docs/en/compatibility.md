# Compatibility matrix

[Português (Brasil)](../pt-BR/compatibility.md)

This matrix distinguishes **engineering compatibility** from **field homologation**. A template export can pass structural/import validation without proving every OID on every firmware. Release 1.5.0 uses real device behavior to define safe defaults, while extended controlled field scenarios remain in progress for the reference hardware.

| UPS / card | Zabbix | Status | Notes |
| --- | --- | --- | --- |
| Vertiv `ITA-20k00AL3A02E00` (20 kVA), UPS firmware `V220` / `IS-UNITY-DP` card, firmware `8.5.1.0` (`IS-UNITY_8.5.1.0_00173`) | 7.0.30 | 1.5.0 released; extended field validation in progress | Core states, electrical values, enum strings and dashboard behavior were observed on real hardware. `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) and `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) return `noSuchObject` on this card/firmware. |
| Other Vertiv/Liebert UPS/card firmware | 7.0 | Compatible by RFC1628 design; not field-certified | UPS-MIB implementation can be partial. Optional standard objects must be confirmed on the target device; private OIDs must be compared with the local UPS UI. |
| Vertiv/Liebert | 8.0 development | Export/semantic parity only | Not a production support claim until a real 8.0 build is imported and run. |

## Field identification

The management card identified itself as vendor `Vertiv`, model `IS-UNITY-DP`, firmware `8.5.1.0`, build `IS-UNITY_8.5.1.0_00173`, with `sysObjectID` `.1.3.6.1.4.1.476.1.42`. The UPS reported model `ITA-20k00AL3A02E00` and firmware `V220`. The reference environment runs **Zabbix Server 7.0.30**. `sysName.0` returned `nobreak-01`, while the UPS-specific name objects returned zero-filled placeholders; therefore inventory `NAME` uses `sysName.0` as the reliable source. Serial numbers are intentionally not published in this matrix.

## Field result — RFC1628 coverage

A complete walk of `1.3.6.1.2.1.33` confirmed working support for the standard identification, partial battery, input, output, bypass, alarm, test-result and configuration groups. Release 1.5.0 uses read-only objects only; the control/configuration groups exposed by the agent are not used for writes.

Observed standard electrical values include three input/output phases, `59.9 Hz`, output load `23/23/24 %`, per-phase output true power `1450/1410/1520 W`, and per-phase input true power `1600/1500/1500 W`. These values are consistent with the Vertiv private objects observed on the same device.

## Field result — RFC1628 battery group

The management card used as the reference device implements only part of the UPS-MIB battery group. Observed behavior:

- `upsBatteryStatus` (`.1.3.6.1.2.1.33.1.2.1.0`) — **supported**;
- `upsEstimatedMinutesRemaining` — **supported**, returning `4320 min` (`72 h`);
- `upsEstimatedChargeRemaining` — **supported**, returning `100 %`;
- `upsBatteryVoltage` — **supported**, returning `5440` tenths of a volt, equivalent to `544.0 V`;
- `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) — **unsupported**, returns `No Such Object available on this agent at this OID`;
- `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) — **unsupported**, returns the same `noSuchObject` response.

Therefore, release 1.5.0 retains the RFC1628 current and temperature objects only as optional items **disabled by default**. They do not participate in the production dashboard or triggers and should only be enabled on another card/firmware after support is confirmed.

On the validated device, battery current continues to use the Vertiv private OID `...1.2.1.4149` (`vertiv.battery.current`), which has been observed in the field. Private temperature `...1.2.1.4156` returned `-0.1 °C` and remains disabled and trigger-free because it is inconsistent with the observed environment. The walk also exposed `...1.2.2.4156 = 31.8` and `...1.2.2.4291 = 73`. These values **are not additional sensors**: they are the Fahrenheit representation of the same Celsius values from `.2.1` (`-0.1 °C = 31.8 °F` and `23 °C ≈ 73 °F`). Therefore there is no evidence of a second valid battery-temperature sensor in this tree. The environmental graph continues to use only the validated inlet temperature.

This is an important compatibility rule: implementing parts of RFC1628 **does not imply that every UPS-MIB scalar is implemented** by an SNMP agent.

## Field result — input power

The scaling of private OIDs `6318`, `6319`, and `6320` is characterized for this card/firmware. They returned `1.6`, `1.5`, and `1.5`, while the standard RFC1628 `upsInputTruePower` objects on the same device returned `1600`, `1500`, and `1500 W`. Therefore, on IS-UNITY-DP 8.5.1.0 these private objects represent **kW per phase**.

Because UPS-MIB already provides standardized input true power in watts and is supported by this device, the production path remains `upsInputTruePower` through LLD. Private OIDs `6318-6320` remain disabled by default because they are redundant and less portable across models/firmwares.

## Field result — events, alarms and tests

With the UPS in normal state, `upsAlarmsPresent` returned `0` and `upsAlarmTable` contained no rows, which is the expected behavior. The observed private `.2.100.*` event objects returned the text `Inactive Event`, confirming the inactive-state encoding for this card/firmware. The text/encoding of the **active** state still needs to be captured during a real event before private event-specific triggers can be implemented.

The RFC1628 test group is also present and returned identification/result/time objects. The template uses these objects for read-only observation only and includes no command to start tests.

## Field-validation status

Release 1.5.0 is a stable software release, but the reference hardware combination remains under extended field validation. The remaining controlled alarm, availability, diagnostic-transition and operator-signoff checks are tracked in [the 1.5.0 field validation record](homologation-1.5.0.md). Until those checks are complete, this matrix intentionally avoids the wording **field-homologated** for the reference hardware.

For every newly certified device, record:

- UPS model and rated capacity;
- management-card model;
- UPS firmware and management-card firmware;
- Zabbix exact version;
- SNMP version/security level;
- actual support for RFC1628 identification, battery, alarm-table and test-result objects;
- comparison of displayed private values with the UPS LCD/web UI;
- observed enum/trap variants.
