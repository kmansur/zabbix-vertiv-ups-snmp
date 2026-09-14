# Versioning

[Português (Brasil)](../pt-BR/versioning.md)

This project uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

Current repository version:

```text
1.5.1
```

Latest stable release:

```text
1.5.0
```

`VERSION` is the source of truth for the current repository version/candidate. `STABLE_VERSION` is the source of truth for the latest tagged stable release.

## Branch/release model

`main` is the active development branch. Production users should consume tagged GitHub Releases. It is valid for `VERSION` on `main` to become newer than `STABLE_VERSION` when a new candidate is under development.

Candidate `1.5.1` is a backward-compatible tooling/documentation patch that adds the optional global-dashboard generator. It does not change the 1.5.0 template monitoring semantics, item keys, macros, OIDs or triggers.

During a development candidate whose changes are outside the template export, the template may legitimately retain the latest stable `vendor.version`. The template validator therefore accepts both the current candidate vendor version and the latest stable vendor version **only while `VERSION` and `STABLE_VERSION` differ**. Once `STABLE_VERSION` is promoted to the candidate, the validator accepts only the candidate vendor version. This prevents publishing a tagged release with stale template metadata when the promoted release requires a template-version bump.

A candidate becomes stable after the documented release gate is accepted by the maintainer and the release workflow validates that both `VERSION` and `STABLE_VERSION` match the tag being published.

Current state:

```text
VERSION:        1.5.1
STABLE_VERSION: 1.5.0
```

## Rules

- **PATCH** — backward-compatible fixes, documentation corrections, maintenance/tooling changes that do not alter the template monitoring contract, and trigger tuning that does not change public keys/macros;
- **MINOR** — new backward-compatible metrics, triggers, graphs, device compatibility or template monitoring features;
- **MAJOR** — incompatible changes to item keys, macro names, template identity, required setup or monitoring behavior.

The maintainer selected `1.5.1` for the global-dashboard generator because the feature is external tooling derived from the existing native dashboard and does not change the imported monitoring template behavior.

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

Release `1.5.0` is exported as `vendor.version: 1.5-0`. Candidate `1.5.1` currently keeps that stable template metadata because the candidate changes only repository tooling/documentation. If `v1.5.1` is promoted as a release artifact that requires the template metadata to move to `1.5-1`, release validation will require that promotion before the tag can be published.

The release workflow validates the tag against both version markers, validates the template/documentation/production rules, runs tests and performs the Zabbix 7.0 upgrade validation before publishing assets.

## Zabbix compatibility does not define project version

The project version describes this repository. The Zabbix export version (`7.0` or `8.0`) describes the target Zabbix configuration format.

Therefore the same project version can exist in both Zabbix 7.0 and Zabbix 8.0 exports.

## Stable technical identifier

Starting with 1.4.0 the visible template name is **Vertiv by SNMP**, while the technical export identifier remains `VERTIV by SNMP`. Keeping the technical identifier stable is deliberate: it allows imports to update existing installations instead of creating a second template only because capitalization changed.
