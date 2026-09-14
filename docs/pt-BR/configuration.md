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
| {$UPS.LOAD.WARN} | 80 | Limite de aviso de carga por linha de saída, em %. Usado pelos protótipos de trigger RFC1628 via LLD. |
| {$UPS.LOAD.CRIT} | 95 | Limite crítico de carga por linha de saída, em %. Usado pelos protótipos de trigger RFC1628 via LLD. |
| {$UPS.BATTERY.TEMP.WARN} | 35 | Limite reservado de aviso de temperatura da bateria. Nenhuma trigger padrão de produção da 1.5.0 utiliza esta macro atualmente. |
| {$UPS.BATTERY.TEMP.CRIT} | 40 | Limite reservado crítico de temperatura da bateria. Nenhuma trigger padrão de produção da 1.5.0 utiliza esta macro atualmente. |
| {$UPS.INLET.TEMP.WARN} | 30 | Limite de aviso da temperatura do ar de entrada, em °C. |
| {$UPS.INLET.TEMP.CRIT} | 35 | Limite crítico da temperatura do ar de entrada, em °C. |

As macros de temperatura da bateria são mantidas intencionalmente por compatibilidade e para futuros perfis de equipamento. Elas **não** habilitam alertas de temperatura da bateria por si só. No equipamento usado na homologação atual, o objeto RFC1628 `upsBatteryTemperature` não é suportado e o valor privado Vertiv de temperatura da bateria não é confiável para alertamento padrão de produção.

## Fluxo recomendado de ajuste

1. Observe os valores normais por alguns dias.
2. Confirme a carga esperada do nobreak em condições normais e degradadas.
3. Confirme a autonomia necessária para o local.
4. Ajuste os limites de aviso e crítico da autonomia.
5. Ajuste os limites de temperatura de entrada conforme os limites operacionais do nobreak e o projeto do ambiente.
6. Sobrescreva macros no host quando modelos de nobreak ou bancos de bateria forem diferentes.
7. Não crie alertas de temperatura da bateria a partir das macros reservadas até confirmar um sensor/OID confiável na placa/firmware alvo.

## Comportamento dos limites

As triggers de autonomia e carga da bateria são avaliadas somente quando `UPS: Output source` informa **Battery**. Isso evita incidentes de bateria baixa durante estados normais de carga ou manutenção.

As triggers de carga usam a descoberta de linhas de saída RFC1628 (`upsOutputPercentLoad`). O item privado agregado `vertiv.output.load` não gera triggers padrão de produção.

As triggers de temperatura do ar de entrada utilizam faixas sem sobreposição para que o evento de aviso não permaneça ativo quando o limite crítico for atingido.

## Credenciais SNMP

Credenciais não são armazenadas no template. Configure-as na interface SNMP do Zabbix ou utilizando a estratégia padrão de macros/credenciais do seu ambiente.

Prefira autenticação e privacidade SNMPv3 quando disponíveis.
