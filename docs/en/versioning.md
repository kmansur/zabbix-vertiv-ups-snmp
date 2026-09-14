# Versioning

[Português (Brasil)](../pt-BR/versioning.md)

This project uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

Current repository candidate:

```text
1.5.0
```

Latest stable release:

```text
1.4.1
```

`VERSION` is the source of truth for the current repository candidate. `STABLE_VERSION` is the source of truth for the latest tagged stable release.

## Branch/release model

`main` is the active development/candidate branch. Production users should consume tagged GitHub Releases. It is therefore valid for `VERSION` on `main` to be newer than `STABLE_VERSION` while a candidate is under validation/homologation.

A candidate becomes stable only after the promotion gate in [Project status](project-status.md) and [Production readiness](production-readiness.md) is complete.

## Rules

- **PATCH** — backward-compatible fixes, documentation corrections, trigger tuning that does not change public keys/macros;
- **MINOR** — new backward-compatible metrics, triggers, graphs, device compatibility or optional features;
- **MAJOR** — incompatible changes to item keys, macro names, template identity, required setup or monitoring behavior.

## Release consistency

Project release identifiers use Semantic Versioning (`X.Y.Z`), while Zabbix template metadata uses the equivalent vendor format (`X.Y-Z`).

```text
VERSION: X.Y.Z
STABLE_VERSION: latest tagged stable X.Y.Z
templates/7.0/... vendor.version: X.Y-Z
templates/8.0/... vendor.version: X.Y-Z
Git tag: vX.Y.Z
GitHub Release: vX.Y.Z
```

Candidate `1.5.0` is exported as `vendor.version: 1.5-0`. The release workflow validates the tag against `VERSION` and validates both template exports before publishing a release.

When `v1.5.0` is actually promoted and published, the release change must also move `STABLE_VERSION` from `1.4.1` to `1.5.0`.

## Zabbix compatibility does not define project version

The project version describes this repository. The Zabbix export version (`7.0` or `8.0`) describes the target Zabbix configuration format.

Therefore the same project version can exist in both Zabbix 7.0 and Zabbix 8.0 exports.

## Stable technical identifier

Starting with 1.4.0 the visible template name is **Vertiv by SNMP**, while the technical export identifier remains `VERTIV by SNMP`. Keeping the technical identifier stable is deliberate: it allows imports to update existing installations instead of creating a second template only because capitalization changed.
