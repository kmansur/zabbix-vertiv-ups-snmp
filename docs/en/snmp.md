# SNMP architecture

[Português (Brasil)](../pt-BR/snmp.md)

## OID namespaces

### RFC 1628 UPS-MIB

Base OID:

```text
1.3.6.1.2.1.33
```

Used for standardized UPS identification/configuration, battery status, runtime, input/output measurements, bypass measurements and line tables.

### Vertiv/Liebert enterprise MIB

Base OID:

```text
1.3.6.1.4.1.476.1.42
```

Used for vendor-specific management-card identification, system status, inverter state, battery details, self-test state, energy, environmental measurements, shutdown reason and power-quality counters.

## Why both are used

RFC 1628 provides stable semantics and scaling for common UPS data. The Vertiv enterprise branch exposes details that are not available in the standard MIB.

Using both provides broader monitoring while avoiding vendor-specific replacements for data that already has a clear standard representation.

## Read-only policy

The project does not include SNMP SET operations or items intended to control the UPS.

Examples deliberately excluded:

- agent reboot;
- delayed UPS reboot;
- delayed shutdown/startup;
- outlet-group power control;
- manual battery-test commands;
- reset power statistics;
- audible-alarm control.

This keeps routine monitoring separate from consequential device-control operations.

## Polling strategy

- status and battery-state data: typically 30 seconds to 1 minute;
- temperature and electrical values: typically 1–2 minutes;
- counters and self-test state: typically 5 minutes;
- energy: 15 minutes;
- identification and nominal configuration: 1 hour.

## SNMP traps

A disabled trap item is supplied for the Vertiv enterprise branch. Before enabling it:

1. configure SNMP trap reception on Zabbix Server/Proxy;
2. configure the UPS to send traps to that receiver;
3. capture real traps from the target model;
4. document the payload;
5. only then add event-specific preprocessing and triggers.

This avoids false assumptions about management-card trap formats.
