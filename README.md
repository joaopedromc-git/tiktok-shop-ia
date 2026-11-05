# Vídeos de afiliado com IA para o TikTok Shop

Pipeline que transforma o anúncio de um produto em vídeos verticais curtos, sem ninguém aparecer. Agentes de IA escrevem os roteiros, o Google Flow (Veo) gera os clipes, a narração sai do edge-tts e a edição é feita em HTML com HyperFrames. As etapas sensíveis (aprovar roteiro e clipes, marcar o produto, publicar) ficam com uma pessoa.

## Como funciona

```
Anúncio do vendedor
  → agente especialista-promocao: roteiro em 9 partes (3 ganchos, 3 descrições, 3 chamadas)
  → aprovação 1 (roteiro)
  → Google Flow: primeiro quadro no editor de imagem + clipe de 8 s com movimento
  → conferência quadro a quadro (fidelidade ao produto e movimento real)
  → aprovação 2 (clipes)
  → narração (edge-tts) + edição HyperFrames (agente editor-video) + render em Docker
  → vídeo final + legenda → publicação manual, marcada como "Conteúdo gerado por IA"
```

- **Memória entre sessões:** o agente de roteiro lê `produtos/aprendizados.md` antes de cada roteiro. Cada falha do Flow e cada violação do TikTok vira uma regra nesse arquivo.
- **Sem repetir:** o banco PostgreSQL guarda produtos, clipes e vídeos; a view `proximo_video` escolhe a próxima combinação ainda não usada.
- **Custo:** zero além de uma assinatura do Google AI Plus (créditos do Flow). Nenhuma API paga.

## Regras de conteúdo

- Só fatos do anúncio do vendedor. Dado de desempenho vai com "segundo o fabricante" na fala e "*Dados do fabricante" na tela.
- Nada de preço, urgência falsa, comparação com marcas ou promessa de resultado.
- Todo vídeo é marcado como gerado por IA na publicação.

## O que deu errado (e virou regra)

A conta recebeu 5 violações automáticas do TikTok. Cada uma está analisada em `produtos/aprendizados.md`:

| Violação | Causa | Regra criada |
|---|---|---|
| Produto inconsistente | Cena ampla com objetos que pareciam parte do produto; padrão do tecido diferente do anúncio | Produto protagonista em todo quadro; clipe com qualquer diferença é rejeitado |
| Quadro estático | Clipes "primeiro quadro + só câmera" e quadros congelados na edição | Produto se movendo de verdade em todo clipe (mão ou exibição de estúdio) |
| Alegação exagerada | Gancho prometia um efeito que o anúncio não prometia | Fala e tela só repetem o texto do vendedor (recurso aceito, pontos removidos) |

O ponto central: a receita que evitava a primeira violação (fidelidade total, câmera só se aproximando) era exatamente a que causava a segunda. A solução foi montar o primeiro quadro fiel no editor de imagem e pedir ao vídeo uma ação real com o produto.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `.claude/agents/` | Agentes `especialista-promocao` (roteiro e prompts do Flow) e `editor-video` (edição HyperFrames) |
| `CLAUDE.md` | Regras fixas do projeto |
| `LEIAME.md` | Arquitetura, instalação e API do render |
| `docs/` | Especificação da arquitetura dos vídeos |
| `db/` | Esquema do PostgreSQL |
| `n8n/` | Fluxo do bot do Telegram (versão inicial, desativada) |
| `render/` | Serviço de narração e montagem (FastAPI + ffmpeg) e o editor HyperFrames |
| `produtos/<produto>/` | Anúncio, roteiros, análises dos clipes, edições (`edicao_*/`), legendas e vídeos finais |

Os vídeos finais estão em `produtos/*/video_*.mp4`, reduzidos para 720p. Fotos de referência, clipes brutos e capturas de tela ficaram fora do repositório.
