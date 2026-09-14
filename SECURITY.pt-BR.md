# Política de segurança

[English](SECURITY.md) | **Português (Brasil)**

## Versões suportadas

A última release estável com tag identificada por `STABLE_VERSION` é a baseline suportada em produção. Correções de segurança são desenvolvidas na `main`, que é a branch ativa de desenvolvimento/candidato, e são publicadas por uma GitHub Release com tag após validação.

Quando um problema de segurança exigir correção urgente, o projeto pode publicar uma release patch a partir da baseline estável apropriada, em vez de tratar uma candidata ainda não lançada na `main` como suportada em produção.

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

## Objetos RFC1628 read-write

Alguns objetos padronizados, como `upsIdentName`, são definidos pelo RFC1628 como read-write. O template apenas os consulta por SNMP GET. Objetos de controle da UPS-MIB (`1.3.6.1.2.1.33.1.8`) e os objetos usados para iniciar/abortar testes (`upsTestId`/`upsTestSpinLock`) não fazem parte da lógica de controle deste projeto. A candidata 1.5.0 lê somente os objetos de **resultado** dos testes.

Métricas privadas com escala/semântica não comprovada ficam desabilitadas por padrão e não alimentam alertas críticos.
