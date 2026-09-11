# Native dashboard

[Português (Brasil)](../pt-BR/dashboard.md)

Version 1.2.0 adds the **VERTIV UPS Overview** template dashboard. It is imported together with the template and automatically follows the monitored host.

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

