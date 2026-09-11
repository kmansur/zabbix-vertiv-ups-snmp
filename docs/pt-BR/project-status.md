# Status do projeto

[English](../en/project-status.md)

**Prontidão da implementação para produção: 100%**

**Homologação em campo: pendente**

A versão **1.5.0** é a candidata endurecida para produção. A nota de 100% significa que todo o trabalho de repositório identificado na revisão crítica foi implementado, protegido por validação automática e não possui bloqueador conhecido de software/documentação. Isso **não** significa que todos os modelos/firmwares Vertiv já foram certificados em campo.

| Área | Nota | Status |
| --- | ---: | --- |
| Estrutura Zabbix 7.0 e comportamento derivado da validação de campo | 25/25 | Completo |
| Dashboard e documentação operacional | 15/15 | Completo |
| Segurança somente leitura e isolamento de métricas experimentais | 15/15 | Completo |
| Disponibilidade, identificação, testes e alarmes ativos RFC1628 | 15/15 | Completo |
| CI, validadores, teste de importação em Zabbix 7 real e gate de release | 15/15 | Completo |
| Proveniência MIB/OID, compatibilidade e procedimento de homologação | 10/10 | Completo |
| Paridade do export Zabbix 8 sem alegar suporte de produção | 5/5 | Completo |

## O que significa 100%

A candidata está pronta para entrar em homologação. Escalas/estados privados do fabricante que não são comprovados não são tratados como dados suportados de produção: ficam desabilitados, isolados ou documentados, sem adivinhação. O parsing específico de traps Vertiv continua fora do caminho crítico até existirem payloads reais; o diagnóstico de alarmes ativos passa a usar a tabela padronizada RFC1628.

## Gate de promoção

Após a homologação em hardware real, faça o merge da candidata no `main`, registre na matriz de compatibilidade as versões exatas de nobreak/placa/firmware/Zabbix, date a entrada 1.5.0 do changelog e crie a tag/release `v1.5.0`.
