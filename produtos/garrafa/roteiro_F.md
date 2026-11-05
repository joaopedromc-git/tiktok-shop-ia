# Roteiro — garrafa, lote F (vídeo F, ROTAÇÃO sem clipe novo) — 03/11/2026

Produto: Garrafa Térmica MODUS 2,4 L, só a **verde-militar** com etiqueta preta "MODUS" (clipe E do lote B e clipes G/H do lote D). Nada da garrafa preta dos clipes B/C do lote A. I, D e F não entram (a garrafa quase não se move).
Sem crédito gasto: nenhum prompt do Flow novo (`prompt` = "reaproveitado" no JSON).

**Formato: receita do body splash D** (maior alcance da conta): cerca de 14 s, pergunta de escolha fácil no quadro 0 entre opções que aparecem nos próprios clipes, título-pergunta curto, letreiro trocando a cada ~1,6 s na apresentação, CTA pede o comentário antes do toque.

Ângulos já usados (não repetidos): A calor no painel · B "um galão pro dia todo" (capacidade) · C "pé na estrada" · D "não molha nada" (sem suor + vedação) · E "quente ou fria" (12 h / 18 h). Corrosão e boca larga só apareceram como reserva (D e E), nunca foram ao ar.

## Ordem dos trechos (cenário nunca colado no mesmo cenário)
| Parte | Trechos, em ordem | Velocidade | Duração | Movimento real |
|---|---|---|---|---|
| Intro | **G 0,8-1,8** (escritório) → **H 1,1-2,1** (fogueira) → **E 3,4-4,3** (mirante) | 1,0× | ~2,9 s | mão entra e pega a alça nos três; um cenário por palavra da fala |
| Apresentação | **H 2,1-3,1** → **G 2,5-4,5** → **H 4,4-5,2** → **G 4,5-6,0** (reserva: H 5,2-5,8 no fim) | 0,9× | ~6,6 s | garrafa levantada (H), inclina e volta no alto (G), volta à mesa (H), desce à mesa (G) |
| CTA | **E 4,3-8,0** | 1,0× | ~3,7 s | mão levanta a garrafa alguns centímetros e segura |

**Proibido:** G 1,9-2,4 s (copo-tampa sai pelo alto; cortar o G da intro antes de 1,85) e H 3,2-4,3 s (a faixa preta do meio some). E 0-3,2 s (garrafa parada sem mão) fora. Nada abaixo de 0,9×.

---

## Opção 1 (ESCOLHIDA, `opcao_escolhida`): "Qual seu rolê?"
A pergunta é de resposta fácil (escolher 1 de 3) e as três respostas estão na tela, uma em cada corte: escritório, fogueira, mirante. A apresentação entrega o que nenhum vídeo da garrafa disse: o aço inox que resiste à corrosão e a boca larga para lavar, os dois do anúncio.

Duração prevista: cerca de 14 s (2,8 + 6,4 + 3,6 de fala, mais respiros).

| Parte | Clipe | Fala | Texto de tela | Rodapé |
|---|---|---|---|---|
| Intro | G (+ H, E) | Trabalho, acampamento ou trilha: qual é o seu rolê? (8 palavras) | **QUAL SEU ROLÊ?** / trabalho, camping ou trilha | (vazio) |
| Apresentação | H (+ G) | Garrafa Térmica MODUS: aço inox que resiste à corrosão, segundo o fabricante. Boca larga pra lavar rápido. (17 palavras) | **AÇO INOX 304*** / boca larga pra lavar. Letreiro trocando a cada ~1,6 s: MODUS → AÇO INOX 304* → RESISTE À CORROSÃO* → BOCA LARGA | *Dados do fabricante |
| CTA | E | Comenta onde você usaria e toca no produto pra conferir. (10 palavras) | **ONDE VOCÊ USARIA?** / comenta e toca no produto | (vazio) |

### Por que funciona
- **Intro:** pergunta no quadro 0, sem precisar saber nada do produto para responder. Cada palavra cai sobre o seu cenário (trabalho no escritório, acampamento na fogueira, trilha no mirante) e em todos a mão pega a garrafa: movimento já no primeiro segundo, garrafa grande e nítida. Não cita recurso; termina com o produto em foco.
- **Apresentação:** abre nomeando o produto e dá um ângulo novo (material e limpeza), que conversa com qualquer intro: quem leva para o trabalho e para o mato quer uma garrafa que não estrague e seja fácil de lavar. Os dados são do texto do vendedor, com "segundo o fabricante" e rodapé. O letreiro troca no ritmo dos cortes H/G/H/G.
- **CTA:** pede o comentário primeiro (como no body splash D) e só depois o toque. Funciona sozinha: "onde você usaria" não depende da pergunta da intro e não repete benefício. Frase diferente das CTAs de B a E.

## Opção 2 (reserva): "Onde ela combina?"
Mesma ordem de trechos. Apresentação com o uso indicado pelo vendedor ("acampamentos, caminhadas ou escaladas") e "acabamento elegante e alça prática".

| Parte | Clipe | Fala | Texto de tela | Rodapé |
|---|---|---|---|---|
| Intro | G (+ H, E) | Escritório, fogueira ou mirante: onde ela combina mais? (8 palavras) | **ONDE ELA COMBINA?** / escritório, fogo ou mirante | (vazio) |
| Apresentação | H (+ G) | Garrafa Térmica MODUS: feita pra acampamento, caminhada e escalada, segundo o fabricante. Alça prática e acabamento elegante. (17 palavras) | **FEITA PRO AR LIVRE*** / alça prática. Letreiro: MODUS → ACAMPAMENTO → CAMINHADA → ESCALADA | *Dados do fabricante |
| CTA | E | Escolhe um e comenta. Depois toca no produto e confere. (10 palavras) | **ESCOLHE UM** / e toca no produto | (vazio) |

## Por que a opção 1 e não a 2
1. "Resiste à corrosão" e "boca larga" são ganhos concretos e inéditos na conta; "acabamento elegante" é vago e o uso ao ar livre já foi dito nos vídeos B e C.
2. "Qual seu rolê?" é mais curta e mais falada; a CTA da opção 2 depende da intro ("escolhe um") e quebra a regra de combinação.

## Alertas
1. **Campo `clipe` do JSON:** o `preparar.py` copia só o clipe principal de cada parte. Para os três arquivos subirem, ficou intro = G, apresentação = H, CTA = E; a intro **começa pelo G**, mas também usa H e E (ver `trecho`/`complemento`), e a apresentação alterna H e G.
2. **Nunca 48H** (só aparece na arte do vendedor). Não citar tempo térmico, cor, preço, urgência. "Livre de BPA" ficou de fora (difícil na voz).
3. **Regra da 5ª violação:** clipe em tela cheia, sem janela/moldura fixa; em todo trecho a mão move a garrafa (a reserva H 5,2-5,8 só tem a mão soltando: usar no máximo 0,6 s). `freezedetect` limpo, nada de quadro congelado.
4. **Clipe E:** a linha pequena da etiqueta tem letras trocadas (aceito pelo operador): zoom máximo 1,10×, sem destaque nela.
5. **Nada desenhado sobre a garrafa** (ícone de ferrugem, gota, brilho de "inox"): para a política de alegação enganosa, realce ligado a qualidade conta como demonstração. Letreiro e título só no alto, longe dos rótulos; transições opacas, sem tingir a etiqueta.
6. Visual diferente das edições da garrafa: B outdoor laranja, C placa de estrada (asfalto/amarelo), D "seco ao toque" (giz/tinta/cobalto), E "termo duplo" (carvão/brasa/gelo). Pode seguir a estrutura do body splash D (título-pergunta de alto contraste, uma cor de destaque), com paleta própria.
7. **Voz:** ouvir "MODUS" (deve soar "Módus") e "rolê".
8. **Link:** confirmar que o produto marcado é o de `<link do produto>`, com a verde-militar.
9. Uso dos clipes: G/H vão para o 3º vídeo (D, E, F) e o E para o 3º (B, C, F).
