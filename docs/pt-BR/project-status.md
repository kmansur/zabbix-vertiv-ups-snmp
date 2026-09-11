# Status do projeto

[English](../en/project-status.md)

**Maturidade atual do projeto: 85%**

Esse percentual é uma pontuação mantida de maturidade de engenharia, e não uma métrica de disponibilidade/SLA. Ele reflete o estado do template, validação em campo, automação e documentação.

| Área | Pontuação | Observações |
| --- | ---: | --- |
| Template principal Zabbix 7.0 e validação em equipamento real | 30/30 | Importação, coleta, normalização de enums e dashboard validados em hardware Vertiv real |
| Dashboard e usabilidade operacional | 15/15 | Dashboard nativo, cores por criticidade, estados mapeados legíveis e gráficos de tendência |
| Documentação, versionamento, CI e automação de segurança | 20/20 | Documentação bilíngue, validadores, pytest, Ruff, CodeQL e automação de release |
| Segurança somente leitura e exclusão de OIDs de controle | 10/10 | Ramos/OIDs de escrita consequencial são explicitamente excluídos e validados |
| Validação de escala elétrica privada | 5/10 | A maioria dos valores exibidos é coerente; a escala da potência privada de entrada ainda precisa de confirmação |
| Cobertura de modelos/firmwares | 3/5 | Um equipamento/placa de produção foi validado em profundidade; falta ampliar a cobertura |
| Processamento específico de traps SNMP | 0/5 | Aguardando captura de payloads reais antes de criar parsers/triggers específicos |
| Validação em execução no Zabbix 8.0 | 2/5 | A paridade do export é automatizada, mas ainda falta testar importação/execução em um Zabbix 8 real |

## Principais trabalhos restantes

1. Validar a escala dos OIDs privados de potência de entrada contra a interface web/LCD do nobreak antes de usar essas métricas em alertas.
2. Capturar traps Vertiv reais e implementar processamento específico somente a partir de codificações confirmadas.
3. Validar modelos adicionais de nobreak e firmwares de placas de gerenciamento.
4. Importar e testar em execução o export 8.0 em um ambiente Zabbix 8 real.
5. Validar a importação do mapa sinótico opcional em ambientes Zabbix 7/8 semelhantes à produção.
