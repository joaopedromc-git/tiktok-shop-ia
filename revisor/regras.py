"""Camada 1 (texto): regras fixas sobre roteiro e legenda, sem IA.

Cada regra diz de onde veio: "original" (valia desde o primeiro vídeo) ou a
violação que a originou. Os testes usam isso para separar o que o revisor pegaria
de verdade do que ele só pega porque a regra nasceu do próprio caso.
"""
import re
from dataclasses import dataclass

NUMERO = (
    r"\d+(?:[.,]\d+)?|um|uma|dois|duas|três|tres|quatro|cinco|seis|sete|oito|nove|dez|"
    r"doze|quinze|vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa|"
    r"cem|cento|duzent\w+|trezent\w+|quatrocent\w+|quinhent\w+|mil"
)
UNIDADE = (
    r"%|h|horas?|litros?|l|ml|mililitros?|cm|centímetros?|metros?|m|w|watts?|mah|graus|°|"
    r"minutos?|dias?|anos?|meses|kg|gramas?|g|polegadas?|oz"
)
DADO_NUMERICO = re.compile(rf"\b(?:{NUMERO})\s*(?:{UNIDADE})(?![\wà-ú])", re.IGNORECASE)
SEGUNDO_FABRICANTE = re.compile(r"segundo o fabricante", re.IGNORECASE)
# Na legenda vale qualquer atribuição ("dados do fabricante", "segundo o fabricante",
# "a dica do fabricante"); na fala o projeto exige a forma fixa "segundo o fabricante".
DADOS_FABRICANTE = re.compile(r"\bfabricante\b", re.IGNORECASE)

# (id, descrição, expressão, origem)
PROIBIDAS = [
    ("preco", "preço, desconto, frete ou oferta",
     r"R\$|\bpreç\w*|\bdesconto\w*|\bfrete\b|\bem oferta\b|\bpromoç\w*|\bbarat\w*", "original"),
    ("urgencia", "urgência ou escassez",
     r"\bsó hoje\b|últimas unidades|\bcorre\b|antes que acabe|tempo limitado|estoque limitado|imperdível|\bacaba hoje\b",
     "original"),
    ("superioridade", "superlativo ou comparação com outras marcas",
     r"melhor do mundo|\bo melhor\b|\ba melhor\b|nenhum outro|nenhuma outra|único no mercado|\bgarantid\w*|\b100 ?%",
     "original"),
    ("saude", "promessa de saúde ou cura",
     r"\bcura\w*|\btrata\b|\bemagrec\w*|medicinal|antibacterian\w*|elimina (?:bactérias|germes)",
     "original"),
    ("promessa_no_tempo", "promessa absoluta ou de desempenho no tempo",
     r"do primeiro ao último|nunca mais|\badeus\b|para sempre|pra sempre|a vida toda|não (?:estraga|quebra|enferruja) nunca",
     "violação 4 (alegação exagerada, facas E)"),
]


@dataclass
class Achado:
    onde: str
    trecho: str
    regra: str
    descricao: str
    origem: str
    gravidade: str = "reprova"


def _proibidas(onde, texto):
    for rid, desc, padrao, origem in PROIBIDAS:
        for m in re.finditer(padrao, texto, re.IGNORECASE):
            yield Achado(onde, m.group(0), rid, desc, origem)


def verificar(roteiro, legenda=None, origens=None):
    """Devolve a lista de achados. `origens` limita às regras dessas origens."""
    achados = []
    for parte in roteiro.get("partes", []):
        nome = parte.get("parte", "?")
        fala = parte.get("fala", "") or ""
        tela = " ".join(filter(None, [parte.get("titulo"), parte.get("linha")]))
        rodape = (parte.get("rodape") or "").strip()

        for campo, texto in (("fala", fala), ("tela", tela)):
            achados += _proibidas(f"{nome}.{campo}", texto)

        if DADO_NUMERICO.search(fala) and not SEGUNDO_FABRICANTE.search(fala):
            m = DADO_NUMERICO.search(fala)
            achados.append(Achado(f"{nome}.fala", m.group(0), "dado_sem_fonte",
                                  'dado numérico sem "segundo o fabricante" na fala', "original"))
        if (SEGUNDO_FABRICANTE.search(fala) or DADO_NUMERICO.search(tela)) and not rodape:
            achados.append(Achado(f"{nome}.tela", tela or fala[:40], "sem_rodape",
                                  'dado do fabricante sem o rodapé "*Dados do fabricante" na tela', "original"))

    if legenda:
        achados += _proibidas("legenda", legenda)
        m = DADO_NUMERICO.search(legenda)
        if m and not DADOS_FABRICANTE.search(legenda):
            achados.append(Achado("legenda", m.group(0), "dado_sem_fonte",
                                  'dado numérico na legenda sem "dados do fabricante"', "original"))

    if origens is not None:
        achados = [a for a in achados if a.origem in origens]
    return achados


def veredito(achados):
    if any(a.gravidade == "reprova" for a in achados):
        return "reprova"
    return "atencao" if achados else "aprova"
