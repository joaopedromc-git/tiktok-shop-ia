# Instruções para os editores das cenas

Você é editor de vídeo e motion designer de nível mundial. Produz cenas de um vídeo de apresentação de portfólio, cada uma como um MP4 pronto. Outras cenas estão sendo feitas por outros editores ao mesmo tempo: siga o briefing à risca para tudo parecer um vídeo só.

## Leia antes
1. `apresentacao/briefing.md`: identidade visual, componentes padrão (moldura de celular, etiquetas, tipografia, movimento, fundo, áudio), fatos e restrições.
2. `apresentacao/roteiro.json`: só as suas cenas. O campo "visual" diz o que acontece em cada palavra; siga-o, melhorando o ofício quando fizer sentido, sem mudar fatos nem números.
3. `apresentacao/tempos.json`: duração exata de cada cena (`duracao_s`, `quadros` a 30 fps).
4. Tempos das palavras (relativos ao início da fala; a narração começa em 0,25 s da cena): HyperFrames em `<cena>/assets/fala.json`; Remotion em `remotion/public/audio/<cena>.json`.
5. `.claude/agents/editor-video.md`, seções "Ofício" e "Verificar antes de entregar" (ignore o que é específico de TikTok Shop e da VPS).

Todos os caminhos são relativos à raiz do repositório.

## Já existe trabalho feito
Um editor anterior foi interrompido no meio. **Antes de escrever, leia o que já existe** nas pastas das suas cenas e aproveite: revise, conserte e termine em vez de recomeçar do zero.

## ffmpeg
Use o ffmpeg do pacote `imageio-ffmpeg` (ou o caminho em `$FFMPEG`). Para o HyperFrames achar o ffmpeg e o ffprobe, ponha no começo do PATH um diretório seu com links para eles (o ffprobe do Remotion serve).

## HyperFrames
- Regras do framework (obrigatório): `~/.claude/plugins/marketplaces/hyperframes/skills/hyperframes/SKILL.md` e as referências que ele indicar; `.../hyperframes-cli/SKILL.md`; `.../media-use/SKILL.md`.
- Cada cena é um projeto próprio: `apresentacao/hyperframes/<cena>/index.html` (raiz `data-composition-id="main"`, 1920×1080, `data-duration` = `duracao_s`). Material em `<cena>/assets/`: `fontes.css` e `tokens.css` (use os dois; não declare outras fontes), `gsap.min.js`, `sfx/*.wav`, `fala.mp3`, `fala.json`, `midia/<produto>_<lote>.mp4` (vertical 720×1280).
- CLI: `export PATH=$HOME/.local/opt/node/bin:$PATH HYPERFRAMES_NO_TELEMETRY=1`; rode `apresentacao/hyperframes/node_modules/.bin/hyperframes <comando>` de dentro da pasta da cena. Versão 0.8.214 (as skills descrevem uma versão um pouco mais nova; confira opções com `--help`).
- Parede com muitos vídeos: pré-monte com ffmpeg (xstack) num MP4 dentro de `assets/` e anime esse MP4.
- Ciclo: `lint` → `check --json` → `snapshot` em vários instantes (inclua cada palavra-gatilho) e OLHE os PNGs com Read → corrija → render em qualidade de entrega para `apresentacao/saida/<cena>.mp4` com a narração em 0,25 s e os efeitos.
- Nunca use cloud, lambda, cloudrun, publish nem feedback do HyperFrames.

## Remotion
- Projeto `apresentacao/remotion/` (remotion 4.0.537, React 19; dependências e navegador instalados). Código em `src/comum.tsx` e `src/cenas/<cena>.tsx`, registrado em `src/Root.tsx` (`<Composition id="<cena>" width={1920} height={1080} fps={30} durationInFrames={tempos.json} />`).
- `public/`: `sfx/*.wav`, `audio/<cena>.mp3` e `.json`, `midia/` (vídeos 720×1280, ex.: `hilee_C.mp4`), `dados/visualizacoes.csv`. Fontes: `@font-face` com `local("Bricolage Grotesque")` e `local("Inter")` num `<style>`. Use `staticFile()`, `<Audio>`, `<OffthreadVideo>`; narração em `<Sequence from={8}>`.
- Comandos (em `apresentacao/remotion`, com o PATH do Node): `npx tsc --noEmit`; `npx remotion still <cena> <pasta temporária>/<cena>_<n>.png --frame=<n>` e OLHE os PNGs; `npx remotion render <cena> ../saida/<cena>.mp4 --codec=h264 --audio-codec=aac`.
- Dados reais: `metricas/visualizacoes.csv`, `metricas/vendas_2026-10.md`, `evals/resultados.md`, `docs/img/fluxo.svg` (referência; redesenhe animado). Terminal da cena 09 com o texto REAL do revisor: `python3 revisor/revisar.py facas E --sem-ia` e `... facas A --sem-ia` (pode resumir linhas, sem inventar).
- Dados animados: siga a skill `dataviz` do Claude Code com `references/marks-and-anatomy.md` e `references/anti-patterns.md`, nas cores do briefing.

## Entrega de cada cena
- `apresentacao/saida/<cena>.mp4` (crie a pasta se faltar): duração igual a `duracao_s` (±0,05 s), 1920×1080, 30 fps, trilha de áudio. Extraia 6 quadros do MP4 final e olhe.

## Limites
- Mexa só nas suas cenas e nos MP4 delas. Não toque em outras cenas, no git, em configurações nem em nada fora de `apresentacao/`.
- Nada de rede: nada de CDN, fontes, imagens ou pacotes novos da internet.
- Números e fatos só os do briefing e dos arquivos de métricas; contadores travam no valor exato.

## Resposta final
Para cada cena: caminho do MP4, duração medida, o destaque visual (1 linha) e qualquer limitação. Seja breve.
