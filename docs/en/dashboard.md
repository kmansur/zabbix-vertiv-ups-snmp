# Native dashboard

[Português (Brasil)](../pt-BR/dashboard.md)

Version 1.2.0 adds the **Vertiv UPS Overview** template dashboard. It is imported together with the template and automatically follows the monitored host.

## Pages

- **Overview** — system status, output source, active alarms, battery status/charge/runtime and all six built-in trend graphs.
- **Electrical** — fixed input, output and bypass summary values plus phase-power and phase-load graphs.
- **Battery & Environment** — battery, runtime, temperatures, test/status metadata and battery/environment trends.

The dashboard uses only template items and graphs already validated by the repository. No write/control OIDs are introduced.

## Card typography

Version 1.3.3 refines **Item value** widgets for better readability in compact cards:

- mapped/status values: 24% value size;
- numeric values: 27% value size;
- decimals and units: 16% size;
- values centered horizontally and vertically;
- change indicators removed from cards to avoid truncating mapped values.

The widget title continues to identify each metric, so the card only needs to display the value and preserves more usable space. Graphs, items, triggers and SNMP collection are unchanged by this adjustment.


## Version 1.4.0 status-card behavior

The finalized dashboard uses the native mapped **Item value** rendering for status cards. This keeps Zabbix value maps reliable across frontends while dynamic thresholds color the card background. Enum/status cards use zero decimal places, so mapped values render with compact raw suffixes such as `Normal (3)` instead of `Normal (3.00)`.

Severity colors use soft backgrounds: green for normal, yellow for attention, orange for degraded/alarm states and red for critical states. Static informational/configuration cards use a neutral or light-blue background.

The private calculated input-power card and input-phase-power graph are intentionally not featured on the dashboard because the supplied Vertiv SNMP documentation does not define the scale of those private OIDs. The underlying items remain available for field validation and troubleshooting.


## Field refinements in version 1.4.1

The **Overview** page uses three primary graphs in one row: battery charge/runtime, output power and output phase load. The cumulative-counter graph was removed from the dashboard because cumulative lines are not a useful operational event visualization.

The **Electrical** page shows blackout, brownout and bad-line values as counter cards and gives the output phase-load graph the full page width. **Battery & Environment** displays runtime in hours and uses a dedicated inlet-temperature graph.

The raw `ups.battery.runtime` item remains in minutes to preserve RFC1628 semantics and trigger behavior. The calculated `ups.battery.runtime.hours` item is presentation-only. Private battery temperature remains available in Latest data and in the legacy `UPS: Temperatures` graph, but is not used by the default environmental graph because some firmware can expose non-physical/sentinel-like values when no useful battery-temperature sensor is present.
