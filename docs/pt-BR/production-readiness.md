# Prontidão para produção e homologação

[English](../en/production-readiness.md)

A versão 1.5.0 foi preparada para entrar em homologação com todo o endurecimento de produção do lado do repositório concluído.

## Gates implementados

- heartbeat dedicado `sysUpTime.0` e alerta SNMP por `nodata()` de cinco minutos;
- aviso de reset do uptime do agente de gerenciamento;
- itens padronizados RFC1628 de identificação e vínculos automáticos de inventário;
- corrente/temperatura de bateria RFC1628 e resultados somente leitura de testes diagnósticos;
- descoberta da tabela de alarmes ativos RFC1628 com value map legível para alarmes conhecidos;
- potência privada de entrada não validada desabilitada por padrão;
- temperatura privada de bateria desabilitada por padrão e retirada dos alertas de produção;
- alarmes de carga baseados em `upsOutputPercentLoad` padronizado por LLD, não no agregado privado;
- gráficos legados enganosos removidos;
- teste de importação pela API de um Zabbix 7 real no CI/workflow de release;
- proveniência das fontes MIB/OID e matriz de compatibilidade.

## Procedimento de homologação

1. Importe o template Zabbix 7 da candidata 1.5.0 com **Update existing** habilitado.
2. Confirme que `ups.snmp.uptime` atualiza a cada minuto e interrompa SNMP brevemente em janela controlada para validar alerta/recuperação de disponibilidade.
3. Compare fabricante/modelo/software/nome RFC1628 com a interface web do nobreak.
4. Compare `ups.battery.current` e `ups.battery.temperature` com a UI; se não forem suportados, registre na matriz de compatibilidade em vez de habilitar a temperatura privada experimental para alertas.
5. Confirme descoberta de entrada/saída/bypass e `upsOutputPercentLoad` por fase.
6. Se for possível gerar uma condição de alarme/teste de bateria com segurança, confirme a descoberta `upsAlarmTable` e os itens RFC1628 de resultados de teste. Não inicie testes por este template.
7. Confirme as páginas Overview, Electrical e Battery & Environment em janelas normal e de incidente.
8. Registre versões exatas de equipamento/placa/firmware/Zabbix na matriz.
9. Somente após esses testes, promova/crie a tag `v1.5.0`.

## Recursos opcionais não bloqueantes

O parsing específico de traps Vertiv não é requisito para monitoramento de produção porque polling e tabela padronizada de alarmes formam o caminho principal de alerta/diagnóstico. O item genérico de traps privados permanece desabilitado até existirem payloads reais documentados.
