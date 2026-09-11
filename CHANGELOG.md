# Changelog

**English** | [Português (Brasil)](CHANGELOG.pt-BR.md)

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- Validate additional Vertiv/Liebert UPS models and management-card firmware.
- Add event-specific SNMP trap processing after real trap payloads are captured and documented.
- Revalidate the Zabbix 8.0 export against RC/final builds.

## [1.0.0] - 2026-09-10

### Added

- Initial maintained release of **VERTIV by SNMP**.
- Zabbix 7.0 versioned template export.
- Zabbix 8.0 compatibility export.
- Standard RFC 1628 UPS-MIB monitoring for battery, input, output, bypass and nominal configuration.
- Vertiv/Liebert enterprise monitoring for system status, battery details, power quality, energy, temperatures and identification.
- LLD for input, output and bypass line tables.
- Configurable macros for runtime, charge, load and temperature thresholds.
- Value maps for major UPS and Vertiv status fields.
- Four built-in graphs for battery/runtime, temperatures, output power and power-quality counters.
- Optional disabled Vertiv enterprise SNMP trap item.
- Bilingual English/Brazilian Portuguese documentation.
- Template/documentation validators, tests and GitHub Actions CI.
- Release and CodeQL workflows.
- MIT licensing for original repository contributions.
- Explicit attribution to the historical `Template Vertiv` reference by Mihguel da Silva Santos Tavares de Araujo.

### Changed from the historical reference

- Reworked the monitoring model from the original `1.3.6.1.4.1.6302...` rectifier-oriented structure to UPS-focused RFC 1628 and Vertiv/Liebert `1.3.6.1.4.1.476.1.42` objects.
- Replaced fixed battery percentage alarms with context-aware runtime/charge triggers evaluated while the UPS is on battery.
- Replaced hard-coded phase assumptions with LLD.
- Removed unrelated macros/value maps and write/control operations.
