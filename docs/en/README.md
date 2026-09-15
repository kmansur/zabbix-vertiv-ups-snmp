# Overview

[Português (Brasil)](../pt-BR/README.md)

`Vertiv by SNMP` is designed to provide practical, safe and transparent monitoring of Vertiv/Liebert UPS systems in Zabbix.

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

After the first import, compare Zabbix values with the UPS LCD/web interface and review unsupported items. This is particularly important for vendor-private objects. See [Electrical summary metrics](electrical-summary.md), [Compatibility matrix](compatibility.md) and [Troubleshooting](troubleshooting.md).

## Project version

Current repository version: **1.5.3**.

Latest stable release: **1.5.3**.

Release 1.5.1 adds the optional global-dashboard generator, bilingual documentation and tests without changing the 1.5.0 monitoring semantics. The maintainer successfully validated its `--dry-run` flow against a real Zabbix 7.0 environment. The replacement path has been hardened to update one editable same-name dashboard in place and fail closed on ambiguity.

The `main` branch is the active development branch. Production users should install a tagged GitHub Release rather than treating the current `main` tree as an immutable release artifact.

Version 1.5.0 passed repository validation, CodeQL, Zabbix 7.0 fresh import and the 1.4.1 → 1.5.0 in-place upgrade test. Extended controlled hardware scenarios remain tracked separately and are not represented as completed field certification.

See [Versioning](versioning.md), [Project status](project-status.md), [Global dashboard](global-dashboard.md), [PDCA review 1.5.1](pdca-1.5.1.md) and [CHANGELOG](../../CHANGELOG.md).

- [MIB/OID sources and provenance](mib-sources.md)
- [Compatibility matrix](compatibility.md)
- [Production readiness and homologation](production-readiness.md)

## Current release tracking

Repository candidate: **1.5.3**. Latest stable release: **1.5.3**. Release 1.5.2 is a licensing/attribution and metadata patch; monitoring semantics remain unchanged from 1.5.1.
