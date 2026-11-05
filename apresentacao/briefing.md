# Briefing: vídeo de apresentação do projeto

Vídeo de portfólio para a trilha **AI Builder** do estágio de GenAI do iFood. Quem assiste é um avaliador técnico que decide em segundos se o projeto merece atenção. O vídeo precisa prender nos primeiros 2 segundos, mostrar o sistema funcionando, os números reais e a honestidade sobre o que deu errado.

## Formato
- 1920×1080, 30 fps, **75 a 90 segundos**.
- Narração em português do Brasil, voz `pt-BR-ThalitaMultilingualNeural` (edge-tts) a +6%. Ritmo de ~2,6 palavras por segundo: 80 s ≈ 200 palavras no total.
- Sem música (não há trilha licenciada); som = narração + efeitos do kit (`render/kit/sfx/`: batida, brilho, clique, pop, subida, tique, whoosh, whoosh_curto).
- Cortes secos entre cenas; cada cena tem a própria entrada e saída animadas.
- Ninguém aparece. O projeto inteiro é "sem aparecer", e o vídeo segue isso.

## Ferramentas (as duas no mesmo vídeo)
- **HyperFrames** (HTML + GSAP → MP4): cenas de tipografia cinética e montagem com os vídeos reais (gancho, montagens com celulares, violações, antes e depois, encerramento).
- **Remotion** (React → MP4): cenas guiadas por dados (diagrama do fluxo, contadores, gráfico de barras, funil, terminal do revisor, placar).
- Cada cena vira um MP4 próprio com a duração exata da sua narração + respiro; a montagem final junta as cenas e o áudio com ffmpeg.

## Identidade visual (vale para as duas ferramentas)
| Papel | Valor |
|---|---|
| Fundo | `#0E0E10` (quase preto), com granulado/vinheta sutil |
| Texto principal | `#F5F4F0` |
| Texto secundário | `#A9A79F` |
| Destaque (números, palavra-chave) | `#C6F432` (lima) |
| Dados / agentes de IA | `#3D8BFF` (azul) |
| Violação / erro | `#FF4D4D` (vermelho) |
| Pessoa / aprovação humana | `#FF8A3D` (laranja) |
| Cartão claro (gráficos) | `#FCFCFB` com texto `#0B0B0B` |

- Fontes (instaladas no container, declaradas com `local()` em `fontes.css`): **Bricolage Grotesque 800** para títulos e números grandes; **Inter** 400–700 para texto. Nada de outra família.
- Movimento: entradas com mola (overshoot leve), nada parado por mais de ~1,5 s, um foco por vez, números sempre contando até o valor, palavras-chave aparecendo no instante em que a narração as diz.
- Vídeos verticais aparecem dentro de **molduras de celular** (cantos arredondados 36 px, borda fina `#2A2A2E`), sempre rodando.
- Legenda dinâmica: só a palavra-chave da frase em destaque (lima), grande; não legendar tudo.

## Fatos (só use estes; nada inventado)
- Sistema que transforma o anúncio de um produto em vídeos de propaganda para o TikTok Shop, como afiliado, **sem ninguém aparecer**. Rodou de verdade de **05/10 a 04/11/2026**.
- **28 vídeos** postados, **6 produtos** (kit de body splash, garrafa térmica MODUS, faqueiro, extensão com USB, garrafa Hilee, peseira).
- Custo: **R$ 0 de API**; só a assinatura do Google AI Plus (créditos do Flow).
- Fluxo: anúncio → agente de roteiro (escreve 9 partes que se combinam) → aprovação de uma pessoa → revisor do texto → primeiro quadro no editor de imagem do Flow → clipe de 8 s no Veo → conferência quadro a quadro → aprovação → narração edge-tts → edição em código (HyperFrames, agente editor) → render em Docker na VPS → revisor do vídeo → postagem manual marcada como "Conteúdo gerado por IA".
- Quem faz: uma sessão do **Claude Code** coordena tudo e opera o Google Flow pelo navegador; três agentes (roteiro, editor, revisor); uma **memória** (`aprendizados.md`, 58 registros) com cada falha e cada violação, lida antes de cada roteiro.
- Resultados: **16.522 visualizações**; mediana de 294 por vídeo; **dois vídeos fazem 45%** (body splash D: 4.938; garrafa A: 2.434).
- Funil de outubro: 17.800 impressões do produto → 135 cliques (0,76%) → **2 vendas** → R$ 290,06 em vendas → **R$ 23,13 de comissão**. O gargalo é o clique.
- O produto pesa mais que o formato: a extensão ficou em ~220 visualizações com qualquer receita.
- **6 violações** automáticas do TikTok (punição 4 a 6 minutos depois de postar): 3 de produto inconsistente, 2 de quadro estático, 1 de alegação exagerada (recurso aceito, pontos devolvidos).
- O conflito: para o produto sair idêntico ao anúncio, os clipes eram foto + câmera se aproximando. Ficava fiel, mas parado → violação de quadro estático. Solução: primeiro quadro fiel no editor de imagem + uma mão movendo o produto.
- **Revisor de conformidade**: 3 camadas (regras fixas, agente de IA comparando cada frase com o anúncio, movimento real medido por fluxo óptico descontando a câmera). Testado nos 27 vídeos postados: pegou a alegação exagerada (1 de 1) e 1 de 2 quadros estáticos. O primeiro vídeo postado depois dele (Hilee C) passou nas 3 verificações e levou violação de produto inconsistente, que é visual e ainda não é coberta. Próximo passo: comparar quadros com as fotos do anúncio usando um modelo de visão.
- Lições: conferir a fidelidade visual desde o primeiro vídeo; validar o produto antes de produzir em volume; medir cada vídeo desde o dia 1; concentrar no que vende.
- Repositório: `github.com/joaopedromc-git/tiktok-shop-ia`.

## Material disponível (no repositório)
- Vídeos finais 720p: `produtos/<produto>/video_<lote>.mp4` (os originais 1080p estão na VPS em `~/tiktok-automacao/dados/<produto>/` quando existem). Mais vistos: `bodysplash/video_D`, `garrafa/video_B`. Com mão em movimento: `facas/video_C`, `facas/video_D`, `garrafa/video_D`, `extensao/video_C`, `hilee/video_C`. Quadro estático (violação): `facas/video_A`.
- `docs/img/visualizacoes.svg`, `docs/img/fluxo.svg`, `docs/img/antes_depois.jpg`, `docs/img/galeria.jpg`.
- `metricas/visualizacoes.csv` (28 linhas: ordem, produto, lote, visualizações, violação), `metricas/vendas_2026-10.md`, `metricas/violacoes.md`.
- `evals/resultados.md`: placar do revisor. Saída real do revisor para `facas E`: regras reprovam "do primeiro ao último" e "adeus"; movimento aprova (27% parado); veredito REPROVA. Para `facas A`: movimento REPROVA, 74% do tempo sem movimento real, trechos parados 2,3–4,7 s e 18,3–20,5 s.

## Restrições
- Nada de preço de produto, nem promessa de resultado. Os números são os reais acima, sem arredondar para cima.
- Não usar nome da pessoa, rosto nem dado pessoal; o repositório pode aparecer no encerramento.
- Tom: direto, confiante e honesto. O vídeo não esconde que o retorno financeiro foi pequeno; mostra que o sistema aprende com os erros.

## Componentes padrão (iguais em todas as cenas)
- **Moldura de celular:** proporção 9:16, cantos 36 px, borda 6 px `#2A2A2E`, sombra `0 30px 80px rgba(0,0,0,.55)`. Tamanho padrão 300×533 px (destaque: 420×747; parede do gancho: 180×320). O vídeo preenche a moldura (`object-fit: cover`) e roda o tempo todo, sem som.
- **Etiqueta (pílula):** Inter 600, 22 px, cantos 999 px, padding 8×16, fundo `rgba(255,255,255,.08)` com borda 1 px `rgba(255,255,255,.14)`; versão de status com a cor do papel (lima, azul, vermelho, laranja) e texto `#0E0E10`.
- **Tipografia:** título de cena Bricolage 800, 96–140 px, entrelinha 0,95, tracking −2%; número gigante Bricolage 800, 200–300 px, algarismos tabulares; texto Inter 500, 40–48 px; legenda/rodapé Inter 500, 26 px em `#A9A79F`.
- **Margem segura:** 96 px nas laterais, 72 px em cima e embaixo.
- **Movimento:** entradas de 0,45–0,6 s com mola leve (GSAP `back.out(1.4)` / Remotion `spring({damping: 14, mass: 0.8})`); saídas de 0,3 s com aceleração (`power2.in`); deslocamento de entrada de 40–80 px ou escala 0,92→1. Um "respiro" de câmera contínuo (escala 1,00→1,03 na cena toda) evita quadro parado.
- **Fundo:** `#0E0E10` + vinheta radial (centro 0% → bordas 35% preto) + granulado sutil (opacidade 0,04), igual nas duas ferramentas.
- **Entrada e saída de cena:** cada cena começa já com algo na tela no quadro 0 (nada de tela preta) e termina com a saída concluída 0,1 s antes do fim, fundo limpo, para o corte seco com a próxima.
- **Áudio da cena:** a narração (`fala.mp3` / `audio/<cena>.mp3`) começa em 0,25 s; os tempos das palavras em `fala.json` / `audio/<cena>.json` são relativos ao início da fala, então tempo na cena = 0,25 + `inicio`. Efeitos a −12 dB em relação à voz (volume 0,25–0,35), nunca sobre uma palavra importante.
- **Saída de cada cena:** `apresentacao/saida/<cena>.mp4`, 1920×1080, 30 fps, H.264 + AAC 48 kHz, duração exata de `tempos.json`.
