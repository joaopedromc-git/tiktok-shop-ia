"""Revisa um vídeo antes de postar.

Uso:
    python revisor/revisar.py <produto> <lote> [--sem-ia] [--sem-video]

Exemplo:
    python revisor/revisar.py facas E

Lê produtos/<produto>/anuncio.md, roteiro_<lote>.json, legenda_<lote>.txt e
video_<lote>.mp4. Sai com código 1 se alguma camada reprovar.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regras  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
ORDEM = {"aprova": 0, "atencao": 1, "reprova": 2}


def carregar(produto, lote):
    pasta = RAIZ / "produtos" / produto

    def ler(nome):
        p = pasta / nome
        return p.read_text(encoding="utf-8") if p.exists() else None

    roteiro = ler(f"roteiro_{lote}.json")
    video = pasta / f"video_{lote}.mp4"
    return {
        "anuncio": ler("anuncio.md"),
        "roteiro": json.loads(roteiro) if roteiro else None,
        "legenda": ler(f"legenda_{lote}.txt"),
        "video": video if video.exists() else None,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("produto")
    ap.add_argument("lote")
    ap.add_argument("--sem-ia", action="store_true", help="não chama o agente de IA")
    ap.add_argument("--sem-video", action="store_true", help="não mede o movimento do vídeo")
    a = ap.parse_args()

    d = carregar(a.produto, a.lote)
    vereditos = []

    if d["roteiro"]:
        achados = regras.verificar(d["roteiro"], d["legenda"])
        v = regras.veredito(achados)
        vereditos.append(v)
        print(f"\n== Regras fixas do texto: {v.upper()}")
        for x in achados:
            print(f"  - [{x.onde}] \"{x.trecho}\": {x.descricao}")
    else:
        print("\n== Regras fixas do texto: sem roteiro_<lote>.json, pulado")

    if d["roteiro"] and d["anuncio"] and not a.sem_ia:
        import ia
        r = ia.revisar(d["anuncio"], d["roteiro"], d["legenda"])
        vereditos.append(r["veredito"])
        print(f"\n== Agente revisor-conformidade: {r['veredito'].upper()}")
        for x in r["achados"]:
            print(f"  - [{x['gravidade']}] [{x['onde']}] \"{x['trecho']}\"\n"
                  f"      {x['motivo']}\n      troca: {x['sugestao']}")

    if d["video"] and not a.sem_video:
        import movimento
        m = movimento.analisar(d["video"])
        vereditos.append(m["veredito"])
        print(f"\n== Movimento real no vídeo: {m['veredito'].upper()}")
        print(f"  {m['fracao_sem_movimento']:.0%} do tempo sem movimento além da câmera "
              f"(reprova a partir de {movimento.REPROVA:.0%}, atenção a partir de {movimento.ATENCAO:.0%})")
        for ini, fim in m["trechos_parados_s"]:
            print(f"  - parado de {ini:.1f} s a {fim:.1f} s".replace(".", ","))

    final = max(vereditos, key=ORDEM.get) if vereditos else "aprova"
    print(f"\nVEREDITO: {final.upper()}")
    sys.exit(1 if final == "reprova" else 0)


if __name__ == "__main__":
    main()
