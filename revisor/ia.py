"""Camada 2 (texto): o agente revisor-conformidade compara roteiro e legenda com o anúncio.

Roda o Claude Code sem ferramentas (`claude -p --tools ""`), com o corpo de
`.claude/agents/revisor-conformidade.md` como prompt de sistema e a saída presa
a um JSON Schema. Usa a assinatura do Claude Code, sem API paga.
"""
import json
import os
import subprocess
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AGENTE = RAIZ / ".claude" / "agents" / "revisor-conformidade.md"
MODELO = os.environ.get("REVISOR_MODELO", "sonnet")

CATEGORIAS = ["alegacao_sem_base", "exagero_de_desempenho", "dado_sem_fonte",
              "preco_e_pressao", "saude_e_seguranca", "variacao_nao_confirmada",
              "contradicao"]
ESQUEMA = {
    "type": "object",
    "properties": {
        "veredito": {"enum": ["aprova", "atencao", "reprova"]},
        "achados": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "onde": {"type": "string"},
                "trecho": {"type": "string"},
                "categoria": {"enum": CATEGORIAS},
                "gravidade": {"enum": ["atencao", "reprova"]},
                "motivo": {"type": "string"},
                "sugestao": {"type": "string"},
            },
            "required": ["onde", "trecho", "categoria", "gravidade", "motivo", "sugestao"],
        }},
    },
    "required": ["veredito", "achados"],
}


def _prompt_do_agente():
    texto = AGENTE.read_text(encoding="utf-8")
    return texto.split("---", 2)[2].strip() if texto.startswith("---") else texto


def _entrada(anuncio, roteiro, legenda):
    partes = [{k: p.get(k, "") for k in ("parte", "fala", "titulo", "linha", "rodape")}
              for p in roteiro.get("partes", [])]
    return (f"# Anúncio do vendedor\n\n{anuncio}\n\n"
            f"# Roteiro\n\n```json\n{json.dumps(partes, ensure_ascii=False, indent=1)}\n```\n\n"
            f"# Legenda do post\n\n{legenda or '(sem legenda)'}\n")


def revisar(anuncio, roteiro, legenda=None):
    cmd = ["claude", "-p", "--model", MODELO, "--tools", "", "--no-session-persistence",
           "--system-prompt", _prompt_do_agente(),
           "--json-schema", json.dumps(ESQUEMA), "--output-format", "json"]
    # Pasta vazia: o agente não lê o CLAUDE.md nem os aprendizados do projeto,
    # que descrevem as violações usadas nos testes.
    with tempfile.TemporaryDirectory() as vazia:
        r = subprocess.run(cmd, input=_entrada(anuncio, roteiro, legenda), cwd=vazia,
                           capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"claude falhou: {r.stderr.strip() or r.stdout.strip()}")
    saida = json.loads(r.stdout)
    resultado = saida.get("structured_output")
    if resultado is None:
        resultado = json.loads(saida["result"])
    return resultado
