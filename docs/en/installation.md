# Installation

[Português (Brasil)](../pt-BR/installation.md)

## Requirements

- Zabbix Server or Proxy able to reach the UPS SNMP interface;
- Zabbix 7.0 or a compatible Zabbix 8.0 development build;
- SNMP enabled on the Vertiv/Liebert management card;
- read access to the standard UPS-MIB and/or Vertiv enterprise MIB.

SNMPv3 is recommended when the management card supports it. SNMPv2c can also be used when required by the device or environment.

## 1. Choose stable release or candidate intentionally

For **production**, download the latest tagged stable GitHub Release identified by `STABLE_VERSION` and use the release asset for your Zabbix version.

Files under `templates/` on the `main` branch represent the current development/candidate version identified by `VERSION`. Use those files only when intentionally testing/homologating that candidate.

Zabbix 8.0 remains a preview compatibility target until runtime/import support is explicitly promoted.

## 2. Verify SNMP from the Zabbix Server or Proxy

Replace the placeholders with the values used in your environment.

UPS-MIB:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33
```

Vertiv/Liebert enterprise MIB:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.4.1.476.1.42
```

If SNMPv3 is used, test with the matching authentication and privacy parameters instead of exposing credentials in shell history.

## 3. Import the template

In Zabbix:

1. open **Data collection → Templates**;
2. click **Import**;
3. select the release/candidate file matching your intended target:
   - Zabbix 7.0: `vertiv-by-snmp-zabbix-7.0.yaml` release asset, or `templates/7.0/vertiv-by-snmp.yaml` when explicitly testing the candidate;
   - Zabbix 8.0 preview: `vertiv-by-snmp-zabbix-8.0.yaml` release asset/candidate equivalent, only when intentionally validating 8.0 compatibility;
4. review the import summary;
5. import the template.

## 4. Configure the UPS host

Create or edit the UPS host and add an **SNMP** interface with the management-card IP address.

Configure the SNMP version and credentials in the host/interface settings according to your security policy.

## 5. Link the template

Link:

```text
Vertiv by SNMP
```

Wait for the first polling cycles.

## 6. Validate the first data

Open **Monitoring → Latest data** and confirm at least:

- SNMP heartbeat (`UPS: SNMP agent uptime`);
- UPS output source;
- system status;
- battery status and charge;
- estimated runtime;
- input/output measurements;
- output load;
- inlet temperature;
- discovered input/output/bypass lines.

Compare the reported measurements with the UPS LCD or web interface. Unsupported optional objects are device/card compatibility information; do not enable them blindly.

## 7. Tune macros

Review the default runtime, battery charge, output-line load and inlet-temperature thresholds before enabling production alerting.

Battery-temperature macros are reserved in candidate 1.5.0 and do not activate a default battery-temperature trigger.

See [Configuration and macros](configuration.md).

## Optional SNMP traps

The template contains a disabled item named `UPS: Vertiv SNMP traps (optional)`.

Leave it disabled unless Zabbix SNMP trap reception is already configured and the actual Vertiv trap payload has been validated. The project deliberately does not invent event parsing rules from condition OID names alone.
