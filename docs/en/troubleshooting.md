# Troubleshooting

[Português (Brasil)](../pt-BR/troubleshooting.md)

## Template import fails

Confirm that you are importing the YAML from the directory matching the Zabbix major/minor version.

Run locally:

```sh
python tools/validate_templates.py
```

If Zabbix reports a schema/import error that the local validator does not detect, open an issue with:

- exact Zabbix version/build;
- complete import error;
- template file used.

## All SNMP items are unsupported

Verify:

- the host has an SNMP interface;
- the interface IP is correct;
- UDP/161 is reachable;
- SNMP version and credentials match the UPS;
- the Zabbix Server or assigned Proxy can reach the device.

Test from the same server/proxy:

```sh
snmpget -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.2.1.0
```

## Only Vertiv enterprise items are unsupported

Some management cards expose the UPS-MIB but not every object under `1.3.6.1.4.1.476.1.42`.

Run:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.4.1.476.1.42
```

Record the UPS model, management-card model and firmware when opening an issue.

## UPS-MIB line discovery returns no phases

Check the standard line tables directly:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.3.3
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.4.4
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.5.3
```

A single-phase UPS may expose only index `.1`; a three-phase model can expose three line indexes. Not every UPS exposes bypass data.

## A value looks scaled incorrectly

Compare it with the UPS LCD/web interface and capture the raw SNMP value with `snmpget -On`.

Do not add a multiplier based only on a Modbus scale. SNMP and Modbus representations may use different scaling.

Open an issue with:

- OID;
- raw SNMP value;
- value shown by the UPS interface;
- model/card/firmware.

## A private Vertiv enum is returned as a string / Numeric (unsigned)

Some Vertiv/Liebert management cards return enumerated private objects as text, such as `Normal Operation`, `on`, `Online`, `fully charged` or `Passed`, while other cards/firmware may return the numeric enum code.

Starting with version 1.3.2, the template normalizes both representations to the canonical numeric code before storage. This keeps value maps and numeric triggers working with both behaviors.

If `Value of type "string" is not suitable for value type "Numeric (unsigned)"` still appears, verify that the template has `vendor.version: 1.3-2` or newer and provide the OID plus the raw text returned by `snmpget -On`.

## Too many alerts

Review host-level macro overrides for runtime, charge, load and temperature thresholds. Defaults are intentionally generic and must be adapted to the installation.

## SNMP traps do not arrive

The trap item is disabled by default. SNMP polling and SNMP trap reception are independent Zabbix paths.

First validate the server/proxy trap receiver outside the template, then enable the trap item.
