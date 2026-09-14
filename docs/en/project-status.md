# Project status

[Português (Brasil)](../pt-BR/project-status.md)

**Repository readiness: PASS**

**Zabbix 7.0 import/upgrade validation: PASS**

**Field homologation: IN PROGRESS (post-release)**

**Latest production release gate: PASS — 1.5.2**

**Current repository version: 1.5.3**

Version **1.5.2** remains the current stable release. Repository candidate **1.5.3** incorporates field-validation evidence and reduces active-alarm LLD cadence from 1m to 30s after a real 30-second alarm demonstrated the observability gap between aggregate polling and the slower discovery cycle.

Version **1.5.1** introduced the optional global-dashboard generator, bilingual deployment documentation and automated conversion/layout tests. The maintainer validated its `--dry-run` flow against a real Zabbix 7.0 environment.

This status deliberately does **not** claim that the reference UPS/card/firmware has completed every field-homologation scenario.

| Area | Status | Notes |
| --- | --- | --- |
| Zabbix 7.0 template structure | PASS | Structural/template validators pass |
| Zabbix 7.0 API fresh import and upgrade | PASS | CI imports the stable baseline and upgrades in place to the current release |
| Read-only safety | PASS | Known control/write OID families are forbidden by validation/tests |
| Experimental/private metric isolation | PASS | Unvalidated values cannot drive default production alerting |
| Documentation/template semantic checks | PASS | Versions, trigger tables, macros, bilingual file pairs and release policy are validated |
| CodeQL/security workflow | PASS | Security analysis passes before release promotion |
| RFC1628 identification, heartbeat, tests and alarm diagnostics | PASS | Production monitoring behavior established in 1.5.0 |
| Global dashboard generator | VALIDATED | Introduced in 1.5.1; real Zabbix 7.0 `--dry-run` validated by maintainer |
| GPLv3 licensing and attribution | PASS | Original template author directly authorized use as a basis and GPLv3 publication on 2026-09-14 |
| Field compatibility record | IN PROGRESS | Heartbeat/nodata, dashboards, SNMP transport, enabled-item support and multiple real UPS events are validated; non-forced reset/test-transition/individual transient alarm-row observations remain open |
| Zabbix 8.0 | PREVIEW | Export parity only; no production support claim |
| Production release `v1.5.2` | PASS | Licensing/metadata patch; monitoring semantics unchanged from 1.5.1 |

## Branch/release model

`main` is the active development branch. `VERSION` identifies the current repository version/candidate and `STABLE_VERSION` identifies the latest tagged stable release. Production users should install a tagged GitHub Release because `main` may move ahead after a new development cycle begins.

Current markers for this release:

```text
VERSION:        1.5.3
STABLE_VERSION: 1.5.2
```

## Release decision

`v1.5.2` is a patch release for licensing, attribution and release metadata. It does not introduce new monitoring behavior. Promotion requires the same repository validators, Zabbix 7.0 import/upgrade path and security checks used by the project release workflow.

Remaining controlled field checks continue in [the 1.5.0 field record](homologation-1.5.0.md) and the corresponding GitHub issue. Completing them may upgrade the compatibility wording to **field-homologated**, but they do not block this licensing/metadata patch release.
