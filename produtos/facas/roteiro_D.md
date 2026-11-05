# Roteiro D — faqueiro 6 peças (`facas`), 19/10/2026

Fonte: `anuncio.md` (texto do vendedor) e fotos `ref_kit_recorte.jpg`, `anuncio_principal.jpg`, `anuncio_usos.jpg` (fotos de uso do próprio vendedor: faca do chefe no tomate, cutelo na carne, tesoura no talo, descascador na batata).
Clipes novos **G, H, I**. Cada um parte de um primeiro quadro 9:16 feito antes no editor de imagem (Nano Banana, 0 crédito), que o operador aprova antes de gerar. Créditos: **50 = G Fast (20) + H Fast (20) + I Lite (10)**, sem margem.
Mão usando a peça nos três clipes. Fundos novos: **tábua de nogueira escura no escuro (G)**, **bancada de pedra verde-sálvia vista de cima (H)**, **área de churrasco com brasa ao fundo (I)**. Nenhum repete ardósia (A, E), caixa preta (D) nem cozinha clara com tomate (F).

Troquei o "mármore claro" da proposta do H por verde-sálvia: a cena do tomate (F) já é bancada branca de mármore/quartzo, e os dois ficariam parecidos.

## Duas opções de ângulo (os mesmos 3 clipes servem às duas)

### Opção 1 (recomendada, **escolhida pelo operador em 19/10/2026**, fala do H ajustada): "Uma peça pra cada tarefa"
| Parte | Clipe | Fala | Texto de tela | Rodapé |
|---|---|---|---|---|
| Intro | G | Você ainda usa a mesma faca pra cebola, carne e cheiro-verde? (11 palavras) | **UMA FACA PRA TUDO?** / cebola, carne, cheiro-verde | (vazio) |
| Apresentação | H | Faqueiro de seis peças: a faca do chefe parte a cebola, a tesoura corta o cheiro-verde, o cutelo encara a carne. Cada tarefa com a peça certa. (26) | **A PEÇA CERTA** / pra cada tarefa da cozinha | (vazio) |
| CTA | I | Qual peça você usaria primeiro? Toca no produto e confere o kit. (12) | **QUAL PEÇA PRIMEIRO?** / toca no produto e confere | (vazio) |

### Opção 2: "Da cozinha ao churrasco"
| Parte | Clipe | Fala | Texto de tela | Rodapé |
|---|---|---|---|---|
| Intro | G | Dia de churrasco, e a faca de casa não dá conta de tudo? (12) | **DIA DE CHURRASCO?** / e a faca não dá conta | (vazio) |
| Apresentação | H | Faqueiro de seis peças pra cozinha e churrasco. Segundo o fabricante, aço inoxidável e cabo de toque firme, que encaixa na mão. Elegante da bancada à churrasqueira. (27) | **COZINHA E CHURRASCO** / aço inox e cabo firme\* | \*Dados do fabricante |
| CTA | I | Prepara o próximo churrasco com o kit completo. Toca no produto e confere. (12) | **PRÓXIMO CHURRASCO** / toca no produto e confere | (vazio) |

**Por que recomendo a 1:** fala e imagem andam juntas nos três clipes (cebola com a faca do chefe, cheiro-verde com a tesoura, carne com o cutelo) e a dor ("a mesma faca pra tudo") é do dia a dia, não só de fim de semana. Não usa dado de desempenho, então não tem rodapé. A 2 é boa se o operador quiser puxar o churrasco, mas tem a fala do H um pouco desencontrada da imagem (tesoura no cheiro-verde enquanto fala de aço e cabo).

## Cena e ação de cada clipe

| Clipe | Modelo | Primeiro quadro (origem → arquivo) | Cena | Ação |
|---|---|---|---|---|
| G, intro | Veo 3.1 Fast | `quadro_tomate.jpg` → `fotos/quadro_G_cebola_916.jpg` | Tábua grossa de nogueira escura, bancada preta, fundo quase preto, luz quente baixa da esquerda raspando a lâmina | Mão com a faca do chefe parte uma cebola descascada ao meio num golpe só (0,5-3 s); as metades caem para os lados; aos ~4 s corta uma fatia fina da metade direita; faca fica na tábua até o fim |
| H, apresentação | Veo 3.1 Fast | `ref_kit_recorte.jpg` → `fotos/quadro_H_salvia_916.jpg` | Vista de cima, pedra verde-sálvia fosca, luz do dia. Metade de cima: cutelo, chefe, carne, descascar e descascador em fila. Metade de baixo: tábua redonda de bétula com cebolinha e salsinha | **Kit inteiro no quadro.** A mão (só uma, pela direita embaixo) pica o cheiro-verde com a tesoura, abrindo e fechando ~1 vez por segundo, pedacinhos verdes caindo; as 5 peças da fila não se mexem |
| I, CTA | Veo 3.1 Lite | `ref_kit_recorte.jpg` → `fotos/quadro_I_churrasco_916.jpg` | Área de churrasco no começo da noite, ângulo alto (~60°), tábua rústica sobre pedra; churrasqueira de tijolo desfocada ao fundo com brasa e chama | Chama e fumaça mexendo o tempo todo; aos ~1 s a mão empurra o cutelo pela carne num corte só, a fatia tomba aos ~4 s; o cutelo fica apoiado na tábua até o fim |

**Kit inteiro no H, não na CTA:** a CTA é Lite, e o único Lite com o kit inteiro (clipe C do lote A) derivou a lâmina branca do descascador depois de ~4,5 s. No H (Fast) o kit aparece todo enquanto a fala diz "faqueiro de seis peças", e o Lite fica com uma peça grande e uma ação curta.

## Como pedir no Flow
- Coleção `facas`. Para cada clipe: (1) no editor de imagem, partir da imagem de origem indicada (para H e I clicar na versão **original** da `ref_kit_recorte.jpg` no histórico antes de cada pedido novo), escolher **9:16** no menu ao lado do Nano Banana e colar o `prompt_quadro` do `roteiro_D.json`; (2) conferir o quadro (ver abaixo); (3) baixar em 1K e subir como arquivo novo com o nome da tabela; (4) no agente: "Generate exactly one video, vertical 9:16, using the attached image as the FIRST FRAME (start frame). Name the video facas_<parte>_<clipe>. PROMPT: <prompt>".
- No I escrever no pedido "generate it with the Veo 3.1 Lite model (10 credits)". Conferir o custo antes de aprovar: 20, 20, 10.
- Ordem sugerida: H (o mais difícil, com o kit inteiro), G, I.
- **Conferência dos quadros antes de mostrar ao operador:** G: relevo de losangos na lâmina, virola preta, cabo marrom rajado, nenhuma outra faca no escuro. H: exatamente 4 facas + 1 tesoura + 1 descascador, cutelo retangular, lâmina do descascador branca, tesoura com 2 alças pretas e parafuso prateado, uma mão só, nada cortado na borda. I: cutelo retangular com o lado chato virado para a câmera (ângulo baixo já deformou o cutelo no lote A; se deformar, pedir vista mais de cima), sem espeto, garfo ou pegador perto da tábua.

## Descrição fixa do produto (igual, palavra por palavra, nos 3 prompts)
> PRODUCT: a 6-piece kitchen knife set made of exactly these six pieces and nothing else: (1) a cleaver with a wide flat rectangular blade, a straight cutting edge and a squared front end; (2) a chef's knife with a broad blade that tapers to a pointed tip; (3) a carving knife of the same length with a narrower blade that tapers to a pointed tip; (4) a small paring knife with a short, narrow pointed blade. All four knives have matte black blades whose flat sides are covered edge to edge with a raised embossed diamond pattern of small pyramid-shaped bumps, a thin bright silver line along the cutting edge, a short glossy black bolster where the blade meets the handle, and a rounded handle with a reddish-brown wood-grain pattern of dark swirling grain lines, slightly thicker at the rounded back end. (5) A pair of kitchen scissors with two black plastic handle loops, a round silver pivot screw, a small serrated grip notch on the inner side of the handles and two plain polished stainless steel blades, one of them with a small hooked notch near the pivot. (6) A Y-shaped vegetable peeler made of matte black plastic, with a straight handle and a short horizontal white ceramic blade held between the two arms of the Y. No brand names, no logos and no lettering on any piece. The blades always stay matte black with the raised diamond pattern clearly visible, the cleaver blade always stays a wide rectangle, the peeler blade always stays white, and the handles always keep the reddish-brown wood-grain look.

## Prompts
Texto completo, pronto para colar, no `roteiro_D.json` (`prompt_quadro` e `prompt`). Todo `prompt` começa com "Use the attached product photo as the exact reference: keep shape, colors, logo, labels and every detail identical." + a descrição fixa, diz qual peça aparece ("the other five pieces of the set are not in the scene" em G e I) e termina com "No text, no captions, no letters, no extra logos, no product changes, no morphing, no people talking to camera."
- **G:** começa do quadro; golpe único descendo pelo meio da cebola até a tábua aos ~3 s, metades caem para os lados mostrando os anéis; aos ~4 s uma fatia fina da metade direita; faca nunca sobe mais que alguns centímetros, lado chato com relevo sempre para a câmera, não gira. Proibidos: outras facas, cepo, utensílios, tigelas, pratos, potes, ervas, segunda mão.
- **H:** vista de cima travada; a tesoura abre e fecha ~1 vez/s sobre o cheiro-verde, pedacinhos caindo; a mão anda devagar rente à tábua, nunca levanta nem vira a tesoura; as 5 peças da fila não se mexem; "exactly four knives, one pair of scissors and one peeler" no quadro o tempo todo; sem segunda mão segurando as ervas. Proibidos: outras facas, cepo, segunda tesoura, utensílios, tigelas, copos, potes, pano.
- **I:** chama e fumaça ao fundo o tempo todo; um corte só no pedaço de carne (1-4 s), fatia tomba; cutelo fica apoiado; nunca sobe, não gira, lado chato para a câmera, retângulo rígido. Proibidos: outras facas, cepo, espetos, garfo de churrasco, pegador, pratos, tigelas, garrafas, copos, pessoas.

## Por que funciona
- **Intro (G):** a pergunta acerta um hábito comum (uma faca só pra tudo) e o corte da cebola num golpe é satisfatório de ver desde o primeiro quadro, com a faca grande e nítida. Não cita recurso; termina na dor. Na opção 2, a cebola vira o vinagrete do churrasco.
- **Apresentação (H):** abre nomeando o faqueiro e mostra as seis peças de uma vez, com a tesoura trabalhando. Ângulo novo: em vez de listar as peças (lote B) ou falar da lâmina (A, B), liga cada peça a uma tarefa, como nas fotos de uso do vendedor.
- **CTA (I):** devolve a escolha ao público ("qual peça primeiro?") sem repetir benefício e serve depois de qualquer apresentação, porque toda apresentação mostra o kit. O fogo da churrasqueira mantém a cena viva mesmo depois do corte.

## Alertas
- **Medidas não entram:** o anúncio diz "20 cm" para chefe, carne e cutelo e "9 cm" para descascar e descascador, mas a foto de medidas do vendedor mostra outros números (30-32 cm no total, lâminas de 17,8 / 19 / 12,7 cm). Por isso nenhuma fala cita tamanho.
- **Cabo:** a descrição diz "cabo madeira" e as especificações dizem "Aço + Plástico". As falas dizem só "cabo de toque firme, que encaixa na mão" (opção 2, texto do vendedor, com "segundo o fabricante"). Nunca "cabo de madeira".
- **Aço inoxidável** (opção 2) está na descrição do vendedor; tratei como especificação: "segundo o fabricante" + rodapé "\*Dados do fabricante".
- "Antiaderente" só aparece no título do anúncio: fora das falas. "Ondulações que prolongam a durabilidade" já foi usado nos lotes A e B: fora deste lote.
- A foto de usos chama o cutelo de "Cut bone knife": **não** dizer que corta osso. "Encara a carne" é o que a foto mostra (cutelo fatiando carne).
- "Tesoura multiuso" está nos itens inclusos; cortar cheiro-verde é uso comum de tesoura de cozinha (a foto do vendedor mostra a tesoura cortando um talo).
- Sem preço, desconto, urgência, marca (INVICTUS/LIEXY) nem cepo. As legendas B e C usaram emoji; a regra pede nenhum emoji, e a `legenda_D.txt` vem sem.
- **Voz:** conferir "cheiro-verde", "cutelo" e "churrasqueira" ao ouvir.

## Riscos por clipe (conferir na tira a cada 0,25 s nos 2 primeiros segundos e a cada 0,5 s depois)
- **G (Fast):** (1) a lâmina pode "afundar" na cebola e parecer encurtar, ou a cebola pode atravessar a lâmina em vez de partir; (2) segunda mão segurando a cebola (é o gesto natural; pedimos uma mão só, mas o Veo tende a pôr); (3) faca virar e mostrar o lado do fio, ou o relevo sumir na luz baixa; (4) a fatia extra pode sair estranha (como o tomate em pé do F). Trecho mais provável de servir: 0-4 s, que cobre a intro (~4 s). No quadro: o Nano Banana pode trocar a mão ou deixar a faca menor ao escurecer a cena.
- **H (Fast):** o mais arriscado. (1) Tesoura deformando ao abrir e fechar (lâminas tortas, alça a mais, parafuso sumindo); (2) segunda mão segurando o maço; (3) a mão esbarrar na fila e mover peças, ou peças da fila mudarem (cutelo afinar, descascador perder a lâmina branca, contagem mudar); (4) a aproximação do Fast cortar a fila nas bordas (aconteceu no lote A: o Fast avança mais que o pedido), por isso o quadro tem margem e a câmera está travada. Se a tesoura falhar no fim, a fala (~10 s) pode usar o trecho bom em câmera lenta até 0,75×.
- **I (Lite):** (1) o Lite deriva detalhe pequeno depois de ~4,5 s: conferir o relevo do cutelo e o cabo rajado de 4 a 8 s (a CTA só precisa de ~5 s, então 0-4,5 s em 0,9× basta); (2) a carne pode "grudar" na lâmina ou o corte não terminar; (3) o Veo pode pôr espeto ou garfo perto da churrasqueira: se aparecer perto da tábua, cobrir ou cortar; (4) fogo forte pode estourar a luz no cutelo. O fogo dá movimento contínuo mesmo se a mão parar cedo.
- **Geral:** se um clipe falhar inteiro, o vídeo ainda tem dois com mão, mas sem crédito de reserva o operador decide antes de montar. Na edição, nada de quadro congelado com o kit parado; o kit inteiro aparece rodando no H.
