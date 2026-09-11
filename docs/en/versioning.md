# Versioning

[Português (Brasil)](../pt-BR/versioning.md)

This project uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

Current version:

```text
1.1.0
```

## Rules

- **PATCH** — backward-compatible fixes, documentation corrections, trigger tuning that does not change public keys/macros;
- **MINOR** — new backward-compatible metrics, triggers, graphs, device compatibility or optional features;
- **MAJOR** — incompatible changes to item keys, macro names, template identity, required setup or monitoring behavior.

Version **1.1.0** is a MINOR release because it adds backward-compatible electrical summary items, value maps, graphs and documentation without changing existing public keys or macros.

## Release consistency

Project release identifiers use Semantic Versioning (`X.Y.Z`), while Zabbix template metadata uses the equivalent vendor format (`X.Y-Z`).

```text
VERSION: X.Y.Z
templates/7.0/... vendor.version: X.Y-Z
templates/8.0/... vendor.version: X.Y-Z
Git tag: vX.Y.Z
GitHub Release: vX.Y.Z
```

For example, project version `1.1.0` is exported as `vendor.version: 1.1-0`. The release workflow validates the tag against `VERSION` and validates both template exports before publishing the release archive.

## Zabbix compatibility does not define project version

The project version describes this repository. The Zabbix export version (`7.0` or `8.0`) describes the target Zabbix configuration format.

Therefore project version `1.1.0` can exist in both Zabbix 7.0 and Zabbix 8.0 exports.
