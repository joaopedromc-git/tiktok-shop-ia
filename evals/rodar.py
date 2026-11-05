"""Roda o revisor em todos os vídeos com resultado conhecido e escreve evals/resultados.md.

Uso:
    python evals/rodar.py            # usa as respostas da IA já guardadas
    python evals/rodar.py --ia       # chama o agente nos casos sem resposta guardada
    python evals/rodar.py --refazer  # chama o agente em todos os casos de novo

As respostas do agente ficam em evals/saida_ia/ e as medidas de movimento em
evals/movimento.json, para o resultado poder ser conferido sem rodar tudo de novo.
"""
import argparse
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "revisor"))
import regras  # noqa: E402
from revisar import carregar  # noqa: E402

AQUI = RAIZ / "evals"
SAIDA_IA = AQUI / "saida_ia"
MOVIMENTO = AQUI / "movimento.json"
ICONE = {"aprova": "✅ aprova", "atencao": "⚠️ atenção", "reprova": "❌ reprova", None: "—"}


def rodar(usar_ia, refazer):
    casos = json.loads((AQUI / "casos.json").read_text(encoding="utf-8"))["casos"]
    mov = json.loads(MOVIMENTO.read_text(encoding="utf-8")) if MOVIMENTO.exists() else {}
    SAIDA_IA.mkdir(exist_ok=True)
    linhas = []
    for c in casos:
        chave = f"{c['produto']}_{c['lote']}"
        d = carregar(c["produto"], c["lote"])
        r = dict(c, chave=chave, regras=None, regras_originais=None, ia=None, mov=None)

        if d["roteiro"]:
            todos = regras.verificar(d["roteiro"], d["legenda"])
            r["regras"] = regras.veredito(todos)
            r["regras_originais"] = regras.veredito([a for a in todos if a.origem == "original"])
            r["regras_achados"] = [f"{a.onde}: \"{a.trecho}\" ({a.regra})" for a in todos]

            arq = SAIDA_IA / f"{chave}.json"
            if usar_ia and (refazer or not arq.exists()):
                import ia
                print(f"agente: {chave}", flush=True)
                arq.write_text(json.dumps(ia.revisar(d["anuncio"], d["roteiro"], d["legenda"]),
                                          ensure_ascii=False, indent=1), encoding="utf-8")
            if arq.exists():
                r["ia"] = json.loads(arq.read_text(encoding="utf-8"))["veredito"]

        if d["video"]:
            if chave not in mov:
                import movimento
                print(f"movimento: {chave}", flush=True)
                mov[chave] = movimento.analisar(d["video"])
                MOVIMENTO.write_text(json.dumps(mov, indent=1), encoding="utf-8")
            r["mov"] = mov[chave]
        linhas.append(r)
    return linhas


def placar(linhas, coluna, positivo):
    """Conta acertos e alarmes entre os vídeos postados."""
    postados = [x for x in linhas if x["postado"] and x[coluna] is not None
                and x["violacao"] != "a_confirmar"]
    pos = [x for x in postados if x["violacao"] == positivo]
    neg = [x for x in postados if x["violacao"] != positivo]
    return {
        "positivos": len(pos),
        "reprovados": sum(x[coluna] == "reprova" for x in pos),
        "sinalizados": sum(x[coluna] in ("reprova", "atencao") for x in pos),
        "negativos": len(neg),
        "falso_reprova": sum(x[coluna] == "reprova" for x in neg),
        "falso_atencao": sum(x[coluna] == "atencao" for x in neg),
    }


def escrever(linhas):
    for x in linhas:
        x["mov_v"] = x["mov"]["veredito"] if x["mov"] else None
    t = placar(linhas, "regras", "alegacao_exagerada")
    to = placar(linhas, "regras_originais", "alegacao_exagerada")
    ti = placar(linhas, "ia", "alegacao_exagerada")
    tm = placar(linhas, "mov_v", "quadro_estatico")

    def frase(p, nome):
        return (f"| {nome} | {p['reprovados']} de {p['positivos']} reprovados "
                f"({p['sinalizados']} de {p['positivos']} sinalizados) | "
                f"{p['falso_reprova']} reprovados, {p['falso_atencao']} em atenção (de {p['negativos']}) |")

    out = ["# Resultados do revisor", "",
           "Gerado por `python evals/rodar.py`. Gabarito em `evals/casos.json`.", "",
           "## Placar (só vídeos postados, com resultado conhecido)", "",
           "| Camada | Vídeos que levaram a violação | Outros vídeos postados (sem essa violação) |",
           "|---|---|---|",
           frase(to, "Texto, regras originais (alegação exagerada)"),
           frase(t, "Texto, todas as regras (alegação exagerada)"),
           frase(ti, "Texto, agente de IA (alegação exagerada)"),
           frase(tm, "Vídeo, movimento real (quadro estático)"),
           frase(placar(linhas, "ia", "produto_inconsistente"), "Texto, agente de IA (produto inconsistente; fora do escopo, é visual)"),
           "",
           "## Por vídeo", "",
           "| Vídeo | Postado | Violação real | Regras originais | Todas as regras | Agente IA | Sem movimento | Movimento |",
           "|---|---|---|---|---|---|---|---|"]
    for x in linhas:
        frac = f"{x['mov']['fracao_sem_movimento']:.0%}" if x["mov"] else "—"
        out.append(f"| {x['produto']} {x['lote']} | {'sim' if x['postado'] else 'não confirmado'} | "
                   f"{x['violacao'] or '—'} | {ICONE[x['regras_originais']]} | {ICONE[x['regras']]} | "
                   f"{ICONE[x['ia']]} | {frac} | {ICONE[x['mov_v']]} |")
    out += ["", "## O que as regras fixas acharam", ""]
    for x in linhas:
        for a in x.get("regras_achados", []):
            out.append(f"- **{x['produto']} {x['lote']}** · {a}")
    (AQUI / "resultados.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out[:12]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ia", action="store_true")
    ap.add_argument("--refazer", action="store_true")
    a = ap.parse_args()
    escrever(rodar(a.ia or a.refazer, a.refazer))
