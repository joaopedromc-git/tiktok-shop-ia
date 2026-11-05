"""Prepara a pasta de edição de um lote na VPS e gera as falas com tempo de palavra.
Roda no PC:  python3 render/kit/preparar.py <codigo> <lote>
Lê produtos/<codigo>/roteiro_<lote>.json e os clipes produtos/<codigo>/clipe_<letra>.mp4.
Na VPS cria dados/<codigo>/edicao_<lote>/assets/ com clipes, sfx, gsap, fontes e fala_<parte>.mp3/.json.
"""
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
VPS = "minha-vps"
REMOTO = "~/tiktok-automacao/dados"
VELOCIDADE = "+6%"


def sh(*cmd, entrada=None):
    r = subprocess.run(cmd, input=entrada, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"falhou: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout


def main(codigo, lote):
    pasta = RAIZ / "produtos" / codigo
    roteiro = json.loads((pasta / f"roteiro_{lote}.json").read_text(encoding="utf-8"))
    destino = f"{REMOTO}/{codigo}/edicao_{lote}/assets"
    sh("ssh", VPS, f"mkdir -p {destino}/sfx")

    kit = RAIZ / "render" / "kit"
    sh("scp", "-q", *map(str, sorted((kit / "sfx").glob("*.wav"))), f"{VPS}:{destino}/sfx/")
    sh("scp", "-q", str(kit / "gsap.min.js"), str(kit / "fontes.css"), f"{VPS}:{destino}/")

    for p in roteiro["partes"]:
        clipe = pasta / f"clipe_{p['clipe']}.mp4"
        if not clipe.exists():
            raise SystemExit(f"falta {clipe}")
        sh("scp", "-q", str(clipe), f"{VPS}:{destino}/")
        # fala pela API do render (voz Thalita), com o tempo de cada palavra no .json
        pedido = json.dumps({"texto": p["fala"], "velocidade": VELOCIDADE,
                             "saida": f"{codigo}/edicao_{lote}/assets/fala_{p['parte']}.mp3"})
        script = ("import json,os,sys,urllib.request;"
                  "r=urllib.request.Request('http://localhost:8000/tts',data=sys.stdin.read().encode(),"
                  "headers={'x-token':os.environ['RENDER_TOKEN'],'content-type':'application/json'});"
                  "d=json.load(urllib.request.urlopen(r));print(d['duracao'],len(d['palavras']))")
        saida = sh("ssh", VPS, f"docker exec -i render python -c \"{script}\"", entrada=pedido)
        print(f"{p['parte']:13} clipe {p['clipe']}  fala {saida.split()[0]} s, {saida.split()[1]} palavras")
    print("pronto:", destino)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
