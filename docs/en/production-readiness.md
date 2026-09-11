# Production readiness and homologation

[Português (Brasil)](../pt-BR/production-readiness.md)

Version 1.5.0 is designed to enter field homologation with all repository-side production hardening complete.

## Implemented gates

- dedicated `sysUpTime.0` heartbeat and five-minute SNMP `nodata()` alert;
- management-agent uptime reset notice;
- standardized RFC1628 identification items plus automatic inventory links;
- RFC1628 battery current/temperature and read-only diagnostic test results;
- RFC1628 active alarm-table discovery with human-readable well-known alarm value map;
- unvalidated private input-power metrics disabled by default;
- private battery-temperature metric disabled by default and removed from production alerting;
- load alarms based on standardized `upsOutputPercentLoad` discovery instead of private aggregate load;
- misleading legacy graphs removed;
- Zabbix 7 API import integration test in CI/release workflow;
- MIB/OID source provenance and compatibility matrix.

## Homologation procedure

1. Import the 1.5.0 Zabbix 7 template with **Update existing** enabled.
2. Confirm `ups.snmp.uptime` updates every minute and stop SNMP briefly in a controlled window to confirm the availability alert/recovery.
3. Compare RFC1628 manufacturer/model/software/name with the UPS web UI.
4. Compare `ups.battery.current` and `ups.battery.temperature` with the UPS UI; if unsupported, document it in the compatibility matrix rather than enabling the private experimental temperature item for alerting.
5. Confirm input/output/bypass discovery and per-phase `upsOutputPercentLoad`.
6. If a safe alarm condition or battery test can be generated, confirm `upsAlarmTable` discovery and RFC1628 test-result items. Do not initiate tests through this template.
7. Confirm the Overview, Electrical and Battery & Environment dashboards with normal and incident windows.
8. Record exact device/card/firmware/Zabbix versions in the compatibility matrix.
9. Only after these checks, promote/tag `v1.5.0`.

## Non-blocking optional features

Vertiv-specific trap parsing is not required for production monitoring because polling and the standardized alarm table provide the primary alert/diagnostic path. The generic private trap item stays disabled until real payloads are captured and documented.
