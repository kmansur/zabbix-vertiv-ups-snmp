# Versionamento

[English](../en/versioning.md)

Este projeto utiliza **Versionamento Semântico** (`MAJOR.MINOR.PATCH`).

Candidata atual do repositório:

```text
1.5.0
```

Última release estável:

```text
1.4.1
```

`VERSION` é a fonte de verdade da candidata atual do repositório. `STABLE_VERSION` é a fonte de verdade da última release estável com tag.

## Modelo de branch/release

A `main` é a branch ativa de desenvolvimento/candidato. Em produção, utilize GitHub Releases com tag. Portanto é válido que `VERSION` na `main` seja mais novo que `STABLE_VERSION` enquanto uma candidata estiver em validação/homologação.

Uma candidata só se torna estável depois de concluir o gate de promoção definido em [Status do projeto](project-status.md) e [Prontidão para produção](production-readiness.md).

## Regras

- **PATCH** — correções retrocompatíveis, correções de documentação e ajustes de triggers que não alterem chaves/macros públicas;
- **MINOR** — novas métricas compatíveis, triggers, gráficos, compatibilidade com equipamentos ou funcionalidades opcionais;
- **MAJOR** — alterações incompatíveis em chaves de itens, nomes de macros, identidade do template, instalação obrigatória ou comportamento do monitoramento.

## Consistência da release

Os identificadores da release usam Versionamento Semântico (`X.Y.Z`), enquanto os metadados do template Zabbix usam o formato de vendor equivalente (`X.Y-Z`).

```text
VERSION: X.Y.Z
STABLE_VERSION: última versão estável X.Y.Z com tag
templates/7.0/... vendor.version: X.Y-Z
templates/8.0/... vendor.version: X.Y-Z
Tag Git: vX.Y.Z
GitHub Release: vX.Y.Z
```

A candidata `1.5.0` é exportada como `vendor.version: 1.5-0`. O workflow de release valida a tag contra `VERSION` e valida os dois exports antes de publicar uma release.

Quando `v1.5.0` for efetivamente promovida e publicada, a alteração de release também deverá atualizar `STABLE_VERSION` de `1.4.1` para `1.5.0`.

## Compatibilidade Zabbix não define a versão do projeto

A versão do projeto descreve este repositório. A versão do export Zabbix (`7.0` ou `8.0`) descreve o formato de configuração de destino.

Portanto a mesma versão de projeto pode existir simultaneamente nos exports Zabbix 7.0 e Zabbix 8.0.

## Identificador técnico estável

A partir da 1.4.0 o nome visível do template é **Vertiv by SNMP**, enquanto o identificador técnico do export permanece `VERTIV by SNMP`. Manter o identificador técnico estável é intencional: isso permite atualizar instalações existentes sem criar um segundo template apenas por causa da capitalização.
