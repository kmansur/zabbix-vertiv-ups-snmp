# Resumo elétrico

[English](../en/electrical-summary.md)

A versão **1.1.0** adiciona itens elétricos fixos preparados para dashboards, mantendo as regras de descoberta de baixo nível da RFC 1628. As chaves fixas foram criadas para permitir dashboards previsíveis, telas de troubleshooting e comparação direta com o resumo apresentado pela interface web/LCD do nobreak.

## Política de escala

Os objetos da RFC 1628 utilizam as escalas definidas pela UPS-MIB. Por exemplo, `upsOutputFrequency` é informado em décimos de hertz e o template aplica multiplicador `0.1`.

A lista de parâmetros SNMP Vertiv fornecida identifica os objetos elétricos privados, mas **não** define a escala numérica de todos os objetos `1.3.6.1.4.1.476.1.42...`. Por isso o template não inventa multiplicadores para esses itens privados. Compare os valores com o LCD/interface web do nobreak antes de criar limites ou dashboards que dependam do valor absoluto.

Isso é intencional: o mapa Modbus fornecido contém escalas dos registradores Modbus, mas isso não prova que a representação SNMP utilize a mesma escala bruta.

## Frequência de saída padronizada

| Chave | OID | Unidade | Observação |
| --- | --- | --- | --- |
| `ups.output.frequency` | `1.3.6.1.2.1.33.1.4.2.0` | Hz | RFC 1628, multiplicador `0.1` |

## Resumo da entrada

| Família de chaves | Medição / OIDs |
| --- | --- |
| `vertiv.input.voltage.l1n/l12/l2n/l23/l3n/l31` | Tensões L-N/L-L, OIDs `4096`-`4101` |
| `vertiv.input.frequency` | Frequência da entrada, OID `4105` |
| `vertiv.input.current.l1/.l2/.l3` | Corrente, OIDs `4113`-`4115` |
| `vertiv.input.pf.l1/.l2/.l3` | Fator de potência, OIDs `4116`-`4118` |
| `vertiv.input.power.l1/.l2/.l3` | Potência real, OIDs `6318`-`6320` |
| `vertiv.input.power.total` | Soma calculada das três potências de fase da entrada |

## Resumo do bypass

`vertiv.bypass.voltage.l12/.l23/.l31/.l1n/.l2n/.l3n` corresponde aos OIDs Vertiv `4125`-`4130`. O item RFC 1628 já existente `ups.bypass.frequency` continua sendo a métrica fixa principal da frequência do bypass.

## Resumo da saída

| Família de chaves | Medição / OIDs |
| --- | --- |
| `vertiv.output.voltage.l12/.l23/.l31` | Tensão L-L, OIDs `4201`-`4203` |
| `vertiv.output.voltage.l1n/.l2n/.l3n` | Tensão L-N, OIDs `4385`-`4387` |
| `vertiv.output.current.l1/.l2/.l3` | Corrente, OIDs `4204`-`4206` |
| `vertiv.output.pf.l1/.l2/.l3` | Fator de potência, OIDs `4210`-`4212` |
| `vertiv.output.load.l1/.l2/.l3` | Percentual de potência/carga, OIDs `4223`-`4225` |
| `vertiv.output.power.l1/.l2/.l3` | Potência real, OIDs `5859`, `5860`, `5959` |
| `vertiv.output.apparent.power.l1/.l2/.l3` | Potência aparente, OIDs `5868`-`5870` |

O prefixo privado completo para os IDs numéricos acima é `1.3.6.1.4.1.476.1.42.3.9.20.1.20.1.2.1`.

Esses itens fixos coexistem intencionalmente com os itens LLD da RFC 1628. A LLD continua importante para portabilidade e descoberta automática de linhas; as chaves privadas fixas fornecem nomes determinísticos para dashboards e análise elétrica específica do equipamento.

## Metadados de bateria adicionados na 1.1.0

| Chave | OID | Valores |
| --- | --- | --- |
| `vertiv.battery.cabinet.type` | `...2.1.6183` | Internal, External, LRT |
| `vertiv.battery.test.interval` | `...2.1.5805` | 8, 12, 16, 20 ou 26 semanas |

## Gráficos de produção

- **UPS: Output phase load**.

O gráfico privado **UPS: Input phase power** foi removido da candidata 1.5.0 porque seus OIDs de origem permanecem sem escala SNMP comprovada. Os itens privados de potência de entrada ficam desabilitados por padrão.

## OIDs de condições/eventos: identificados, mas ainda não ativados

Os arquivos Vertiv fornecidos identificam objetos úteis na árvore privada `.2.100.*`, incluindo bateria baixa/em descarga, bypass indisponível, saída desligada, falha de inversor, falha de ventilador, falha do carregador, substituir bateria, sobrecarga de saída e falha de cabeamento de entrada.

Entretanto, os arquivos fornecidos não definem a codificação numérica do estado retornado ao consultar esses objetos. Por isso a versão 1.1.0 **não** inventa interpretação `0/1`, `3/6` ou qualquer outra e não cria triggers específicas de polling para esses eventos.

No próximo passo de validação, consulte um nobreak representativo em condição normal e, quando for seguro, durante uma condição conhecida. Depois de confirmarmos os estados retornados, esses OIDs podem ser promovidos para itens e triggers suportados.

## Limitação conhecida de escala

Os OIDs privados Vertiv de potência de entrada (`6318`-`6320`) são mantidos para troubleshooting, mas a escala numérica não é definida pela lista de parâmetros SNMP fornecida. No equipamento atualmente testado, o total calculado não apresentou magnitude compatível com a interface web do nobreak. Por isso o card/gráfico de potência de entrada não é destacado no dashboard nativo e nenhum trigger deve depender desses valores até que a escala seja confirmada no firmware alvo.
