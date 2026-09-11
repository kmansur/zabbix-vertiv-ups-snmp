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
