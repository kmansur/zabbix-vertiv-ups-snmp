# MIB/OID sources and provenance

[Português (Brasil)](../pt-BR/mib-sources.md)

The template uses **numeric OIDs**, so no MIB file must be installed on the Zabbix server/proxy for collection to work. MIBs and supplied parameter lists are development/documentation references only.

## Standards source

- IETF RFC 1628 — UPS Management Information Base, base OID `1.3.6.1.2.1.33`.
- SNMPv2-MIB `sysUpTime.0`, OID `1.3.6.1.2.1.1.3.0`, is used as the dedicated SNMP heartbeat.

The canonical RFC is authoritative when it contains objects that are absent from the supplied extracted parameter list, such as `upsBatteryCurrent` and `upsBatteryTemperature`.

## Field-supplied reference files

These files were used during development but are **not redistributed** by this repository because redistribution rights were not established. Their SHA-256 hashes allow the exact reviewed source material to be identified:

| File | SHA-256 | Purpose |
| --- | --- | --- |
| `SNMP_upsMibParams.txt` | `794198d1715f3e1100643ba0f128abbb94f401c4eb7303b0a591ea95879bb133` | Extracted UPS-MIB parameter OIDs |
| `SNMP_upsMibEvents.txt` | `c0be3ffc0f5729c1674a1f6a17d3c0a27246e9e962e77ab699ff654067f1783c` | Selected RFC1628 well-known alarm OIDs |
| `SNMP_Parameters.txt` | `076ede2bfe1a91714840d7928ddef582aee5fafe43626ab34336ed1f9d241908` | Vertiv/Liebert private parameter/OID list |
| `SNMP_Events.txt` | `249e6d58e8cfc453767899f45555129b1b7cb1dbf52c33e42835bd413663b9a2` | Vertiv condition identifiers |
| `ModbusDataMap.txt` | `c41b1bbedf1b8395b2b838477c4457102ce40fdeda51c701fd1ae49b25e3acdb` | Modbus reference only; its scaling is not copied to SNMP |

## Scaling rule

RFC1628 scaling is applied exactly as defined by the standard. Vertiv private SNMP objects receive no multiplier unless their SNMP representation has been independently validated. Modbus scaling is never assumed to apply to SNMP.

## Event rule

The private Vertiv condition lists identify event names/OIDs but do not define the state encoding of pollable `.2.100.*` objects or the exact trap payload format. Production logic therefore does not fabricate those encodings. Active-alarm diagnosis uses RFC1628 `upsAlarmTable`; the generic private trap item remains disabled until real payloads are captured.
