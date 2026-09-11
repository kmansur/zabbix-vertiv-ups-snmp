# Project status

[Português (Brasil)](../pt-BR/project-status.md)

**Current project maturity: 85%**

This percentage is a maintained engineering maturity score, not an uptime/SLA metric. It reflects the state of the template, field validation, automation and documentation.

| Area | Score | Notes |
| --- | ---: | --- |
| Zabbix 7.0 core template and real-device validation | 30/30 | Import, collection, enum normalization and dashboard validated on real Vertiv hardware |
| Dashboard and operator usability | 15/15 | Native dashboard, severity colors, readable mapped statuses and trend graphs |
| Documentation, versioning, CI and security automation | 20/20 | Bilingual docs, validators, pytest, Ruff, CodeQL and release automation |
| Read-only safety and control-OID exclusion | 10/10 | Consequential write/control branches are explicitly excluded and validated |
| Private electrical scaling validation | 5/10 | Most displayed values are plausible; private input-power scale still requires confirmation |
| Model/firmware coverage | 3/5 | One production device/card behavior has been validated in depth; broader coverage is pending |
| Event-specific SNMP trap processing | 0/5 | Waiting for real trap payload capture before creating event-specific parsers/triggers |
| Zabbix 8.0 runtime validation | 2/5 | Export parity is automated, but import/runtime testing against an actual Zabbix 8 build is pending |

## Main remaining work

1. Validate private input-power OID scaling against the UPS web/LCD values before using those metrics for alerting.
2. Capture real Vertiv trap payloads and implement event-specific trap processing only from verified encodings.
3. Validate additional UPS models and management-card firmware.
4. Import and runtime-test the 8.0 export on an actual Zabbix 8 environment.
5. Validate the optional synoptic map import on production-like Zabbix 7/8 instances.
