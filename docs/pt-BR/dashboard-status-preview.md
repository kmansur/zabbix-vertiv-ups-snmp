# Preview dos cards de status do dashboard

[English](../en/dashboard-status-preview.md)

Este branch provisório mantém os fundos dinâmicos em tons suaves e volta os cards de status para a renderização nativa do **Item value**, depois que o experimento com macro no campo Description se mostrou pouco confiável no frontend Zabbix 7 testado.

## Comportamento atual do preview

- Os cards de status mantêm fundos dinâmicos em verde/amarelo/laranja/vermelho usando o item numérico original e seus thresholds.
- O texto de status é renderizado nativamente pelo value map já existente.
- Cards de status/enum usam zero casas decimais, deixando o sufixo bruto mais curto, por exemplo `(1)` em vez de `(1.00)`.
- Cards com textos longos mantêm a largura ampliada criada no preview anterior.
- Active alarms é exibido como inteiro.
- Battery charge e Runtime remaining mantêm os fundos dinâmicos por criticidade.

## Limitação confirmada

A tentativa de remover o sufixo numérico entre parênteses usando macro/expressão regular no campo Description produziu strings quebradas como `\1`, `\3` e `\0` no frontend Zabbix 7 testado. Este branch remove intencionalmente esse experimento.

O branch main permanece inalterado enquanto este comportamento visual é avaliado.
