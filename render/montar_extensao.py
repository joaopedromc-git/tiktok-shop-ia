"""Montagem avulsa da extensão (07/10/2026), no mesmo estilo do body splash.
Roda dentro do container render:  docker exec render python /data/extensao/montar.py
Cada cena: trecho de clipe (ou foto) esticado para caber a fala, texto no alto, fala no início.
"""
import asyncio
import json
import subprocess
import textwrap
from pathlib import Path

import edge_tts

BASE = Path("/data/extensao")
BRUTO, TMP = BASE / "bruto", BASE / "tmp"
SAIDA = BASE / "extensao_v1.mp4"
L, A, FPS = 1080, 1920, 30
VOZ, RITMO = "pt-BR-ThalitaMultilingualNeural", "+6%"
NEGRITO = "/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf"
MEDIA = "/usr/share/fonts/truetype/montserrat/Montserrat-Bold.ttf"
DESTAQUE = "0xFFD34D"
MINIMO, INICIO, FOLGA = 4.0, 0.12, 0.35

# fonte, início e fim no clipe, foco (0 = esquerda, 0.5 = centro, 1 = direita),
# título (amarelo), subtítulo (branco), rodapé, fala
# Clipe B: até ~5 s mostra outra extensão (sem USB nem botão), então só uso 5,5–8 s.
# Fecho com o último quadro do B (estúdio claro), já que não há a foto do anúncio.
CENAS = [
    ("clipeA.mp4", 2.0, 8.0, 0.5, "Falta tomada aí?", "", "",
     "Uma tomada só pra ligar tudo isso? Aí vira essa bagunça."),
    ("clipeB.mp4", 5.5, 6.75, 0.5, "5 tomadas", "num lugar só", "",
     "Essa extensão tem cinco tomadas num lugar só."),
    ("clipeB.mp4", 6.75, 8.0, 0.5, "4 USB • 1 Tipo-C", "liga/desliga", "",
     "E ainda quatro USB, uma tipo cê e botão de liga e desliga."),
    ("clipeC.mp4", 0.0, 4.0, 0.5, "Mesa • quarto • sala", "", "",
     "Serve na mesa de trabalho, no quarto ou na sala."),
    ("final.png", 0, 0, 0.5, "Em oferta", "Toque no produto", "",
     "Tá em oferta no TikTok Shop. Toca no produto aqui no vídeo e confere."),
]


def rodar(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("ffmpeg falhou:\n" + r.stderr[-2500:])
    return r


def duracao(p):
    r = rodar(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(p)])
    return float(json.loads(r.stdout)["format"]["duration"])


def linhas(texto, largura, tam, y0, fonte, cor, i, nome, borda=0, caixa=True, atraso=0.0):
    """Uma drawtext por linha, centralizada, com fundo escuro e entrada suave."""
    fs = []
    for j, lin in enumerate(textwrap.wrap(texto, largura)):
        arq = TMP / f"{nome}{i}_{j}.txt"
        arq.write_text(lin, encoding="utf-8")
        alfa = f"if(lt(t,{atraso}),0,min(1,(t-{atraso})/0.25))"
        fs.append(
            f"drawtext=fontfile={fonte}:textfile={arq}:fontsize={tam}:fontcolor={cor}"
            f":x=(w-text_w)/2:y={y0 + j * int(tam * 1.3)}:alpha='{alfa}'"
            + (f":box=1:boxcolor=black@0.5:boxborderw=18" if caixa else "")
            + (f":borderw={borda}:bordercolor=black@0.7" if borda else ""))
    return fs, y0 + len(fs) * int(tam * 1.3)


async def falar(texto, arq):
    await edge_tts.Communicate(texto, VOZ, rate=RITMO).save(str(arq))


def cena(i, c):
    fonte, ini, fim, foco, titulo, sub, rodape, fala = c
    audio = TMP / f"fala{i}.mp3"
    asyncio.run(falar(fala, audio))
    d = round(max(MINIMO, INICIO + duracao(audio) + FOLGA), 3)

    # textos: título amarelo grande, subtítulo branco menor, rodapé pequeno
    y = int(A * 0.13)
    # gancho maior (quebra em 2 linhas); título longo um pouco menor para não quebrar
    larg, tam = (12, 112) if i == 0 else ((24, 76) if len(titulo) > 16 else (16, 92))
    f1, y = linhas(titulo, larg, tam, y, NEGRITO, DESTAQUE, i, "t", atraso=0.05)
    f2, _ = linhas(sub, 24, 58, y + 14, MEDIA, "white", i, "s", atraso=0.2)
    f3, _ = linhas(rodape, 40, 32, int(A * 0.64), MEDIA, "white", i, "r", borda=2, caixa=False)
    txt = ",".join(f1 + f2 + f3)

    if fonte.endswith(".png"):
        # quadro parado em tela cheia com zoom lento
        quadros = int(d * FPS)
        entrada = ["-loop", "1", "-t", str(d), "-i", str(BRUTO / fonte)]
        v = (f"[0:v]scale={L * 2}:{A * 2},zoompan=z='1+0.10*on/{quadros}':d=1:"
             f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={L}x{A}:fps={FPS},"
             f"trim=duration={d},setpts=PTS-STARTPTS,setsar=1,{txt},format=yuv420p[v]")
    else:
        # clipe: trecho [ini, fim] esticado (câmera lenta) para durar d,
        # com leve aproximação para o lado do frasco em foco
        fator = d / (fim - ini)
        z = 1.0 if foco == 0.5 else 1.18
        entrada = ["-ss", str(ini), "-t", str(fim - ini), "-i", str(BRUTO / fonte)]
        v = (f"[0:v]setpts={fator:.4f}*(PTS-STARTPTS),"
             f"scale={int(L * z)}:{int(A * z)},"
             f"crop={L}:{A}:{int((L * z - L) * foco)}:{int((A * z - A) / 2)},"
             f"fps={FPS},tpad=stop_mode=clone:stop_duration=5,trim=duration={d},"
             f"setpts=PTS-STARTPTS,setsar=1,{txt},format=yuv420p[v]")

    a = (f"[1:a]aresample=44100,aformat=channel_layouts=stereo,"
         f"adelay={int(INICIO * 1000)}:all=1,apad,atrim=duration={d},"
         f"afade=t=out:st={d - 0.06}:d=0.06[a]")
    out = TMP / f"cena{i}.mp4"
    rodar(["ffmpeg", "-y", "-v", "error", *entrada, "-i", str(audio),
           "-filter_complex", v + ";" + a, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", str(FPS),
           "-c:a", "aac", "-b:a", "192k", "-ar", "44100", str(out)])
    print(f"cena {i + 1}: {d:.2f} s ({duracao(audio):.2f} s de fala)")
    return out


def main():
    TMP.mkdir(parents=True, exist_ok=True)
    cenas = [cena(i, c) for i, c in enumerate(CENAS)]
    lista = TMP / "lista.txt"
    lista.write_text("".join(f"file '{c}'\n" for c in cenas))
    junto = TMP / "junto.mp4"
    rodar(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lista),
           "-c", "copy", str(junto)])
    # volume da narração no padrão das redes (-14 LUFS); a música entra no TikTok
    rodar(["ffmpeg", "-y", "-v", "error", "-i", str(junto), "-c:v", "copy",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
           "-ar", "44100", "-movflags", "+faststart", str(SAIDA)])
    print(f"pronto: {SAIDA} ({duracao(SAIDA):.2f} s)")


if __name__ == "__main__":
    main()
