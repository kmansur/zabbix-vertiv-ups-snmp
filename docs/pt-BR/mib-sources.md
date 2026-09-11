# Fontes MIB/OID e proveniência

[English](../en/mib-sources.md)

O template usa **OIDs numéricos**, portanto nenhum arquivo MIB precisa ser instalado no Zabbix Server/Proxy para a coleta funcionar. MIBs e listas de parâmetros fornecidas são apenas referências de desenvolvimento/documentação.

## Fonte padronizada

- IETF RFC 1628 — UPS Management Information Base, OID base `1.3.6.1.2.1.33`.
- SNMPv2-MIB `sysUpTime.0`, OID `1.3.6.1.2.1.1.3.0`, é usado como heartbeat SNMP dedicado.

O RFC canônico é autoritativo quando contém objetos ausentes da lista extraída fornecida, como `upsBatteryCurrent` e `upsBatteryTemperature`.

## Arquivos de referência fornecidos em campo

Estes arquivos foram usados no desenvolvimento, mas **não são redistribuídos** pelo repositório porque o direito de redistribuição não foi estabelecido. Os hashes SHA-256 identificam exatamente o material revisado:

| Arquivo | SHA-256 | Finalidade |
| --- | --- | --- |
| `SNMP_upsMibParams.txt` | `794198d1715f3e1100643ba0f128abbb94f401c4eb7303b0a591ea95879bb133` | OIDs extraídos da UPS-MIB |
| `SNMP_upsMibEvents.txt` | `c0be3ffc0f5729c1674a1f6a17d3c0a27246e9e962e77ab699ff654067f1783c` | Alarmes conhecidos RFC1628 selecionados |
| `SNMP_Parameters.txt` | `076ede2bfe1a91714840d7928ddef582aee5fafe43626ab34336ed1f9d241908` | Lista de parâmetros/OIDs privados Vertiv/Liebert |
| `SNMP_Events.txt` | `249e6d58e8cfc453767899f45555129b1b7cb1dbf52c33e42835bd413663b9a2` | Identificadores de condições Vertiv |
| `ModbusDataMap.txt` | `c41b1bbedf1b8395b2b838477c4457102ce40fdeda51c701fd1ae49b25e3acdb` | Referência Modbus; sua escala não é copiada para SNMP |

## Regra de escala

A escala RFC1628 é aplicada exatamente como definida pelo padrão. OIDs SNMP privados Vertiv não recebem multiplicador até que sua representação SNMP seja validada de forma independente. Escala Modbus nunca é presumida para SNMP.

## Regra de eventos

As listas privadas de condições Vertiv identificam nomes/OIDs de eventos, mas não definem o encoding de estado dos objetos `.2.100.*` nem o formato exato do payload de traps. A lógica de produção não inventa esses encodings. O diagnóstico de alarmes ativos usa `upsAlarmTable` RFC1628; o item genérico de traps privados continua desabilitado até existirem capturas reais.
