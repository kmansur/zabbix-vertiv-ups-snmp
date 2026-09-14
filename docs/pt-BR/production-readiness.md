# Prontidão para produção e homologação

[English](../en/production-readiness.md)

A versão 1.5.0 é a release estável atual. Os gates de segurança, validação, CI e segurança de código do repositório foram aprovados e o mantenedor aprovou a release de software em 14/09/2026.

Checks controlados adicionais em hardware continuam em andamento e estão registrados em [Registro de validação em campo — 1.5.0](homologation-1.5.0.md). Esses testes refinam a evidência de compatibilidade específica do equipamento e não devem ser confundidos com o gate da release de software.

## Gates implementados no repositório

- heartbeat dedicado `sysUpTime.0` e alerta SNMP por `nodata()` de cinco minutos;
- aviso de reset do uptime do agente de gerenciamento;
- itens padronizados RFC1628 de identificação e vínculos automáticos de inventário;
- resultados somente leitura de testes diagnósticos RFC1628 e respectivas triggers de resultado;
- descoberta da tabela de alarmes ativos RFC1628 com value map legível para alarmes conhecidos;
- corrente/temperatura de bateria RFC1628 retidas como itens opcionais **desabilitados por padrão** após a placa de referência retornar `noSuchObject` para ambos;
- corrente de bateria de produção mantida no OID privado Vertiv `4149`, observado em campo;
- temperatura privada de bateria desabilitada por padrão e retirada de dashboard/alertas de produção por retornar aproximadamente `-0,1 °C` no equipamento de referência;
- potência privada de entrada desabilitada por padrão mesmo após caracterização da escala, pois a potência real padronizada RFC1628 é preferida;
- alarmes de carga baseados em `upsOutputPercentLoad` padronizado por LLD, não no agregado privado;
- gráficos legados enganosos removidos;
- teste de importação nova e upgrade pela API de um Zabbix 7 real no CI/workflow de release;
- proveniência das fontes MIB/OID e matriz de compatibilidade;
- validação da documentação contra triggers, macros, versão e política de release atuais do template;
- análise de segurança CodeQL no caminho de release.

## Resultado de campo da bateria

No Vertiv ITA-20kVA usado no desenvolvimento, a placa SNMP implementa parcialmente o grupo de bateria da UPS-MIB. `upsBatteryStatus`, carga, autonomia e tensão funcionam, enquanto `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) e `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) retornam `No Such Object available on this agent at this OID`.

A release 1.5.0 trata esse comportamento como característica de compatibilidade da placa, não como falha de coleta do Zabbix: os dois escalares permanecem disponíveis para outras placas/firmwares, mas ficam desabilitados e sem triggers por padrão. Nenhum widget padrão depende deles.

A corrente privada Vertiv (`vertiv.battery.current`, OID final `4149`) já foi observada funcionando no equipamento e permanece no dashboard. Não existe trigger padrão de temperatura da bateria até haver sensor/OID de temperatura suportado e validado para o equipamento alvo.

## Histórico e planejamento de capacidade

O template prioriza visibilidade operacional de um nobreak, com vários itens de status/bateria coletados a cada 30 segundos e valores elétricos normalmente a cada minuto. Em ambientes com muitos equipamentos, revise a retenção de histórico/trends do Zabbix antes de vincular o template em larga escala.

A quantidade aproximada de amostras brutas gerada por um único item continuamente suportado é:

| Intervalo | Amostras por dia por item |
| --- | ---: |
| 30 s | 2.880 |
| 1 min | 1.440 |
| 2 min | 720 |
| 5 min | 288 |
| 15 min | 96 |
| 1 h | 24 |

O heartbeat dedicado `ups.snmp.uptime` mantém propositalmente apenas 7 dias de histórico e **não** usa descarte de valores inalterados, pois a trigger de disponibilidade `nodata()` de cinco minutos depende de receber uma amostra em cada ciclo de polling.

## Procedimento de validação em campo pós-release

Os checks controlados abaixo continuam após a release de software e servem para fortalecer a alegação de compatibilidade do hardware de referência:

1. Confirmar que `ups.snmp.uptime` atualiza a cada minuto e validar problema/recuperação de disponibilidade após interrupção SNMP controlada por cinco minutos.
2. Comparar fabricante/modelo/software/nome RFC1628 com a interface web e registrar objetos padrão não implementados.
3. Confirmar status da bateria, corrente privada validada, carga e autonomia; manter os dois escalares RFC1628 não suportados desabilitados nessa placa/firmware.
4. Confirmar descoberta de entrada/saída/bypass e `upsOutputPercentLoad` por fase.
5. Durante um alarme real seguro, confirmar descoberta e recuperação de `upsAlarmTable`.
6. Durante uma transição segura de resultado de teste diagnóstico/bateria, confirmar itens/triggers somente leitura. Não iniciar testes pelo template.
7. Revisar Overview, Electrical e Battery & Environment em janelas normal e representativa de incidente.
8. Registrar nível de segurança SNMP e versões exatas de nobreak/placa/firmware/Zabbix.
9. Concluir e aprovar [o registro de validação em campo](homologation-1.5.0.md).

A conclusão desses testes poderá elevar a redação de compatibilidade dessa combinação exata de hardware para **homologada em campo**. Até lá, a release permanece estável como software, com limitação explícita na alegação de certificação específica do equipamento.

## Recursos opcionais não bloqueantes

O parsing específico de traps Vertiv não é requisito para monitoramento de produção porque polling e tabela padronizada de alarmes formam o caminho principal de alerta/diagnóstico. O item genérico de traps privados permanece desabilitado até existirem payloads reais documentados.
