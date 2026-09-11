# Overview

[Português (Brasil)](../pt-BR/README.md)

`VERTIV by SNMP` is designed to provide practical, safe and transparent monitoring of Vertiv/Liebert UPS systems in Zabbix.

The template uses two SNMP namespaces:

- **RFC 1628 UPS-MIB** — `1.3.6.1.2.1.33`, used for standardized UPS measurements and line tables;
- **Vertiv/Liebert enterprise MIB** — `1.3.6.1.4.1.476.1.42`, used for vendor-specific status, identification, battery, environmental and detailed electrical metrics.

## Design goals

1. **Read-only monitoring.** No reboot, shutdown, outlet control or configuration write OIDs are included.
2. **Portable electrical monitoring.** Standardized UPS-MIB objects are preferred when they provide clearly defined units and semantics.
3. **Vendor detail where useful.** Vertiv-specific OIDs add system status, self-test, battery charge state, energy, environmental, power-quality and fixed phase-summary metrics.
4. **Dynamic line discovery plus deterministic summaries.** LLD remains available for portability, while fixed L-N/L-L and per-phase keys make dashboards predictable.
5. **No fabricated scaling.** Private OIDs with undocumented SNMP scaling are stored without guessed multipliers and must be compared with the UPS UI.
6. **Safe defaults.** Trigger thresholds are exposed as user macros and can be overridden per template, host group or host.
7. **Traceable maintenance.** Zabbix 7.0 and 8.0 exports are versioned separately but validated for semantic parity.

## Important compatibility note

Vertiv/Liebert products and management cards can expose different subsets of the enterprise MIB. An item being unsupported does not automatically mean the template is wrong; the device may not implement that OID.

After the first import, compare Zabbix values with the UPS LCD/web interface and review unsupported items. This is particularly important for the private electrical summary objects added in 1.1.0. See [Electrical summary metrics](electrical-summary.md) and [Troubleshooting](troubleshooting.md).

## Project version

Current version: **1.1.0**.

See [Versioning](versioning.md) and [CHANGELOG](../../CHANGELOG.md).
