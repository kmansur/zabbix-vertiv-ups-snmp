# Versioning

[Português (Brasil)](../pt-BR/versioning.md)

This project uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

Current repository version:

```text
1.5.0
```

Latest stable release:

```text
1.5.0
```

`VERSION` is the source of truth for the current repository version/candidate. `STABLE_VERSION` is the source of truth for the latest tagged stable release.

## Branch/release model

`main` is the active development branch. Production users should consume tagged GitHub Releases. It is valid for `VERSION` on `main` to become newer than `STABLE_VERSION` when a new candidate is under development.

A candidate becomes stable after the documented release gate is accepted by the maintainer and the release workflow validates that both `VERSION` and `STABLE_VERSION` match the tag being published.

For release `1.5.0`, both files contain `1.5.0`.

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

Release `1.5.0` is exported as `vendor.version: 1.5-0`. The release workflow validates the tag against both version markers, validates the template/documentation/production rules, runs tests and performs the Zabbix 7.0 upgrade validation before publishing assets.

## Zabbix compatibility does not define project version

The project version describes this repository. The Zabbix export version (`7.0` or `8.0`) describes the target Zabbix configuration format.

Therefore the same project version can exist in both Zabbix 7.0 and Zabbix 8.0 exports.

## Stable technical identifier

Starting with 1.4.0 the visible template name is **Vertiv by SNMP**, while the technical export identifier remains `VERTIV by SNMP`. Keeping the technical identifier stable is deliberate: it allows imports to update existing installations instead of creating a second template only because capitalization changed.
