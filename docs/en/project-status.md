# Project status

[Português (Brasil)](../pt-BR/project-status.md)

**Production implementation readiness: 100%**

**Field homologation: pending**

Version **1.5.0** is the production-hardening candidate. The 100% score means that all repository-side work identified by the production review is implemented, guarded by automated validation, and has no known software/documentation blocker. It does **not** claim that every Vertiv UPS model/firmware has been field-certified.

| Area | Score | Status |
| --- | ---: | --- |
| Zabbix 7.0 template structure and field-derived behavior | 25/25 | Complete |
| Operator dashboard and documentation | 15/15 | Complete |
| Read-only safety and experimental-metric isolation | 15/15 | Complete |
| RFC1628 availability, identification, test and active-alarm coverage | 15/15 | Complete |
| CI, validators, real Zabbix 7 import test and release gating | 15/15 | Complete |
| MIB/OID provenance, compatibility and homologation procedure | 10/10 | Complete |
| Zabbix 8 export parity without claiming production support | 5/5 | Complete |

## Meaning of 100%

The candidate is ready to enter homologation. Unknown vendor-private scaling/state encodings are not treated as supported production data: they are disabled, isolated or documented instead of guessed. Optional event-specific Vertiv trap parsing remains outside the production path until real payloads are captured; active-alarm diagnostics are provided by the standardized RFC1628 alarm table.

## Promotion gate

After real-hardware homologation succeeds, merge the candidate to `main`, record the exact UPS/card/firmware/Zabbix versions in the compatibility matrix, date the 1.5.0 changelog entry and create tag/release `v1.5.0`.
