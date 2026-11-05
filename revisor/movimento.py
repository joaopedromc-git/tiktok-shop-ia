"""Camada 1 (vídeo): mede quanto do vídeo tem movimento real na cena.

O TikTok pune "imagem estática de um produto contra um fundo inalterado". Zoom,
deslocamento de câmera e texto animado não contam como movimento. Por isso o
cálculo:
1. extrai o vídeo em cinza, 180x320, 6 quadros por segundo;
2. calcula o fluxo óptico (Farneback) entre quadros vizinhos na faixa central
   (20% a 72% da altura, onde fica o produto e quase nunca há texto);
3. ajusta um movimento de câmera (escala + rotação + translação) a esse fluxo e
   desconta. O que sobra (resíduo) é o que se moveu dentro da cena;
4. um par de quadros é "sem movimento real" quando o percentil 90 do resíduo
   fica abaixo de 0,5 px. Cortes (diferença média > 25) ficam fora da conta.

Dependências: numpy, opencv-python-headless e ffmpeg (no PATH ou em $FFMPEG).
"""
import os
import subprocess

import cv2
import numpy as np

LARGURA, ALTURA, FPS = 180, 320, 6
LIMITE_RESIDUO = 0.5      # px; abaixo disso, nada se moveu além da câmera
LIMITE_CORTE = 25         # diferença média que indica troca de cena
# Fração do tempo sem movimento real. Números redondos, sem ajuste fino para
# acertar os casos conhecidos; o desempenho está em evals/resultados.md.
REPROVA, ATENCAO = 0.60, 0.45


def _quadros(video):
    ffmpeg = os.environ.get("FFMPEG", "ffmpeg")
    saida = subprocess.run(
        [ffmpeg, "-loglevel", "error", "-i", str(video),
         "-vf", f"fps={FPS},scale={LARGURA}:{ALTURA},format=gray",
         "-f", "rawvideo", "-"],
        capture_output=True, check=True).stdout
    return np.frombuffer(saida, np.uint8).reshape(-1, ALTURA, LARGURA)


def _residuos(quadros):
    y0, y1 = int(ALTURA * .20), int(ALTURA * .72)
    ys, xs = np.mgrid[y0:y1:4, 0:LARGURA:4]
    pontos = np.stack([xs.ravel(), ys.ravel()], 1).astype(np.float32)
    residuos = []
    for a, b in zip(quadros[:-1], quadros[1:]):
        if np.abs(a.astype(np.int16) - b).mean() > LIMITE_CORTE:
            residuos.append(np.nan)
            continue
        fluxo = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        destino = pontos + fluxo[ys, xs].reshape(-1, 2)
        camera, _ = cv2.estimateAffinePartial2D(
            pontos, destino, method=cv2.RANSAC, ransacReprojThreshold=1.0)
        if camera is None:
            residuos.append(np.nan)
            continue
        previsto = pontos @ camera[:, :2].T + camera[:, 2]
        residuos.append(float(np.percentile(np.linalg.norm(destino - previsto, axis=1), 90)))
    return np.array(residuos)


def _trechos_parados(parado, minimo=1.0):
    """Trechos contínuos sem movimento real com pelo menos `minimo` segundos."""
    trechos, inicio = [], None
    for i, p in enumerate(list(parado) + [False]):
        if p and inicio is None:
            inicio = i
        elif not p and inicio is not None:
            if (i - inicio) / FPS >= minimo:
                trechos.append((round(inicio / FPS, 1), round(i / FPS, 1)))
            inicio = None
    return trechos


def analisar(video):
    quadros = _quadros(video)
    r = _residuos(quadros)
    validos = r[~np.isnan(r)]
    parado = np.where(np.isnan(r), False, r < LIMITE_RESIDUO)
    fracao = float((validos < LIMITE_RESIDUO).mean()) if len(validos) else 1.0
    if fracao >= REPROVA:
        veredito = "reprova"
    elif fracao >= ATENCAO:
        veredito = "atencao"
    else:
        veredito = "aprova"
    return {
        "duracao_s": round(len(quadros) / FPS, 1),
        "fracao_sem_movimento": round(fracao, 3),
        "residuo_mediano_px": round(float(np.median(validos)), 2) if len(validos) else 0.0,
        "trechos_parados_s": _trechos_parados(parado),
        "veredito": veredito,
    }
