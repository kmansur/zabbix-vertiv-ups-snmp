# Electrical summary metrics

[Português (Brasil)](../pt-BR/electrical-summary.md)

Version **1.1.0** adds fixed, dashboard-ready electrical summary items while keeping the RFC 1628 low-level discovery rules. The fixed keys are intended for predictable dashboards, troubleshooting views and comparisons with the UPS web/LCD summary screen.

## Scaling policy

RFC 1628 objects use the standard scaling defined by UPS-MIB. For example, `upsOutputFrequency` is reported in tenths of hertz and the template applies a `0.1` multiplier.

The supplied Vertiv SNMP parameter list identifies the private electrical objects but does **not** define the numeric scale for every `1.3.6.1.4.1.476.1.42...` object. The template therefore does not guess multipliers for these private items. Compare them with the UPS LCD/web interface before creating thresholds or dashboards that depend on their absolute values.

This is deliberate: the supplied Modbus map contains scaling information for Modbus registers, but that does not prove that the SNMP representation uses the same raw scale.

## Standard output frequency

| Item key | OID | Unit | Notes |
| --- | --- | --- | --- |
| `ups.output.frequency` | `1.3.6.1.2.1.33.1.4.2.0` | Hz | RFC 1628, multiplier `0.1` |

## Input summary

| Item key family | Measurement / OIDs |
| --- | --- |
| `vertiv.input.voltage.l1n/l12/l2n/l23/l3n/l31` | L-N/L-L voltage, OIDs `4096`-`4101` |
| `vertiv.input.frequency` | System input frequency, OID `4105` |
| `vertiv.input.current.l1/.l2/.l3` | Current, OIDs `4113`-`4115` |
| `vertiv.input.pf.l1/.l2/.l3` | Power factor, OIDs `4116`-`4118` |
| `vertiv.input.power.l1/.l2/.l3` | Real power, OIDs `6318`-`6320` |
| `vertiv.input.power.total` | Calculated sum of the three input phase-power items |

## Bypass summary

`vertiv.bypass.voltage.l12/.l23/.l31/.l1n/.l2n/.l3n` maps to Vertiv OIDs `4125`-`4130`. The existing RFC 1628 `ups.bypass.frequency` remains the primary fixed bypass-frequency metric.

## Output summary

| Item key family | Measurement / OIDs |
| --- | --- |
| `vertiv.output.voltage.l12/.l23/.l31` | L-L voltage, OIDs `4201`-`4203` |
| `vertiv.output.voltage.l1n/.l2n/.l3n` | L-N voltage, OIDs `4385`-`4387` |
| `vertiv.output.current.l1/.l2/.l3` | Current, OIDs `4204`-`4206` |
| `vertiv.output.pf.l1/.l2/.l3` | Power factor, OIDs `4210`-`4212` |
| `vertiv.output.load.l1/.l2/.l3` | Percent power/load, OIDs `4223`-`4225` |
| `vertiv.output.power.l1/.l2/.l3` | Real power, OIDs `5859`, `5860`, `5959` |
| `vertiv.output.apparent.power.l1/.l2/.l3` | Apparent power, OIDs `5868`-`5870` |

The complete private prefix for the numeric IDs above is `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1`.

These fixed items intentionally coexist with RFC 1628 LLD items. LLD remains useful for portability and automatic line discovery; fixed private keys provide deterministic names for dashboards and model-specific electrical analysis.

## Battery metadata added in 1.1.0

| Item key | OID | Values |
| --- | --- | --- |
| `vertiv.battery.cabinet.type` | `...2.1.6183` | Internal, External, LRT |
| `vertiv.battery.test.interval` | `...2.1.5805` | 8, 12, 16, 20 or 26 weeks |

## Production graphs

- **UPS: Output phase load**.

The private **UPS: Input phase power** graph is removed from the 1.5.0 candidate because its source OIDs still lack a verified SNMP scale. The private input-power items are disabled by default.

## Event-condition OIDs: identified but not activated

The supplied Vertiv files identify useful condition objects under the private `.2.100.*` branch, including battery low/discharging, bypass unavailable, output off, inverter failure, fan failure, charger failure, replace battery, output overload and input wiring fault.

However, the supplied files do not define the numeric state encoding returned when those objects are polled. Version 1.1.0 therefore does **not** fabricate `0/1`, `3/6` or any other event-state interpretation and does not create event-specific polling triggers for them.

For the next validation step, query a representative UPS while normal and, where safely possible, while a known condition is active. Once the returned states are confirmed, those event OIDs can be promoted to supported items and triggers.

## Known scale limitation

The private Vertiv input-power OIDs (`6318`-`6320`) are retained for troubleshooting, but their numeric scale is not defined by the supplied SNMP parameter list. On the currently tested device, the calculated total did not match the expected magnitude from the UPS web interface. For that reason the input-power card/graph is not featured in the native dashboard and no trigger should rely on these values until the scale is confirmed on the target firmware.
