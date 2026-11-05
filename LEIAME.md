# Automação de vídeos — TikTok Shop

## Arquitetura decidida (06/10/2026)

- **VPS (Docker):** n8n orquestra e conversa com o Telegram; o container `render` faz narração (edge-tts) e montagem (ffmpeg); o PostgreSQL guarda produto, clipe e vídeo.
- **PC:** gera imagem e clipe no Google Flow (créditos do AI Plus), pelo Claude in Chrome ou à mão. Os clipes sobem para a VPS.
- **Custo:** zero além do que já é pago.
- **Unidade de trabalho:** 9 clipes por produto (3 introduções, 3 descrições/exibições, 3 CTAs). Cada vídeo é intro + descrição + CTA.
- **Paradas de aprovação no Telegram:** roteiro (antes de gerar) e clipes (antes de montar).
- **Rotação:** nunca repete combinação; nunca duas com a mesma introdução no mesmo dia; alterna produtos; escolhe sempre a combinação menos parecida com as já feitas.
- **Limite prático:** os 9 primeiros vídeos de um produto têm no máximo 1 parte em comum entre si. A partir do 10º, passam a repetir 2 das 3 partes. Recomendo gerar clipes novos depois do 9º em vez de ir até os 27.
- **Manual sempre:** marcar o produto, marcar "Conteúdo gerado por IA", escolher a música comercial e publicar.

## Instalação

Roda em qualquer servidor com Docker que já tenha o n8n e um PostgreSQL.

- **Acesso à VPS:** os scripts do PC (`render/kit/preparar.py`) e o agente `editor-video` falam com o servidor por `ssh minha-vps` e `scp ... minha-vps:`. `minha-vps` não é um servidor público: é um apelido de SSH. Crie o seu em `~/.ssh/config`:
  ```
  Host minha-vps
      HostName <endereço do seu servidor>
      User <seu usuário>
      IdentityFile ~/.ssh/<sua chave>
  ```
  Teste com `ssh minha-vps echo ok`. Se preferir outro nome, troque `VPS` em `render/kit/preparar.py` e os comandos em `.claude/agents/editor-video.md`.
- **Configuração:** copie `.env.exemplo` para `.env` e preencha `RENDER_TOKEN` (uma senha longa e aleatória) e `REDE_N8N` (a rede Docker onde o n8n roda).
- **Subir ou atualizar o render:** `docker compose up -d --build`. Se der erro, `docker logs render`.
- **Banco:** crie o banco `tiktok` e as tabelas (o script não apaga nada):
  ```
  docker exec -i <container-do-postgres> sh -c 'psql -U $POSTGRES_USER -d tiktok' < db/schema.sql
  ```
- **Testar a narração:**
  ```
  docker exec render python -c "import urllib.request,json,os;r=urllib.request.Request('http://localhost:8000/tts',data=json.dumps({'texto':'Segundo o fabricante, são dois vírgula quatro litros.','saida':'teste/fala.mp3'}).encode(),headers={'content-type':'application/json','x-token':os.environ['RENDER_TOKEN']});print(urllib.request.urlopen(r).read().decode())"
  ```
  O áudio sai em `dados/teste/fala.mp3`. Vozes disponíveis (`GET /vozes`): Thalita, Antonio e Francisca. Para trocar, mude `VOZ` no `docker-compose.yml`.
- **Credenciais no n8n:** Postgres (banco `tiktok`), Header Auth `x-token` para o render, bot do Telegram e Gemini (AI Studio, camada gratuita). Em `n8n/bot.ts`, troque `ID_DA_CREDENCIAL` e `SEU_CHAT_ID` pelos seus.
- **Editor (HyperFrames):** `render/kit/gsap.min.js` não vem no repositório; baixe o GSAP (`npm pack gsap` ou o CDN oficial) e coloque o `gsap.min.js` nessa pasta.

## Bot do Telegram (fluxo `TikTok – Bot`, fonte em `n8n/bot.ts`)

| Mensagem ou botão | O que acontece |
|---|---|
| `/produto` + texto do anúncio (pode ir como legenda de foto ou álbum) | O Gemini escreve 3 intros, 3 descrições e 3 CTAs, que são gravadas no banco. O bot manda o roteiro com **Aprovar** e **Refazer** (parada 1). |
| ✅ Aprovar roteiro | O bot manda os 9 prompts do Google Flow, com o nome de arquivo de cada clipe. |
| 🔁 Refazer | Novo roteiro. Clipes já gerados ou aprovados não mudam. |
| Qualquer outra coisa | Ajuda e o seu chat id. |

## API do render (o n8n chama `http://render:8000`, cabeçalho `x-token`)

| Chamada | Para quê |
|---|---|
| `GET /saude` | Conferir se está no ar |
| `PUT /arquivo/{caminho}` | Guardar um arquivo (corpo binário) |
| `GET /arquivo/{caminho}` | Baixar um arquivo (para mandar no Telegram) |
| `POST /tts` | `{texto, saida, voz?, velocidade?}` → narração em mp3 |
| `POST /montar` | `{saida, partes:[{clipe, audio?, texto_tela?, rodape?}], estilo?}` → vídeo 1080x1920 |
| `POST /capa` | `{video, saida, segundo?, titulo?}` → capa em jpg (use o clipe bruto) |
| `GET /vozes` | Vozes pt-BR do edge-tts |

Padrão de pasta sugerido: `modus2400/clipes/intro_1.mp4`, `modus2400/audio/intro_1.mp3`, `modus2400/videos/v_1_2_3.mp4`.

O que a montagem faz: corta e redimensiona qualquer clipe para 9:16, troca o som do clipe pela narração, congela o último quadro se a fala for maior que o clipe, e escreve o texto de tela centralizado no alto e o rodapé pequeno acima da faixa que o TikTok cobre. Fonte, tamanho, cor e posição mudam pelo campo `estilo`.

## Próximo vídeo do dia

`SELECT * FROM tiktok.proximo_video LIMIT 1;` devolve a combinação a montar. Depois de montar, o n8n grava a linha em `tiktok.video`. Se a consulta voltar vazia, não há mais combinação válida para hoje.
