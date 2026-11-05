# Produtos

Uma pasta por produto. O nome da pasta é o código usado no banco e no revisor (`piseira` é a peseira de tricô).

| Arquivo | O que é | Quem escreve |
|---|---|---|
| `anuncio.md` | Texto do vendedor e o que pode ou não ser dito | Operador e sessão principal |
| `roteiro_<lote>.json` / `.md` | Falas, textos de tela, rodapé e os prompts do Flow de cada vídeo | Agente `especialista-promocao` |
| `analise_<lote>.md` | Conferência quadro a quadro dos clipes gerados (o que serve, em que trecho) | Sessão principal |
| `edicao_<lote>/` | `escolhas.md` (identidade visual), `gerar.py` e `index.html` (composição HyperFrames), `fala/` (tempo de cada palavra) | Agente `editor-video` |
| `legenda_<lote>.txt` | Legenda do post | Agente `especialista-promocao` |
| `video_<lote>.mp4` | Vídeo final, reduzido para 720p neste repositório | Render |

Os `gerar.py` e `index.html` de cada edição são **saídas do agente editor**, não código de biblioteca: cada vídeo tem a sua composição, com paleta, fontes e animações próprias. São mantidos para mostrar o que o agente produz.

`aprendizados.md` é a memória do projeto: cada falha do Flow, violação e resultado de venda vira um registro, lido pelo agente de roteiro antes de cada roteiro.
