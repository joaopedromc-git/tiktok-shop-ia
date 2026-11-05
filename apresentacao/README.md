# Vídeo de apresentação

Vídeo de 1 min 26 s (`docs/apresentacao.mp4`) feito com agentes, como os vídeos do projeto.

| Etapa | Quem fez | Arquivo |
|---|---|---|
| Fatos, identidade visual e componentes | sessão principal | `briefing.md` |
| Roteiro de 10 cenas, amarrado palavra por palavra ao que aparece na tela | agente roteirista | `roteiro.json`, `roteiro.md` |
| Narração com o tempo de cada palavra (edge-tts, voz Thalita) | script | `narrar.py` → `audio/`, `tempos.json` |
| Cenas de tipografia e montagem com os vídeos reais (01, 02, 04, 07, 08, 10) | dois agentes editores | `hyperframes/<cena>/index.html` |
| Cenas guiadas por dados: fluxo, alcance, funil e revisor (03, 05, 06, 09) | agente editor | `remotion/src/` |
| Montagem e volume (-16 LUFS) | script | `montar.py` |

As regras que os editores seguiram estão em `instrucoes_editores.md`. Cada cena foi conferida por quadros antes do render; os números são os de `metricas/` e `evals/`, e o terminal da cena 09 mostra a saída real do revisor.

## Refazer

```
pip install edge-tts imageio-ffmpeg
python apresentacao/narrar.py            # narração e tempos
python apresentacao/preparar_cenas.py    # copia estilo, efeitos, narração e mídia para cada cena
cd apresentacao/hyperframes && npm install && cd <cena> && npx hyperframes render --quality delivery -o ../../saida/<cena>.mp4
cd apresentacao/remotion && npm install && npx remotion render <id> ../saida/<cena>.mp4 --codec=h264 --audio-codec=aac
python apresentacao/montar.py            # junta as 10 cenas em saida/apresentacao.mp4
```

O `gsap.min.js` não vem no repositório; coloque-o em `comum/` antes de preparar as cenas. As paredes de vídeos das cenas 01 e 10 são pré-montadas com ffmpeg (xstack) dentro de `assets/`.
