# Matriz de compatibilidade

[English](../en/compatibility.md)

Esta matriz separa **compatibilidade de engenharia** de **homologação em campo**. Um export pode passar na validação estrutural/importação sem comprovar cada OID em todos os firmwares. A homologação 1.5.0 usa o comportamento real do equipamento para definir os defaults seguros do template.

| Nobreak / placa | Zabbix | Status | Observações |
| --- | --- | --- | --- |
| Vertiv ITA-20kVA / placa usada no desenvolvimento | 7.0 | Homologação 1.5.0 em andamento | Estados principais, valores elétricos, enums textuais e dashboard foram observados em hardware real. `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) e `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) retornam `noSuchObject` nesta placa/firmware. O modelo/firmware exato da placa ainda deve ser registrado. |
| Outros Vertiv/Liebert / firmwares de placa | 7.0 | Compatível por projeto RFC1628; não certificado em campo | A implementação de UPS-MIB pode ser parcial. Objetos padrão opcionais devem ser confirmados no equipamento; OIDs privados precisam ser comparados com a UI local do nobreak. |
| Vertiv/Liebert | 8.0 desenvolvimento | Apenas export/paridade semântica | Não é alegação de suporte de produção até importação e execução em uma build 8.0 real. |

## Resultado de campo — grupo de bateria RFC1628

A placa usada na homologação implementa apenas parte do grupo UPS-MIB de bateria. Foram observados:

- `upsBatteryStatus` (`.1.3.6.1.2.1.33.1.2.1.0`) — **suportado**;
- `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) — **não suportado**, retorna `No Such Object available on this agent at this OID`;
- `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) — **não suportado**, retorna a mesma resposta `noSuchObject`.

Por isso, a candidata 1.5.0 mantém corrente e temperatura RFC1628 no template apenas como itens opcionais **desabilitados por padrão**. Eles não participam de dashboard nem triggers de produção e só devem ser habilitados em outra placa/firmware depois de confirmar suporte.

No equipamento validado, a corrente de bateria continua sendo coletada pelo OID privado Vertiv `...1.2.1.4149` (`vertiv.battery.current`), que já foi observado em campo. A temperatura privada Vertiv `...4156` retornou aproximadamente `-0,1 °C`, valor incompatível com o ambiente observado, e portanto também permanece desabilitada e sem trigger de produção. O gráfico ambiental usa apenas a temperatura de entrada validada.

Esse comportamento é um exemplo importante: conformidade com partes da RFC1628 **não implica implementação de todos os escalares do UPS-MIB** pelo agente SNMP.

## Registro de homologação

Para cada novo equipamento certificado, registre:

- modelo e capacidade nominal do nobreak;
- modelo da placa de gerenciamento;
- firmware do nobreak e da placa;
- versão exata do Zabbix;
- versão/nível de segurança SNMP;
- suporte real aos objetos RFC1628 de identificação, bateria, tabela de alarmes e resultado de testes;
- comparação dos valores privados exibidos com LCD/interface web;
- variantes de enums/traps observadas.
