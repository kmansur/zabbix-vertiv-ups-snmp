# Métricas e OIDs

[English](../en/metrics.md)

A tabela abaixo documenta os itens fixos incluídos no template atual. A disponibilidade dos OIDs pode variar conforme o modelo do nobreak e a placa de gerenciamento.

## Identificação

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `vertiv.agent.manufacturer` | UPS: Agent manufacturer | `1.3.6.1.4.1.476.1.42.2.1.1.0` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.agent.model` | UPS: Agent model | `1.3.6.1.4.1.476.1.42.2.1.2.0` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.agent.firmware` | UPS: Agent firmware version | `1.3.6.1.4.1.476.1.42.2.1.3.0` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.agent.serial` | UPS: Agent serial number | `1.3.6.1.4.1.476.1.42.2.1.4.0` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.system.model` | UPS: System model | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4240` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.system.serial` | UPS: System serial number | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4244` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.system.firmware` | UPS: Firmware version | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4335` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.system.name` | UPS: System name | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4329` | — | 1h | Vertiv/Liebert enterprise MIB |

## Status

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `vertiv.system.status` | UPS: System status | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4123` | — | 30s | Vertiv/Liebert enterprise MIB |
| `ups.output.source` | UPS: Output source | `1.3.6.1.2.1.33.1.4.1.0` | — | 30s | RFC 1628 UPS-MIB |
| `ups.alarms.present` | UPS: Alarms present | `1.3.6.1.2.1.33.1.6.1.0` | — | 30s | RFC 1628 UPS-MIB |
| `vertiv.inverter.state` | UPS: Inverter state | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4746` | — | 1m | Vertiv/Liebert enterprise MIB |
| `vertiv.eco.status` | UPS: ECO mode status | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.6198` | — | 5m | Vertiv/Liebert enterprise MIB |
| `vertiv.topology` | UPS: Topology | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.6199` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.shutdown.reason` | UPS: Shutdown reason | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.6197` | — | 5m | Vertiv/Liebert enterprise MIB |
| `vertiv.system.operating.time` | UPS: Total system operating time | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4292` | h | 1h | Vertiv/Liebert enterprise MIB |

## Bateria

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `ups.battery.status` | UPS: Battery status | `1.3.6.1.2.1.33.1.2.1.0` | — | 30s | RFC 1628 UPS-MIB |
| `ups.battery.seconds` | UPS: Seconds on battery | `1.3.6.1.2.1.33.1.2.2.0` | s | 30s | RFC 1628 UPS-MIB |
| `ups.battery.runtime` | UPS: Estimated runtime remaining | `1.3.6.1.2.1.33.1.2.3.0` | min | 30s | RFC 1628 UPS-MIB |
| `ups.battery.charge` | UPS: Estimated battery charge | `1.3.6.1.2.1.33.1.2.4.0` | % | 30s | RFC 1628 UPS-MIB |
| `ups.battery.voltage` | UPS: Battery voltage | `1.3.6.1.2.1.33.1.2.5.0` | V | 1m | RFC 1628 UPS-MIB |
| `vertiv.battery.current` | UPS: Battery current | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4149` | A | 1m | Vertiv/Liebert enterprise MIB |
| `vertiv.battery.temperature` | UPS: Battery temperature | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4156` | °C | 2m | Vertiv/Liebert enterprise MIB |
| `vertiv.battery.charge.status` | UPS: Battery charge state | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5799` | — | 1m | Vertiv/Liebert enterprise MIB |
| `vertiv.battery.test.result` | UPS: Battery test result | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.6181` | — | 5m | Vertiv/Liebert enterprise MIB |
| `vertiv.battery.autotest` | UPS: Automatic battery test | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5803` | — | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.battery.discharge.count` | UPS: Total number of battery discharges | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5767` | — | 5m | Vertiv/Liebert enterprise MIB |
| `vertiv.battery.low.warning.time` | UPS: Low battery warning time | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5802` | min | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.dc.bus.voltage` | UPS: DC bus voltage | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4148` | V | 1m | Vertiv/Liebert enterprise MIB |

## Entrada e qualidade de energia

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `ups.input.line.bads` | UPS: Input line bad count | `1.3.6.1.2.1.33.1.3.1.0` | — | 5m | RFC 1628 UPS-MIB |
| `vertiv.input.blackout.count` | UPS: Input blackout count | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4120` | — | 5m | Vertiv/Liebert enterprise MIB |
| `vertiv.input.brownout.count` | UPS: Input brownout count | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4119` | — | 5m | Vertiv/Liebert enterprise MIB |
| `vertiv.input.energy` | UPS: Input energy | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5900` | kWh | 15m | Vertiv/Liebert enterprise MIB |
| `ups.input.num_lines` | UPS: Input number of lines | `1.3.6.1.2.1.33.1.3.2.0` | — | 1h | RFC 1628 UPS-MIB |

## Saída e energia

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `vertiv.output.apparent.power` | UPS: Output apparent power | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4209` | VA | 1m | Vertiv/Liebert enterprise MIB |
| `vertiv.output.power` | UPS: Output power | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4208` | W | 1m | Vertiv/Liebert enterprise MIB |
| `vertiv.output.load` | UPS: Output load | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5861` | % | 1m | Vertiv/Liebert enterprise MIB |
| `vertiv.output.rating.va` | UPS: Output apparent power rating | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4264` | VA | 1h | Vertiv/Liebert enterprise MIB |
| `vertiv.output.energy` | UPS: Output energy | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.5166` | kWh | 15m | Vertiv/Liebert enterprise MIB |
| `ups.output.num_lines` | UPS: Output number of lines | `1.3.6.1.2.1.33.1.4.3.0` | — | 1h | RFC 1628 UPS-MIB |

## Ambiente

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `vertiv.inlet.temperature` | UPS: Inlet air temperature | `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1.4291` | °C | 2m | Vertiv/Liebert enterprise MIB |

## Configuração

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `ups.config.input.voltage` | UPS: Nominal input voltage | `1.3.6.1.2.1.33.1.9.1.0` | V | 1h | RFC 1628 UPS-MIB |
| `ups.config.input.frequency` | UPS: Nominal input frequency | `1.3.6.1.2.1.33.1.9.2.0` | Hz | 1h | RFC 1628 UPS-MIB |
| `ups.config.output.voltage` | UPS: Nominal output voltage | `1.3.6.1.2.1.33.1.9.3.0` | V | 1h | RFC 1628 UPS-MIB |
| `ups.config.output.frequency` | UPS: Nominal output frequency | `1.3.6.1.2.1.33.1.9.4.0` | Hz | 1h | RFC 1628 UPS-MIB |
| `ups.config.output.va` | UPS: Nominal output VA | `1.3.6.1.2.1.33.1.9.5.0` | VA | 1h | RFC 1628 UPS-MIB |
| `ups.config.low.battery.time` | UPS: Configured low battery time | `1.3.6.1.2.1.33.1.9.7.0` | min | 1h | RFC 1628 UPS-MIB |

## Eventos

| Chave | Item | OID | Unidade | Intervalo | Fonte |
| --- | --- | --- | --- | --- | --- |
| `snmptrap["1\.3\.6\.1\.4\.1\.476\.1\.42"]` | UPS: Vertiv SNMP traps (optional) | — | — | 0 | Other |

## Descoberta de baixo nível

O template descobre as tabelas de linhas de entrada, saída e bypass utilizando colunas da UPS-MIB.

### UPS input lines discovery

- Chave de descoberta: `ups.input.lines.discovery`
- OID de descoberta: `discovery[{#UPSINPUTVOLTAGE},1.3.6.1.2.1.33.1.3.3.1.3]`

Protótipos:

| Chave | Protótipo de item | OID | Unidade |
| --- | --- | --- | --- |
| `ups.input.frequency[{#SNMPINDEX}]` | UPS: Input line {#SNMPINDEX}: Frequency | `1.3.6.1.2.1.33.1.3.3.1.2.{#SNMPINDEX}` | Hz |
| `ups.input.voltage[{#SNMPINDEX}]` | UPS: Input line {#SNMPINDEX}: Voltage | `1.3.6.1.2.1.33.1.3.3.1.3.{#SNMPINDEX}` | V |
| `ups.input.current[{#SNMPINDEX}]` | UPS: Input line {#SNMPINDEX}: Current | `1.3.6.1.2.1.33.1.3.3.1.4.{#SNMPINDEX}` | A |
| `ups.input.power[{#SNMPINDEX}]` | UPS: Input line {#SNMPINDEX}: True power | `1.3.6.1.2.1.33.1.3.3.1.5.{#SNMPINDEX}` | W |

### UPS output lines discovery

- Chave de descoberta: `ups.output.lines.discovery`
- OID de descoberta: `discovery[{#UPSOUTPUTVOLTAGE},1.3.6.1.2.1.33.1.4.4.1.2]`

Protótipos:

| Chave | Protótipo de item | OID | Unidade |
| --- | --- | --- | --- |
| `ups.output.voltage[{#SNMPINDEX}]` | UPS: Output line {#SNMPINDEX}: Voltage | `1.3.6.1.2.1.33.1.4.4.1.2.{#SNMPINDEX}` | V |
| `ups.output.current[{#SNMPINDEX}]` | UPS: Output line {#SNMPINDEX}: Current | `1.3.6.1.2.1.33.1.4.4.1.3.{#SNMPINDEX}` | A |
| `ups.output.power[{#SNMPINDEX}]` | UPS: Output line {#SNMPINDEX}: Power | `1.3.6.1.2.1.33.1.4.4.1.4.{#SNMPINDEX}` | W |
| `ups.output.load[{#SNMPINDEX}]` | UPS: Output line {#SNMPINDEX}: Load | `1.3.6.1.2.1.33.1.4.4.1.5.{#SNMPINDEX}` | % |

### UPS bypass lines discovery

- Chave de descoberta: `ups.bypass.lines.discovery`
- OID de descoberta: `discovery[{#UPSBYPASSVOLTAGE},1.3.6.1.2.1.33.1.5.3.1.2]`

Protótipos:

| Chave | Protótipo de item | OID | Unidade |
| --- | --- | --- | --- |
| `ups.bypass.voltage[{#SNMPINDEX}]` | UPS: Bypass line {#SNMPINDEX}: Voltage | `1.3.6.1.2.1.33.1.5.3.1.2.{#SNMPINDEX}` | V |

## Observação sobre escala

As escalas padronizadas da UPS-MIB são aplicadas quando definidas pela RFC 1628, como décimos de hertz, décimos de ampère ou décimos de volt nos objetos correspondentes.

Nenhum multiplicador arbitrário é aplicado aos OIDs privados Vertiv sem que a definição SNMP fornecida estabeleça essa escala. Durante a implantação, compare sempre os valores específicos do fabricante com o LCD/interface web do nobreak.
