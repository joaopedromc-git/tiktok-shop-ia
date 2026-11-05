# Automação de vídeos — TikTok Shop (afiliado, vídeos de IA, sem aparecer)

Responder em português do Brasil, direto. Para passos: **Onde fazer / O que fazer / Caso necessário**.
Ler `LEIAME.md` antes de qualquer coisa: tem a arquitetura decidida, a API do render e a instalação.
## Regras que não mudam
- Custo zero além do Google AI Plus. Nada de API paga.
- Dado de desempenho do produto só com "segundo o fabricante" na fala e "*Dados do fabricante" na tela. Só usar o que está no anúncio do vendedor.
- A conta levou uma violação por inconsistência de produto (índice 185). Clipe de IA com letreiro, cor ou formato diferente do anúncio é rejeitado na parada 2.
- **2ª violação (peseira, 08/10/2026, −15 pontos, contestação negada):** detalhes em `produtos/aprendizados.md`. Desde então:
  - O produto vendido é o protagonista em **todos** os quadros (ocupa a maior parte da tela); nada de cena ampla com outros objetos que possam parecer parte do produto (almofadas, roupa de cama, acessórios). Foto do vendedor com outros itens só serve de primeiro quadro se for recortada só no produto.
  - Clipe com **qualquer** diferença visível do produto (padrão, textura, proporção, letreiro, cor) é rejeitado, mesmo "parecido". Nada de aceitar por pressa.
  - Nunca mostrar variações (cores, tamanhos) por desenho ou aproximação; só citar variação conferida no link do produto.
  - Na capa e no 1º segundo, o produto aparece grande e nítido.
  - Conferir que o link do `anuncio.md` é o mesmo produto que o operador vai marcar.
- **3ª e 5ª violações (facas 12/10 e Hilee B 28/10/2026, −4 pontos cada, "conteúdo em quadro estático"):** detalhes em `produtos/aprendizados.md`. Desde então:
  - **Todos os clipes** precisam do produto se movendo de verdade: pela mão (levantar, abrir, inclinar, girar, levar; mão só encostando não basta) ou em **exibição de estúdio com movimento** (produto girando, subindo, tampa abrindo; definição do operador em 03/11/2026). Só aproximação de câmera sobre produto parado **não conta**. Nada de câmera lenta abaixo de 0,9× e clipe sempre em tela cheia, sem moldura fixa.
  - Proibido clipe "locked-off, nothing moves" e proibido os 3 clipes no mesmo fundo.
  - O operador (14/10/2026): "o importante é não parecer uma foto parada, ou movimentos mínimos". Sombra ou luz mexendo não substitui mão; fogo, ondas e fumaça ao fundo ajudam, mas a ação principal é o produto se movendo (mão ou exibição de estúdio).
  - Na edição, **nada de quadro congelado** por mais de ~1 s (cartões com o produto parado, Ken Burns sobre foto/arte). O vídeo de fundo tem que estar rodando o tempo todo.
  - Sem crédito para gerar movimento de verdade, **não montar vídeo**: avisar o operador e esperar os créditos.
- **Revisor de conformidade (`revisor/`):** depois do roteiro aprovado e antes de gastar crédito do Flow, rodar `python revisor/revisar.py <codigo> <lote> --sem-video`; depois do render e antes de subir para o Drive, rodar de novo com o vídeo. Reprovado não segue: corrigir e rodar outra vez. "Atenção" vai para o operador decidir, com os trechos apontados.
- Nunca postar, digitar senha, resolver captcha ou aceitar termos. Marcar produto, marcar "Conteúdo gerado por IA", escolher música e publicar são sempre manuais.
- Todo vídeo pronto vai com a legenda para postar (gancho, benefício do anúncio, pergunta, chamada e 5-6 hashtags); regra completa no passo 9 da especificação.
- Tokens e senhas vão no `.env` ou nas credenciais do n8n, nunca no chat nem em arquivo versionado.
