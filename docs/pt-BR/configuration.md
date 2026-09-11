# Configuração e macros

[English](../en/configuration.md)

O template não exige scripts personalizados. Todo o monitoramento é realizado pela interface SNMP do host.

## Macros de usuário

| Macro | Padrão | Descrição |
| --- | --- | --- |
| {$UPS.RUNTIME.WARN} | 10 | Limite de aviso de autonomia da bateria, em minutos. |
| {$UPS.RUNTIME.CRIT} | 5 | Limite crítico de autonomia da bateria, em minutos. |
| {$UPS.BATTERY.CHARGE.WARN} | 40 | Limite de aviso da carga da bateria, em %. Aplicado quando o nobreak está em bateria. |
| {$UPS.BATTERY.CHARGE.CRIT} | 20 | Limite crítico da carga da bateria, em %. Aplicado quando o nobreak está em bateria. |
| {$UPS.LOAD.WARN} | 80 | Limite de aviso de carga do nobreak, em %. |
| {$UPS.LOAD.CRIT} | 95 | Limite crítico de carga do nobreak, em %. |
| {$UPS.BATTERY.TEMP.WARN} | 35 | Limite de aviso de temperatura da bateria, em °C. |
| {$UPS.BATTERY.TEMP.CRIT} | 40 | Limite crítico de temperatura da bateria, em °C. |
| {$UPS.INLET.TEMP.WARN} | 30 | Limite de aviso da temperatura do ar de entrada, em °C. |
| {$UPS.INLET.TEMP.CRIT} | 35 | Limite crítico da temperatura do ar de entrada, em °C. |

## Fluxo recomendado de ajuste

1. Observe os valores normais por alguns dias.
2. Confirme a carga esperada do nobreak em condições normais e degradadas.
3. Confirme a autonomia necessária para o local.
4. Ajuste os limites de aviso e crítico da autonomia.
5. Ajuste os limites de temperatura conforme os limites operacionais do fabricante e o projeto da sala.
6. Sobrescreva macros no host quando modelos de nobreak ou bancos de bateria forem diferentes.

## Comportamento dos limites

As triggers de autonomia e carga da bateria são avaliadas somente quando `UPS: Output source` informa **Battery**. Isso evita incidentes de bateria baixa durante estados normais de carga ou manutenção.

As triggers de aviso de carga e temperatura usam faixas sem sobreposição para que o evento de aviso não permaneça ativo quando o limite crítico for atingido.

## Credenciais SNMP

Credenciais não são armazenadas no template. Configure-as na interface SNMP do Zabbix ou utilizando a estratégia padrão de macros/credenciais do seu ambiente.

Prefira autenticação e privacidade SNMPv3 quando disponíveis.
