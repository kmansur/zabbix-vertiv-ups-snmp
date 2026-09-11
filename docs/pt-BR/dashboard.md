# Dashboard nativo

[English](../en/dashboard.md)

A versão 1.2.0 adiciona o dashboard de template **Vertiv UPS Overview**. Ele é importado junto com o template e acompanha automaticamente o host monitorado.

## Páginas

- **Overview** — estado do sistema, fonte da saída, alarmes ativos, estado/carga/autonomia da bateria e os seis gráficos de tendência nativos.
- **Electrical** — resumo fixo de entrada, saída e bypass, além dos gráficos de potência por fase e carga por fase.
- **Battery & Environment** — bateria, autonomia, temperaturas, teste/estado e tendências de bateria/ambiente.

O dashboard utiliza somente itens e gráficos já validados pelo repositório. Nenhum OID de escrita/controle é introduzido.

## Tipografia dos cards

A versão 1.3.3 ajusta os widgets **Item value** para melhorar a leitura em cards compactos:

- valores de estado/value map: tamanho 24%;
- valores numéricos: tamanho 27%;
- casas decimais e unidades: tamanho 16%;
- valor centralizado horizontal e verticalmente;
- indicador de mudança removido dos cards para evitar truncamento de valores mapeados.

O título do widget continua identificando cada métrica, portanto o card mostra somente o valor e preserva mais espaço útil. Os gráficos, itens, triggers e coleta SNMP não são alterados por esse ajuste.


## Comportamento dos cards de status na versão 1.4.0

O dashboard final utiliza a renderização nativa mapeada do **Item value** nos cards de status. Isso mantém os value maps do Zabbix confiáveis entre diferentes frontends, enquanto thresholds dinâmicos definem a cor de fundo do card. Cards de enum/status usam zero casas decimais, portanto valores mapeados aparecem com sufixos compactos como `Normal (3)` em vez de `Normal (3.00)`.

As cores de criticidade usam fundos suaves: verde para normal, amarelo para atenção, laranja para estados degradados/alarme e vermelho para estados críticos. Cards informativos/de configuração usam fundo neutro ou azul-claro.

O card calculado de potência de entrada e o gráfico de potência de entrada por fase não são mais destacados no dashboard porque a documentação SNMP Vertiv fornecida não define a escala desses OIDs privados. Os itens continuam disponíveis para validação em campo e troubleshooting.


## Ajustes de campo na versão 1.4.1

A página **Overview** usa três gráficos principais em uma única linha: carga/autonomia da bateria, potência de saída e carga de saída por fase. O antigo gráfico de contadores cumulativos foi retirado do dashboard porque uma linha crescente/cumulativa não representa bem eventos operacionais.

A página **Electrical** apresenta blackout, brownout e linhas inválidas como cards de contadores e usa o gráfico de carga por fase em largura total. A página **Battery & Environment** exibe autonomia em horas e usa um gráfico dedicado de temperatura de entrada.

O item bruto `ups.battery.runtime` permanece em minutos para preservar a semântica RFC1628 e as triggers. O item calculado `ups.battery.runtime.hours` existe apenas para apresentação. A temperatura privada de bateria continua disponível em Latest data e no gráfico legado `UPS: Temperatures`, mas não é usada no gráfico ambiental padrão porque alguns firmwares podem expor valores não físicos/sentinela quando não há sensor útil.
