# Matriz de compatibilidade

[English](../en/compatibility.md)

Esta matriz separa **compatibilidade de engenharia** de **homologação em campo**. Um export pode passar na validação estrutural/importação sem comprovar cada OID em todos os firmwares. A homologação 1.5.0 usa o comportamento real do equipamento para definir os defaults seguros do template.

| Nobreak / placa | Zabbix | Status | Observações |
| --- | --- | --- | --- |
| Vertiv `ITA-20k00AL3A02E00` (20 kVA), firmware UPS `V220` / placa `IS-UNITY-DP`, firmware `8.5.1.0` (`IS-UNITY_8.5.1.0_00173`) | 7.0.30 | Homologação 1.5.0 em andamento | Estados principais, valores elétricos, enums textuais e dashboard foram observados em hardware real. `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) e `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) retornam `noSuchObject` nesta placa/firmware. |
| Outros Vertiv/Liebert / firmwares de placa | 7.0 | Compatível por projeto RFC1628; não certificado em campo | A implementação de UPS-MIB pode ser parcial. Objetos padrão opcionais devem ser confirmados no equipamento; OIDs privados precisam ser comparados com a UI local do nobreak. |
| Vertiv/Liebert | 8.0 desenvolvimento | Apenas export/paridade semântica | Não é alegação de suporte de produção até importação e execução em uma build 8.0 real. |

## Identificação observada em campo

A placa respondeu como fabricante `Vertiv`, modelo `IS-UNITY-DP`, firmware `8.5.1.0`, build `IS-UNITY_8.5.1.0_00173` e `sysObjectID` `.1.3.6.1.4.1.476.1.42`. O nobreak reportou modelo `ITA-20k00AL3A02E00` e firmware `V220`. O ambiente de homologação usa **Zabbix Server 7.0.30**. O `sysName.0` retornou `nobreak-01`, enquanto os objetos de nome do UPS retornaram preenchimento de zeros; por isso o inventory `NAME` passa a usar `sysName.0` como fonte confiável. Números de série não são publicados nesta matriz.

## Resultado de campo — cobertura RFC1628

O walk completo da árvore `1.3.6.1.2.1.33` confirmou suporte funcional aos grupos padronizados de identificação, bateria parcial, entrada, saída, bypass, alarmes, resultados de teste e configuração. A candidata usa apenas objetos de leitura; os grupos de controle/configuração presentes no agente não são usados para escrita.

Valores elétricos padronizados observados incluem três fases de entrada e saída, frequência de `59,9 Hz`, carga de saída de `23/23/24 %`, potência real de saída por fase de `1450/1410/1520 W` e potência real de entrada por fase de `1600/1500/1500 W`. Esses valores são coerentes com os objetos privados Vertiv observados no mesmo equipamento.

## Resultado de campo — grupo de bateria RFC1628

A placa usada na homologação implementa apenas parte do grupo UPS-MIB de bateria. Foram observados:

- `upsBatteryStatus` (`.1.3.6.1.2.1.33.1.2.1.0`) — **suportado**;
- `upsEstimatedMinutesRemaining` — **suportado**, retornando `4320 min` (`72 h`);
- `upsEstimatedChargeRemaining` — **suportado**, retornando `100 %`;
- `upsBatteryVoltage` — **suportado**, retornando `5440` décimos de volt, equivalente a `544,0 V`;
- `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) — **não suportado**, retorna `No Such Object available on this agent at this OID`;
- `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) — **não suportado**, retorna a mesma resposta `noSuchObject`.

Por isso, a candidata 1.5.0 mantém corrente e temperatura RFC1628 no template apenas como itens opcionais **desabilitados por padrão**. Eles não participam de dashboard nem triggers de produção e só devem ser habilitados em outra placa/firmware depois de confirmar suporte.

No equipamento validado, a corrente de bateria continua sendo coletada pelo OID privado Vertiv `...1.2.1.4149` (`vertiv.battery.current`), que já foi observado em campo. A temperatura privada `...1.2.1.4156` retornou `-0,1 °C` e permanece desabilitada e sem trigger de produção por ser incompatível com o ambiente observado. O walk também revelou `...1.2.2.4156 = 31,8` e `...1.2.2.4291 = 73`. Esses valores **não representam sensores adicionais**: são a representação em Fahrenheit dos mesmos valores Celsius da instância `.2.1` (`-0,1 °C = 31,8 °F` e `23 °C ≈ 73 °F`). Portanto, não existe evidência de uma segunda temperatura válida de bateria nessa árvore. O gráfico ambiental continua usando apenas a temperatura de entrada validada.

Esse comportamento é um exemplo importante: conformidade com partes da RFC1628 **não implica implementação de todos os escalares do UPS-MIB** pelo agente SNMP.

## Resultado de campo — potência de entrada

A escala dos OIDs privados `6318`, `6319` e `6320` está agora caracterizada para esta placa/firmware. Eles retornaram `1,6`, `1,5` e `1,5`, enquanto os objetos padronizados RFC1628 `upsInputTruePower` retornaram no mesmo equipamento `1600`, `1500` e `1500 W`. Portanto, nesta IS-UNITY-DP 8.5.1.0 os objetos privados representam **kW por fase**.

Como a própria UPS-MIB padronizada fornece a potência real de entrada em watts e já é suportada pelo equipamento, o caminho de produção continua sendo `upsInputTruePower` via LLD. Os OIDs privados `6318-6320` permanecem desabilitados por padrão por serem redundantes e menos portáveis entre modelos/firmwares.

## Resultado de campo — eventos, alarmes e testes

Com o equipamento em estado normal, `upsAlarmsPresent` retornou `0` e a `upsAlarmTable` não apresentou linhas, comportamento esperado. Os objetos privados `.2.100.*` observados retornaram o texto `Inactive Event`; esse estado inativo está portanto confirmado para esta placa/firmware. O texto/encoding do estado **ativo** ainda precisa ser capturado em um evento real antes de criar triggers privados específicos.

O grupo RFC1628 de testes também está presente e respondeu aos objetos de identificação/resultado/tempo. O template usa esses objetos somente para leitura e não inclui nenhum comando para iniciar testes.

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
