# Contribuindo

[English](CONTRIBUTING.md) | **Português (Brasil)**

Contribuições, relatos de compatibilidade de equipamentos, bugs, melhorias de documentação e atualizações de compatibilidade com Zabbix são bem-vindos.

## Política de branch e release

A `main` é a branch ativa de desenvolvimento/candidato. Uma GitHub Release com tag é o ponto de distribuição para produção.

- `VERSION` identifica a candidata atual do repositório.
- `STABLE_VERSION` identifica a última release estável com tag.
- A documentação de produção deve distinguir os dois estados sempre que forem diferentes.
- Mudanças candidatas devem passar por pull request e pela suíte de validação antes do merge.
- Uma candidata só recebe tag estável depois de concluir o gate de homologação em campo.

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
python tools/validate_production.py
```

## Fluxo dos templates Zabbix

Os exports específicos por versão ficam em:

```text
templates/7.0/vertiv-by-snmp.yaml
templates/8.0/vertiv-by-snmp.yaml
```

Ao alterar um template:

1. preserve o UUID do template, exceto se estiver criando intencionalmente um novo template;
2. preserve chaves e UUIDs de itens em alterações compatíveis;
3. mantenha equivalência semântica entre Zabbix 7.0 e 8.0 enquanto o export 8.0 permanecer preliminar;
4. atualize `VERSION` e todos os `vendor.version` para uma nova candidata/release;
5. atualize `STABLE_VERSION` apenas quando essa versão tiver sido efetivamente publicada com tag/release estável;
6. importe no build Zabbix alvo sempre que possível;
7. valide Latest data contra o LCD/interface web do nobreak;
8. documente modelo do nobreak, placa de gerenciamento, firmware e build Zabbix utilizados na validação em execução;
9. registre a evidência da homologação em campo em `docs/homologation/` antes de promover uma candidata para estável.

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
