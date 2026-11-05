"""Gera os efeitos sonoros do kit por síntese (sem direito autoral de terceiros).
Roda em qualquer Python 3, sem dependências:  python gerar_sfx.py <pasta_saida>
Cada som sai em WAV 44,1 kHz estéreo, pico em -3 dBFS.
"""
import math
import random
import struct
import sys
import wave
from pathlib import Path

TAXA = 44100
random.seed(7)  # mesmos sons a cada execução


def salvar(nome, amostras, pasta, abertura=0.0):
    """Normaliza para -3 dBFS e grava em estéreo (abertura > 0 atrasa um canal, dá largura)."""
    pico = max(1e-9, max(abs(a) for a in amostras))
    ganho = 10 ** (-3 / 20) / pico
    atraso = int(abertura * TAXA)
    with wave.open(str(pasta / f"{nome}.wav"), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(TAXA)
        quadros = bytearray()
        for i, a in enumerate(amostras):
            d = amostras[i - atraso] if i >= atraso else 0.0
            quadros += struct.pack("<hh", int(a * ganho * 32767), int(d * ganho * 32767))
        w.writeframes(bytes(quadros))


def ruido(n, cor="branco"):
    if cor == "branco":
        return [random.uniform(-1, 1) for _ in range(n)]
    # rosa aproximado (Paul Kellet), mais encorpado para whoosh
    b0 = b1 = b2 = 0.0
    out = []
    for _ in range(n):
        x = random.uniform(-1, 1)
        b0 = 0.99765 * b0 + x * 0.0990460
        b1 = 0.96300 * b1 + x * 0.2965164
        b2 = 0.57000 * b2 + x * 1.0526913
        out.append(b0 + b1 + b2 + x * 0.1848)
    return out


def passa_banda(sinal, freq_de, freq_ate, q=4.0):
    """Filtro passa-banda (biquad) com frequência central varrendo de freq_de a freq_ate."""
    out, x1 = [], [0.0, 0.0]
    y = [0.0, 0.0]
    n = len(sinal)
    for i, x in enumerate(sinal):
        f = freq_de * (freq_ate / freq_de) ** (i / n)
        w0 = 2 * math.pi * f / TAXA
        alfa = math.sin(w0) / (2 * q)
        b0, b2 = alfa, -alfa
        a0, a1, a2 = 1 + alfa, -2 * math.cos(w0), 1 - alfa
        v = (b0 * x + b2 * x1[1] - a1 * y[0] - a2 * y[1]) / a0
        x1 = [x, x1[0]]
        y = [v, y[0]]
        out.append(v)
    return out


def envelope(n, ataque, decaimento_forma=2.0):
    """Sobe em 'ataque' (fração) e cai com curva de potência."""
    na = max(1, int(n * ataque))
    env = []
    for i in range(n):
        if i < na:
            env.append(i / na)
        else:
            env.append((1 - (i - na) / max(1, n - na)) ** decaimento_forma)
    return env


def seno_varrido(n, f_de, f_ate, curva=1.0):
    fase, out = 0.0, []
    for i in range(n):
        f = f_de + (f_ate - f_de) * (i / n) ** curva
        fase += 2 * math.pi * f / TAXA
        out.append(math.sin(fase))
    return out


def mix(*sinais):
    n = max(len(s) for s in sinais)
    return [sum(s[i] if i < len(s) else 0.0 for s in sinais) for i in range(n)]


def mult(a, b):
    return [x * y for x, y in zip(a, b)]


def gerar(pasta: Path):
    pasta.mkdir(parents=True, exist_ok=True)

    # whoosh: ruído rosa com banda subindo e descendo (passagem rápida)
    n = int(0.55 * TAXA)
    w = passa_banda(ruido(n, "rosa"), 300, 2400, q=2.5)
    salvar("whoosh", mult(w, envelope(n, 0.45, 2.2)), pasta, abertura=0.004)

    # whoosh_curto: transição seca entre cenas
    n = int(0.3 * TAXA)
    w = passa_banda(ruido(n, "rosa"), 800, 4000, q=2.0)
    salvar("whoosh_curto", mult(w, envelope(n, 0.3, 2.5)), pasta, abertura=0.003)

    # pop: bolha descendo de tom (texto entrando)
    n = int(0.09 * TAXA)
    p = seno_varrido(n, 900, 260, curva=0.5)
    salvar("pop", mult(p, envelope(n, 0.05, 3.0)), pasta)

    # batida: impacto grave do gancho (sub + estalo)
    n = int(0.8 * TAXA)
    sub = mult(seno_varrido(n, 95, 38, curva=0.4), envelope(n, 0.01, 2.6))
    m = int(0.03 * TAXA)
    estalo = mult(passa_banda(ruido(m), 2000, 600, q=1.0), envelope(m, 0.02, 2.0))
    salvar("batida", mix(sub, [e * 0.6 for e in estalo]), pasta)

    # subida: tensão crescendo antes da CTA (ruído + tom subindo)
    n = int(1.4 * TAXA)
    r = passa_banda(ruido(n, "rosa"), 400, 6000, q=3.0)
    t = seno_varrido(n, 220, 880, curva=2.0)
    sobe = [(i / n) ** 2.2 for i in range(n)]
    salvar("subida", mult(mix(r, [x * 0.25 for x in t]), sobe), pasta, abertura=0.006)

    # clique: toque de interface (CTA "toque no produto")
    n = int(0.05 * TAXA)
    c = mix(mult(seno_varrido(n, 2400, 1800), envelope(n, 0.01, 4.0)),
            [x * 0.4 for x in mult(ruido(n), envelope(n, 0.0, 8.0))])
    salvar("clique", c, pasta)

    # brilho: cintilar para destacar o produto
    n = int(0.9 * TAXA)
    notas = [1568, 2093, 2637, 3136]
    b = [0.0] * n
    for k, f in enumerate(notas):
        ini = int(k * 0.06 * TAXA)
        for i in range(ini, n):
            j = i - ini
            b[i] += math.sin(2 * math.pi * f * j / TAXA) * math.exp(-j / (0.18 * TAXA)) * 0.5
    salvar("brilho", b, pasta, abertura=0.008)

    # tique: marcação leve para listas ("4 USB • 1 tipo C")
    n = int(0.03 * TAXA)
    salvar("tique", mult(seno_varrido(n, 1400, 1100), envelope(n, 0.02, 5.0)), pasta)


if __name__ == "__main__":
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else "sfx")
    gerar(destino)
    print("sons em", destino, sorted(p.name for p in destino.glob("*.wav")))
