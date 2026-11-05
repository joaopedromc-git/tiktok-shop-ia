"""Copia para cada cena o que ela usa: estilo comum, efeitos, narração e mídia.

Uso: python apresentacao/preparar_cenas.py
HyperFrames: apresentacao/hyperframes/<cena>/assets/
Remotion:    apresentacao/remotion/public/
Mídia vira <produto>_<lote>.mp4 (ex.: produtos/facas/video_A.mp4 -> facas_A.mp4) e imagens mantêm o nome.
"""
import json
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent


def nome_midia(rel):
    p = Path(rel)
    if p.suffix == ".mp4" and p.parts[0] == "produtos":
        return f"{p.parts[1]}_{p.stem.removeprefix('video_')}.mp4"
    return p.name


def copiar(origem, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    if not destino.exists() or destino.stat().st_mtime < origem.stat().st_mtime:
        shutil.copy2(origem, destino)


def comum(destino):
    for arq in ("fontes.css", "tokens.css", "gsap.min.js"):
        copiar(AQUI / "comum" / arq, destino / arq)
    for wav in (AQUI / "comum" / "sfx").glob("*.wav"):
        copiar(wav, destino / "sfx" / wav.name)


roteiro = json.loads((AQUI / "roteiro.json").read_text(encoding="utf-8"))
publico = AQUI / "remotion" / "public"
comum(publico)
for c in roteiro["cenas"]:
    if c["ferramenta"] == "hyperframes":
        destino = AQUI / "hyperframes" / c["id"] / "assets"
        comum(destino)
        copiar(AQUI / "audio" / f"{c['id']}.mp3", destino / "fala.mp3")
        copiar(AQUI / "audio" / f"{c['id']}.json", destino / "fala.json")
    else:
        destino = publico
        copiar(AQUI / "audio" / f"{c['id']}.mp3", destino / "audio" / f"{c['id']}.mp3")
        copiar(AQUI / "audio" / f"{c['id']}.json", destino / "audio" / f"{c['id']}.json")
    for rel in c["midia"]:
        copiar(RAIZ / rel, destino / "midia" / nome_midia(rel))
    print(f"{c['id']:16} {c['ferramenta']:11} {len(c['midia'])} arquivos de mídia -> {destino.relative_to(AQUI)}")
for dado in ("metricas/visualizacoes.csv",):
    copiar(RAIZ / dado, publico / "dados" / Path(dado).name)
