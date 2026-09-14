# Project status

[Português (Brasil)](../pt-BR/project-status.md)

**Repository readiness: PASS**

**Zabbix 7.0 import/upgrade validation: PASS**

**Field homologation: IN PROGRESS**

**Production release gate: BLOCKED until homologation is completed**

Version **1.5.0** is the current production-hardening candidate. Repository-side structural, safety, documentation and CI controls are implemented and validated automatically, but this status is deliberately not expressed as a percentage because repository completeness is not the same as hardware certification.

| Area | Status | Notes |
| --- | --- | --- |
| Zabbix 7.0 template structure | PASS | Structural/template validators pass |
| Zabbix 7.0 API fresh import and upgrade | PASS | CI imports stable baseline and upgrades to candidate |
| Read-only safety | PASS | Known control/write OID families are forbidden by validation/tests |
| Experimental/private metric isolation | PASS | Unvalidated values cannot drive default production alerting |
| Documentation/template semantic checks | PASS | Versions, trigger tables, macros, bilingual file pairs and release policy are validated |
| RFC1628 identification, heartbeat, tests and alarm diagnostics | PASS | Implemented in the candidate |
| Field compatibility record | IN PROGRESS | One Vertiv ITA-20kVA / IS-UNITY-DP environment is the current homologation reference |
| Zabbix 8.0 | PREVIEW | Export parity only; no production support claim |
| Production release `v1.5.0` | BLOCKED | Requires completed field-homologation record |

## Branch/release model

`main` is the active development/candidate branch. `VERSION` identifies the current repository candidate and `STABLE_VERSION` identifies the latest tagged stable release. Production users should install a tagged GitHub Release.

## Promotion gate

Candidate `1.5.0` may be promoted only when the field-homologation record is complete and all mandatory checks are PASS. At that point:

1. update the compatibility matrix with the exact UPS/card/firmware/Zabbix versions and final result;
2. close all mandatory pending items in the homologation record;
3. date the `1.5.0` changelog entry;
4. update `STABLE_VERSION` to `1.5.0` in the release change;
5. create tag/release `v1.5.0` only after CI/release validation succeeds.

The candidate is already developed on `main`; there is no separate candidate-to-main merge step in this repository model.
