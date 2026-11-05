"""Junta as cenas renderizadas no vídeo final.

Uso: python apresentacao/montar.py
Lê apresentacao/saida/<cena>.mp4 na ordem do roteiro e escreve apresentacao/saida/apresentacao.mp4
(1920x1080, 30 fps, H.264 + AAC, volume normalizado em -16 LUFS).
"""
import json
import re
import subprocess
from pathlib import Path

import imageio_ffmpeg

AQUI = Path(__file__).resolve().parent
SAIDA = AQUI / "saida"
FF = imageio_ffmpeg.get_ffmpeg_exe()


def info(arq):
    err = subprocess.run([FF, "-hide_banner", "-i", str(arq)], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return {"duracao": int(h) * 3600 + int(m) * 60 + float(s),
            "video": re.search(r"Video: .*?(\d{3,4})x(\d{3,4}).*?([\d.]+) fps", err).groups(),
            "audio": "Audio:" in err}


tempos = {c["id"]: c for c in json.loads((AQUI / "tempos.json").read_text())["cenas"]}
cenas = [c["id"] for c in json.loads((AQUI / "roteiro.json").read_text(encoding="utf-8"))["cenas"]]

entradas, filtros = [], []
for i, cena in enumerate(cenas):
    arq = SAIDA / f"{cena}.mp4"
    if not arq.exists():
        raise SystemExit(f"falta {arq}")
    d = info(arq)
    alvo = tempos[cena]["duracao_s"]
    aviso = "" if abs(d["duracao"] - alvo) < 0.1 else f"  <- esperado {alvo:.2f} s"
    print(f"{cena:16} {d['duracao']:6.2f} s  {'x'.join(d['video'][:2])} {d['video'][2]} fps  "
          f"{'com' if d['audio'] else 'SEM'} áudio{aviso}")
    entradas += ["-i", str(arq)]
    # cada cena: vídeo em 1920x1080/30 fps e áudio estéreo 48 kHz (cena sem áudio ganha silêncio)
    filtros.append(f"[{i}:v]scale=1920:1080,fps=30,format=yuv420p,setsar=1[v{i}]")
    if d["audio"]:
        filtros.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,"
                       f"apad=whole_dur={d['duracao']:.3f}[a{i}]")
    else:
        filtros.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{d['duracao']:.3f}[a{i}]")

pares = "".join(f"[v{i}][a{i}]" for i in range(len(cenas)))
filtros.append(f"{pares}concat=n={len(cenas)}:v=1:a=1[v][a0]")
filtros.append("[a0]loudnorm=I=-16:TP=-1.5:LRA=11[a]")
final = SAIDA / "apresentacao.mp4"
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *entradas,
                "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart",
                "-map_metadata", "-1", str(final)], check=True)
d = info(final)
print(f"\nfinal: {final}  {d['duracao']:.2f} s  {final.stat().st_size / 1e6:.1f} MB")
