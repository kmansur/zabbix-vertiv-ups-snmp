# Contributing

**English** | [Português (Brasil)](CONTRIBUTING.pt-BR.md)

Contributions, device compatibility reports, bug reports, documentation improvements and Zabbix compatibility updates are welcome.

## Branch and release policy

`main` is the active development/candidate branch. A tagged GitHub Release is the production distribution point.

- `VERSION` identifies the current repository candidate.
- `STABLE_VERSION` identifies the latest tagged stable release.
- Production documentation must distinguish those two states whenever they differ.
- Candidate changes must go through a pull request and pass the repository validation suite before merge.
- A candidate is tagged stable only after the field-homologation gate is complete.

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
python tools/validate_production.py
```

## Zabbix template workflow

Version-specific exports are stored at:

```text
templates/7.0/vertiv-by-snmp.yaml
templates/8.0/vertiv-by-snmp.yaml
```

When changing a template:

1. preserve the template UUID unless intentionally creating a new template;
2. preserve item keys and UUIDs for backward-compatible changes;
3. keep Zabbix 7.0 and 8.0 semantics aligned while 8.0 remains a preview export;
4. update `VERSION` and every `vendor.version` for a new candidate/release;
5. update `STABLE_VERSION` only when that version has actually been tagged/released stable;
6. import into the target Zabbix build whenever possible;
7. validate Latest data against the UPS LCD/web interface;
8. document the exact UPS model, management card, firmware and Zabbix build used for runtime validation;
9. record field-homologation evidence under `docs/homologation/` before promoting a candidate to stable.

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
