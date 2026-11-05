#!/usr/bin/env python3
"""Gera produtos/extensao/edicao_B/index.html (neon tech: Bebas Neue / Inter 800,
legenda caixa-palavra em vidro escuro, HUD com cantos de mira e cartão do produto herói com contorno neon).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Assets extras (gerados no container com ffmpeg, ver escolhas.md):
  e_quadro.jpg = clipe_E quadro 114 (4,75 s), extensão grande e nítida
  f_quadro.jpg = clipe_F quadro 6 (0,25 s), antes da falha de 0,75-1,3 s
  f_rev.mp4    = clipe_F 1,40-2,96 s invertido (vira aproximação), sem áudio
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 4.5, 0.25), "apresentacao": (4.5, 14.3, 4.75), "cta": (14.3, 19.45, 14.6)}
TOTAL = 19.45
H1 = (6.0, 8.1)     # cartão herói 1: 4 USB + tipo-C
H2 = (10.88, 14.3)  # cartão herói 2: 5 tomadas + liga/desliga + resumo


def topo_legenda(t):
    if t < 4.5: return 1290
    if t < 5.98: return 1362
    if t < 8.08: return 1300
    if t < 10.85: return 1352
    if t < 14.3: return 1300
    return 1318


GRUPOS = {
    "intro": [[0, 1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11]],
    "apresentacao": [[0], [1, 2, 3], [4, 5, 6], [7, 8], [9, 10], [11, 12], [13, 14, 15], [16, 17], [18, 19],
                     [20], [21, 22], [23, 24], [25, 26, 27]],
    "cta": [[0, 1], [2, 3], [4, 5], [6], [7, 8], [9, 10], [11, 12, 13]],
}
CHAVE = {
    "intro": {6, 8, 11},
    "apresentacao": {0, 6, 9, 13, 17, 22, 25},
    "cta": {3, 4, 6, 10, 12, 13},
}
TEXTO = {
    ("intro", 11): "carregador?",
    ("apresentacao", 9): "tipo-C", ("apresentacao", 10): "",
    ("cta", 3): "pertinho?",
}

leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    ini, fim, voz = P[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.03, 3)
        e = round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.03, 3) if gi + 1 < len(grupos) else fim
        gid = f"leg-{parte}-{gi}"
        top = topo_legenda(s + 0.05)
        spans, k = "", 0
        for wi in g:
            txt = TEXTO.get((parte, wi), pal[wi]["palavra"])
            if not txt:
                continue
            cls = "pal k" if wi in CHAVE[parte] else "pal"
            spans += f'<span id="{gid}-{k}" class="{cls}">{txt}</span>'
            t = max(s, round(voz + pal[wi]["inicio"] - 0.03, 3))
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:22,scale:0.86}},{{opacity:1,y:0,scale:1,duration:0.11,ease:"back.out(2.2)"}},{t});')
            k += 1
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="7"><div class="cap" style="top:{top}px">{spans}</div></div>'
        )

# ---- geometria do cartão herói (medida no e_quadro.jpg, 1080x1920) ----
S, TX, TY = 0.62, 285, 110
def sc(x, y):
    return round(TX + S * x), round(TY + S * y)
JAN = (150, 205, 1020, 1665)  # janela do cartão em coordenadas do quadro (x0, y0, x1, y1)
jx0, jy0 = sc(JAN[0], JAN[1]); jx1, jy1 = sc(JAN[2], JAN[3])
INSET = f"inset({JAN[1]}px {1080 - JAN[2]}px {1920 - JAN[3]}px {JAN[0]}px round 56px)"
bx, by = sc(382, 517); br = round(S * 128)          # botão (anel verde), raio com folga
ux0, uy0 = sc(322, 862); ux1, uy1 = sc(440, 1165)   # 4 USB
cx0, cy0 = sc(335, 1210); cx1, cy1 = sc(420, 1245)  # tipo-C
sx0, sy0 = sc(540, 375); sx1, sy1 = sc(905, 1435)   # coluna das 5 tomadas
sock_y = [sc(0, y)[1] for y in (455, 645, 835, 1030, 1350)]
PAD = 10
LAB_R = 350  # borda direita das etiquetas da esquerda


def hero(h):
    """HTML do cartão herói (mesma geometria nos dois momentos)."""
    digs = "".join(f'<b id="{h}-d{i}" class="dig" style="left:{sx1 + 16}px;top:{y - 26}px">{i + 1}</b>'
                   for i, y in enumerate(sock_y))
    return f'''
    <img id="{h}-bg" class="hbg" src="assets/e_quadro.jpg" alt="" />
    <div id="{h}-tint" class="htint"></div>
    <div id="{h}-grid" class="hgrid"></div>
    <div id="{h}-card" class="hcard"><img id="{h}-img" class="himg" src="assets/e_quadro.jpg" alt="Extensão filtro de linha" /><div id="{h}-sw" class="hsw"><i id="{h}-swi"></i></div></div>
    <div id="{h}-edge" class="hedge" style="left:{jx0}px;top:{jy0}px;width:{jx1 - jx0}px;height:{jy1 - jy0}px"></div>
    <div id="{h}-bring" class="ring" style="left:{bx - br}px;top:{by - br}px;width:{2 * br}px;height:{2 * br}px"></div>
    <div id="{h}-bu" class="brk" style="left:{ux0 - PAD}px;top:{uy0 - PAD}px;width:{ux1 - ux0 + 2 * PAD}px;height:{uy1 - uy0 + 2 * PAD}px"></div>
    <div id="{h}-bc" class="brk" style="left:{cx0 - PAD}px;top:{cy0 - PAD}px;width:{cx1 - cx0 + 2 * PAD}px;height:{cy1 - cy0 + 2 * PAD}px"></div>
    <div id="{h}-bs" class="brk" style="left:{sx0 - PAD}px;top:{sy0 - PAD}px;width:{sx1 - sx0 + 2 * PAD}px;height:{sy1 - sy0 + 2 * PAD}px"></div>
    {digs}
    <div id="{h}-lb" class="lead" style="left:{LAB_R}px;top:{by - 3}px;width:{bx - br - LAB_R}px"></div>
    <div id="{h}-lu" class="lead" style="left:{LAB_R}px;top:{(uy0 + uy1) // 2 - 3}px;width:{ux0 - PAD - LAB_R}px"></div>
    <div id="{h}-lc" class="lead" style="left:{LAB_R}px;top:{(cy0 + cy1) // 2 - 3}px;width:{cx0 - PAD - LAB_R}px"></div>
    <div id="{h}-eb" class="etq" style="top:{by - 55}px"><span style="font-size:66px">LIGA/DESLIGA</span></div>
    <div id="{h}-eu" class="etq" style="top:{(uy0 + uy1) // 2 - 55}px"><span><em id="{h}-nu">4</em> USB</span></div>
    <div id="{h}-ec" class="etq" style="top:{(cy0 + cy1) // 2 - 55}px"><span>TIPO-C</span></div>
    <div id="{h}-es" class="etq dir" style="top:{jy1 + 8}px;left:{(sx0 + sx1) // 2 - 150}px"><span style="font-size:76px"><em>5</em> TOMADAS</span></div>'''


def card_in(h, t):
    return f'''tl.fromTo("#{h}-card",{{x:0,y:0,scale:1,clipPath:"inset(0px 0px 0px 0px round 0px)"}},{{x:{TX},y:{TY},scale:{S},clipPath:"{INSET}",duration:0.42,ease:"power3.inOut"}},{t});
tl.fromTo("#{h}-bg",{{filter:"blur(0px) brightness(1)",scale:1}},{{filter:"blur(28px) brightness(0.42)",scale:1.12,duration:0.42,ease:"power2.out"}},{t});
tl.fromTo("#{h}-tint",{{opacity:0}},{{opacity:1,duration:0.4}},{t});
tl.fromTo("#{h}-grid",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:0.5,ease:"power2.out"}},{round(t + 0.1, 3)});
tl.fromTo("#{h}-edge",{{opacity:0,scale:1.04}},{{opacity:1,scale:1,duration:0.22,ease:"power2.out"}},{round(t + 0.36, 3)});
tl.fromTo("#{h}-card",{{filter:"brightness(1)"}},{{filter:"brightness(1.04)",duration:1.6,ease:"none",immediateRender:false}},{round(t + 0.45, 3)});'''


def pino(h, alvo, lead, etq, t):
    """Destaque (anel/colchete) + linha + etiqueta entrando em sequência."""
    js = f'tl.fromTo("#{h}-{alvo}",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.2,ease:"back.out(2)"}},{t});\n'
    if lead:
        js += f'tl.fromTo("#{h}-{lead}",{{scaleX:0,opacity:1,transformOrigin:"100% 50%"}},{{scaleX:1,opacity:1,duration:0.16,ease:"power2.out"}},{round(t + 0.08, 3)});\n'
    js += f'tl.fromTo("#{h}-{etq}",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.2,ease:"back.out(1.8)"}},{round(t + 0.12, 3)});'
    return js


html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
:root{--base:#0B0F1A;--neon:#3DF5A7;--texto:#F2F5FF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0B0F1A}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0B0F1A}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden}
.full{width:100%;height:100%;object-fit:cover}
#camD,#camE1,#camE2,#camR,#camF{z-index:1}
#camE2{transform-origin:540px 1450px}
#camF{transform-origin:533px 891px}
/* cartão do produto herói: quadro nítido do E, contorno neon, fundo do próprio quadro desfocado + grade */
.hero{z-index:2;overflow:hidden}
.hbg{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.htint{position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 60% 35%,rgba(11,15,26,.35) 0,rgba(11,15,26,.88) 100%)}
.hgrid{position:absolute;inset:0;background:
  repeating-linear-gradient(0deg,rgba(61,245,167,.075) 0 2px,rgba(0,0,0,0) 2px 64px),
  repeating-linear-gradient(90deg,rgba(61,245,167,.075) 0 2px,rgba(0,0,0,0) 2px 64px)}
.hcard{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;overflow:hidden}
.himg{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.hsw{position:absolute;inset:0;mix-blend-mode:screen;overflow:hidden}
.hsw i{position:absolute;left:0;top:0;width:100%;height:100%;display:block;
  background:linear-gradient(115deg,rgba(61,245,167,0) 38%,rgba(190,255,225,.42) 50%,rgba(61,245,167,0) 62%)}
.hedge{position:absolute;border:5px solid var(--neon);border-radius:35px;
  box-shadow:0 0 28px rgba(61,245,167,.75),0 0 80px rgba(61,245,167,.3),inset 0 0 24px rgba(61,245,167,.35)}
.ring{position:absolute;border:6px solid var(--neon);border-radius:50%;box-shadow:0 0 22px rgba(61,245,167,.9),inset 0 0 14px rgba(61,245,167,.5)}
.brk{position:absolute;border:5px solid var(--neon);border-radius:14px;box-shadow:0 0 20px rgba(61,245,167,.85),inset 0 0 12px rgba(61,245,167,.4)}
.dig{position:absolute;display:block;font-family:"Bebas Neue";font-weight:400;font-size:52px;line-height:1;color:var(--neon);
  text-shadow:0 0 14px rgba(61,245,167,.9),0 2px 6px rgba(0,0,0,.8)}
.ring,.brk,.dig,.etq,.lead,.hedge{opacity:0}
.lead{position:absolute;height:6px;background:var(--neon);border-radius:3px;box-shadow:0 0 12px var(--neon)}
.etq{position:absolute;left:40px;width:310px;height:110px;display:flex;justify-content:flex-end;align-items:center}
.etq.dir{width:300px;justify-content:center}
.etq span{display:block;font-family:"Bebas Neue";font-weight:400;font-size:84px;line-height:1;color:var(--texto);white-space:nowrap;
  background:rgba(11,15,26,.9);border:3px solid rgba(61,245,167,.85);border-radius:14px;padding:8px 20px 4px;
  box-shadow:0 0 26px rgba(61,245,167,.35),0 10px 24px rgba(0,0,0,.5)}
.etq em{font-style:normal;color:var(--neon);text-shadow:0 0 14px rgba(61,245,167,.8)}
/* luz e moldura */
.vinheta{z-index:3;background:radial-gradient(ellipse 85% 62% at 50% 50%,rgba(0,0,0,0) 58%,rgba(0,0,0,.42) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(11,15,26,.66) 0,rgba(11,15,26,.36) 15%,rgba(11,15,26,0) 30%)}
.flash{z-index:9;background:#FFFFFF}
.flashn{z-index:9;background:radial-gradient(ellipse at 50% 45%,rgba(190,255,225,.9) 0,rgba(61,245,167,.55) 45%,rgba(61,245,167,0) 80%)}
#wipe{z-index:9;overflow:hidden}
#wipe i{position:absolute;left:0;top:0;width:1080px;height:300px;display:block;
  background:linear-gradient(to bottom,rgba(61,245,167,0) 0,rgba(61,245,167,.55) 60%,#CFFFE9 82%,rgba(61,245,167,0) 100%)}
/* mira (cantos) */
.mira{z-index:5}
.vf{position:absolute;display:block}
.vf i{position:absolute;width:74px;height:74px;display:block;border-color:var(--neon);border-style:solid;
  filter:drop-shadow(0 0 10px rgba(61,245,167,.85))}
.vf .c1{left:0;top:0;border-width:7px 0 0 7px;border-radius:16px 0 0 0}
.vf .c2{right:0;top:0;border-width:7px 7px 0 0;border-radius:0 16px 0 0}
.vf .c3{left:0;bottom:0;border-width:0 0 7px 7px;border-radius:0 0 0 16px}
.vf .c4{right:0;bottom:0;border-width:0 7px 7px 0;border-radius:0 0 16px 0}
/* títulos: Bebas Neue, alinhados à esquerda, palavra-chave neon com brilho */
.titulo{z-index:5}
.bloco{position:absolute;left:64px;display:block}
.tl{display:block;font-family:"Bebas Neue";font-weight:400;color:var(--texto);line-height:.9;white-space:nowrap;letter-spacing:2px;
  text-shadow:0 6px 0 rgba(11,15,26,.85),0 12px 30px rgba(0,0,0,.5)}
.tl.neon{color:var(--neon);text-shadow:0 0 22px rgba(61,245,167,.65),0 6px 0 rgba(11,15,26,.85),0 12px 30px rgba(0,0,0,.5)}
.mask{position:absolute;left:64px;overflow:hidden;display:block}
.barra{position:absolute;left:64px;height:8px;background:var(--neon);border-radius:4px;box-shadow:0 0 16px var(--neon);display:block}
.pilula{position:absolute;left:64px;display:block;font-family:"Inter";font-weight:800;font-size:46px;line-height:1;color:var(--base);
  background:var(--neon);border-radius:999px;padding:14px 30px 16px;white-space:nowrap;box-shadow:0 0 30px rgba(61,245,167,.55)}
/* legenda caixa-palavra: vidro escuro com fio neon; palavra-chave na etiqueta verde-neon */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:860px;display:flex;justify-content:center;align-items:flex-start;gap:14px;flex-wrap:nowrap}
.pal{display:block;font-family:"Inter";font-weight:800;font-size:72px;line-height:1.08;color:var(--texto);white-space:nowrap;
  background:rgba(11,15,26,.9);border:2px solid rgba(61,245,167,.38);border-radius:16px;padding:4px 22px 10px;
  box-shadow:0 8px 22px rgba(0,0,0,.45)}
.pal.k{color:var(--base);background:var(--neon);border-color:var(--neon);box-shadow:0 0 30px rgba(61,245,167,.6),0 8px 22px rgba(0,0,0,.4)}
/* CTA */
#tap{z-index:6}
.onda{position:absolute;left:383px;top:741px;width:300px;height:300px;display:block;border-radius:50%;border:8px solid var(--neon);
  box-shadow:0 0 30px rgba(61,245,167,.8)}
#cta{z-index:8}
#cta-b{position:absolute;left:48px;top:1446px;display:flex;align-items:center;gap:18px;font-family:"Bebas Neue";font-weight:400;
  font-size:66px;line-height:1;color:var(--base);background:var(--neon);padding:12px 40px 10px 14px;border-radius:999px;white-space:nowrap;
  box-shadow:0 0 44px rgba(61,245,167,.6),0 10px 24px rgba(0,0,0,.45)}
#cta-b svg{display:block;width:72px;height:72px}
#cta-o{position:absolute;left:40px;top:1432px;width:110px;height:110px;display:block;border:5px solid var(--neon);border-radius:50%}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: clipe D só no trecho limpo 2,0-6,5 s (0,3-1,6 s tem falha de imagem) -->
  <div id="camD" class="cam"><video id="vD" class="clip full" data-start="0" data-duration="4.5" data-media-start="2.0" data-track-index="0" src="assets/clipe_D.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: clipe E em 0,77x; cartão herói (quadro 4,75 s) nos dois trechos de portas -->
  <div id="camE1" class="cam"><video id="vE1" class="clip full" data-start="4.5" data-duration="1.5" data-media-start="0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <div id="h1" class="clip hero" data-start="%%H1S%%" data-duration="%%H1D%%" data-track-index="1">%%HERO1%%
  </div>
  <div id="camE2" class="cam"><video id="vE2" class="clip full" data-start="8.1" data-duration="2.78" data-media-start="1.155" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <div id="h2" class="clip hero" data-start="%%H2S%%" data-duration="%%H2D%%" data-track-index="1">%%HERO2%%
  </div>
  <!-- CTA: clipe F 1,40-2,96 s invertido (aproxima) em 0,77x, depois quadro 0,25 s congelado -->
  <div id="camR" class="cam"><video id="vR" class="clip full" data-start="14.3" data-duration="1.6" data-media-start="0" data-playback-rate="0.77" data-track-index="0" src="assets/f_rev.mp4" muted playsinline></video></div>
  <div id="camF" class="cam"><img id="iF" class="clip full" data-start="15.9" data-duration="3.55" data-track-index="0" src="assets/f_quadro.jpg" alt="Extensão filtro de linha" /></div>

  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="3"></div>
  <div id="wipe" class="clip" data-start="4.34" data-duration="0.34" data-track-index="4"><i id="wipe-i"></i></div>
  <div id="flash1" class="clip flashn" data-start="6.0" data-duration="0.22" data-track-index="4"></div>
  <div id="flash2" class="clip flashn" data-start="10.88" data-duration="0.22" data-track-index="4"></div>
  <div id="flash3" class="clip flash" data-start="14.3" data-duration="0.14" data-track-index="4"></div>

  <!-- mira (cantos neon) no clipe E e na aproximação da CTA -->
  <div id="vfE" class="clip mira" data-start="4.5" data-duration="1.5" data-track-index="5">
    <div id="vfE-b" class="vf" style="left:300px;top:495px;width:460px;height:840px"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i></div>
  </div>
  <div id="vfC" class="clip mira" data-start="14.3" data-duration="3.15" data-track-index="5">
    <div id="vfC-b" class="vf" style="left:318px;top:478px;width:430px;height:826px"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i></div>
  </div>

  <!-- títulos -->
  <div id="ti" class="clip titulo" data-start="0" data-duration="4.4" data-track-index="6">
    <div id="ti-b" class="bloco" style="top:192px">
      <div id="ti-l0" class="tl" style="font-size:160px">FILA DO</div>
      <div id="ti-l1" class="tl neon" style="font-size:160px">CARREGADOR?</div>
    </div>
    <div id="ti-p" class="pilula" style="top:440px">todo mundo sem bateria</div>
  </div>
  <div id="ta" class="clip titulo" data-start="4.55" data-duration="1.45" data-track-index="6">
    <div class="mask" style="top:192px;height:132px"><div id="ta-l0" class="tl" style="font-size:140px">CARREGA</div></div>
    <div class="mask" style="top:318px;height:132px"><div id="ta-l1" class="tl neon" style="font-size:140px">TUDO JUNTO</div></div>
    <i id="ta-bar" class="barra" style="top:458px;width:400px"></i>
  </div>
  <div id="tc" class="clip titulo" data-start="15.9" data-duration="1.55" data-track-index="6">
    <div id="tc-b" class="bloco" style="top:192px">
      <div id="tc-l0" class="tl" style="font-size:150px">TOQUE NA</div>
      <div id="tc-l1" class="tl neon" style="font-size:150px">EXTENSÃO</div>
    </div>
  </div>
  <div id="tap" class="clip" data-start="16.05" data-duration="0.8" data-track-index="6"><i id="tap1" class="onda"></i><i id="tap2" class="onda"></i></div>
  <div id="cta" class="clip" data-start="17.45" data-duration="2.0" data-track-index="6">
    <i id="cta-o"></i>
    <span id="cta-b"><svg viewBox="0 0 72 72"><circle cx="36" cy="36" r="34" fill="#0B0F1A"/><path d="M50 22 L24 48 M23 30 L23 49 L42 49" fill="none" stroke="#3DF5A7" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>CONFIRA NO TIKTOK SHOP</span>
  </div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="4.2" data-track-index="8" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.75" data-duration="9.48" data-track-index="8" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="14.6" data-duration="4.728" data-track-index="8" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-000" data-start="0" data-duration="0.8" data-track-index="9" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-pop-162" data-start="1.62" data-duration="0.09" data-track-index="9" data-volume="0.35" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whoosh-436" data-start="4.36" data-duration="0.55" data-track-index="9" data-volume="0.4" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-whooshc-588" data-start="5.88" data-duration="0.3" data-track-index="9" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-730" data-start="7.3" data-duration="0.03" data-track-index="9" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whooshc-1080" data-start="10.8" data-duration="0.3" data-track-index="9" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1230" data-start="12.3" data-duration="0.03" data-track-index="9" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1390" data-start="13.9" data-duration="0.4" data-media-start="1.0" data-track-index="9" data-volume="0.38" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1607" data-start="16.07" data-duration="0.05" data-track-index="9" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-1745" data-start="17.45" data-duration="0.09" data-track-index="9" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });
const SAI = (sel, t) => tl.to(sel, {y:-50, opacity:0, duration:0.18, ease:"power2.in"}, t);

// ---- INTRO: gancho. Extensão inteira + 3 celulares no quadro 0, punch-in 1,12->1 e título gigante batendo ----
tl.fromTo("#camD", {scale:1.12}, {scale:1, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camD", {scale:1.025, duration:4.1, ease:"none"}, 0.4);
tl.fromTo("#ti-l0", {scale:1.15, transformOrigin:"0% 50%"}, {scale:1, duration:0.32, ease:"back.out(1.7)"}, 0);
tl.fromTo("#ti-l1", {scale:1.15, transformOrigin:"0% 50%"}, {scale:1, duration:0.32, ease:"back.out(1.7)"}, 0.04);
tl.to("#ti-b", {scale:0.74, transformOrigin:"0% 0%", duration:0.3, ease:"power3.inOut"}, 1.5);
tl.fromTo("#ti-p", {opacity:0, y:-24, scale:0.8, transformOrigin:"0% 50%"}, {opacity:1, y:-22, scale:1, duration:0.24, ease:"back.out(2)"}, 1.62);
tl.to("#ti-l1", {scale:1.07, transformOrigin:"0% 50%", duration:0.16, yoyo:true, repeat:1, ease:"sine.inOut"}, 3.25);
SAI("#ti-b", 4.16);
SAI("#ti-p", 3.05);

// passagem: barra neon varre de cima a baixo e corta para o E
tl.fromTo("#wipe-i", {y:-320}, {y:1940, duration:0.34, ease:"power2.inOut"}, 4.34);

// ---- APRESENTAÇÃO ----
tl.fromTo("#camE1", {scale:1.08}, {scale:1, duration:0.4, ease:"power3.out"}, 4.5);
tl.to("#camE1", {scale:1.02, duration:1.1, ease:"none"}, 4.9);
tl.fromTo("#vfE-b", {scale:1.3, opacity:0}, {scale:1, opacity:1, duration:0.3, ease:"power3.out"}, 4.6);
tl.to("#vfE-b", {scale:0.97, duration:0.12, yoyo:true, repeat:1, ease:"sine.inOut"}, 4.9);
tl.fromTo("#ta-l0", {yPercent:105}, {yPercent:0, duration:0.3, ease:"power3.out"}, 4.6);
tl.fromTo("#ta-l1", {yPercent:105}, {yPercent:0, duration:0.3, ease:"power3.out"}, 4.72);
tl.fromTo("#ta-bar", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.3, ease:"power2.out"}, 4.6);
tl.to("#ta-l0", {yPercent:-105, duration:0.2, ease:"power2.in"}, 5.75);
tl.to("#ta-l1", {yPercent:-105, duration:0.2, ease:"power2.in"}, 5.78);
tl.to("#ta-bar", {scaleX:0, transformOrigin:"100% 50%", duration:0.18, ease:"power2.in"}, 5.8);

// cartão herói 1: "com quatro USB e uma tipo cê"
tl.fromTo("#flash1", {opacity:0.7}, {opacity:0, duration:0.2}, 6.0);
%%CARD1%%
%%PINO_U1%%
%%CONTA_USB%%
%%PINO_C1%%
tl.to(["#h1-bu","#h1-lu","#h1-eu","#h1-bc","#h1-lc","#h1-ec"], {opacity:0, duration:0.14}, 7.94);

// volta ao vídeo: zoom lento e punch-in em "sem esperar a vez"
tl.fromTo("#camE2", {scale:1}, {scale:1.03, duration:1.42, ease:"none"}, 8.1);
tl.to("#camE2", {scale:1.06, duration:0.24, ease:"power3.out"}, 9.52);
tl.to("#camE2", {scale:1.07, duration:1.12, ease:"none"}, 9.76);

// cartão herói 2: "Sobram cinco tomadas e botão liga e desliga" + resumo
tl.fromTo("#flash2", {opacity:0.7}, {opacity:0, duration:0.2}, 10.88);
%%CARD2%%
tl.fromTo("#h2-bs", {opacity:0, scale:1.08}, {opacity:1, scale:1, duration:0.22, ease:"back.out(2)"}, 11.3);
%%DIGITOS%%
tl.fromTo("#h2-es", {opacity:0, y:30}, {opacity:1, y:0, duration:0.22, ease:"back.out(1.8)"}, 11.72);
%%PINO_B2%%
tl.fromTo("#h2-swi", {xPercent:-120}, {xPercent:120, duration:0.9, ease:"power2.inOut"}, 13.25);
%%RESUMO%%

// ---- CTA: aproximação (mira fecha na extensão), toque, botão com seta para baixo/esquerda ----
tl.fromTo("#flash3", {opacity:0.5}, {opacity:0, duration:0.12}, 14.3);
tl.fromTo("#camR", {scale:1.03}, {scale:1.05, duration:1.6, ease:"none"}, 14.3);
tl.fromTo("#vfC-b", {scale:1.75, opacity:0}, {scale:1, opacity:1, duration:1.7, ease:"power2.inOut"}, 14.32);
tl.fromTo("#camF", {scale:1.04}, {scale:1.09, duration:3.55, ease:"none"}, 15.9);
tl.fromTo("#tc-l0", {scale:1.8, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.26, ease:"back.out(1.7)"}, 15.9);
tl.fromTo("#tc-l1", {scale:1.8, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.26, ease:"back.out(1.7)"}, 15.98);
tl.to("#tc-b", {scale:0.93, transformOrigin:"0% 50%", duration:0.08, ease:"power2.in"}, 16.06);
tl.to("#tc-b", {scale:1, duration:0.25, ease:"back.out(3)"}, 16.14);
tl.fromTo("#tap1", {scale:0.15, opacity:1}, {scale:1.2, opacity:0, duration:0.6, ease:"power2.out"}, 16.07);
tl.fromTo("#tap2", {scale:0.15, opacity:0.8}, {scale:0.9, opacity:0, duration:0.55, ease:"power2.out"}, 16.2);
tl.to("#vfC-b", {opacity:0, duration:0.25}, 17.2);
SAI("#tc-b", 17.27);
tl.fromTo("#cta-b", {scale:0.6, opacity:0, transformOrigin:"10% 50%"}, {scale:1, opacity:1, duration:0.26, ease:"back.out(2.2)"}, 17.45);
tl.to("#cta-b", {scale:1.04, duration:0.38, yoyo:true, repeat:3, ease:"sine.inOut"}, 17.75);
tl.fromTo("#cta-o", {scale:0.3, opacity:0.95}, {scale:1.7, opacity:0, duration:0.6, ease:"power2.out"}, 17.5);
tl.fromTo("#cta-o", {scale:0.3, opacity:0.95}, {scale:1.7, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, 18.4);

// ---- legenda caixa-palavra ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

conta = "\n".join(f'tl.set("#h1-nu",{{textContent:"{v}"}},{t});' for t, v in
                  [(6.1, "0"), (6.3, "1"), (6.4, "2"), (6.5, "3"), (6.62, "4")])
conta += '\ntl.fromTo("#h1-nu",{scale:1.5},{scale:1,duration:0.25,ease:"back.out(2.5)",immediateRender:false},6.62);'
digitos = "\n".join(
    f'tl.fromTo("#h2-d{i}",{{opacity:0,scale:1.8}},{{opacity:1,scale:1,duration:0.14,ease:"back.out(2.5)"}},{round(11.37 + i * 0.08, 3)});'
    for i in range(5))
resumo = "\n".join([
    'tl.fromTo(["#h2-bu","#h2-bc"],{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.2,ease:"back.out(2)",stagger:0.1},13.3);',
    'tl.fromTo(["#h2-lu","#h2-lc"],{scaleX:0,opacity:1,transformOrigin:"100% 50%"},{scaleX:1,duration:0.16,ease:"power2.out",stagger:0.1},13.38);',
    'tl.fromTo(["#h2-eu","#h2-ec"],{opacity:0,x:-40},{opacity:1,x:0,duration:0.2,ease:"back.out(1.8)",stagger:0.1},13.42);',
])

html = (html.replace("%%TOTAL%%", str(TOTAL))
        .replace("%%H1S%%", str(H1[0])).replace("%%H1D%%", str(round(H1[1] - H1[0], 3)))
        .replace("%%H2S%%", str(H2[0])).replace("%%H2D%%", str(round(H2[1] - H2[0], 3)))
        .replace("%%HERO1%%", hero("h1")).replace("%%HERO2%%", hero("h2"))
        .replace("%%CARD1%%", card_in("h1", 6.0)).replace("%%CARD2%%", card_in("h2", 10.88))
        .replace("%%PINO_U1%%", pino("h1", "bu", "lu", "eu", 6.18))
        .replace("%%CONTA_USB%%", conta)
        .replace("%%PINO_C1%%", pino("h1", "bc", "lc", "ec", 7.3))
        .replace("%%DIGITOS%%", digitos)
        .replace("%%PINO_B2%%", pino("h2", "bring", "lb", "eb", 12.3))
        .replace("%%RESUMO%%", resumo)
        .replace("%%LEG_HTML%%", "\n".join(leg_html)).replace("%%LEG_JS%%", "\n".join(leg_js)))
open(OUT, "w").write(html)
print("ok", OUT)
