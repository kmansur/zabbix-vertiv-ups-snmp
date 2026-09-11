# Arquitetura SNMP

[English](../en/snmp.md)

## Espaços de OIDs

### RFC 1628 UPS-MIB

OID base:

```text
1.3.6.1.2.1.33
```

Utilizado para identificação/configuração padronizada do nobreak, status da bateria, autonomia, medições de entrada/saída, bypass e tabelas de linhas.

### MIB privada Vertiv/Liebert

OID base:

```text
1.3.6.1.4.1.476.1.42
```

Utilizado para identificação da placa de gerenciamento, status do sistema, estado do inversor, detalhes de bateria, autoteste, energia, medições ambientais, motivo de shutdown e contadores de qualidade de energia.

## Por que utilizar as duas

A RFC 1628 fornece semântica e escala estáveis para dados comuns de UPS. A árvore privada Vertiv expõe detalhes que não estão disponíveis na MIB padrão.

O uso conjunto amplia o monitoramento e evita substituir dados padronizados por OIDs privados quando já existe uma representação padrão clara.

## Política somente leitura

O projeto não inclui operações SNMP SET nem itens destinados a controlar o nobreak.

Exemplos deliberadamente excluídos:

- reboot do agente;
- reboot atrasado do nobreak;
- shutdown/startup atrasado;
- controle de grupo de tomadas;
- comandos de teste manual da bateria;
- reset de estatísticas de energia;
- controle do alarme sonoro.

Isso mantém o monitoramento rotineiro separado de operações de controle com impacto no equipamento.

## Estratégia de polling

- status e estado da bateria: normalmente 30 segundos a 1 minuto;
- temperaturas e valores elétricos: normalmente 1–2 minutos;
- contadores e estado de autoteste: normalmente 5 minutos;
- energia: 15 minutos;
- identificação e configuração nominal: 1 hora.

## Traps SNMP

Um item de trap desabilitado é fornecido para a árvore privada Vertiv. Antes de habilitá-lo:

1. configure a recepção de traps no Zabbix Server/Proxy;
2. configure o nobreak para enviar traps ao receptor;
3. capture traps reais do modelo utilizado;
4. documente o payload;
5. somente então adicione preprocessing e triggers específicos dos eventos.

Isso evita assumir incorretamente o formato de trap das diferentes placas de gerenciamento.

## Disponibilidade e diagnóstico padronizado na candidata 1.5.0

- `sysUpTime.0` (`1.3.6.1.2.1.1.3.0`) é coletado a cada minuto sem descarte de valores repetidos e alimenta o trigger de indisponibilidade SNMP por `nodata(5m)`.
- `upsAlarmTable` (`1.3.6.1.2.1.33.1.6.2`) é descoberta dinamicamente para identificar alarmes ativos pelo OID de descrição.
- `upsTestResultsSummary/Detail/StartTime/ElapsedTime` são lidos para diagnosticar testes; os objetos de comando `upsTestId`/`upsTestSpinLock` não são usados para iniciar testes.
