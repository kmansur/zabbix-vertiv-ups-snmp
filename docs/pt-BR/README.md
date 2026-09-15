# Visão geral

[English](../en/README.md)

`Vertiv by SNMP` foi desenvolvido para oferecer monitoramento prático, seguro e transparente de nobreaks Vertiv/Liebert no Zabbix.

O template utiliza dois espaços de OIDs SNMP:

- **RFC 1628 UPS-MIB** — `1.3.6.1.2.1.33`, utilizado para medições padronizadas de UPS e tabelas de linhas;
- **MIB privada Vertiv/Liebert** — `1.3.6.1.4.1.476.1.42`, utilizada para status, identificação, bateria, ambiente e métricas elétricas detalhadas específicas do fabricante.

## Objetivos do projeto

1. **Monitoramento somente leitura.** Nenhum OID de reboot, shutdown, controle de tomadas ou escrita de configuração é incluído.
2. **Monitoramento elétrico portátil.** Objetos padronizados da UPS-MIB são preferidos quando possuem unidades e semântica claramente definidas.
3. **Detalhes do fabricante quando úteis.** OIDs Vertiv adicionam status do sistema, autoteste, estado de carga, energia, ambiente, qualidade e métricas elétricas fixas por fase.
4. **Descoberta dinâmica mais resumo determinístico.** A LLD continua disponível para portabilidade, enquanto chaves fixas L-N/L-L e por fase facilitam dashboards previsíveis.
5. **Sem inventar escala.** OIDs privados cuja escala SNMP não está documentada são armazenados sem multiplicadores presumidos e precisam ser comparados com a interface do nobreak.
6. **Padrões seguros.** Limites de triggers são expostos como macros e podem ser sobrescritos por template, grupo de hosts ou host.
7. **Manutenção rastreável.** Os exports Zabbix 7.0 e 8.0 são versionados separadamente e validados para manter equivalência semântica.

## Observação importante sobre compatibilidade

Produtos e placas de gerenciamento Vertiv/Liebert podem expor subconjuntos diferentes da MIB privada. Um item ficar unsupported não significa automaticamente que o template está incorreto; o equipamento pode não implementar aquele OID.

Após a primeira importação, compare os valores do Zabbix com o LCD/interface web do nobreak e revise os itens unsupported. Isso é especialmente importante para objetos privados do fabricante. Consulte [Resumo elétrico](electrical-summary.md), [Matriz de compatibilidade](compatibility.md) e [Troubleshooting](troubleshooting.md).

## Versão do projeto

Versão atual do repositório: **1.5.3**.

Última versão estável: **1.5.3**.

A release 1.5.1 adiciona o gerador opcional de dashboard global, documentação bilíngue e testes sem alterar a semântica de monitoramento da 1.5.0. O mantenedor validou com sucesso o fluxo `--dry-run` em um ambiente Zabbix 7.0 real. O caminho de substituição foi endurecido para atualizar in-place um único dashboard editável de mesmo nome e falhar de forma segura em caso de ambiguidade.

A branch `main` é a branch ativa de desenvolvimento. Para produção, utilize uma GitHub Release com tag em vez de tratar o conteúdo atual da `main` como um artefato imutável de release.

A versão 1.5.0 passou pela validação do repositório, CodeQL, importação nova no Zabbix 7.0 e teste de upgrade in-place 1.4.1 → 1.5.0. Cenários controlados adicionais em hardware continuam sendo acompanhados separadamente e não são apresentados como certificação de campo concluída.

Consulte [Versionamento](versioning.md), [Status do projeto](project-status.md), [Dashboard global](global-dashboard.md), [Revisão PDCA 1.5.1](pdca-1.5.1.md) e o [CHANGELOG](../../CHANGELOG.pt-BR.md).

- [Fontes MIB/OID e proveniência](mib-sources.md)
- [Matriz de compatibilidade](compatibility.md)
- [Prontidão para produção e homologação](production-readiness.md)

## Acompanhamento da release atual

Candidata atual do repositório: **1.5.3**. Última release estável: **1.5.3**. A 1.5.2 é um patch de licenciamento/atribuição e metadados; a semântica de monitoramento permanece igual à 1.5.1.
