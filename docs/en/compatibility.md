# Compatibility matrix

[Português (Brasil)](../pt-BR/compatibility.md)

This matrix distinguishes **engineering compatibility** from **field homologation**. A template export can pass structural/import validation without proving every vendor-private object on every firmware.

| UPS / card | Zabbix | Status | Notes |
| --- | --- | --- | --- |
| Vertiv ITA-20kVA / management card used during development | 7.0 | Field-derived baseline; 1.5.0 homologation pending | Core states, electrical values, enum strings and dashboard behavior were observed on real hardware. Exact management-card model/firmware should be recorded during the 1.5.0 homologation run. |
| Other Vertiv/Liebert UPS/card firmware | 7.0 | Compatible by RFC1628 design; not field-certified | Standard objects should be portable; private OIDs must be compared with the local UPS UI. |
| Vertiv/Liebert | 8.0 development | Export/semantic parity only | Not a production support claim until a real 8.0 build is imported and run. |

## Homologation record

For every newly certified device, record:

- UPS model and rated capacity;
- management-card model;
- UPS firmware and management-card firmware;
- Zabbix exact version;
- SNMP version/security level;
- whether RFC1628 identity, battery current/temperature, alarm table and test-result objects are supported;
- comparison of displayed private values with the UPS LCD/web UI;
- observed enum/trap variants.
