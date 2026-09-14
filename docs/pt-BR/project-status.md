# Status do projeto

[English](../en/project-status.md)

**Prontidão do repositório: PASS**

**Validação de importação/upgrade no Zabbix 7.0: PASS**

**Homologação em campo: EM ANDAMENTO**

**Gate de release para produção: BLOQUEADO até concluir a homologação**

A versão **1.5.0** é a candidata atual endurecida para produção. Os controles estruturais, de segurança, documentação e CI do repositório estão implementados e validados automaticamente, mas o status deixou de ser expresso como percentual porque completude do repositório não equivale a certificação em hardware real.

| Área | Status | Observações |
| --- | --- | --- |
| Estrutura do template Zabbix 7.0 | PASS | Validadores estruturais/do template passam |
| Importação nova e upgrade via API no Zabbix 7.0 | PASS | O CI importa a baseline estável e atualiza para a candidata |
| Segurança somente leitura | PASS | Famílias conhecidas de OIDs de controle/escrita são proibidas pelos validadores/testes |
| Isolamento de métricas privadas/experimentais | PASS | Valores não validados não podem gerar alertas padrão de produção |
| Verificação semântica documentação/template | PASS | Versões, tabelas de triggers, macros, pares bilíngues e política de release são validados |
| Identificação, heartbeat, testes e diagnóstico de alarmes RFC1628 | PASS | Implementados na candidata |
| Registro de compatibilidade em campo | EM ANDAMENTO | Um ambiente Vertiv ITA-20kVA / IS-UNITY-DP é a referência atual de homologação |
| Zabbix 8.0 | PREVIEW | Apenas paridade de export; sem alegação de suporte de produção |
| Release de produção `v1.5.0` | BLOQUEADO | Requer registro de homologação em campo concluído |

## Modelo de branch/release

A `main` é a branch ativa de desenvolvimento/candidato. `VERSION` identifica a candidata atual do repositório e `STABLE_VERSION` identifica a última release estável com tag. Para produção, utilize uma GitHub Release com tag.

## Gate de promoção

A candidata `1.5.0` só pode ser promovida quando o registro de homologação em campo estiver completo e todos os checks obrigatórios estiverem em PASS. Nesse momento:

1. atualize a matriz de compatibilidade com versões exatas do nobreak/placa/firmware/Zabbix e o resultado final;
2. encerre todos os itens obrigatórios pendentes no registro de homologação;
3. coloque a data na entrada `1.5.0` do changelog;
4. atualize `STABLE_VERSION` para `1.5.0` na alteração de release;
5. crie a tag/release `v1.5.0` somente depois que as validações de CI/release forem aprovadas.

A candidata já é desenvolvida na `main`; não existe etapa separada de merge de uma branch candidata para `main` neste modelo de repositório.
