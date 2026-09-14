# Vertiv by SNMP

[![CI](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml/badge.svg)](https://github.com/kmansur/zabbix-vertiv-ups-snmp/actions/workflows/security.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**English** | [Português (Brasil)](README.pt-BR.md)

Zabbix template for read-only monitoring of **Vertiv/Liebert UPS systems via SNMP**. It combines the standard RFC 1628 UPS-MIB with Vertiv/Liebert enterprise OIDs to monitor power source, battery, electrical input/output, bypass, environmental data, power-quality counters, self-test status, and device identification.

## Dashboard preview

<p align="center">
  <a href="docs/en/dashboard.md">
    <img src="docs/images/dashboard-overview.png" alt="Vertiv UPS Overview dashboard" width="100%">
  </a>
</p>

<p align="center"><strong>Overview</strong> — operational health, battery, output power and per-phase load at a glance.</p>

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="docs/en/dashboard.md#electrical">
        <img src="docs/images/dashboard-electrical.png" alt="Vertiv UPS Electrical dashboard" width="100%">
      </a>
      <br>
      <sub><strong>Electrical</strong> — input, output and bypass measurements, frequency, topology and power-quality counters.</sub>
    </td>
    <td width="50%" valign="top">
      <a href="docs/en/dashboard.md#battery--environment">
        <img src="docs/images/dashboard-battery-environment.png" alt="Vertiv UPS Battery and Environment dashboard" width="100%">
      </a>
      <br>
      <sub><strong>Battery &amp; Environment</strong> — charge, runtime, battery state, test/configuration data and inlet temperature.</sub>
    </td>
  </tr>
</table>

<p align="center">📖 <a href="docs/en/dashboard.md"><strong>Read the dashboard interpretation guide</strong></a> — what each graph means, what normal behavior looks like, and what to investigate during an incident.</p>

## Compatibility

| Zabbix | Template | Status |
| --- | --- | --- |
| 7.0 | `templates/7.0/vertiv-by-snmp.yaml` | Supported export; validate device-specific OIDs on the target UPS |
| 8.0 | `templates/8.0/vertiv-by-snmp.yaml` | Preview compatibility export for Zabbix 8.0 development builds; runtime validation is still required |

Zabbix 8.0 is currently documented by Zabbix as a development version. See [docs/en/zabbix-8.0.md](docs/en/zabbix-8.0.md).

## Project status

Current stable release: **1.4.1**

Homologation candidate: **1.5.0** — **100% production implementation complete**; real-hardware homologation pending. See [project status](docs/en/project-status.md).

## What the template monitors

- UPS and management-card identification;
- global UPS status and output source;
- active alarm count;
- battery status, charge, runtime, voltage, current and temperature;
- battery test result, discharge count and low-battery warning time;
- input quality counters including line-bad, blackout and brownout counts;
- output load, real power and apparent power;
- input and output energy;
- inlet air temperature and total operating time;
- nominal electrical configuration;
- input, output and bypass lines/phases through low-level discovery (LLD);
- fixed L-N/L-L input, output and bypass summary metrics for deterministic dashboards;
- fixed per-phase current, power factor, load and power metrics;
- calculated total input power and battery cabinet/test-interval metadata;
- optional Vertiv enterprise SNMP trap collection.

An optional Zabbix network-map synoptic can be generated per UPS host with `tools/generate_synoptic_map.py`.

The template is intentionally **read-only**. Reboot, shutdown, outlet control and other SNMP write operations are not included.

## Repository layout

```text
.github/                 GitHub Actions, issue templates and PR template
docs/
├── en/                  English documentation
├── images/              Dashboard screenshots used by the documentation
└── pt-BR/               Brazilian Portuguese documentation
templates/
├── 7.0/                 Zabbix 7.0 export
└── 8.0/                 Zabbix 8.0 export
tests/                   Validator tests
tools/                   Template and documentation validation tools
```

## Quick start

1. Configure SNMP on the Vertiv/Liebert UPS management card. Prefer SNMPv3 when supported.
2. In Zabbix, create or select the UPS host and configure its SNMP interface.
3. Import the YAML for your Zabbix version.
4. Link **Vertiv by SNMP** to the host.
5. Review **Monitoring → Latest data** and confirm the reported values against the UPS LCD/web interface.
6. Tune the template macros for the expected battery runtime, load and temperature limits.

Detailed instructions: [docs/en/installation.md](docs/en/installation.md).

## Default thresholds

| Macro | Default | Purpose |
| --- | ---: | --- |
| `{$UPS.RUNTIME.WARN}` | 10 min | Low runtime warning |
| `{$UPS.RUNTIME.CRIT}` | 5 min | Critical runtime |
| `{$UPS.BATTERY.CHARGE.WARN}` | 40% | Low battery charge while on battery |
| `{$UPS.BATTERY.CHARGE.CRIT}` | 20% | Critical battery charge while on battery |
| `{$UPS.LOAD.WARN}` | 80% | High UPS load |
| `{$UPS.LOAD.CRIT}` | 95% | Critical UPS load |
| `{$UPS.BATTERY.TEMP.WARN}` | 35 °C | High battery temperature |
| `{$UPS.BATTERY.TEMP.CRIT}` | 40 °C | Critical battery temperature |
| `{$UPS.INLET.TEMP.WARN}` | 30 °C | High inlet temperature |
| `{$UPS.INLET.TEMP.CRIT}` | 35 °C | Critical inlet temperature |

## Documentation

English:

- [Overview](docs/en/README.md)
- [Installation](docs/en/installation.md)
- [Configuration and macros](docs/en/configuration.md)
- [Metrics and OIDs](docs/en/metrics.md)
- [Electrical summary metrics](docs/en/electrical-summary.md)
- [Native dashboard](docs/en/dashboard.md)
- [Optional synoptic map](docs/en/synoptic-map.md)
- [Triggers](docs/en/triggers.md)
- [SNMP architecture](docs/en/snmp.md)
- [Troubleshooting](docs/en/troubleshooting.md)
- [Zabbix 8.0 compatibility](docs/en/zabbix-8.0.md)
- [Versioning](docs/en/versioning.md)
- [License and attribution](docs/en/license-attribution.md)
- [MIB/OID sources and provenance](docs/en/mib-sources.md)
- [Compatibility matrix](docs/en/compatibility.md)
- [Production readiness and homologation](docs/en/production-readiness.md)

Brazilian Portuguese documentation is available under [docs/pt-BR/](docs/pt-BR/README.md).

## Development and validation

Install the development dependencies:

```sh
python -m pip install -r requirements-dev.txt
```

Run:

```sh
python -m compileall -q tools tests
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Versioning

Candidate project version: **1.5.0**. Stable remains 1.4.1 until field homologation. The project follows Semantic Versioning.

Project releases use `X.Y.Z`, while the Zabbix template `vendor.version` follows the Zabbix convention `X.Y-Z`. Therefore candidate version `1.5.0` is exported as `vendor.version: 1.5-0`.

```text
VERSION / Git tag / GitHub Release: X.Y.Z
Zabbix vendor.version: X.Y-Z
```

## License and attribution

Original work in this repository is distributed under the **MIT License**.

This project credits the original **Template Vertiv** by **Mihguel da Silva Santos Tavares de Araujo** as a structural and historical reference:

https://github.com/Mihguel-Araujo/Template-Zabbix/blob/main/Template%20Vertiv

No explicit license was found in the referenced repository at the time of review, therefore the original file is not redistributed here and is not relicensed by this project.

See [LICENSE](LICENSE), [NOTICE.md](NOTICE.md), and [docs/en/license-attribution.md](docs/en/license-attribution.md).

Maintained by **Karim Mansur / Net Tech**.
