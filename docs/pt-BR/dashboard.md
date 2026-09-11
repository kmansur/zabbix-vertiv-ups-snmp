# Dashboard nativo

[English](../en/dashboard.md)

A versão 1.2.0 adiciona o dashboard de template **VERTIV UPS Overview**. Ele é importado junto com o template e acompanha automaticamente o host monitorado.

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

