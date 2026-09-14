# Prontidão para produção e homologação

[English](../en/production-readiness.md)

A versão 1.5.0 foi preparada para entrar em homologação com todo o endurecimento de produção do lado do repositório concluído. A homologação em hardware continua sendo usada para transformar suposições de compatibilidade em defaults comprovadamente seguros.

## Gates implementados

- heartbeat dedicado `sysUpTime.0` e alerta SNMP por `nodata()` de cinco minutos;
- aviso de reset do uptime do agente de gerenciamento;
- itens padronizados RFC1628 de identificação e vínculos automáticos de inventário;
- resultados somente leitura de testes diagnósticos RFC1628;
- descoberta da tabela de alarmes ativos RFC1628 com value map legível para alarmes conhecidos;
- corrente/temperatura de bateria RFC1628 retidas como itens opcionais **desabilitados por padrão** após a placa homologada retornar `noSuchObject` para ambos;
- corrente de bateria de produção mantida no OID privado Vertiv `4149`, observado em campo;
- temperatura privada de bateria desabilitada por padrão e retirada de dashboard/alertas de produção por retornar aproximadamente `-0,1 °C` no equipamento validado;
- potência privada de entrada não validada desabilitada por padrão;
- alarmes de carga baseados em `upsOutputPercentLoad` padronizado por LLD, não no agregado privado;
- gráficos legados enganosos removidos;
- teste de importação e upgrade pela API de um Zabbix 7 real no CI/workflow de release;
- proveniência das fontes MIB/OID e matriz de compatibilidade.

## Resultado de homologação de bateria

No Vertiv ITA-20kVA usado no desenvolvimento, a placa SNMP implementa parcialmente o grupo de bateria da UPS-MIB. O item `upsBatteryStatus` funciona, enquanto `upsBatteryCurrent` (`.1.3.6.1.2.1.33.1.2.6.0`) e `upsBatteryTemperature` (`.1.3.6.1.2.1.33.1.2.7.0`) retornam `No Such Object available on this agent at this OID`.

A candidata 1.5.0 trata esse comportamento como uma característica de compatibilidade da placa, não como falha de coleta do Zabbix: os dois escalares permanecem disponíveis no template para outras placas/firmwares, mas ficam desabilitados e sem triggers por padrão. Nenhum widget padrão depende deles.

A corrente privada Vertiv (`vertiv.battery.current`, OID final `4149`) já foi observada funcionando no equipamento e permanece no dashboard. Não há trigger padrão de temperatura de bateria até existir um sensor/OID de temperatura validado para o equipamento; para ambiente, o dashboard continua usando a temperatura de entrada confirmada em campo.

## Histórico e planejamento de capacidade

O template prioriza visibilidade operacional de um nobreak, com vários itens de status/bateria coletados a cada 30 segundos e valores elétricos normalmente a cada minuto. Em ambientes com muitos equipamentos, revise a retenção de histórico antes de vincular o template em larga escala.

A quantidade aproximada de amostras brutas gerada por um único item continuamente suportado é:

| Intervalo | Amostras por dia por item |
| --- | ---: |
| 30 s | 2.880 |
| 1 min | 1.440 |
| 2 min | 720 |
| 5 min | 288 |
| 15 min | 96 |
| 1 h | 24 |

Vários itens numéricos mantêm atualmente 90 dias de histórico bruto para que uma instalação nova seja útil sem depender de configuração adicional de housekeeping. Em implantações maiores, use a política global de housekeeping/retenção do Zabbix ou overrides no template/host de acordo com a capacidade do banco. Um padrão prático de produção é manter histórico de alta resolução somente pelo período necessário para análise de incidentes e conservar trends numéricas por mais tempo para capacidade. Itens de identificação/texto/log não se beneficiam de trends numéricas e são configurados dessa forma.

O heartbeat dedicado `ups.snmp.uptime` mantém propositalmente apenas 7 dias de histórico e **não** usa descarte de valores inalterados, pois o trigger de disponibilidade `nodata()` de cinco minutos depende de receber uma amostra em cada ciclo de polling.

## Procedimento de homologação

1. Importe o template Zabbix 7 da candidata 1.5.0 com **Update existing** habilitado.
2. Confirme que `ups.snmp.uptime` atualiza a cada minuto e interrompa SNMP brevemente em janela controlada para validar alerta/recuperação de disponibilidade.
3. Compare fabricante/modelo/software/nome RFC1628 com a interface web do nobreak e registre qualquer objeto padrão não implementado pela placa.
4. Confirme `ups.battery.status`, `vertiv.battery.current`, carga e autonomia. Os itens opcionais `ups.battery.current` e `ups.battery.temperature` devem permanecer desabilitados neste equipamento, pois o comportamento `noSuchObject` já foi comprovado.
5. Confirme descoberta de entrada/saída/bypass e `upsOutputPercentLoad` por fase.
6. Se for possível gerar uma condição de alarme/teste de bateria com segurança, confirme a descoberta `upsAlarmTable` e os itens RFC1628 de resultados de teste. Não inicie testes por este template.
7. Confirme as páginas Overview, Electrical e Battery & Environment em janelas normal e de incidente.
8. Registre versões exatas de equipamento/placa/firmware/Zabbix na matriz.
9. Somente após esses testes, promova/crie a tag `v1.5.0`.

## Recursos opcionais não bloqueantes

O parsing específico de traps Vertiv não é requisito para monitoramento de produção porque polling e tabela padronizada de alarmes formam o caminho principal de alerta/diagnóstico. O item genérico de traps privados permanece desabilitado até existirem payloads reais documentados.
