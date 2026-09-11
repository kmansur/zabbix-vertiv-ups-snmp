# Dashboard status-card preview

[Português (Brasil)](../pt-BR/dashboard-status-preview.md)

This provisional branch keeps the dynamic pastel backgrounds and returns status cards to the native **Item value** rendering after the description-macro experiment proved unreliable on the tested Zabbix 7 frontend.

## Current preview behavior

- Status cards keep dynamic green/yellow/orange/red backgrounds based on the original numeric item and thresholds.
- Status text is rendered natively through the existing value map.
- Status/enum cards use zero decimal places, so mapped values render with a shorter raw suffix such as `(1)` instead of `(1.00)`.
- Long cards retain the widened layout introduced by the previous preview.
- Active alarms are rendered as an integer.
- Battery charge and runtime keep their dynamic severity backgrounds.

## Confirmed limitation

The attempt to strip the parenthesized numeric suffix by rendering a macro/regular expression in the widget Description field produced broken strings such as `\1`, `\3`, and `\0` on the tested Zabbix 7 frontend. This branch intentionally removes that experiment.

The main branch remains unchanged while this visual behavior is evaluated.
