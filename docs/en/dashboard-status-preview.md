# Dashboard status-card preview

[Português (Brasil)](../pt-BR/dashboard-status-preview.md)

This provisional branch experiments with cleaner and more operational UPS status cards without changing SNMP collection, triggers, or the project version.

## What changes

- Status/value-map cards show only the mapped text (for example `Normal operation`, `Normal`, `Passed`, `External`, `8 weeks`).
- The raw numeric suffix normally rendered by the Item value widget is suppressed by showing a value-map-aware `{ITEM.LASTVALUE}` macro in the widget Description field.
- Numeric thresholds continue to use the original numeric item, so background colors can change dynamically.
- Pastel colors are used for readability: green = normal, yellow = attention, orange = alarm/degraded, red = critical, blue = informational/configuration.
- System status receives additional width in the Overview row.
- Active alarms, battery charge, and remaining runtime receive numeric threshold backgrounds.

This is a preview only. The main branch remains unchanged until the visual result is approved.
