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

Before creating a tag, all of these must contain the same version:

```text
VERSION
templates/zabbix-7.0/... vendor.version
templates/zabbix-8.0/... vendor.version
Git tag vX.Y.Z
GitHub Release
```

The release workflow validates the tag against `VERSION` and validates both template exports before publishing the release archive.

## Zabbix compatibility does not define project version

The project version describes this repository. The Zabbix export version (`7.0` or `8.0`) describes the target Zabbix configuration format.

Therefore project version `1.1.0` can exist in both Zabbix 7.0 and Zabbix 8.0 exports.
