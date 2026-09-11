# Mapa sinótico opcional

[English](../en/synoptic-map.md)

A versão 1.3.0 adiciona um gerador opcional de mapa de rede do Zabbix para uma visão sinótica de um nobreak Vertiv monitorado. O mapa complementa o dashboard nativo do template; ele não o substitui.

## O que o mapa mostra

O mapa gerado possui um elemento central ligado ao host do nobreak e quatro blocos operacionais: **INPUT**, **BYPASS**, **OUTPUT** e **BATTERY**. O Zabbix destaca dinamicamente o ícone central do nobreak quando o host possui problemas. Os blocos periféricos são elementos esquemáticos intencionalmente estáticos; o projeto não cria vínculos item-forma que não sejam suportados pelo formato genérico de importação.

Dois pequenos ícones de nobreak são incorporados ao export, portanto o mapa não depende de uma biblioteca de ícones previamente existente no Zabbix.

## Gerar um mapa

O host deve existir previamente no Zabbix e deve estar vinculado ao **Vertiv by SNMP**.

Para Zabbix 7.0:

```sh
python tools/generate_synoptic_map.py \
  --host "UPS-SRV01" \
  --output vertiv-ups-synoptic.yaml
```

Para Zabbix 8.0:

```sh
python tools/generate_synoptic_map.py \
  --host "UPS-SRV01" \
  --zabbix-version 8.0 \
  --output vertiv-ups-synoptic.yaml
```

Use o **nome exato do host no Zabbix**, e não o nome visível, salvo quando ambos forem iguais.

## Importar

1. Acesse **Monitoring → Maps**.
2. Clique em **Import**.
3. Selecione o YAML gerado.
4. Habilite a criação/atualização do mapa e a criação das imagens conforme necessário.
5. Importe o arquivo.

O Zabbix exige que hosts referenciados existam antes da importação de um mapa. A importação de imagens exige uma conta Super admin. O gerador é somente leitura em relação ao nobreak e não contém nenhuma operação SNMP de escrita/controle.
