# Troubleshooting

[English](../en/troubleshooting.md)

## A importação do template falha

Confirme que está importando o YAML do diretório correspondente à versão major/minor do Zabbix.

Execute localmente:

```sh
python tools/validate_templates.py
```

Se o Zabbix informar um erro de schema/importação que o validador local não detectou, abra uma issue informando:

- versão/build exato do Zabbix;
- mensagem completa do erro de importação;
- arquivo de template utilizado.

## Todos os itens SNMP ficam unsupported

Verifique:

- se o host possui uma interface SNMP;
- se o IP da interface está correto;
- se UDP/161 está acessível;
- se a versão SNMP e credenciais correspondem ao nobreak;
- se o Zabbix Server ou Proxy associado consegue alcançar o equipamento.

Teste a partir do mesmo servidor/proxy:

```sh
snmpget -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.2.1.0
```

## Apenas os itens da árvore privada Vertiv ficam unsupported

Algumas placas de gerenciamento expõem a UPS-MIB, mas não todos os objetos de `1.3.6.1.4.1.476.1.42`.

Execute:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.4.1.476.1.42
```

Ao abrir uma issue, informe o modelo do nobreak, modelo da placa de gerenciamento e firmware.

## A descoberta de linhas da UPS-MIB não encontra fases

Consulte diretamente as tabelas padrão:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.3.3
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.4.4
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33.1.5.3
```

Um nobreak monofásico pode expor apenas o índice `.1`; um modelo trifásico pode expor três índices. Nem todos os nobreaks fornecem dados de bypass.

## Um valor parece estar com escala incorreta

Compare com o LCD/interface web do nobreak e capture o valor SNMP bruto utilizando `snmpget -On`.

Não adicione multiplicador apenas com base na escala do Modbus. As representações SNMP e Modbus podem utilizar escalas diferentes.

Abra uma issue informando:

- OID;
- valor SNMP bruto;
- valor exibido pela interface do nobreak;
- modelo/placa/firmware.

## Um enum privado Vertiv aparece como string / Numeric (unsigned)

Algumas placas Vertiv/Liebert retornam objetos enumerados da árvore privada como texto, por exemplo `Normal Operation`, `on`, `Online`, `fully charged` ou `Passed`, enquanto outras placas/firmwares podem retornar o código numérico do enum.

A partir da versão 1.3.2, o template normaliza automaticamente os dois formatos para o código numérico canônico antes do armazenamento. Isso mantém os value maps e triggers numéricos funcionando em ambos os comportamentos.

Se ainda ocorrer a mensagem `Value of type "string" is not suitable for value type "Numeric (unsigned)"`, confirme que o template possui `vendor.version: 1.3-2` ou superior e envie o OID e o texto bruto retornado por `snmpget -On`.

## Muitos alertas

Revise as macros sobrescritas no host para autonomia, carga da bateria, carga do nobreak e temperatura. Os padrões são genéricos e devem ser adaptados à instalação.

## Traps SNMP não chegam

O item de trap fica desabilitado por padrão. Polling SNMP e recepção de traps são caminhos independentes no Zabbix.

Primeiro valide o receptor de traps no server/proxy fora do template e somente depois habilite o item.
