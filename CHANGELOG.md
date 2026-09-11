# Changelog

**English** | [Português (Brasil)](CHANGELOG.pt-BR.md)

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Planned

- Validate additional Vertiv/Liebert UPS models and management-card firmware.
- Add event-specific SNMP trap processing after real trap payloads are captured and documented.
- Revalidate the Zabbix 8.0 export against RC/final builds.

## [1.4.0] - 2026-09-11

### Added

- Project maturity/status documentation with an explicit **85%** engineering-maturity score and remaining validation work.
- Dependency monitoring for Python packages in addition to GitHub Actions.
- Repository hygiene tests for release packaging and workflow baselines.

### Changed

- Visible template name changed to **Vertiv by SNMP**. The technical template identifier remains `VERTIV by SNMP` intentionally so existing installations can update in place without creating a duplicate template.
- Native dashboard renamed to **Vertiv UPS Overview**.
- Finalized severity-colored status cards using native value-map rendering and zero decimal places for compact mapped enum values.
- Updated GitHub Actions checkout/setup-python actions to v7.
- Private input-power values remain available for troubleshooting but are no longer featured in the dashboard until their vendor-specific scale is validated.

### Fixed

- Aligned the template validator with the finalized dashboard typography/color configuration.
- Removed stale preview-only macro-rendering text from template metadata.
- Release packaging now uses unique Zabbix 7.0/8.0 asset filenames, includes the synoptic-map generator/tools, and publishes SHA-256 checksums.
- Removed preview-only dashboard documentation from the finalized project.

## [1.3.3] - 2026-09-11

### Changed

- Tuned dashboard card value sizes to prevent truncation.
- Mapped/status values use 24%; numeric values use 27%.
- Decimal and unit sizes use 16%.
- Removed change indicators from compact cards, preserving space for values such as `Normal operation`, `External` and `8 weeks`.
- Kept layout, graphs, items, triggers and SNMP collection functionally unchanged.

## [1.3.2] - 2026-09-11

### Fixed

- Normalize Vertiv private enums that some management cards return as SNMP `STRING` values instead of numeric enums.
- The ten affected status/configuration items now accept both the textual representation returned by the card and the canonical numeric enum.
- Numeric item types, value maps and numeric trigger expressions are preserved for compatibility across different cards/firmware.
- Live mappings validated on real hardware for `Normal Operation`, `on`, `off`, `Online`, `None`, `fully charged`, `Passed`, `disabled`, `8 weeks` and `External`.
- Repository validation now requires enum-normalization preprocessing on these items.

## [1.3.1] - 2026-09-11

### Fixed

- Fixed the native template dashboard UUID to a valid RFC 4122 UUID version 4, as required by Zabbix 7.0 template import validation.
- Strengthened repository validation so every exported `uuid` must be a UUIDv4, preventing recurrence of the import error `UUIDv4 is expected`.

## [1.3.0] - 2026-09-11

### Added

- Optional Zabbix network-map synoptic generator for one Vertiv UPS host.
- Embedded normal/problem UPS icons in the generated YAML.
- Input, bypass, output and battery schematic blocks with dynamic highlighting of the central host element.
- Automated tests for map format, host references and embedded PNG images.
- Bilingual map generation/import documentation.

### Safety / compatibility

- The map adds no SNMP write/control OIDs.
- The referenced host must already exist before map import.
- Peripheral blocks remain static to avoid fabricating unsupported dynamic item-to-shape bindings.

## [1.2.0] - 2026-09-11

### Added

- Native **Vertiv UPS Overview** template dashboard.
- Overview, Electrical and Battery & Environment pages.
- Status cards for UPS state, output source, alarms, battery charge/runtime and key electrical values.
- Dashboard integration with all six built-in template graphs.
- Bilingual dashboard documentation.

## [1.1.0] - 2026-09-11

### Added

- RFC 1628 output-frequency item with the standard `0.1 Hz` scaling.
- Fixed dashboard-ready Vertiv input, output and bypass L-N/L-L voltage items.
- Fixed per-phase input current, power factor and real-power items.
- Fixed per-phase output current, power factor, percent load, real power and apparent power items.
- Calculated total input power from the three Vertiv phase-power values.
- Battery cabinet type and automatic battery-test interval value maps/items.
- Input phase-power and output phase-load graphs.
- Bilingual electrical-summary documentation.

### Safety / validation

- No guessed multiplier is applied to newly added Vertiv private electrical OIDs because the supplied SNMP parameter list does not define their numeric scale.
- Vertiv `.2.100.*` condition OIDs remain intentionally excluded from active polling/triggers until their returned state encoding is validated on real hardware.
- No SNMP write/control OIDs were added.

## [1.0.0] - 2026-09-10

### Added

- Initial maintained release of **Vertiv by SNMP**.
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
