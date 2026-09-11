# Política de segurança

[English](SECURITY.md) | **Português (Brasil)**

## Versões suportadas

Correções de segurança são aplicadas à versão mais recente do projeto na branch `main`.

## Relatando uma vulnerabilidade

Não publique segredos nem credenciais reais de nobreak em uma issue pública.

Inclua somente as informações mínimas necessárias para reproduzir o problema. Remova:

- community strings SNMP;
- usuários SNMPv3 quando forem sensíveis;
- chaves/senhas de autenticação e privacidade;
- endereços IP públicos de gerenciamento;
- hostnames internos quando identificarem um ambiente privado.

Se o problema puder ser descrito com segurança sem informações sensíveis, abra uma issue no GitHub e indique claramente o impacto de segurança.

## Modelo de segurança do projeto

O template mantido foi projetado para **monitoramento SNMP somente leitura**. Ele não inclui reboot, shutdown, chaveamento de tomadas ou outras ações SNMP de escrita.

SNMPv3 com autenticação e privacidade é recomendado quando suportado pelo equipamento. Quando SNMPv2c for necessário, restrinja o acesso à community por IP de origem e política de rede.
