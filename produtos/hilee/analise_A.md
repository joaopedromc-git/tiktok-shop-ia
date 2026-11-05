# Análise — hilee, lote A ("Gelada o dia todo, sem abrir tudo"), clipes gerados em 21/10/2026

Conferência em 1080p na VPS (`dados/hilee/clipes_A/`): tira a cada 0,5 s (`tira_A/B/C.jpg`), zoom nos trechos de risco (`det_A.jpg`, `det_B.jpg`), `freezedetect` (n=0,003, d=1 s). Clipes 1080×1920, 8 s. Custo: A 20 (Fast) + B 20 (Fast) + C 10 (Lite) = 50 (**créditos zerados**). Os três caíram direto na coleção `hilee`.

Quadros usados (aprovados pelo operador, "as primeiras geradas"): `fotos/quadro_A_gelo_916.jpg`, `quadro_B_inicio_916.jpg` + `quadro_B_fim_916.jpg` (primeiro + último quadro), `quadro_C_piscina_916.jpg`. A alça da preta aparece como um aro pequeno do lado esquerdo (o operador aceitou; a alça real é rígida e gira no eixo da tampinha, ver `roteiro_A.md`).

## A — intro (Fast), estúdio azul-gelo — **usar 0-1,75 s** (seco)
- 0-1,75 s: cubos de gelo caem dos dois lados, fumaça fria na base, garrafa seca e fiel (tampa fechada, anel HILEE, aro da alça).
- **A partir de ~1,8 s a água do gelo que bate na tampa escorre pela borda direita e pinga no corpo** (conferido a cada 0,2 s pelo editor); aos 6,5-7 s outro respingo. Garrafa térmica não sua: não usar depois de 1,75 s.
- Faixa de luz azul varre o fundo de 2,5 s em diante. `freezedetect` limpo.

## B — apresentação (Fast), estúdio pêssego, primeiro + último quadro — **usar 0-6,4 s**
- 0-1,0 s: garrafa fechada parada no pedestal.
- 1,0-3,0 s: a mão entra pela direita, pega a tampinha e ela abre para trás (a mão levanta a tampinha em vez de só apertar o botão; leitura natural). Garrafa fiel no zoom: anel HILEE, bocal, vedação cinza.
- 3,0-3,5 s: a mão sai; 3,5-6,4 s: tampa aberta, faixa de luz quente passa no fundo.
- **Parado a partir de 6,5 s** (`freezedetect` freeze_start 6,5): não usar.

## C — CTA (Lite), beira de piscina, Roxo Escuro — **serve inteiro (0-8 s)**
- 0-1,0 s: só a garrafa e a água brilhando; 1,0-6,5 s: a mão entra pelo alto à direita, segura a alça malva (levanta levemente, a base continua na pedra); 6,5-7 s a mão sai.
- Cores e alça fiéis do começo ao fim (tampinha lavanda, botão creme, anel grafite). `freezedetect` limpo.

## Plano de montagem
- Intro ~4,2 s: A 0-2,6 s a ~0,65× (≈4 s).
- Apresentação ~9,7 s: B 0-6,4 s a 0,85× (≈7,5 s) + completar com C 0-1,0 s ou A 0-1,2 s em outro corte (nada de esticar o B parado).
- CTA ~4,6 s: C 1,0-6,0 s.
