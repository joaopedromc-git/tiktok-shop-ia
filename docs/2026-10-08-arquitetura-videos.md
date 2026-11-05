# Arquitetura dos vídeos — TikTok Shop

Data: 08/10/2026. Status: **aprovada inteira pelo operador em 08/10/2026.**

## Parte 1 — Visão geral (aprovada)

### Estrutura de cada vídeo
| Parte | Papel | Efeito no espectador |
|---|---|---|
| Introdução | Situação-problema **ou** o produto aparecendo | Para a rolagem; cria a necessidade |
| Apresentação | O que é, o que faz, benefícios, condições fixas, por que comprar | Interesse e desejo, só com fatos do anúncio |
| CTA | Chamada para tocar no produto | Ação |

Cada vídeo = 3 clipes do Flow (um por parte). Os clipes têm letra sequencial por produto:

| Vídeo | Intro | Apresentação | CTA |
|---|---|---|---|
| A | A | B | C |
| B | D | E | F |
| C | G | H | I |

Com os 9 clipes, as combinações são {A,D,G} × {B,E,H} × {C,F,I} = 27. **Todas precisam harmonizar** e cada uma ter impacto sozinha.
Por enquanto só se monta o vídeo "oficial" de cada lote (A, B, C). As combinações cruzadas ficam para depois, quando o operador pedir.
Os 3 produtos atuais (extensao, bodysplash, garrafa) já têm o vídeo A postado; o próximo passo de cada um é o lote D, E, F → vídeo B.

### Condições
Só o que não muda: o que vem na caixa, garantia, variações, "frete pelo TikTok Shop" — e só se estiver no anúncio. **Nunca** preço, desconto, cupom ou urgência. A CTA manda conferir o preço no produto.

### Peças
| Peça | Onde | Função |
|---|---|---|
| o operador | App do Claude no celular (Remote Control) ou terminal | Manda produto, aprova, posta |
| Sessão principal (Claude Code) | PC ligado, pasta do projeto, Chrome conectado | Coordena, opera o Flow, confere clipes, manda montar |
| Agente especialista | `.claude/agents/especialista-promocao.md` | Escreve roteiro, textos de tela e prompts |
| Aprendizados | `produtos/aprendizados.md` | O que funcionou/falhou no Flow; o agente lê sempre |
| Google Drive | Pasta `TikTok/` (rclone `gdrive:`, raiz presa nessa pasta) | Entrada das fotos e saída dos vídeos |
| Google Flow | Projeto **TikTok Shop**, uma coleção por produto | Gera os clipes |
| Render | VPS, container `render` | Voz Thalita, montagem, estilo de texto |
| Pasta local | `produtos/<codigo>/` | Tudo do produto: fotos, anúncio, roteiros, clipes, vídeos |

### Fluxo de um lote
1. **Entrada:** o operador sobe as fotos em `TikTok/<codigo>/` no Drive e manda no chat o texto do anúncio + link. Produto existente: só pede o próximo lote.
2. Sessão puxa as fotos (`rclone copy gdrive:<codigo> produtos/<codigo>/fotos/`) e grava `anuncio.md`.
3. **Roteiro:** o agente lê anúncio, fotos, roteiros anteriores do produto e `aprendizados.md`, e entrega `roteiro_<lote>.md` + `roteiro_<lote>.json`.
4. **✋ Aprovação 1:** o operador aprova ou pede ajuste no chat.
5. **Geração:** no Flow, coleção do produto, os 3 clipes com a foto do anúncio como referência; arrastar cada clipe para a coleção logo depois.
6. **Conferência:** quadros de cada clipe contra a foto. Regerar é último recurso: primeiro corrigir o prompt e anotar em `aprendizados.md`.
7. **✋ Aprovação 2 — só no primeiro lote de um produto novo:** o operador vê os 3 clipes.
8. **Montagem:** baixar os clipes (`clipe_<letra>.mp4`), subir para a VPS, montar `video_<lote>.mp4`.
9. **Entrega:** `produtos/<codigo>/video_<lote>.mp4` e `gdrive:<codigo>/videos/`.
   **Legenda junto (o operador, 08/10/2026):** todo vídeo pronto vai com a legenda para postar: gancho na 1ª linha, 1-2 linhas de benefício só com fatos do anúncio (dado com "dados do fabricante"), uma pergunta para puxar comentário, chamada para tocar no produto e 5-6 hashtags (nicho do produto + #achadinhos #tiktokshop). Emoji pode. Nunca preço, desconto ou urgência. Salvar em `produtos/<codigo>/legenda_<lote>.txt`, `gdrive:<codigo>/videos/` e `tiktok.video.legenda`, e mandar o texto no chat pronto para copiar.
10. **Postagem (sempre do operador):** marcar produto, "Conteúdo gerado por IA", música, publicar.

### Fica de fora
- O `/produto` pelo bot e o Gemini. O fluxo `TikTok – Bot` foi desativado em 08/10/2026 (não apagado).
- Telegram não é usado nesta versão.

## Parte 2 — Regras do agente (aprovada)

**Entrada:** `anuncio.md`, fotos, roteiros anteriores do produto, `aprendizados.md`, letra do lote.
**Saída:** para cada uma das 3 partes: fala, texto de tela (título + linha opcional), rodapé, prompt do Flow, e a descrição fixa do produto.

### Fala
- Português do Brasil falado, frases curtas, sem gíria forçada. Escrita para a voz Thalita (números por extenso; siglas que a voz soletra mal vão em grafia fonética, ex.: "tipo cê").
- Tamanho máximo (o clipe tem 8 s e aceita até ~30% de câmera lenta): intro ≤ 14 palavras (~5 s), apresentação ≤ 28 palavras (~10 s), CTA ≤ 14 palavras (~5 s).
- Benefício = função traduzida em ganho real ("4 USB" → "carrega celular, fone e relógio sem adaptador").
- Dado de desempenho só com "segundo o fabricante" e rodapé "*Dados do fabricante".

### Regras de combinação (para as 27 harmonizarem)
- Cada parte se sustenta sozinha: nada de "e ainda", "como eu disse", "isso aí" apontando para outra parte.
- Toda intro termina com o produto (ou a dor que ele resolve) em foco, sem citar recurso específico.
- Toda apresentação começa nomeando o produto ("Essa extensão…", "O kit Body Man…") e cobre um ângulo diferente dos lotes anteriores (função, benefício, uso).
- Toda CTA funciona depois de qualquer apresentação e não repete benefício.
- Não repetir frase nem gancho de lote anterior do mesmo produto.

### Prompt do Flow (meta: acertar de primeira)
- Em inglês. Começa com a frase de referência da foto e com a **descrição fixa do produto**, copiada igual em todos os prompts do produto (formato, cor, quantidade e posição de cada elemento, materiais, logo/letreiro).
- Um plano contínuo de 8 s, vertical 9:16, uma ação só, câmera simples (dolly lento, orbit curto ou estático).
- **Atualizado em 12-15/10/2026 (violações 2 e 3):** produto protagonista em todos os quadros; movimento real na cena (mão no produto) em pelo menos 2 dos 3 clipes; nada de "locked-off, nothing moves"; fundos diferentes nos 3; primeiro quadro 9:16 feito no editor de imagem do Flow. Regras completas no `CLAUDE.md` ("Regras que não mudam") e no agente `especialista-promocao`.
- O produto aparece **completo e igual do primeiro ao último quadro**; proibido "revelar" o produto se transformando.
- Luz e ambiente coerentes com o uso real; mãos permitidas, rosto falando não.
- Termina com: no text, no captions, no extra logos, no product changes, no morphing.
- Intro de problema pode não mostrar o produto, mas nunca mostra outro produto parecido em destaque.

### Texto de tela
Estilo fixo dos vídeos A (título amarelo Montserrat ExtraBold, linha branca, faixa escura, terço superior, entrada suave). Sem emoji (a fonte não desenha). Título ≤ 20 caracteres.
**Desde a edição com HyperFrames (08/10/2026),** o visual muda a cada vídeo (paleta, fontes e legenda novas, escolhidas pelo agente `editor-video` e registradas em `edicao_<lote>/escolhas.md`); o estilo fixo acima vale só para a montagem antiga com FFmpeg.

## Parte 3 — Montagem (aprovada; o operador vai acrescentar regras de edição)
- Um script único `render/montar.py` que lê `roteiro_<lote>.json` (troca os scripts avulsos `montar_bodysplash.py` e `montar_extensao.py`).
- 3 cenas, uma por clipe. Duração da cena = fala + folga, mínimo 4 s; se a fala passar de 8 s, câmera lenta até 0,77×. Trecho do clipe definido no JSON (início/fim), para cortar quadros ruins.
- A apresentação pode ter até 2 textos de tela em sequência.
- Narração Thalita +6%, normalização −14 LUFS, sem música (entra no TikTok).
- Saída 1080×1920, 30 fps, H.264.

## Parte 4 — Erros (aprovada)
| Situação | O que fazer |
|---|---|
| Clipe com produto diferente da foto | Corrigir prompt, anotar em aprendizados, regerar. Após 2 regerações do mesmo clipe, parar e perguntar ao operador |
| Flow sem créditos ou pedindo login/captcha | Parar e avisar; nunca digitar senha nem resolver captcha |
| Fotos não encontradas no Drive | Perguntar no chat |
| Fala estourando 8 s × 1,3 | Devolver ao agente para encurtar, antes da aprovação |
| Sessão ou PC caiu | Retomar pelo estado da pasta do produto (o que existe em `produtos/<codigo>/` diz em que passo parou) |

## Parte 5 — Edição com HyperFrames (aprovada em 08/10/2026)
Referência do operador: vídeo "Turn Claude into a motion graphics editor" (@calsaistudio). Gráficos feitos em código pelo Claude com HyperFrames + FFmpeg; linha do tempo com voz, gráficos e efeitos sonoros. Tudo gratuito; **nunca** usar o render na nuvem da HeyGen (`hyperframes cloud`/`lambda`).

### Peças
| Peça | Onde | Função |
|---|---|---|
| Agente editor | `.claude/agents/editor-video.md` | Escreve a composição HyperFrames de cada vídeo, usando as skills do HyperFrames |
| Kit de estilo | `render/kit/estilo.md` | Regras fixas, paletas, pares de fonte, presets de animação, catálogo de sons |
| Sons | `render/kit/sfx/` | whoosh, pop, batida grave, subida, clique, brilho — gerados por código (`render/kit/gerar_sfx.py`), sem direito autoral |
| Render | container `render` na VPS | Node 22 + HyperFrames + Chromium, além do FFmpeg e do edge-tts |

### Fluxo de um vídeo
1. Voz: edge-tts (Thalita, +6%) gera cada fala com o tempo de cada palavra (`fala_<parte>.mp3` + `fala_<parte>.json`).
2. Análise dos clipes: a sessão extrai quadros e anota onde o produto e cada detalhe aparecem, e os trechos sem defeito (`analise_<lote>.md`).
3. Edição: o agente editor recebe roteiro, falas com tempo, análise e kit; escolhe o estilo que mais harmoniza (diferente do vídeo anterior do mesmo produto) e escreve `produtos/<codigo>/edicao_<lote>/index.html`.
4. Checagem: `hyperframes lint` + quadros-chave revisados pela sessão antes do render completo.
5. Render na VPS, normalização −14 LUFS, entrega (Parte 1).

### Regras fixas do editor (o resto varia por vídeo)
- Gancho no 1º segundo: impacto visual (zoom, flash ou texto grande) + sonoro (batida) antes da voz.
- Quebra de padrão a cada 2-3 s sem poluir; no máximo 1 efeito sonoro a cada ~1,5 s, sempre abaixo da voz.
- Legenda palavra por palavra sincronizada, palavra-chave destacada.
- Callouts (setas, círculos) só sobre detalhes que aparecem de fato no quadro, no tempo anotado na análise.
- Zonas seguras: nada importante nos 20% de baixo nem na faixa direita (~15%).
- "*Dados do fabricante" quando a fala tem dado; nenhum texto mostra algo fora do anúncio.
- Emoji permitido com moderação (o Chromium desenha).
- 1080×1920, 30 fps, H.264, AAC.

### Reserva
O `/montar` com FFmpeg puro continua como reserva, caso o HyperFrames falhe.

## Banco `tiktok` (decidido em 08/10/2026: usar para não repetir)
O esquema atual serve sem mudança de tabela:
- `produto`: um por código (extensao, bodysplash, garrafa…).
- `clipe`: `variante` = número do lote (1 = A, 2 = B, 3 = C). A letra sai da parte + lote: intro/descricao/cta do lote 1 = A/B/C, lote 2 = D/E/F, lote 3 = G/H/I. `parte` continua `descricao` para a apresentação. `status` = `aprovado` depois da conferência; `arq_clipe` = caminho na VPS.
- `video`: uma linha por vídeo montado, com a combinação (intro, descrição, CTA). `UNIQUE` impede repetir combinação. `status`: `enviado` quando sobe no Drive; `postado` quando o operador avisar que postou.
- A view `proximo_video` escolhe a próxima combinação cruzada quando o operador pedir.
- Os vídeos A já postados entram como registro retroativo (clipes A, B, C com status `aprovado`; vídeo com status `postado`).

## Pendências para o operador
1. **Garrafa, vídeo A:** o operador manda o roteiro depois.
2. Regras extras de edição no render (o operador vai mandar).
