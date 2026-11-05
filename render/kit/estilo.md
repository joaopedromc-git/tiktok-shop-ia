# Kit de estilo — vídeos TikTok Shop

O agente `editor-video` lê este arquivo antes de cada edição. **Regras fixas** valem sempre; o **cardápio** é para combinar livremente, escolhendo o que mais harmoniza com o produto e os clipes. Nunca repetir a mesma combinação (paleta + par de fontes + estilo de legenda) do vídeo anterior do mesmo produto.

## Regras fixas
1. **Formato:** 1080×1920, 30 fps. Duração = soma das 3 partes (intro, apresentação, CTA), tipicamente 15-25 s.
2. **Gancho (0-1 s):** impacto visual (punch-in de 1,2→1,0 em 0,4 s, flash branco de 2-3 quadros, ou texto gigante entrando com escala) **e** `batida.wav` em 0 s. A voz começa entre 0,15 e 0,35 s.
3. **Ritmo:** uma quebra de padrão a cada 2-3 s (punch-in, mudança de enquadramento por escala/posição do vídeo, callout, texto novo). Nada parado por mais de 3 s.
4. **Som:** no máximo 1 efeito a cada ~1,5 s. Volumes: voz 1,0; efeitos 0,25-0,45 (batida até 0,6). Nunca efeito sobre palavra-chave da fala.
5. **Legenda:** fala inteira, palavra por palavra no tempo do `fala_<parte>.json`; 1 a 3 palavras por vez; palavra-chave destacada (cor de destaque ou escala 1,1). Posição entre 55% e 72% da altura.
6. **Zonas seguras:** nada importante abaixo de 80% da altura nem nos 15% da direita (botões do TikTok). Títulos entre 10% e 35% da altura.
7. **Callouts** (seta, círculo, sublinhado, etiqueta) só sobre detalhes que a `analise_<lote>.md` diz que aparecem naquele tempo e posição. Se o quadro se mexe, acompanhar com keyframes ou não usar callout.
8. **Fatos:** nenhum texto mostra algo que não esteja no roteiro. Rodapé "*Dados do fabricante" (pequeno, 28-32 px, branco 80%, em 76-78% da altura) durante toda parte cuja fala tenha dado.
9. **Transições** entre partes: corte seco com `whoosh_curto`, ou deslize/zoom de 0,25-0,35 s com `whoosh`. Nunca mais longo que 0,4 s.
10. **CTA:** `subida.wav` terminando no início da CTA (ou `brilho` no produto); `clique.wav` no momento do "toque"; elemento apontando para baixo/esquerda, onde aparece o produto marcado no TikTok (canto inferior esquerdo, acima de 80% da altura).
11. **Vídeo de fundo** sempre `muted`; a voz e os efeitos são `<audio>` separados, **cada um com `id` único** (sem id o render sai mudo).
12. **Fontes:** só as do `fontes.css`. Emoji com moderação (no máximo 2 por vídeo), via "Noto Color Emoji".
13. **Técnico (HyperFrames):** `window.__timelines["main"]` com GSAP pausado; sem `Math.random`, `Date.now` nem internet (GSAP vem de `assets/gsap.min.js`); todo elemento temporizado com `id`, `data-start`, `data-duration`, `class="clip"`. Rodar `hyperframes lint` e corrigir todos os erros.

## Cardápio

### Paletas (fundo de etiqueta / destaque / texto)
| Nome | Base escura | Destaque | Texto | Combina com |
|---|---|---|---|---|
| amarelo-impacto | #111111 | #FFD34D | #FFFFFF | casa, utilidade, tecnologia barata |
| neon-tech | #0B0F1A | #3DF5A7 | #F2F5FF | eletrônicos, gadgets, iluminação |
| premium-noir | #0A0A0A | #C9A86A | #F5F1E8 | perfumes, cosméticos, kits presente |
| coral-vivo | #1A1020 | #FF5A5F | #FFFFFF | moda, beleza, acessórios |
| azul-limpo | #0E1B2C | #4FC3F7 | #FFFFFF | limpeza, banho, cozinha |
| outdoor | #12140F | #F28C28 | #FFFFFF | camping, garrafas, ferramentas |

### Pares de fonte (título / legenda)
- Anton / Poppins 800 — impacto clássico de TikTok
- Bebas Neue / Inter 800 — limpo e moderno
- Archivo Black / Poppins 700 — robusto
- DM Serif Display / Inter 600 — premium, elegante
- Bricolage Grotesque 800 / Bricolage Grotesque 600 — atual, editorial
- Montserrat 900 / Montserrat 700 — o estilo dos vídeos A

### Estilos de legenda
- **caixa-palavra:** cada palavra numa etiqueta da cor base, a palavra-chave na etiqueta da cor de destaque.
- **contorno-pop:** texto branco com contorno preto 8-10 px, entra com escala 0,8→1 (0,12 s); palavra-chave na cor de destaque.
- **karaoke:** a frase inteira em branco 60%, cada palavra acende em 100% no seu tempo; palavra-chave na cor de destaque.
- **sublinhado:** palavra-chave ganha um traço da cor de destaque que se desenha por baixo.

### Animações de título
slam (escala 2→1 com back.out), máquina de escrever (letras em sequência a cada 0,03 s), corte por máscara (sobe por trás de uma linha), deslize lateral com desfoque de movimento, contagem (para números do anúncio, ex.: "0 → 5 tomadas").

### Tratamento do vídeo
Punch-in, zoom lento contínuo (1,0→1,08), pan lateral leve, contorno ou brilho sobre o vídeo rodando (destacar o produto; **nunca congelar quadro**, regra da 3ª violação), leve vinheta, divisão de tela (detalhe + produto inteiro). Clipe sempre em tela cheia, sem moldura ou janela fixa. Câmera lenta nunca abaixo de 0,9× (5ª violação, 28/10/2026).

### Sons (`assets/sfx/`)
| Arquivo | Uso |
|---|---|
| batida.wav | gancho em 0 s; revelação forte |
| whoosh.wav | transição com movimento, título deslizando |
| whoosh_curto.wav | corte seco entre partes |
| pop.wav | etiqueta/texto entrando |
| tique.wav | itens de lista aparecendo um a um |
| brilho.wav | destacar o produto, "novo" |
| subida.wav | tensão terminando na entrada da CTA |
| clique.wav | o "toque no produto" da CTA |
