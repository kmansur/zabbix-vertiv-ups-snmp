# Global dashboard

[Português (Brasil)](../pt-BR/global-dashboard.md)

**Introduced in repository candidate:** `1.5.1`  
**Latest stable release while this candidate is under review:** `1.5.0`

The template already ships with the native **Vertiv UPS Overview** template dashboard. That dashboard follows the host context automatically when the template is linked to a UPS.

A Zabbix **global dashboard** is a different object. Template exports do not promote a template dashboard into **Monitoring → Dashboards**. For that reason this project provides `tools/create_global_dashboard.py`, which uses the native template dashboard as the source of truth and recreates it through the Zabbix API for a real monitored host.

The maintainer successfully validated the generator in `--dry-run` mode against a real Zabbix 7.0 environment before the 1.5.1 candidate documentation was finalized. This confirms API version detection, target-host discovery, item/graph resolution and payload generation in the reference workflow; actual dashboard creation remains an explicit operator action.

## Why use the generator

The generator avoids maintaining a second hand-written dashboard definition. It:

- detects the connected Zabbix major/minor version;
- loads `templates/<major.minor>/vertiv-by-snmp.yaml`;
- finds the native `Vertiv UPS Overview` dashboard;
- resolves template item keys to item IDs on the selected host;
- resolves graph names to graph IDs on the selected host;
- preserves pages, widget positions, dimensions, titles, thresholds, colors and other supported fields;
- creates the resulting object with `dashboard.create`.

This makes the global dashboard track future changes made to the native template dashboard.

## Requirements

- Zabbix 7.0 or 8.0 matching an export present in this repository;
- the Vertiv template already imported and linked to the target UPS host;
- Python 3.9+;
- PyYAML (`pip install -r requirements-dev.txt` is sufficient);
- a Zabbix API token whose user role can read the target host/items/graphs and create dashboards.

## Dry run first

From the repository root:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.example.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --dry-run
```

The command resolves all references and prints the exact `dashboard.create` payload without creating anything.

For an internal lab or management endpoint that deliberately uses an untrusted certificate, append `--insecure`. Do not use that option as the normal production default.

## Create the dashboard

After reviewing the dry-run output:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.example.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01"
```

Default name:

```text
Vertiv UPS - <visible host name>
```

Use a custom name when needed:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.example.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --dashboard-name "Vertiv UPS - Datacenter"
```

## Private or public

By default the generated dashboard is private. Add `--public` to create a public dashboard:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.example.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --public
```

Sharing with specific users/groups should be configured after creation according to the local Zabbix access policy.

## Recreating an existing dashboard

The tool refuses to overwrite a dashboard with the same name. This is intentional.

After reviewing the dry-run output, use `--replace` to delete and recreate the existing dashboard:

```bash
python3 tools/create_global_dashboard.py \
  --url https://zabbix.example.com \
  --token "$ZABBIX_API_TOKEN" \
  --host "UPS-DATACENTER-01" \
  --replace
```

`--replace` recreates the dashboard object, so custom sharing and manual edits on that global dashboard must be reapplied. Prefer keeping layout changes in the template dashboard and regenerating from the repository.

## TLS

TLS certificate verification is enabled by default. `--insecure` exists only for controlled test environments with an untrusted certificate and should not be the normal production mode.

## Zabbix 7.0 and 8.0

The utility selects the repository export that matches the API server's major/minor version. This repository currently provides exports for Zabbix 7.0 and 8.0.

A server version without a matching `templates/<major.minor>/vertiv-by-snmp.yaml` export is rejected instead of attempting an unsafe cross-version conversion.

## Template dashboard vs global dashboard

| Characteristic | Template dashboard | Generated global dashboard |
|---|---|---|
| Location | Host/template context | Monitoring → Dashboards |
| Host binding | Automatic host context | Bound to the selected host when generated |
| Distributed with template import | Yes | No |
| Created by this repository tool | No | Yes |
| Best use | Per-host troubleshooting | NOC/operations entry point and shared navigation |

The generated global dashboard intentionally binds its item and graph widgets to one host. For multiple UPS devices, create one global dashboard per host or build a separate fleet/NOC dashboard using host-pattern or navigator widgets.

## Versioning note

Candidate `1.5.1` introduces this helper tool and documentation without changing the imported monitoring semantics of stable template `1.5.0`. `VERSION` can therefore be `1.5.1` while `STABLE_VERSION` and the unchanged template `vendor.version` remain at `1.5.0` / `1.5-0` until an explicit release promotion. See [Versioning](versioning.md).

## Security notes

- Use an API token with the minimum practical privileges.
- Do not commit API tokens to this repository.
- Revoke/rotate a token immediately if it is exposed in shell history, chat, logs or another uncontrolled location.
- The tool performs read operations for host/item/graph discovery and creates a dashboard. It only deletes a dashboard when `--replace` is explicitly supplied.
- No SNMP write operation is introduced by this feature.
