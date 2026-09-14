# Versionamento

[English](../en/versioning.md)

Este projeto utiliza **Versionamento Semântico** (`MAJOR.MINOR.PATCH`).

Versão atual do repositório:

```text
1.5.0
```

Última release estável:

```text
1.5.0
```

`VERSION` é a fonte de verdade da versão/candidata atual do repositório. `STABLE_VERSION` é a fonte de verdade da última release estável com tag.

## Modelo de branch/release

A `main` é a branch ativa de desenvolvimento. Em produção, utilize GitHub Releases com tag. É válido que `VERSION` na `main` fique mais novo que `STABLE_VERSION` quando uma nova candidata estiver em desenvolvimento.

Uma candidata se torna estável depois que o gate de release documentado é aceito pelo mantenedor e o workflow de release valida que `VERSION` e `STABLE_VERSION` correspondem à tag que será publicada.

Para a release `1.5.0`, os dois arquivos contêm `1.5.0`.

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

A release `1.5.0` é exportada como `vendor.version: 1.5-0`. O workflow de release valida a tag contra os dois marcadores de versão, valida as regras de template/documentação/produção, executa os testes e realiza a validação de upgrade no Zabbix 7.0 antes de publicar os artefatos.

## Compatibilidade Zabbix não define a versão do projeto

A versão do projeto descreve este repositório. A versão do export Zabbix (`7.0` ou `8.0`) descreve o formato de configuração de destino.

Portanto a mesma versão de projeto pode existir simultaneamente nos exports Zabbix 7.0 e Zabbix 8.0.

## Identificador técnico estável

A partir da 1.4.0 o nome visível do template é **Vertiv by SNMP**, enquanto o identificador técnico do export permanece `VERTIV by SNMP`. Manter o identificador técnico estável é intencional: isso permite atualizar instalações existentes sem criar um segundo template apenas por causa da capitalização.
