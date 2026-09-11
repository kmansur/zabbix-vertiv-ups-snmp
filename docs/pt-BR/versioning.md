# Versionamento

[English](../en/versioning.md)

Este projeto utiliza **Versionamento Semântico** (`MAJOR.MINOR.PATCH`).

Versão atual:

```text
1.1.0
```

## Regras

- **PATCH** — correções compatíveis, correções de documentação e ajustes de triggers que não alterem chaves/macros públicas;
- **MINOR** — novas métricas compatíveis, triggers, gráficos, compatibilidade com equipamentos ou funcionalidades opcionais;
- **MAJOR** — alterações incompatíveis em chaves de itens, nomes de macros, identidade do template, instalação obrigatória ou comportamento do monitoramento.

A versão **1.1.0** é uma release MINOR porque adiciona itens elétricos de resumo, value maps, gráficos e documentação de forma retrocompatível, sem alterar chaves ou macros públicas existentes.

## Consistência da release

Os identificadores da release usam Versionamento Semântico (`X.Y.Z`), enquanto os metadados do template Zabbix usam o formato de vendor equivalente (`X.Y-Z`).

```text
VERSION: X.Y.Z
templates/7.0/... vendor.version: X.Y-Z
templates/8.0/... vendor.version: X.Y-Z
Tag Git: vX.Y.Z
GitHub Release: vX.Y.Z
```

Por exemplo, a versão `1.1.0` do projeto é exportada como `vendor.version: 1.1-0`. O workflow de release valida a tag contra `VERSION` e valida os dois exports antes de publicar o pacote da release.

## Compatibilidade Zabbix não define a versão do projeto

A versão do projeto descreve este repositório. A versão do export Zabbix (`7.0` ou `8.0`) descreve o formato de configuração de destino.

Portanto a versão de projeto `1.1.0` pode existir simultaneamente nos exports Zabbix 7.0 e Zabbix 8.0.
