# Project status

[Português (Brasil)](../pt-BR/project-status.md)

**Repository readiness: PASS**

**Zabbix 7.0 import/upgrade validation: PASS**

**Field homologation: IN PROGRESS (post-release)**

**Production release gate: PASS — maintainer approved 1.5.0 on 2026-09-14**

Version **1.5.0** is the current stable release. Repository-side structural, safety, documentation, CI and security controls passed, including real Zabbix 7.0 fresh import and in-place upgrade from 1.4.1. The maintainer accepted that evidence for the 1.5.0 release while keeping the remaining controlled hardware scenarios open as post-release field validation.

This status deliberately does **not** claim that the reference UPS/card/firmware has completed every field-homologation scenario.

| Area | Status | Notes |
| --- | --- | --- |
| Zabbix 7.0 template structure | PASS | Structural/template validators pass |
| Zabbix 7.0 API fresh import and upgrade | PASS | CI imports 1.4.1 and upgrades in place to 1.5.0 |
| Read-only safety | PASS | Known control/write OID families are forbidden by validation/tests |
| Experimental/private metric isolation | PASS | Unvalidated values cannot drive default production alerting |
| Documentation/template semantic checks | PASS | Versions, trigger tables, macros, bilingual file pairs and release policy are validated |
| CodeQL/security workflow | PASS | Release branch is promoted only after the security workflow succeeds |
| RFC1628 identification, heartbeat, tests and alarm diagnostics | PASS | Included in release 1.5.0 |
| Field compatibility record | IN PROGRESS | Real-hardware evidence exists for one Vertiv ITA-20kVA / IS-UNITY-DP environment; controlled event scenarios remain open |
| Zabbix 8.0 | PREVIEW | Export parity only; no production support claim |
| Production release `v1.5.0` | PASS | Approved by the maintainer based on repository/CI/security gates and collected field evidence |

## Branch/release model

`main` is the active development branch. `VERSION` identifies the current repository version/candidate and `STABLE_VERSION` identifies the latest tagged stable release. Production users should install a tagged GitHub Release because `main` may move ahead after a new development cycle begins.

For the 1.5.0 release, both version markers are `1.5.0`.

## Release decision

The maintainer approved `v1.5.0` for release on **2026-09-14** after:

1. repository/template/documentation validators passed;
2. Python 3.9, 3.13 and 3.14 CI jobs passed;
3. CodeQL passed;
4. a real Zabbix 7.0 fresh import passed;
5. an in-place Zabbix API upgrade from stable 1.4.1 to 1.5.0 passed;
6. existing real-hardware evidence confirmed the safe defaults used by the template.

Remaining controlled field checks are tracked in [the 1.5.0 field record](homologation-1.5.0.md) and the corresponding GitHub issue. Completing them may upgrade the compatibility wording to **field-homologated**, but they are no longer a blocker for publishing the 1.5.0 software release.
