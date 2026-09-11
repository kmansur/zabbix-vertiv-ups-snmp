# Visão geral

[English](../en/README.md)

`VERTIV by SNMP` foi desenvolvido para oferecer monitoramento prático, seguro e transparente de nobreaks Vertiv/Liebert no Zabbix.

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

Após a primeira importação, compare os valores do Zabbix com o LCD/interface web do nobreak e revise os itens unsupported. Isso é especialmente importante para os objetos elétricos privados adicionados na versão 1.1.0. Consulte [Resumo elétrico](electrical-summary.md) e [Troubleshooting](troubleshooting.md).

## Versão do projeto

Versão atual: **1.1.0**.

Consulte [Versionamento](versioning.md) e o [CHANGELOG](../../CHANGELOG.pt-BR.md).
