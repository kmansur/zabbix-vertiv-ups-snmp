# Field validation record — release 1.5.0

[Português (Brasil)](../pt-BR/homologation-1.5.0.md)

**Release:** 1.5.0  
**Record date:** 2026-09-14  
**Software release status:** **APPROVED**  
**Extended field-validation status:** **IN PROGRESS**

This record separates evidence already collected on real hardware from controlled scenarios that still require field action. The maintainer approved the 1.5.0 software release after repository validation, CodeQL, Zabbix 7.0 fresh import and the 1.4.1 → 1.5.0 in-place upgrade passed. Pending field checks are not converted into PASS from CI evidence and the reference hardware is not yet described as fully field-homologated.

## Reference environment

| Component | Observed value |
| --- | --- |
| UPS | Vertiv `ITA-20k00AL3A02E00`, 20 kVA |
| UPS firmware | `V220` |
| Management card | `IS-UNITY-DP` |
| Card firmware | `8.5.1.0` / `IS-UNITY_8.5.1.0_00173` |
| sysObjectID | `.1.3.6.1.4.1.476.1.42` |
| Zabbix Server | `7.0.30` |
| Template release | `1.5.0` / `vendor.version: 1.5-0` |

Serial numbers and credentials are intentionally excluded.

## Evidence already collected

| Check | Status | Evidence/notes |
| --- | --- | --- |
| Device/card identification | PASS | Manufacturer/card/firmware/UPS model values observed on real hardware |
| RFC1628 identification coverage | PASS | Identification objects present; `sysName.0` selected for inventory NAME because UPS-specific name objects returned placeholder values |
| RFC1628 battery status/charge/runtime/voltage | PASS | Status supported; runtime observed at 4320 min, charge 100%, voltage 544.0 V after RFC scaling |
| RFC1628 battery current | COMPATIBILITY EXCEPTION | `upsBatteryCurrent` returned `noSuchObject`; release item remains disabled by default |
| RFC1628 battery temperature | COMPATIBILITY EXCEPTION | `upsBatteryTemperature` returned `noSuchObject`; release item remains disabled by default |
| Vertiv private battery current | PASS | Private OID ending `4149` observed working and retained in the production dashboard |
| Vertiv private battery temperature | REJECTED FOR PRODUCTION | Private OID ending `4156` returned approximately `-0.1 °C`; disabled and trigger-free |
| RFC1628 input/output electrical values | PASS | Three-phase values observed and consistent with the UPS environment |
| Private input-power scaling characterization | PASS | Private values 1.6/1.5/1.5 correlated with standard 1600/1500/1500 W; private items remain disabled because RFC1628 is preferred |
| Normal alarm-table behavior | PASS | `upsAlarmsPresent=0`; `upsAlarmTable` empty in normal state as expected |
| Private event inactive state | PASS (inactive only) | `.2.100.*` objects returned `Inactive Event`; active-state encoding remains unknown |
| RFC1628 test result objects present | PASS | Result/time objects observed; template reads result objects only |
| Repository structural/read-only validation | PASS | Automated template/production validators prohibit known control OIDs and unsupported default alert paths |
| Zabbix 7.0 fresh import | PASS (CI) | Release export imports through the Zabbix API |
| Zabbix 7.0 in-place upgrade | PASS (CI) | Stable 1.4.1 imports and upgrades in place to 1.5.0 through the Zabbix API |
| CodeQL | PASS | Security analysis completed successfully before promotion |

## Post-release field checks still pending

The following checks require controlled access to the real monitoring environment. They are **not software-release blockers**, but they remain required before describing this exact hardware combination as fully field-homologated:

- [ ] Confirm `ups.snmp.uptime` updates every minute on the production/homologation host.
- [ ] In a controlled window, interrupt SNMP reachability long enough to verify the five-minute `nodata()` problem event and automatic recovery.
- [ ] Confirm the management-agent uptime-reset informational event with a known card/agent restart, or document an accepted alternative verification method.
- [ ] Generate or wait for a safe real UPS alarm and confirm `upsAlarmTable` discovery creates the expected description/time rows and clears them after recovery.
- [ ] Observe a safe diagnostic/battery-test result transition and confirm the read-only result items/triggers. The template itself must not start the test.
- [ ] Review all three dashboard pages during a normal window and at least one representative incident/event window.
- [ ] Record the SNMP version/security level used in the reference environment.
- [ ] Confirm no unexpected unsupported items remain enabled by default on this exact card/firmware.
- [ ] Record final operator sign-off and field-homologation date.

## Release decision

**Maintainer decision: APPROVED TO TAG/PUBLISH `v1.5.0` on 2026-09-14.**

The release decision is based on repository, CI, security and already-collected real-hardware evidence. This approval changes the software release gate only; it does not mark the pending hardware checkboxes as complete.

When every post-release field checkbox above is complete:

1. change the extended field-validation status to **PASS** and add the final homologation date/sign-off;
2. update the compatibility matrix wording to `1.5.0 field-homologated` for this exact hardware combination;
3. close the post-release field-validation tracking issue.
