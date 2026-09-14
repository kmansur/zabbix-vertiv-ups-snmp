# PDCA review — candidate 1.5.1

[Português (Brasil)](../pt-BR/pdca-1.5.1.md)

**Review date:** 2026-09-14  
**Scope:** repository candidate `1.5.1`, PR #16 and the global-dashboard generator  
**Stable baseline:** `1.5.0`

## Executive assessment

Candidate 1.5.1 is a tooling/documentation maintenance release. It does not add SNMP write operations or change the monitoring semantics of the stable 1.5.0 template. The principal new surface is `tools/create_global_dashboard.py`, which converts the native template dashboard into a host-bound global dashboard through the Zabbix API.

The review identified a meaningful reliability risk in the first `--replace` implementation: same-name dashboards could be treated as a unique identity and the previous flow deleted existing dashboards before creating the replacement. The correction changes replacement to a fail-closed, in-place update model. Only editable exact-name dashboards are considered, more than one match aborts without mutation, and the tool never calls `dashboard.delete`.

## PLAN

### Objectives

1. Provide a reproducible global dashboard without maintaining a second independent layout.
2. Keep the native `Vertiv UPS Overview` template dashboard as the single source of truth.
3. Support Zabbix 7.0 and 8.0 repository exports without cross-version guessing.
4. Resolve item and graph references against the selected real host before any write.
5. Make replacement safe under API errors, duplicate names and restricted permissions.
6. Preserve the project's read-only SNMP safety model.
7. Keep EN/PT-BR documentation, tests, versioning and release policy synchronized.

### Acceptance criteria

- `--dry-run` performs no dashboard writes.
- New dashboard creation uses `dashboard.create` only after all references resolve.
- `--replace` only targets editable exact-name dashboards.
- Zero editable matches creates a new dashboard; one match updates in place; multiple matches abort.
- Existing dashboards are never pre-deleted.
- No `dashboard.delete` call exists in the generator.
- Automated tests cover create, update, no-replace refusal, editable filtering and ambiguous matches.
- CI must pass Python 3.9/3.13/3.14, Ruff, pytest, repository validators and the Zabbix 7.0 import/upgrade job.
- CodeQL must pass before merge.

## DO

Implemented in candidate 1.5.1:

- global-dashboard generator driven from the native template dashboard;
- automatic server major/minor detection and matching versioned YAML selection;
- host item-key and graph-name resolution to concrete IDs;
- `--dry-run`, `--public`, custom name, TLS validation and controlled `--insecure` support;
- safe replacement using `dashboard.update` rather than delete/recreate;
- `dashboard.get` lookup restricted with `editable=true`;
- explicit rejection when more than one editable exact-name dashboard is found;
- update payload intentionally omits `users` and `userGroups`, avoiding deliberate replacement of sharing definitions;
- tests for the replacement safety invariants;
- bilingual operational documentation and automated bilingual-document presence validation;
- repository candidate version advanced to `1.5.1`, while `STABLE_VERSION` remains `1.5.0` pending explicit promotion.

The maintainer also successfully exercised the generator with `--dry-run` against a real Zabbix 7.0 environment, validating API version detection, target-host discovery, item/graph resolution and payload generation. Actual create/update against that production-like endpoint remains an explicit operator action and is not claimed as field-validated by this report.

## CHECK

### Strengths confirmed

- The monitoring template remains read-only and no control/write SNMP OIDs were introduced.
- The global dashboard is generated from a single source of truth rather than copied into a second manually maintained definition.
- Replacement now fails closed when identity is ambiguous.
- In-place update eliminates the previous loss window where a failed create could leave operators without the old dashboard.
- Existing dashboard identity is retained during update.
- Unit tests directly verify that no delete occurs in the safe replacement path.
- Candidate/stable version separation remains explicit: repository `VERSION=1.5.1`, stable marker `STABLE_VERSION=1.5.0` until release promotion.

### Residual risks / gaps

| Area | Status | Assessment |
| --- | --- | --- |
| Zabbix 7.0 real `--dry-run` | Validated | Real API discovery/reference resolution confirmed by maintainer. |
| Zabbix 7.0 template import/upgrade CI | Required gate | Must remain green on the final PR head. |
| Dashboard create/update against a disposable live Zabbix API | Open improvement | Unit-tested API behavior; a dedicated integration test would strengthen confidence. |
| Zabbix 8.0 semantic export parity | Covered by repository validation | Real API/import/runtime validation is still pending. |
| Additional Vertiv models/firmware | Open field work | Device MIB subsets can vary. |
| Reference hardware extended homologation | In progress | Remains separate from repository/tooling correctness. |
| `main` protection/ruleset | Recommended | Enforced required checks would reduce process risk. |

### Critical findings addressed in this cycle

1. **Ambiguous same-name replacement:** fixed by editable-only lookup plus rejection of multiple matches.
2. **Delete-before-create loss window:** fixed by `dashboard.update` in place; `dashboard.delete` is not used.

## ACT

### Before merge

- Require final CI and CodeQL success on the post-fix PR head.
- Keep PR #16 unmerged if any Python, validator, import/upgrade or security check fails.
- Do not promote `STABLE_VERSION` merely because the branch is mergeable.

### After merge / before release promotion

- Decide explicitly when candidate 1.5.1 becomes stable.
- Promote release metadata/tag only through the existing release workflow and version gates.
- Prefer a controlled test of actual global-dashboard create and in-place update in a non-critical Zabbix instance before broad operational use.

### Next PDCA priorities

1. Add disposable-Zabbix integration coverage for `dashboard.create` / `dashboard.update` if practical.
2. Perform real Zabbix 8.0 import/API/runtime validation.
3. Complete remaining controlled reference-hardware scenarios.
4. Enforce branch/ruleset protection for required CI, import and security checks.

## Conclusion

The corrected 1.5.1 design is materially safer than the initial implementation because replacement is now identity-constrained, fail-closed and non-destructive. From an engineering-process perspective, the candidate is suitable for merge only after the final PR head passes all configured CI and CodeQL gates. Stable release promotion remains a separate maintainer decision.
