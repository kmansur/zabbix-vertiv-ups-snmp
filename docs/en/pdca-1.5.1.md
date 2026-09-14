# PDCA review — release 1.5.1

[Português (Brasil)](../pt-BR/pdca-1.5.1.md)

**Review date:** 2026-09-14  
**Scope:** release `1.5.1`, PR #16 and the global-dashboard generator  
**Stable baseline:** `1.5.0`  
**Promotion target:** `1.5.1`

## Executive assessment

Release 1.5.1 is a tooling/documentation maintenance release. It does not add SNMP write operations or change the monitoring semantics introduced by stable template 1.5.0. Its principal new surface is `tools/create_global_dashboard.py`, which converts the native template dashboard into a host-bound global dashboard through the Zabbix API.

The PDCA cycle found two material reliability issues in the first `--replace` implementation: same-name dashboards could be treated as a unique identity, and the previous flow deleted existing dashboards before creating a replacement. Both findings were corrected. Replacement is now fail-closed and in-place: only editable exact-name dashboards are considered, more than one match aborts without mutation, exactly one match is updated with `dashboard.update`, and the tool never calls `dashboard.delete`.

The repository metadata is now promoted for release: `VERSION=1.5.1`, `STABLE_VERSION=1.5.1`, and both Zabbix exports use `vendor.version: 1.5-1`. Monitoring semantics remain unchanged from 1.5.0; the template metadata bump keeps the tagged release internally consistent.

## PLAN

### Objectives

1. Generate a reproducible global dashboard without maintaining a second independent layout.
2. Keep `Vertiv UPS Overview` as the single source of truth.
3. Support repository exports for Zabbix 7.0 and 8.0 without cross-version guessing.
4. Resolve host item/graph references before any write.
5. Make replacement safe under API failures, duplicate names and restricted permissions.
6. Preserve the read-only SNMP safety model.
7. Keep EN/PT-BR documentation, tests and versioning synchronized.
8. Promote release metadata only after the corrected implementation passes the repository gates.

### Acceptance criteria

- `--dry-run` performs no dashboard writes.
- New creation uses `dashboard.create` only after reference resolution.
- `--replace` only considers editable exact-name dashboards.
- Zero editable matches creates; one updates in place; multiple matches abort.
- Existing dashboards are never pre-deleted.
- The generator contains no `dashboard.delete` call.
- Tests cover create, update, refusal without `--replace`, editable filtering and ambiguity.
- Python 3.9/3.13/3.14, Ruff, pytest, repository validators, Zabbix 7.0 import/upgrade and CodeQL must pass.
- `VERSION`, `STABLE_VERSION` and template `vendor.version` must be release-consistent before tagging.

## DO

Implemented in 1.5.1:

- template-driven global-dashboard generator;
- automatic server major/minor detection and matching YAML selection;
- host item-key and graph-name resolution to concrete IDs;
- `--dry-run`, `--public`, custom name, TLS validation and controlled `--insecure` support;
- safe replacement using `dashboard.update` rather than delete/recreate;
- `dashboard.get` lookup restricted with `editable=true`;
- explicit rejection of multiple editable exact-name matches;
- update payload intentionally omits `users` and `userGroups`, avoiding deliberate replacement of sharing definitions;
- regression tests for all replacement safety invariants;
- bilingual global-dashboard documentation and bilingual PDCA report;
- release promotion to `VERSION=1.5.1`, `STABLE_VERSION=1.5.1` and `vendor.version: 1.5-1` in both Zabbix exports.

The maintainer also successfully exercised `--dry-run` against a real Zabbix 7.0 environment, validating API version detection, host discovery, item/graph resolution and payload generation. Actual dashboard create/update against that production-like endpoint remains an explicit operator action and is not claimed as field-validated here.

## CHECK

### Validation outcome

The corrected implementation passed:

- Python 3.9 — compile, Ruff lint/format, pytest and repository validators;
- Python 3.13 — compile, Ruff lint/format, pytest and repository validators;
- Python 3.14 — compile, Ruff lint/format, pytest and repository validators;
- Zabbix template validation;
- bilingual documentation validation;
- production-readiness validation;
- disposable Zabbix 7.0 stable-baseline import and in-place upgrade to the candidate;
- CodeQL Python analysis.

Both review findings are resolved in the PR discussion:

1. **P2 — ambiguous same-name replacement:** fixed by editable-only lookup plus rejection of multiple matches.
2. **P1 — delete-before-create loss window:** fixed by in-place `dashboard.update`; `dashboard.delete` is not used.

A final CI/CodeQL cycle is required on the promoted release head before merge/tag.

### Strengths confirmed

- Monitoring remains read-only; no SNMP control/write OIDs were added.
- The global dashboard is generated from a single source of truth.
- Replacement fails closed when identity is ambiguous.
- In-place update removes the old delete/create loss window.
- Existing dashboard identity is retained.
- Unit tests assert that the safe replacement path never deletes a dashboard.
- Release metadata is internally aligned at 1.5.1.

### Residual risks / gaps

| Area | Status | Assessment |
| --- | --- | --- |
| Real Zabbix 7.0 `--dry-run` | Validated | Real API discovery and reference resolution confirmed by maintainer. |
| Zabbix 7.0 template import/upgrade CI | Passed before promotion; re-run required on final release head | Stable baseline import and candidate in-place upgrade succeeded. |
| Dashboard create/update against a disposable live Zabbix API | Open improvement | API behavior is unit-tested; a dedicated integration test would add confidence. |
| Zabbix 8.0 semantic export parity | Covered by repository validation | Real API/import/runtime validation is still pending. |
| Additional Vertiv models/firmware | Open field work | Device MIB subsets can vary. |
| Reference hardware extended homologation | In progress | Separate from repository/tooling correctness. |
| `main` protection/ruleset | Recommended | Enforced required checks would reduce process risk. |

## ACT

### Merge and release decision

The maintainer approved promotion of 1.5.1 and requested merge plus tag creation. Release metadata was therefore promoted before merge so the existing tag-triggered release workflow can validate a consistent repository state.

The PR must only be merged after the final promoted head passes CI and CodeQL. The tag `v1.5.1` must point to the final merged release commit.

### Next PDCA priorities

1. Add disposable-Zabbix integration coverage for `dashboard.create` / `dashboard.update` if practical.
2. Perform real Zabbix 8.0 import/API/runtime validation.
3. Complete remaining controlled reference-hardware scenarios.
4. Enforce branch/ruleset protection for CI, import and security checks.

## Conclusion

The corrected 1.5.1 implementation is materially safer than the initial design: replacement is identity-constrained, fail-closed and non-destructive. The release metadata has been promoted consistently, and the final merge/tag is authorized by the maintainer subject to the promoted head passing the configured CI and CodeQL gates.
