# Security Policy

**English** | [Português (Brasil)](SECURITY.pt-BR.md)

## Supported versions

Security fixes are applied to the latest released project version on `main`.

## Reporting a vulnerability

Do not publish secrets or live UPS credentials in a public issue.

For a report, include only the minimum information necessary to reproduce the problem. Remove:

- SNMP community strings;
- SNMPv3 usernames when sensitive;
- authentication and privacy keys/passwords;
- public management IP addresses;
- internal hostnames when they identify a private environment.

If the issue can be described safely without sensitive information, open a GitHub issue and mark the security impact clearly.

## Project security model

The maintained template is designed for **read-only SNMP monitoring**. It does not include UPS reboot, shutdown, outlet switching or other SNMP write actions.

SNMPv3 with authentication and privacy is recommended where supported by the device. When SNMPv2c is required, restrict community access by source IP and network policy.

## RFC1628 read-write objects

Some standard objects, such as `upsIdentName`, are defined by RFC1628 as read-write. The template only queries them with SNMP GET. UPS-MIB control objects (`1.3.6.1.2.1.33.1.8`) and the objects used to start/abort tests (`upsTestId`/`upsTestSpinLock`) are not part of this project's control logic. The 1.5.0 candidate reads only test **result** objects.

Private metrics with unverified scaling/semantics are disabled by default and cannot drive critical production alerts.
