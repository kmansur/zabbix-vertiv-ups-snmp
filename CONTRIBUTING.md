# Contributing

**English** | [Português (Brasil)](CONTRIBUTING.pt-BR.md)

Contributions, device compatibility reports, bug reports, documentation improvements and Zabbix compatibility updates are welcome.

## Development workflow

1. Create a branch from `main`.
2. Make one focused change.
3. Run the local validation commands.
4. Update English and Brazilian Portuguese documentation together.
5. Update both changelog files when the change is user-visible.
6. Open a pull request.

Recommended branch names:

- `feature/<description>`
- `fix/<description>`
- `docs/<description>`
- `refactor/<description>`
- `ci/<description>`
- `chore/<description>`

## Commit messages

Conventional Commits are recommended:

- `feat:` new functionality;
- `fix:` bug fix;
- `docs:` documentation;
- `refactor:` internal restructuring;
- `test:` tests;
- `ci:` CI/CD;
- `chore:` repository maintenance.

## Local validation

```sh
python -m pip install -r requirements-dev.txt
python -m compileall -q tools tests
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
```

## Zabbix template workflow

Version-specific exports belong under:

```text
templates/zabbix-<major.minor>/
```

When changing a template:

1. preserve the template UUID unless intentionally creating a new template;
2. preserve item keys and UUIDs for backward-compatible changes;
3. keep Zabbix 7.0 and 8.0 semantics aligned;
4. update `VERSION` and every `vendor.version` for a release;
5. import into the target Zabbix build whenever possible;
6. validate Latest data against the UPS LCD/web interface;
7. document the exact UPS model, management card, firmware and Zabbix build used for runtime validation.

## Device compatibility reports

Please include:

- UPS model;
- management-card model;
- firmware;
- Zabbix version;
- whether SNMPv2c or SNMPv3 is used;
- unsupported item keys/OIDs;
- raw `snmpget -On` or `snmpwalk -On` output for the affected OID;
- expected value shown by the UPS interface.

Remove communities, usernames, authentication keys, privacy keys and public IP information before posting logs.
