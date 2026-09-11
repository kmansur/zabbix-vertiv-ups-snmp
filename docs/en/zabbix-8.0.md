# Zabbix 8.0 compatibility

[Português (Brasil)](../pt-BR/zabbix-8.0.md)

The repository contains a separate export at:

```text
templates/zabbix-8.0/vertiv-by-snmp.yaml
```

Zabbix currently documents 8.0 as a development version. The 8.0 file uses export version `8.0` and is kept semantically aligned with the 7.0 template.

## Current status

- YAML and project-level structural validation: **enabled in CI**;
- semantic parity with the 7.0 export: **enabled in CI**;
- actual Zabbix 8.0 frontend import: **must be confirmed against the target build**;
- collection against a real Vertiv UPS: **must be confirmed per model/card/firmware**.

## Why the exports are separate

Zabbix export serialization can change between major versions. Keeping separate files allows the project to:

- preserve the exact export version;
- document validation against specific Zabbix builds;
- adopt Zabbix 8-only fields later without breaking Zabbix 7.0;
- keep stable UUIDs, keys, macros and functional behavior across versions.

When Zabbix 8.0 reaches RC/final and is tested with this template, update this document and the compatibility table in both root READMEs.
