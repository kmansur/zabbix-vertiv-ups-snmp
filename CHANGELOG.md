# Changelog

**English** | [Português (Brasil)](CHANGELOG.pt-BR.md)

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [1.5.1] - 2026-09-14

Released repository version: **1.5.1**.

### Added

- Global dashboard generator `tools/create_global_dashboard.py` that recreates the native `Vertiv UPS Overview` template dashboard as a host-bound global Zabbix dashboard through the API.
- Automatic Zabbix major/minor detection and matching source selection from `templates/<major.minor>/vertiv-by-snmp.yaml`.
- Host item/graph reference resolution, `--dry-run`, private/public dashboard creation, custom names, explicit `--replace` behavior and controlled `--insecure` TLS mode.
- Bilingual EN/PT-BR deployment documentation for the global dashboard workflow.
- Automated tests covering Zabbix 7.0/8.0 dashboard source exports, item/graph conversion and layout/scalar field preservation.

### Changed

- Repository candidate version advanced from `1.5.0` to `1.5.1` for the global-dashboard tooling/documentation patch.
- `STABLE_VERSION` remains `1.5.0` until the 1.5.1 release is explicitly promoted/tagged.
- The template dashboard remains the single source of truth; the project does not maintain a second hand-written global dashboard definition.

### Validated

- The maintainer successfully executed the generator in `--dry-run` mode against a real Zabbix 7.0 environment and confirmed host/template discovery and payload generation.

### Planned

- Complete the post-release controlled field-validation scenarios and operator sign-off for the reference ITA-20kVA / IS-UNITY-DP environment.
- Protect `main` with an enforced GitHub ruleset requiring CI/import/security checks.
- Validate additional Vertiv/Liebert UPS models and management-card firmware.
- Add event-specific SNMP trap processing after real trap payloads are captured and documented.
- Revalidate the Zabbix 8.0 export against RC/final builds.

## [1.5.0] - 2026-09-14

### Added

- Dedicated SNMP heartbeat via `sysUpTime.0`, `nodata(5m)` availability trigger and management-agent uptime reset notice.
- RFC1628 identification, optional standardized battery current/temperature objects and read-only diagnostic-test result objects.
- RFC1628 diagnostic-result warning/failure triggers; the template does not start or abort tests.
- `upsAlarmTable` discovery with a value map for all 24 RFC1628 well-known alarms.
- MIB/OID provenance, compatibility matrix and a bilingual 1.5.0 field-validation record.
- Production-specific validator and real Zabbix 7 API-import CI test.
- `STABLE_VERSION` release marker, separate from the repository `VERSION` marker.

### Changed

- Documentation validation now checks bilingual document coverage, candidate/stable version references, trigger-table parity, macro parity, local links and branch/release policy against the Zabbix 7.0 export.
- Project readiness reporting now uses explicit PASS / IN PROGRESS / BLOCKED-or-approved gates instead of a percentage.
- Release workflow requires both `VERSION` and `STABLE_VERSION` to match the published tag.
- RFC1628 `upsBatteryCurrent` and `upsBatteryTemperature` are retained for compatible devices but remain disabled and trigger-free by default because the reference card returns `noSuchObject`.
- No default battery-temperature trigger is active in 1.5.0; the private temperature object is also disabled after field-invalid/sentinel-like behavior.
- Load alerting uses RFC1628 `upsOutputPercentLoad` prototypes; the private aggregate load no longer generates triggers.
- The active-alarm card turns red for any positive count instead of implying severity from the number of alarms.
- `main` is explicitly documented as the development branch; production consumers are directed to tagged GitHub Releases.

### Fixed

- Removed stale documentation claiming default battery-temperature triggers in 1.5.0.
- Removed stale documentation claiming private aggregate `vertiv.output.load` drives load triggers.
- Added the two RFC1628 diagnostic-result triggers and the SNMP heartbeat/restart triggers to the documented trigger set.
- Corrected the obsolete `templates/zabbix-<major.minor>/` contribution path.
- Corrected homologation-record links to the actual EN/PT-BR versioned files.
- Clarified that battery-temperature macros are retained/reserved but do not enable default production alerting.
- Removed wording that could incorrectly imply completed field homologation of the reference management card.

### Safety / reliability

- Private input-power and private battery-temperature metrics are disabled by default.
- Legacy graphs based on experimental metrics/cumulative counters were removed.
- No control/write or test-start OIDs were added.
- CodeQL, Python 3.9/3.13/3.14 tests, documentation/template/production validators and the Zabbix 7.0 import/upgrade path were required before release promotion.

### Release decision

- Maintainer approved `v1.5.0` for release on 2026-09-14 after repository validation, CodeQL, a real Zabbix 7.0 fresh import and an in-place `1.4.1 → 1.5.0` upgrade passed.
- Controlled hardware alarm/availability/diagnostic-transition checks remain open as post-release field validation. Release 1.5.0 is not described as fully field-homologated for the reference hardware until those checks are complete.

## [1.4.1] - 2026-09-11

### Fixed

- Reflowed the dashboard after removing unvalidated private input-power metrics, eliminating large empty regions.
- Runtime is displayed in hours through a presentation calculated item while the original RFC1628 minutes item remains authoritative for triggers and troubleshooting.
- The battery graph now uses hours, avoiding the frontend `Kmin` representation.
- Cumulative blackout, brownout and bad-line counters are no longer used as a dashboard trend graph and are shown as numeric cards on the Electrical page.
- The default environment graph now shows inlet temperature only; private battery temperature remains collected and available without distorting the default graph when the management card reports sentinel-like values such as `-0.1 °C`.
- Output phase load now spans the Electrical page and electrical cards were reflowed.
- Discharge/event counters are displayed without decimal places.

### Field note

On the validated Vertiv ITA-20kVA device, the UPS web interface itself reports `4320 min` runtime and `-0.1 °C` battery temperature. Version 1.4.1 does not rewrite those source values; it converts runtime to hours for presentation and keeps the private battery-temperature value out of the default environmental trend.

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
- Template/documentation validators, tests and CI in GitHub Actions.
- Release and CodeQL workflows.
- MIT licensing for original repository contributions.
- Explicit attribution to the historical `Template Vertiv` reference by Mihguel da Silva Santos Tavares de Araujo.

### Changed from the historical reference

- Reworked the monitoring model from the original `1.3.6.1.4.1.6302...` rectifier-oriented structure to UPS-focused RFC 1628 and Vertiv/Liebert `1.3.6.1.4.1.476.1.42` objects.
- Replaced fixed battery percentage alarms with context-aware runtime/charge triggers evaluated while the UPS is on battery.
- Replaced hard-coded phase assumptions with LLD.
- Removed unrelated macros/value maps and write/control operations.
