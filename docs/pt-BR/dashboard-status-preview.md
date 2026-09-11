# Preview dos cards de status do dashboard

[English](../en/dashboard-status-preview.md)

Este branch provisório testa cards de status do nobreak mais limpos e operacionais sem alterar a coleta SNMP, triggers ou a versão do projeto.

## O que muda

- Cards de status/value map mostram somente o texto mapeado (por exemplo `Normal operation`, `Normal`, `Passed`, `External`, `8 weeks`).
- O sufixo numérico bruto normalmente exibido pelo widget Item value é ocultado mostrando uma macro `{ITEM.LASTVALUE}` consciente de value map no campo Description do widget.
- Os thresholds continuam usando o item numérico original, portanto a cor de fundo pode mudar dinamicamente.
- São usadas cores em tons suaves para manter legibilidade: verde = normal, amarelo = atenção, laranja = alarme/degradado, vermelho = crítico, azul = informativo/configuração.
- O card System status recebe largura adicional na linha Overview.
- Active alarms, Battery charge e Runtime remaining recebem fundos dinâmicos por threshold numérico.

Este é apenas um preview. O branch main permanece inalterado até a aprovação visual.
