# Análise — hilee, lote C ("Time canudo ou time direto?"), clipes gerados em 03/11/2026

Veo 3.1 Fast, 20 créditos cada (60; **sobram 10**). Agente do Flow com primeiro quadro (G, I) e primeiro + último quadro (H). Quadros feitos pelo agente com Nano Banana Pro (0 crédito) a partir de `fotos/base_C/` (cópias de `quadro_B_fim`, `quadro_B_inicio`, `quadro_E_parque`): `fotos/quadro_G_ceu_916.jpg`, `quadro_H_inicio_916.jpg`, `quadro_H_fim_916.jpg`, `quadro_I_cozinha_916.jpg`. Clipes 1080×1920, 24 fps, ~7,85 s (baixados em 1080p). Tiras a cada 0,5 s: `tira_G/H/I.jpg`; detalhes: `det_G/H/I.jpg`. Na VPS: `dados/hilee/clipes_C/`.

## G — intro, preta de tampa aberta na mão contra o céu azul — **usar 0-3,5 s**
- 0-2,5 s: a mão inclina o topo para a câmera e o bocal aberto e a vedação cinza aparecem (fiéis no zoom); 2,5-3,5 volta a ficar em pé (relevo HILEE visível).
- 3,5-8 s: segura quase parada (sobe/desce mínimo); só as nuvens andam. **Não usar como trecho longo** (regra da 5ª violação). `freezedetect` limpo.

## H — apresentação, preta, estúdio sálvia, pedestal de concreto, primeiro + último quadro — **usar 0,5-6,0 s**
- 0-0,6 tampa fechada parada; 0,6-2,0 a mão entra pela direita e pega o corpo abaixo do anel.
- **~2,2-2,7 a tampinha abre** (borrão de movimento curto na tampa, natural a 1,0×); 2,7-4,4 a garrafa sobe e inclina para a câmera (bocal + canudo + vedação fiéis); 4,4-6,0 desce ao pedestal; 6,0-6,4 a mão sai.
- **Parado a partir de 6,4 s** (`freezedetect` 6,42-7,54): não usar.

## I — CTA, Roxo Escuro, bancada de mármore na cozinha — **usar 0,5-6,3 s**
- Dois dedos na alça desde o início; ~1,0 s levanta pela alça e mantém no ar balançando (1,5-4,0 s, ora mais alto, ora mais baixo); 4,5-6,0 pousa com a mão ainda na alça; ~6,5 solta; 7-8 sem mão.
- A alça malva **estica um pouco quando a garrafa fica pendurada** (anúncio: alça de silicone; aceito). Cores fiéis (corpo ameixa, tampinha lavanda, botão creme, anel grafite). `freezedetect` limpo.

## Plano de montagem (roteiro_C.json, ~14,6 s)
- Intro (~3 s): G 0-3,0 (1,0×).
- Apresentação (~7,6 s): H 0,5-6,0 (1,0×; tampinha abre em "dois jeitos de beber") + completar com G 1,0-2,5 ou I 1,0-3,0 se faltar.
- CTA (~4 s): I 1,0-5,0.
- Regras: tela cheia, nada abaixo de 0,9×, sem quadro congelado, nada de gota/água/brilho na garrafa.
