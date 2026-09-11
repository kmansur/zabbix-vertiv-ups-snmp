# Optional synoptic map

[Português (Brasil)](../pt-BR/synoptic-map.md)

Version 1.3.0 adds an optional generator for a Zabbix network-map synoptic view of one monitored Vertiv UPS. The map complements the native template dashboard; it does not replace it.

## What the map shows

The generated map contains a central UPS host element and four operational blocks: **INPUT**, **BYPASS**, **OUTPUT**, and **BATTERY**. Zabbix dynamically highlights the central UPS icon when the host has problems. The peripheral blocks are intentionally static schematic elements; the project does not invent unsupported item-to-shape bindings.

Two small UPS icons are embedded in the export, so the map does not depend on a pre-existing Zabbix icon library.

## Generate a map

The host must already exist in Zabbix and should already be linked to **Vertiv by SNMP**.

For Zabbix 7.0:

```sh
python tools/generate_synoptic_map.py \
  --host "UPS-SRV01" \
  --output vertiv-ups-synoptic.yaml
```

For Zabbix 8.0:

```sh
python tools/generate_synoptic_map.py \
  --host "UPS-SRV01" \
  --zabbix-version 8.0 \
  --output vertiv-ups-synoptic.yaml
```

Use the **exact Zabbix host name**, not the visible name unless both are identical.

## Import

1. Open **Monitoring → Maps**.
2. Click **Import**.
3. Select the generated YAML file.
4. Enable creation/update of the map and creation of its images as appropriate.
5. Import the file.

Zabbix requires referenced hosts to exist before a map is imported. Image importing requires a Super admin account. The generator is read-only with respect to the UPS and contains no SNMP write/control operations.
