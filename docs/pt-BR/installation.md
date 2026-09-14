# Instalação

[English](../en/installation.md)

## Requisitos

- Zabbix Server ou Proxy com acesso à interface SNMP do nobreak;
- Zabbix 7.0 ou build compatível de desenvolvimento do Zabbix 8.0;
- SNMP habilitado na placa de gerenciamento Vertiv/Liebert;
- acesso de leitura à UPS-MIB padrão e/ou à MIB privada Vertiv.

SNMPv3 é recomendado quando a placa de gerenciamento oferece suporte. SNMPv2c também pode ser utilizado quando necessário pelo equipamento ou ambiente.

## 1. Escolha conscientemente entre release estável e candidata

Para **produção**, baixe a última GitHub Release estável com tag identificada por `STABLE_VERSION` e utilize o asset correspondente à sua versão do Zabbix.

Os arquivos em `templates/` na branch `main` representam a versão atual de desenvolvimento/candidata identificada por `VERSION`. Use esses arquivos somente quando a intenção for testar/homologar essa candidata.

O Zabbix 8.0 permanece como alvo preliminar de compatibilidade até a validação real de importação/execução ser explicitamente promovida.

## 2. Valide o SNMP a partir do Zabbix Server ou Proxy

Substitua os valores de exemplo pelos utilizados no seu ambiente.

UPS-MIB:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.2.1.33
```

MIB privada Vertiv/Liebert:

```sh
snmpwalk -v2c -c COMMUNITY -On UPS_IP 1.3.6.1.4.1.476.1.42
```

Se utilizar SNMPv3, faça o teste com os parâmetros correspondentes de autenticação e privacidade, evitando expor credenciais no histórico do shell.

## 3. Importe o template

No Zabbix:

1. abra **Data collection → Templates**;
2. clique em **Import**;
3. selecione o arquivo de release/candidata de acordo com o alvo pretendido:
   - Zabbix 7.0: asset `vertiv-by-snmp-zabbix-7.0.yaml` da release ou `templates/7.0/vertiv-by-snmp.yaml` somente quando estiver testando explicitamente a candidata;
   - Zabbix 8.0 preliminar: asset `vertiv-by-snmp-zabbix-8.0.yaml`/equivalente da candidata somente quando estiver validando compatibilidade 8.0 intencionalmente;
4. revise o resumo da importação;
5. importe o template.

## 4. Configure o host do nobreak

Crie ou edite o host do nobreak e adicione uma interface **SNMP** com o endereço IP da placa de gerenciamento.

Configure a versão SNMP e as credenciais nas configurações do host/interface de acordo com sua política de segurança.

## 5. Vincule o template

Vincule:

```text
Vertiv by SNMP
```

Aguarde os primeiros ciclos de coleta.

## 6. Valide os primeiros dados

Abra **Monitoring → Latest data** e confirme pelo menos:

- heartbeat SNMP (`UPS: SNMP agent uptime`);
- fonte da saída do nobreak;
- status do sistema;
- status e carga da bateria;
- autonomia estimada;
- medições de entrada/saída;
- carga da saída;
- temperatura do ar de entrada;
- linhas de entrada, saída e bypass descobertas.

Compare as medições com o LCD ou interface web do nobreak. Objetos opcionais unsupported são informação de compatibilidade da placa/equipamento; não os habilite cegamente.

## 7. Ajuste as macros

Revise os limites padrão de autonomia, carga da bateria, carga por linha de saída e temperatura de entrada antes de utilizar alertas em produção.

As macros de temperatura da bateria são reservadas na candidata 1.5.0 e não ativam trigger padrão de temperatura da bateria.

Consulte [Configuração e macros](configuration.md).

## Traps SNMP opcionais

O template contém um item desabilitado chamado `UPS: Vertiv SNMP traps (optional)`.

Mantenha-o desabilitado enquanto a recepção de traps no Zabbix não estiver configurada e o payload real dos traps Vertiv não tiver sido validado. O projeto deliberadamente não cria regras de interpretação apenas a partir dos nomes dos OIDs de condição.
