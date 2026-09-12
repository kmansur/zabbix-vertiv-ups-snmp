# Native dashboard

[Português (Brasil)](../pt-BR/dashboard.md)

The **Vertiv UPS Overview** template dashboard is imported together with the template and automatically follows the monitored host. The screenshots below were captured from a real Vertiv UPS running the v1.4.1 dashboard while the unit was in normal online operation. Values are examples only; voltage, load, runtime and temperature depend on the UPS model, battery system and connected load.

> **1.5.0 candidate note:** during homologation, the tested management card returned `noSuchObject` for RFC1628 `upsBatteryCurrent` and `upsBatteryTemperature`. Those two standard items are therefore disabled by default. The Battery temperature card visible in the 1.4.1 screenshot is replaced by **Battery status** in the 1.5.0 candidate; battery current continues to use the field-validated Vertiv private OID.

The dashboard is intentionally split into three pages:

- **Overview** — operational health, battery state, output power and phase load at a glance.
- **Electrical** — detailed input, output and bypass measurements plus cumulative power-quality counters.
- **Battery & Environment** — battery, runtime, test/configuration status and environmental temperature.

The dashboard uses only read-only monitoring items and graphs already provided by the template. It does not introduce SNMP write/control operations.

## Status-card colors

Status cards use soft background colors to make state changes visible without overwhelming the page:

- **Green** — normal/healthy state.
- **Yellow** — attention or non-normal state that should be reviewed.
- **Orange** — degraded condition or stronger warning.
- **Red** — critical/fault state.
- **Light blue / neutral** — informational or configuration value rather than a health state.

Mapped enum cards keep the native Zabbix value-map rendering, for example `Normal (3)` or `Passed (1)`. This preserves reliable numeric semantics for triggers and thresholds while still presenting a readable state label.

## Overview

![Vertiv UPS Overview dashboard](../images/dashboard-overview.png)

The Overview page is the first place to look during normal operation and during an incident. Its top row answers six questions immediately: Is the UPS healthy? Where is the load being powered from? Are alarms active? Is the battery healthy? Is it charged? How much runtime is estimated?

### System status, output source and alarms

- **System status** should normally remain green and show `Normal operation`.
- **Output source** should normally show `Normal`. A change to Battery or Bypass is operationally significant even if the load remains powered.
- **Active alarms** is the number of currently reported UPS-MIB alarms. Zero is the expected healthy state. In the 1.5.0 candidate, any positive value receives critical visual emphasis; count is not used to infer alarm severity.
- **Battery status** should normally show `Normal`.
- **Battery charge** is the estimated state of charge.
- **Runtime remaining** is a display-oriented conversion of the RFC1628 runtime value from minutes to hours. The raw item remains in minutes for trigger logic.

### Battery charge and runtime

This graph combines two different scales:

- **Left axis:** battery charge in percent.
- **Right axis:** estimated runtime in hours.

During normal utility operation with a fully charged battery, both lines may remain almost flat. During a real outage or battery test, charge and runtime should decrease as the UPS supplies the load.

How to read it:

- A gradual decline during battery operation is expected.
- A sudden runtime drop can be caused by a large increase in load or by the UPS recalculating its estimate.
- Falling runtime while charge still appears high can be meaningful because runtime is load-dependent, whereas charge is an energy-state estimate.
- Runtime is an estimate reported by the UPS, not a guaranteed autonomy figure. In the example screenshot, the device reports about 72 hours; that value comes from the UPS itself and should be interpreted in the context of its current load and battery configuration.

### Output power

The graph displays:

- **Output power (kW):** active/real power actually consumed by the load.
- **Output apparent power (kVA):** electrical capacity being demanded from the UPS.

Normally, apparent power is equal to or greater than active power. The gap between kW and kVA is related to the load power factor.

How to read it:

- A smooth trend reflects relatively stable IT/electrical load.
- Sudden upward steps normally indicate equipment being powered on or increased demand.
- Sudden downward steps may indicate load removal or an unexpected shutdown.
- A sustained rise toward the UPS capacity deserves attention even if no overload alarm has fired yet.
- A growing separation between kW and kVA can indicate a worsening aggregate power factor or a different load mix.

### Output phase load

This graph shows the output-load percentage for L1, L2 and L3.

How to read it:

- The three lines should remain reasonably close on a balanced three-phase installation.
- A short transient difference is common when equipment switches or cycles.
- A persistent separation between one phase and the others indicates load imbalance and should be investigated.
- A phase approaching the configured warning/critical load thresholds is more important than the total average alone.

The example screenshot shows all three phases in roughly the low-to-mid 20% range, which is a well-balanced operating condition.

## Electrical

![Vertiv UPS Electrical dashboard](../images/dashboard-electrical.png)

The Electrical page is intended for power-path validation and troubleshooting.

### Voltage cards

The dashboard presents representative line-to-neutral and line-to-line values for input, output and bypass:

- **Input L1-N / L1-L2** — utility/input voltage.
- **Output L1-N / L1-L2** — voltage delivered to the protected load.
- **Bypass L1-N / L1-L2** — alternate path voltage available to the UPS.

In a balanced three-phase system, line-to-line voltage is approximately √3 times line-to-neutral voltage. The sample values are consistent with that relationship. Large deviations between phases, sudden steps or an unavailable bypass voltage deserve investigation.

### Power and frequency cards

- **Output power** and **Output apparent power** provide an instantaneous summary of load demand.
- **Output frequency**, **Input frequency** and **Bypass frequency** should normally remain close to the site's nominal frequency.
- **Topology** shows the operating class reported by the Vertiv UPS; the sample unit reports `Online`.

A persistent input/output frequency difference, unstable input frequency or a bypass frequency outside the accepted range may explain transfer or bypass-availability events.

### Power-quality counters

The cards **Input blackouts**, **Input brownouts** and **Bad input lines** are cumulative counters. They are not current active alarms.

How to read them:

- `68` blackouts means the UPS has accumulated 68 blackout events over the counter's lifetime/reset interval; it does **not** mean 68 outages are currently active.
- Brownouts count input undervoltage/sag events as exposed by the device.
- Bad input lines comes from the UPS-MIB input-line-bad counter/state and should normally remain at zero on a healthy source.
- The most useful signal is often an **increase** in the counter. Compare the current value with its previous value when investigating a recent event.

These counters are shown as cards rather than trend graphs because plotting a cumulative counter often produces a mostly flat or stair-step line and can be misleading as an operational event view.

### Output phase load — full-width view

The full-width graph is the same L1/L2/L3 load view shown on Overview, but with more horizontal space for troubleshooting. Use it to compare phase behavior over a longer incident window and to identify persistent imbalance or phase-specific changes.

## Battery & Environment

![Vertiv UPS Battery and Environment dashboard](../images/dashboard-battery-environment.png)

This page concentrates battery health, test/configuration state and environmental temperature. The screenshot above is from v1.4.1; in the 1.5.0 candidate the old **Battery temperature** card is replaced by **Battery status** after field testing confirmed that the management card does not implement `upsBatteryTemperature`.

### Battery and status cards

- **Battery charge** — estimated charge percentage.
- **Runtime remaining** — estimated autonomy in hours for display purposes.
- **Battery current** — current into/out of the battery from the Vertiv private `...4149` OID, validated on the homologation device.
- **Battery status** — standardized RFC1628 `upsBatteryStatus`, supported by the tested card.
- **Inlet temperature** — UPS inlet/ambient-air temperature.
- **Battery test result** — most recent battery-test state.
- **Shutdown reason** — last/current shutdown reason reported by the device.
- **ECO mode** — ECO-mode state.
- **Battery cabinet** — detected/configured battery-cabinet type.
- **Battery test interval** — configured automatic test interval.
- **Battery discharges** — cumulative number of battery discharge events.

`Battery discharges` is a historical counter, not the number of batteries and not the number of currently active discharges.

### Battery current and temperature: real compatibility

The 1.5.0 candidate initially added RFC1628 `upsBatteryCurrent` and `upsBatteryTemperature` to improve portability. Homologation showed that the tested ITA-20kVA management card returns `No Such Object available on this agent at this OID` for both scalars.

The candidate's final policy is:

- `ups.battery.current` and `ups.battery.temperature` remain in the template but are **disabled by default**, trigger-free and absent from the dashboard;
- `vertiv.battery.current` (`...4149`) remains the displayed battery current because it works on the validated device;
- `vertiv.battery.temperature` (`...4156`) remains disabled because it returned approximately `-0.1 °C`, inconsistent with the observed environment;
- no default battery-temperature trigger exists until a supported and validated battery-temperature sensor/OID is available;
- default environmental monitoring uses **Inlet temperature**.

This prevents unsupported items and alerts based on an invalid sensor value while retaining compatibility for other cards that may implement the optional RFC1628 scalars.

### Inlet temperature

The graph shows only the inlet-air temperature, which is the useful environmental metric confirmed on the field-tested unit.

How to read it:

- Look at the numeric Y-axis before judging visual movement. Zabbix automatically scales the graph, so a change from 24 °C to 25 °C can look large even though it is only a 1 °C variation.
- A stable narrow band is normal.
- A sustained upward trend is more important than one isolated sample.
- Warning/critical lines in the graph come from the configured template triggers/macros; adapt them to the equipment room and manufacturer requirements rather than treating example defaults as universal environmental limits.

### Battery charge and runtime — focused view

The same dual-axis graph from Overview is repeated here so battery investigation does not require switching pages. Use the longer time range selector in Zabbix when analyzing a discharge, recharge cycle or battery test.

## Why there are no additional default graphs

Version 1.4.1 and the 1.5.0 candidate intentionally keep the default dashboard small. The current graphs answer the main operational questions without duplicating every numeric item as a trend.

Items such as input/output/bypass voltage and frequency are still retained in history and can be graphed from Latest data when investigating power-quality incidents. They are kept as cards in the default dashboard because, under normal operation, those values are usually stable and adding permanent graphs would increase visual noise.

The private Vertiv input-power phase OIDs are also not featured because their SNMP scaling has not yet been validated across devices/firmware. The project avoids presenting an apparently authoritative graph until that scale is confirmed in the field.

## Recommended reading order during an incident

1. Check **System status**, **Output source** and **Active alarms**.
2. Check **Battery status**, **Battery charge** and **Runtime remaining**.
3. Inspect **Output power** for a sudden load change.
4. Inspect **Output phase load** for overload or imbalance.
5. Open **Electrical** and compare input/output/bypass voltage and frequency.
6. Check whether blackout/brownout counters increased.
7. Open **Battery & Environment** and review battery current, inlet temperature, battery-test result and shutdown reason.
8. Expand the dashboard time range to include the period before and after the incident.

## Field-validation notes

The dashboard was field-tested with a Vertiv UPS/management card that returns private enum values as strings such as `Normal Operation`, `Online`, `Passed` and `External`. The template normalizes those responses to canonical numeric values so Zabbix value maps, triggers and colored cards remain consistent.

The same homologation confirmed that the agent implements UPS-MIB only partially: support for `upsBatteryStatus`, runtime and other RFC1628 objects does not imply support for `upsBatteryCurrent` or `upsBatteryTemperature`.

The raw RFC1628 runtime item remains authoritative for trigger calculations, while `ups.battery.runtime.hours` exists only to make the dashboard easier to read.
