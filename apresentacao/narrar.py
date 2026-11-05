"""Gera a narração de cada cena (voz Thalita, edge-tts, +6%) com o tempo de cada palavra.

Uso: python apresentacao/narrar.py
Lê apresentacao/roteiro.json e escreve:
  apresentacao/audio/<cena>.mp3 e .json  (palavras com início e fim, em segundos)
  apresentacao/tempos.json                (duração de cada cena em segundos e em quadros a 30 fps)
"""
import asyncio
import json
import math
from pathlib import Path

import edge_tts

AQUI = Path(__file__).resolve().parent
VOZ, VELOCIDADE = "pt-BR-ThalitaMultilingualNeural", "+6%"
ENTRADA, RESPIRO, FPS = 0.25, 0.45, 30   # silêncio antes e depois da fala


async def narrar(texto, saida):
    palavras = []
    com = edge_tts.Communicate(texto, VOZ, rate=VELOCIDADE, boundary="WordBoundary")
    with open(saida, "wb") as arq:
        async for parte in com.stream():
            if parte["type"] == "audio":
                arq.write(parte["data"])
            elif parte["type"] == "WordBoundary":
                palavras.append({"palavra": parte["text"],
                                 "inicio": round(parte["offset"] / 1e7, 3),
                                 "fim": round((parte["offset"] + parte["duration"]) / 1e7, 3)})
    return palavras


async def main():
    roteiro = json.loads((AQUI / "roteiro.json").read_text(encoding="utf-8"))
    (AQUI / "audio").mkdir(exist_ok=True)
    tempos = {"fps": FPS, "entrada_s": ENTRADA, "cenas": []}
    for c in roteiro["cenas"]:
        mp3 = AQUI / "audio" / f"{c['id']}.mp3"
        palavras = await narrar(c["fala"], mp3)
        fala = palavras[-1]["fim"]
        dur = ENTRADA + fala + RESPIRO
        (AQUI / "audio" / f"{c['id']}.json").write_text(
            json.dumps({"texto": c["fala"], "entrada_s": ENTRADA, "palavras": palavras},
                       ensure_ascii=False, indent=1), encoding="utf-8")
        tempos["cenas"].append({"id": c["id"], "ferramenta": c["ferramenta"], "fala_s": fala,
                                "duracao_s": round(dur, 3), "quadros": math.ceil(dur * FPS)})
        print(f"{c['id']:16} {c['ferramenta']:11} fala {fala:5.2f} s  cena {dur:5.2f} s  {len(palavras)} palavras")
    total = sum(c["duracao_s"] for c in tempos["cenas"])
    tempos["total_s"] = round(total, 2)
    (AQUI / "tempos.json").write_text(json.dumps(tempos, indent=1), encoding="utf-8")
    print(f"total {total:.1f} s")


asyncio.run(main())
