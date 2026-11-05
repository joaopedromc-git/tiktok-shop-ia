"""Servico de render: narracao (edge-tts) + montagem 9:16 (ffmpeg).
Chamado pelo n8n dentro da rede Docker. Todos os caminhos sao relativos a DADOS.
"""
import asyncio
import json
import os
import subprocess
import tempfile
import textwrap
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

DADOS = Path(os.environ.get("DADOS", "/data")).resolve()
TOKEN = os.environ.get("RENDER_TOKEN", "")
VOZ_PADRAO = os.environ.get("VOZ", "pt-BR-ThalitaMultilingualNeural")
FONTES = [
    os.environ.get("FONTE", ""),
    "/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
L, A, FPS = 1080, 1920, 30
trava = asyncio.Lock()  # um render por vez: a VPS tem 3 nucleos

app = FastAPI(title="render")


def autorizar(x_token: str = Header(default="")):
    if TOKEN and x_token != TOKEN:
        raise HTTPException(401, "token invalido")


def caminho(rel: str, deve_existir: bool = False) -> Path:
    p = (DADOS / rel).resolve()
    if DADOS not in p.parents:
        raise HTTPException(400, f"caminho fora da pasta de dados: {rel}")
    if deve_existir and not p.is_file():
        raise HTTPException(404, f"arquivo nao encontrado: {rel}")
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def fonte() -> str:
    for f in FONTES:
        if f and Path(f).is_file():
            return f
    raise HTTPException(500, "nenhuma fonte encontrada")


def duracao(p: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", str(p)], capture_output=True, text=True)
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        raise HTTPException(422, f"nao consegui ler a duracao de {p.name}")


def rodar(cmd: list[str]):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise HTTPException(500, "ffmpeg falhou: " + r.stderr[-1500:])


class Estilo(BaseModel):
    tamanho: int = 78            # altura da letra do texto de tela
    cor: str = "white"
    contorno: str = "black"
    espessura: int = 6
    y: float = 0.16              # topo do texto, fracao da altura
    letras_por_linha: int = 18
    rodape_tamanho: int = 30
    rodape_y: float = 0.64       # acima da faixa que o TikTok cobre


class Parte(BaseModel):
    clipe: str
    audio: str | None = None     # narracao; sem ela a parte fica muda
    texto_tela: str = ""
    rodape: str = ""             # ex.: *Dados do fabricante


class Montagem(BaseModel):
    saida: str
    partes: list[Parte] = Field(min_length=1, max_length=6)
    estilo: Estilo = Estilo()
    folga: float = 0.35          # silencio depois de cada fala


class Fala(BaseModel):
    texto: str
    saida: str
    voz: str | None = None
    velocidade: str = "+0%"


class Capa(BaseModel):
    video: str                   # use o clipe bruto, sem texto de tela
    saida: str
    segundo: float = 1.0
    titulo: str = ""
    estilo: Estilo = Estilo(tamanho=96, y=0.30, letras_por_linha=14)


def texto_filtro(tmp: Path, nome: str, texto: str, tam: int, y: float,
                 largura: int, e: Estilo, borda: int) -> str:
    # uma chamada por linha: o drawtext nao centraliza linha a linha sozinho
    partes = []
    for j, linha in enumerate(textwrap.wrap(texto, largura)):
        arq = tmp / f"{nome}_{j}.txt"
        arq.write_text(linha, encoding="utf-8")
        partes.append(
            f"drawtext=fontfile={fonte()}:textfile={arq}:fontsize={tam}"
            f":fontcolor={e.cor}:bordercolor={e.contorno}:borderw={borda}"
            f":x=(w-text_w)/2:y=h*{y}+{j * int(tam * 1.25)}")
    return ",".join(partes)


def textos(tmp: Path, i: int, texto: str, rodape: str, e: Estilo) -> str:
    f = ""
    if texto.strip():
        f += "," + texto_filtro(tmp, f"t{i}", texto, e.tamanho, e.y,
                                e.letras_por_linha, e, e.espessura)
    if rodape.strip():
        f += "," + texto_filtro(tmp, f"r{i}", rodape, e.rodape_tamanho,
                                e.rodape_y, 40, e, 3)
    return f


@app.get("/saude")
def saude():
    return {"ok": True, "fonte": fonte(), "voz": VOZ_PADRAO}


@app.get("/vozes", dependencies=[Depends(autorizar)])
async def vozes():
    import edge_tts
    return [v["ShortName"] for v in await edge_tts.list_voices()
            if v["Locale"] == "pt-BR"]


@app.post("/tts", dependencies=[Depends(autorizar)])
async def tts(f: Fala):
    import edge_tts
    saida = caminho(f.saida)
    # tempo de cada palavra (edge-tts dá em unidades de 100 ns), para a legenda sincronizada
    palavras = []
    try:
        com = edge_tts.Communicate(f.texto, f.voz or VOZ_PADRAO,
                                   rate=f.velocidade, boundary="WordBoundary")
        with open(saida, "wb") as arq:
            async for parte in com.stream():
                if parte["type"] == "audio":
                    arq.write(parte["data"])
                elif parte["type"] == "WordBoundary":
                    palavras.append({"palavra": parte["text"],
                                     "inicio": round(parte["offset"] / 1e7, 3),
                                     "fim": round((parte["offset"] + parte["duration"]) / 1e7, 3)})
    except Exception as ex:
        saida.unlink(missing_ok=True)
        raise HTTPException(502, f"edge-tts falhou: {ex}")
    saida.with_suffix(".json").write_text(
        json.dumps({"texto": f.texto, "palavras": palavras}, ensure_ascii=False), encoding="utf-8")
    return {"arquivo": f.saida, "duracao": round(duracao(saida), 2), "palavras": palavras}


@app.post("/montar", dependencies=[Depends(autorizar)])
async def montar(m: Montagem):
    saida = caminho(m.saida)
    async with trava:
        return await asyncio.to_thread(_montar, m, saida)


def _montar(m: Montagem, saida: Path):
    entradas, filtros, rotulos, tempos = [], [], "", []
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        n = 0
        for i, p in enumerate(m.partes):
            clipe = caminho(p.clipe, True)
            d = duracao(clipe)
            entradas += ["-i", str(clipe)]
            iv = n
            n += 1
            if p.audio:
                audio = caminho(p.audio, True)
                d = max(d, duracao(audio) + m.folga)
                entradas += ["-i", str(audio)]
                fa = f"[{n}:a]aresample=44100,aformat=channel_layouts=stereo,apad"
                n += 1
            else:
                fa = "anullsrc=r=44100:cl=stereo"
            d = round(d, 3)
            tempos.append(d)
            # fala maior que o clipe: congela o ultimo quadro ate a fala acabar
            filtros.append(
                f"[{iv}:v]scale={L}:{A}:force_original_aspect_ratio=increase,"
                f"crop={L}:{A},fps={FPS},setsar=1,"
                f"tpad=stop_mode=clone:stop_duration=30,trim=duration={d},"
                f"setpts=PTS-STARTPTS{textos(tmp, i, p.texto_tela, p.rodape, m.estilo)}"
                f",format=yuv420p[v{i}]")
            filtros.append(f"{fa},atrim=duration={d},asetpts=PTS-STARTPTS[a{i}]")
            rotulos += f"[v{i}][a{i}]"
        k = len(m.partes)
        filtros.append(f"{rotulos}concat=n={k}:v=1:a=1[v][a]")
        rodar(["ffmpeg", "-y", "-v", "error", *entradas,
               "-filter_complex", ";".join(filtros),
               "-map", "[v]", "-map", "[a]",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
               "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
               str(saida)])
    return {"arquivo": m.saida, "duracao": round(sum(tempos), 2),
            "partes": tempos}


@app.post("/capa", dependencies=[Depends(autorizar)])
def capa(c: Capa):
    video, saida = caminho(c.video, True), caminho(c.saida)
    with tempfile.TemporaryDirectory() as t:
        vf = f"scale={L}:{A}:force_original_aspect_ratio=increase,crop={L}:{A}"
        vf += textos(Path(t), 0, c.titulo, "", c.estilo)
        rodar(["ffmpeg", "-y", "-v", "error", "-ss", str(c.segundo),
               "-i", str(video), "-frames:v", "1", "-vf", vf, "-q:v", "2",
               str(saida)])
    return {"arquivo": c.saida}


# O n8n guarda e busca arquivos por aqui, sem precisar montar a pasta nele.
@app.put("/arquivo/{rel:path}", dependencies=[Depends(autorizar)])
async def enviar(rel: str, req: Request):
    destino = caminho(rel)
    with open(destino, "wb") as f:
        async for bloco in req.stream():
            f.write(bloco)
    return {"arquivo": rel, "bytes": destino.stat().st_size}


@app.get("/arquivo/{rel:path}", dependencies=[Depends(autorizar)])
def baixar(rel: str):
    return FileResponse(caminho(rel, True))
