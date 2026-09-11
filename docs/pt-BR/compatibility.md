# Matriz de compatibilidade

[English](../en/compatibility.md)

Esta matriz separa **compatibilidade de engenharia** de **homologação em campo**. Um export pode passar na validação estrutural/importação sem comprovar cada OID privado em todos os firmwares.

| Nobreak / placa | Zabbix | Status | Observações |
| --- | --- | --- | --- |
| Vertiv ITA-20kVA / placa usada no desenvolvimento | 7.0 | Baseline derivada de campo; homologação 1.5.0 pendente | Estados principais, valores elétricos, enums textuais e dashboard foram observados em hardware real. O modelo/firmware exato da placa deve ser registrado na rodada de homologação 1.5.0. |
| Outros Vertiv/Liebert / firmwares de placa | 7.0 | Compatível por projeto RFC1628; não certificado em campo | Objetos padrão devem ser portáveis; OIDs privados precisam ser comparados com a UI local do nobreak. |
| Vertiv/Liebert | 8.0 desenvolvimento | Apenas export/paridade semântica | Não é alegação de suporte de produção até importação e execução em uma build 8.0 real. |

## Registro de homologação

Para cada novo equipamento certificado, registre:

- modelo e capacidade nominal do nobreak;
- modelo da placa de gerenciamento;
- firmware do nobreak e da placa;
- versão exata do Zabbix;
- versão/nível de segurança SNMP;
- suporte aos objetos RFC1628 de identificação, corrente/temperatura da bateria, tabela de alarmes e resultado de testes;
- comparação dos valores privados exibidos com LCD/interface web;
- variantes de enums/traps observadas.
