"""Testes das regras fixas com frases inventadas (nenhuma vem dos casos de violação).

Rodar: python revisor/test_regras.py   (ou pytest revisor/)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regras  # noqa: E402


def achados(fala, titulo="", linha="", rodape="", legenda=None):
    roteiro = {"partes": [{"parte": "x", "fala": fala, "titulo": titulo, "linha": linha, "rodape": rodape}]}
    return {a.regra for a in regras.verificar(roteiro, legenda)}


def test_dado_numerico_precisa_de_fonte():
    assert achados("Aguenta doze horas gelada.") == {"dado_sem_fonte"}
    assert achados("Segundo o fabricante, aguenta doze horas gelada.") == {"sem_rodape"}
    assert achados("Segundo o fabricante, aguenta doze horas gelada.", rodape="*Dados do fabricante") == set()


def test_contagem_nao_e_dado_de_desempenho():
    assert achados("Vem com seis peças e três tamanhos.") == set()


def test_dado_na_tela_precisa_de_rodape():
    assert achados("Olha esse kit.", titulo="24 H*") == {"sem_rodape"}
    assert achados("Olha esse kit.", titulo="24 H*", rodape="*Dados do fabricante") == set()


def test_preco_urgencia_e_superioridade():
    assert achados("Só hoje com desconto!") == {"preco", "urgencia"}
    assert achados("O melhor do mundo.") == {"superioridade"}


def test_promessa_no_tempo():
    assert achados("Nunca mais troque de garrafa.") == {"promessa_no_tempo"}


def test_legenda_aceita_qualquer_atribuicao_ao_fabricante():
    assert achados("ok", legenda="Cabe 2 litros, segundo o fabricante.") == set()
    assert achados("ok", legenda="A dica do fabricante: a 15 cm da pele.") == set()
    assert achados("ok", legenda="Cabe 2 litros.") == {"dado_sem_fonte"}


if __name__ == "__main__":
    for nome, f in list(globals().items()):
        if nome.startswith("test_"):
            f()
            print("ok", nome)
