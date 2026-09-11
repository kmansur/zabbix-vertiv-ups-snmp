# Compatibilidade com Zabbix 8.0

[English](../en/zabbix-8.0.md)

O repositório contém um export separado em:

```text
templates/zabbix-8.0/vertiv-by-snmp.yaml
```

A documentação atual da Zabbix identifica a versão 8.0 como versão em desenvolvimento. O arquivo 8.0 utiliza export version `8.0` e é mantido semanticamente alinhado ao template 7.0.

## Status atual

- validação YAML e estrutural do projeto: **habilitada no CI**;
- paridade semântica com o export 7.0: **habilitada no CI**;
- importação real no frontend Zabbix 8.0: **deve ser confirmada no build utilizado**;
- coleta contra um nobreak Vertiv real: **deve ser confirmada por modelo/placa/firmware**.

## Por que os exports são separados

A serialização dos exports Zabbix pode mudar entre versões major. Manter arquivos separados permite:

- preservar a versão exata do export;
- documentar a validação contra builds específicos do Zabbix;
- adotar futuramente campos exclusivos do Zabbix 8 sem quebrar o Zabbix 7.0;
- manter UUIDs, chaves, macros e comportamento funcional estáveis entre as versões.

Quando o Zabbix 8.0 chegar a RC/final e este template for testado, atualize este documento e a tabela de compatibilidade dos dois READMEs principais.
