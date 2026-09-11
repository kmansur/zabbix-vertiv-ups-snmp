# Contribuindo

[English](CONTRIBUTING.md) | **Português (Brasil)**

Contribuições, relatos de compatibilidade de equipamentos, bugs, melhorias de documentação e atualizações de compatibilidade com Zabbix são bem-vindos.

## Fluxo de desenvolvimento

1. Crie uma branch a partir de `main`.
2. Faça uma alteração focada.
3. Execute as validações locais.
4. Atualize em conjunto a documentação em inglês e português do Brasil.
5. Atualize os dois arquivos de changelog quando a alteração for visível ao usuário.
6. Abra um pull request.

Nomes de branches recomendados:

- `feature/<descricao>`
- `fix/<descricao>`
- `docs/<descricao>`
- `refactor/<descricao>`
- `ci/<descricao>`
- `chore/<descricao>`

## Mensagens de commit

Conventional Commits são recomendados:

- `feat:` nova funcionalidade;
- `fix:` correção de bug;
- `docs:` documentação;
- `refactor:` reorganização interna;
- `test:` testes;
- `ci:` CI/CD;
- `chore:` manutenção do repositório.

## Validação local

```sh
python -m pip install -r requirements-dev.txt
python -m compileall -q tools tests
ruff check tools tests
ruff format --check tools tests
pytest -q
python tools/validate_templates.py
python tools/validate_docs.py
```

## Fluxo dos templates Zabbix

Exports específicos por versão ficam em:

```text
templates/zabbix-<major.minor>/
```

Ao alterar um template:

1. preserve o UUID do template, exceto se estiver criando intencionalmente um novo template;
2. preserve chaves e UUIDs de itens em alterações compatíveis;
3. mantenha equivalência semântica entre Zabbix 7.0 e 8.0;
4. atualize `VERSION` e todos os `vendor.version` para uma release;
5. importe no build Zabbix alvo sempre que possível;
6. valide Latest data contra o LCD/interface web do nobreak;
7. documente modelo do nobreak, placa de gerenciamento, firmware e build Zabbix utilizados na validação em execução.

## Relatos de compatibilidade

Inclua:

- modelo do nobreak;
- modelo da placa de gerenciamento;
- firmware;
- versão do Zabbix;
- utilização de SNMPv2c ou SNMPv3;
- chaves/OIDs unsupported;
- saída bruta de `snmpget -On` ou `snmpwalk -On` para o OID afetado;
- valor esperado exibido pela interface do nobreak.

Remova communities, usuários, chaves de autenticação, chaves de privacidade e informações de IP público antes de publicar logs.
