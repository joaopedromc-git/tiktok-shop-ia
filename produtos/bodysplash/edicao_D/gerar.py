#!/usr/bin/env python3
"""Gera produtos/bodysplash/edicao_D/index.html ("qual é o seu": grafite / lima elétrica / branco,
Anton + Inter 800, legenda sublinhado). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Combinação cruzada (vídeo D, "qual combina com você"), sem crédito para clipe novo. Regra número 1 (3ª violação,
quadro estático): o vídeo de fundo roda do primeiro ao último quadro. Não há <img>, quadro congelado nem cartão.
Trechos (analise_D.md):
  intro        A 5,50-7,93 s em 0,9x  (frascos sobem da caixa entre fumaça; enquadrado nos frascos)
  apresentação F 0,00-7,92 s em 0,99x (mãos trazendo a bandeja para a frente)
  CTA          E 4,00-7,87 s em 0,9x  (câmera deslizando; ancorado no alto, y <= -150: "bodyman" fora do quadro)
Os três frascos sempre juntos: nada aponta, rotula ou destaca um frasco; "limpo / versátil / marcante" trocam
num letreiro central, no tempo da fala. Efeitos só por cima do vídeo rodando e longe da cor dos rótulos.
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 2.7, 0.25), "apresentacao": (2.7, 10.7, 2.95), "cta": (10.7, 15.0, 11.0)}
TOTAL = 15.0
DUR_MP3 = {"intro": 2.28, "apresentacao": 7.608, "cta": 3.816}
TOPO_LEG = 1268

GRUPOS = {
    "intro": [[0, 1], [2], [3], [4, 5]],
    "apresentacao": [[0, 1, 2], [3, 4], [5, 6], [7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17, 18], [19],
                     [20, 21], [22, 23], [24]],
    "cta": [[0], [1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]],
}
CHAVE = {
    "intro": {2, 5},
    "apresentacao": {1, 2, 7, 15, 19, 24},
    "cta": {0, 4, 6, 8, 12},
}
EXIBE = {("intro", 5): "você?", ("apresentacao", 2): "Man,", ("apresentacao", 4): "Primacial:",
         ("apresentacao", 11): "dia,", ("apresentacao", 15): "versátil,", ("apresentacao", 24): "atenção.",
         ("cta", 12): "kit."}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---- legenda sublinhado: palavra sobe 18 px e acende no seu tempo; palavra-chave ganha traço lima por baixo ----
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = P[parte][2]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.04, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.04, 3), fim_voz)
        else:
            e = min(fim_voz, P[parte][1])
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.03, 3)
            chave = wi in CHAVE[parte]
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            ul = f'<i id="{gid}-{k}-u" class="ul"></i>' if chave else ""
            spans += f'<span id="{gid}-{k}" class="pal">{ul}<em class="tx">{txt}</em></span>'
            leg_js.append(
                f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.11,ease:"power2.out"}},{t});')
            if chave:
                leg_js.append(
                    f'tl.fromTo("#{gid}-{k}-u",{{scaleX:0}},{{scaleX:1,duration:0.2,ease:"power2.out"}},{round(t + 0.05, 3)});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{TOPO_LEG}px">{spans}</div></div>'
        )

T_KIT = t_pal("apresentacao", 0)
T_LIMPO = t_pal("apresentacao", 7)
T_VERS = t_pal("apresentacao", 15)
T_MARC = t_pal("apresentacao", 19)
T_QUANDO = t_pal("apresentacao", 21)
T_SEU = t_pal("cta", 4)
T_TOCA = t_pal("cta", 6)
T_TOCA0 = round(T_TOCA - 0.03, 3)

# ---- fumaça por cima da caixa (intro): (x, y, largura, deriva x) ----
PUFFS = [(-160, 1530, 660, 140), (250, 1600, 720, -90), (600, 1540, 640, 120),
         (40, 1720, 780, 110), (500, 1730, 760, -130), (820, 1650, 600, -100)]
puff_html = "\n".join(
    f'    <i id="pf{i}" class="puff" style="left:{x}px;top:{y}px;width:{w}px;height:{round(w * 0.62)}px"></i>'
    for i, (x, y, w, dx) in enumerate(PUFFS))
puff_js = "\n".join(
    f'tl.fromTo("#pf{i}",{{x:0,y:0,scale:1,opacity:{0.8 - 0.06 * (i % 3)}}},'
    f'{{x:{dx},y:-{40 + 15 * (i % 3)},scale:1.25,opacity:{0.22 + 0.05 * (i % 2)},duration:2.7,ease:"none"}},0);'
    for i, (x, y, w, dx) in enumerate(PUFFS))

# ---- partículas de luz no fundo azul do clipe F (só acima das tampas, y < 420 px): (x, y, tamanho, opacidade) ----
DOTS = [(70, 330, 14, .55), (180, 120, 9, .45), (300, 260, 20, .35), (430, 70, 11, .5), (520, 380, 8, .5),
        (610, 190, 17, .4), (700, 300, 10, .55), (790, 90, 22, .3), (860, 240, 12, .5), (960, 360, 16, .4),
        (1010, 140, 9, .5), (360, 400, 12, .45)]
dot_html = "\n".join(
    f'    <i id="dt{i}" class="dot" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px"></i>'
    for i, (x, y, s, o) in enumerate(DOTS))
dot_js = "\n".join(
    f'tl.fromTo("#dt{i}",{{x:0,y:0,opacity:0}},{{keyframes:[{{opacity:{o},duration:0.6}},'
    f'{{x:{(-1) ** i * (18 + 4 * (i % 4))},y:-{70 + 9 * (i % 5)},opacity:{round(o * 0.55, 2)},duration:6.8}},'
    f'{{opacity:0,duration:0.6}}],ease:"none"}},2.7);'
    for i, (x, y, s, o) in enumerate(DOTS))

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* nomes completos das fontes do container (Anton-Regular.ttf; Inter é variável) */
@font-face{font-family:"Anton Seu";src:local("Anton Regular"),local("Anton-Regular"),local("Anton")}
@font-face{font-family:"Inter Seu";font-weight:100 900;src:local("Inter Thin"),local("Inter-Thin"),local("Inter")}
:root{--grafite:#101215;--lima:#D4FF3A;--branco:#FFFFFF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#101215}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#101215;font-family:"Inter Seu";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camA{transform-origin:46% 0%}
#camF{transform-origin:42% 48%}
#camE{transform-origin:50% 0%}
/* fumaça clara subindo por cima da caixa (borda de baixo da intro) */
#fumaca{z-index:3;overflow:hidden}
.puff{position:absolute;display:block;border-radius:50%;
  background:radial-gradient(closest-side,rgba(226,228,234,.40) 0,rgba(226,228,234,.22) 45%,rgba(226,228,234,0) 100%)}
/* vazamento de luz quente só no alto (longe dos rótulos) */
#leak{z-index:2;overflow:hidden}
#leak-b{position:absolute;left:0;top:-330px;width:760px;height:760px;display:block;border-radius:50%;mix-blend-mode:screen;
  background:radial-gradient(closest-side,rgba(255,196,120,.55) 0,rgba(255,170,90,.22) 45%,rgba(255,170,90,0) 100%)}
/* partículas de luz no fundo azul do F */
#bokeh{z-index:2;overflow:hidden}
.dot{position:absolute;display:block;border-radius:50%;background:radial-gradient(closest-side,rgba(225,236,255,.95),rgba(225,236,255,0))}
/* brilho correndo nas tampas (faixa das tampas apenas) */
#brilho{z-index:2}
#br-m{position:absolute;left:0;top:%%BR_T%%px;width:1080px;height:%%BR_H%%px;overflow:hidden;display:block}
#br-b{position:absolute;left:0;top:-300px;width:240px;height:1100px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.62) 50%,rgba(255,255,255,0) 100%)}
.vinheta{z-index:3;background:radial-gradient(ellipse 96% 70% at 50% 50%,rgba(0,0,0,0) 64%,rgba(16,18,21,.45) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(16,18,21,.66) 0,rgba(16,18,21,.34) 13%,rgba(16,18,21,0) 27%)}
.baixo{z-index:3;background:linear-gradient(to top,rgba(16,18,21,.86) 0,rgba(16,18,21,.58) 13%,rgba(16,18,21,0) 28%)}
.flash{z-index:9;background:#FFFFFF;opacity:0}
/* títulos: Anton branco, destaque lima */
.titulo{z-index:6}
.tw{position:absolute;left:50px;width:860px;display:flex;justify-content:center}
.tt{display:block;font-family:"Anton Seu";font-weight:400;line-height:1.02;white-space:nowrap;color:var(--branco);
  letter-spacing:1px;text-shadow:0 6px 22px rgba(0,0,0,.55)}
.tt .l{color:var(--lima)}
.mask{position:absolute;left:50px;width:860px;overflow:hidden;display:flex;justify-content:center}
.pill{display:block;white-space:nowrap;background:rgba(16,18,21,.88);color:var(--branco);font-family:"Inter Seu";font-weight:800;
  font-size:40px;line-height:1;padding:16px 30px 18px;border-radius:40px;box-shadow:inset 0 0 0 3px var(--lima),0 10px 24px rgba(0,0,0,.4)}
/* letreiro que troca limpo / versátil / marcante no mesmo lugar (não aponta para frasco) */
#slot{position:absolute;left:220px;width:520px;height:104px;overflow:hidden;display:block;border-radius:16px;background:var(--lima);
  box-shadow:0 12px 28px rgba(0,0,0,.45)}
#slot-col{display:block}
#slot-col b{display:block;height:104px;font-family:"Anton Seu";font-weight:400;font-size:82px;line-height:104px;text-align:center;
  color:var(--grafite);letter-spacing:3px}
/* balão de comentário da CTA */
#bolha{position:absolute;left:150px;top:150px;display:block;background:var(--lima);border-radius:34px;padding:18px 44px 22px;
  box-shadow:0 14px 30px rgba(0,0,0,.45)}
#bolha b{display:block;font-family:"Anton Seu";font-weight:400;font-size:100px;line-height:1.02;white-space:nowrap;color:var(--grafite);letter-spacing:1px}
#bolha i{position:absolute;left:58px;bottom:-34px;width:60px;height:40px;display:block;background:var(--lima);clip-path:polygon(0 0,100% 0,0 100%)}
/* legenda sublinhado */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start;gap:20px;flex-wrap:nowrap}
.pal{position:relative;display:block;font-family:"Inter Seu";font-weight:800;font-size:74px;line-height:1.12;white-space:nowrap;color:#FFFFFF;
  -webkit-text-stroke:8px #101215;paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.55)}
.ul{position:absolute;left:-6px;right:-6px;bottom:4px;height:16px;display:block;border-radius:8px;background:var(--lima);
  transform-origin:0 50%;z-index:0;box-shadow:0 0 0 4px #101215}
.tx{position:relative;z-index:1;display:block;font-style:normal}
/* CTA: botão lima com seta para baixo/esquerda + linha "e toca no produto" */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border-radius:50%;background:var(--lima);
  box-shadow:0 0 0 6px rgba(16,18,21,.92),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:116px;height:116px}
#tq-o{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border:7px solid var(--lima);border-radius:50%;opacity:0}
#tq-l{position:absolute;left:196px;top:1426px;display:block}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO (0-2,7 s): clipe A (lote A) 5,50-7,93 s em 0,9x, frascos subindo da caixa; enquadrado nos frascos -->
  <div id="camA" class="cam"><video id="vA" class="clip full" data-start="0" data-duration="2.7" data-media-start="5.5" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_A.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO (2,7-10,7 s): clipe F 0-7,92 s em 0,99x, mãos trazendo a bandeja -->
  <div id="camF" class="cam"><video id="vF" class="clip full" data-start="2.7" data-duration="8" data-media-start="0" data-playback-rate="0.99" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>
  <!-- CTA (10,7-15 s): clipe E 4,0-7,87 s em 0,9x, ancorado no alto (escala >= 1,1, y <= -150): "bodyman" sempre fora -->
  <div id="camE" class="cam"><video id="vE" class="clip full" data-start="10.7" data-duration="4.3" data-media-start="4" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>

  <div id="leak" class="clip" data-start="0" data-duration="2.7" data-track-index="1"><i id="leak-b"></i></div>
  <div id="bokeh" class="clip" data-start="2.7" data-duration="8" data-track-index="1">
%%DOT_HTML%%
  </div>
  <div id="brilho" class="clip" data-start="%%BR_S%%" data-duration="0.8" data-track-index="2"><span id="br-m"><i id="br-b"></i></span></div>
  <div id="fumaca" class="clip" data-start="0" data-duration="2.7" data-track-index="3">
%%PUFF_HTML%%
  </div>
  <div id="baixo" class="clip baixo" data-start="0" data-duration="2.7" data-track-index="4"></div>
  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="5"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="11"></div>

  <!-- intro: "QUAL É O SEU?" bate em cima dos frascos; "3 body splashes no kit" abre em "combina" -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="2.7" data-track-index="6">
    <div class="tw" style="top:168px"><div id="t1-l" class="tt" style="font-size:150px">QUAL É O <span class="l">SEU?</span></div></div>
    <div class="tw" style="top:346px"><div id="t1-p" class="pill">3 body splashes no kit</div></div>
  </div>

  <!-- apresentação: "KIT BODY MAN" e o letreiro central que troca no tempo da fala -->
  <div id="t2" class="clip titulo" data-start="2.7" data-duration="8" data-track-index="7">
    <div class="mask" style="top:176px;height:140px"><div id="t2-l" class="tt" style="font-size:128px">KIT <span class="l">BODY MAN</span></div></div>
    <span id="slot" style="top:336px"><span id="slot-col"><b>LIMPO</b><b>VERSÁTIL</b><b>MARCANTE</b></span></span>
  </div>

  <!-- CTA: balão "COMENTA O SEU" + botão com seta e "e toca no produto" -->
  <div id="t3" class="clip titulo" data-start="10.9" data-duration="4.1" data-track-index="8">
    <span id="bolha"><b>COMENTA O SEU</b><i></i></span>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="10">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#101215" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <span id="tq-l" class="pill">e toca no produto</span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="9"></div>
  <div id="fl2" class="clip flash" data-start="2.66" data-duration="0.14" data-track-index="9"></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="2.95" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="11" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="2.42" data-duration="0.55" data-track-index="15" data-volume="0.36" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="14" data-volume="0.38" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-brilho-1" data-start="%%SBRI%%" data-duration="0.9" data-track-index="14" data-volume="0.3" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-subida-1" data-start="10.1" data-duration="0.6" data-media-start="0.8" data-track-index="15" data-volume="0.36" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (clipe A): flash + punch-in + tremor no impacto; fumaça clara por cima da caixa; luz quente no alto ----
tl.fromTo("#fl1", {opacity:0.9}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camA", {scale:1.42, filter:"blur(0px)"}, {scale:1.28, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camA", {scale:1.16, duration:2.12, ease:"none"}, 0.4);
tl.fromTo("#camA", {x:0, y:0}, {keyframes:[{x:16, y:-9, duration:0.05}, {x:-13, y:7, duration:0.06}, {x:9, y:-5, duration:0.06}, {x:-5, y:3, duration:0.07}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, 0.02);
%%PUFF_JS%%
tl.fromTo("#leak-b", {x:-420, opacity:0}, {keyframes:[{x:-120, opacity:1, duration:0.9}, {x:520, opacity:0.75, duration:1.8}], ease:"none"}, 0);
// título bate de 2 -> 1 com desfoque de movimento; pílula abre em "combina"
tl.fromTo("#t1-l", {scale:2, opacity:0, filter:"blur(14px)", transformOrigin:"50% 55%"}, {scale:1, opacity:1, filter:"blur(0px)", duration:0.32, ease:"back.out(1.7)"}, 0.05);
tl.fromTo("#t1-p", {clipPath:"inset(0% 100% 0% 0% round 40px)"}, {clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}, %%TPILL%%);
// passagem: zoom com desfoque (sai) + flash curto
tl.to("#camA", {scale:1.36, filter:"blur(18px)", duration:0.18, ease:"power2.in"}, 2.52);
tl.to("#t1-l", {scale:1.25, opacity:0, filter:"blur(12px)", duration:0.18, ease:"power2.in"}, 2.52);
tl.to("#t1-p", {opacity:0, y:-20, duration:0.16, ease:"power2.in"}, 2.52);
tl.fromTo("#fl2", {opacity:0}, {keyframes:[{opacity:0.55, duration:0.04}, {opacity:0, duration:0.1}], ease:"none"}, 2.66);

// ---- APRESENTAÇÃO (clipe F): entra do desfoque; punch no ritmo de limpo / versátil / marcante (os três juntos) ----
tl.fromTo("#camF", {scale:1.24, x:0, filter:"blur(18px)"}, {scale:1.02, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, 2.7);
tl.to("#camF", {scale:1.05, duration:%%DF1%%, ease:"none"}, 3.0);
tl.to("#camF", {scale:1.1, duration:0.12, ease:"power2.out"}, %%TP1%%);
tl.to("#camF", {scale:1.06, duration:0.5, ease:"power2.inOut"}, %%TP1B%%);
tl.to("#camF", {scale:1.07, duration:%%DF2%%, ease:"none"}, %%TP1C%%);
tl.to("#camF", {scale:1.11, duration:0.12, ease:"power2.out"}, %%TP2%%);
tl.to("#camF", {scale:1.075, duration:0.5, ease:"power2.inOut"}, %%TP2B%%);
tl.to("#camF", {scale:1.08, duration:%%DF3%%, ease:"none"}, %%TP2C%%);
tl.to("#camF", {scale:1.12, duration:0.12, ease:"power2.out"}, %%TP3%%);
tl.to("#camF", {scale:1.085, duration:0.5, ease:"power2.inOut"}, %%TP3B%%);
// produto herói: a câmera fecha nos três frascos enquanto o brilho corre nas tampas
tl.to("#camF", {scale:1.11, duration:0.6, ease:"power2.inOut"}, %%THERO%%);
tl.to("#camF", {scale:1.12, duration:%%DF4%%, ease:"none"}, %%THERO2%%);
tl.fromTo("#camF", {x:0, y:0}, {keyframes:[{x:12, y:-6, duration:0.05}, {x:-10, y:5, duration:0.06}, {x:6, y:-3, duration:0.06}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, %%TP3%%);
tl.fromTo("#br-b", {x:-420, rotation:16}, {x:1320, rotation:16, duration:0.72, ease:"power1.inOut"}, %%BR_S%%);
%%DOT_JS%%
// títulos
tl.fromTo("#t2-l", {yPercent:110, filter:"blur(8px)"}, {yPercent:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%TKIT%%);
tl.fromTo("#slot", {scaleX:0, opacity:0, transformOrigin:"50% 50%"}, {scaleX:1, opacity:1, duration:0.22, ease:"back.out(1.6)"}, %%TS1%%);
tl.fromTo("#slot-col", {y:104}, {y:0, duration:0.26, ease:"back.out(1.5)"}, %%TS1%%);
tl.to("#slot-col", {y:-104, duration:0.28, ease:"back.out(1.5)"}, %%TS2%%);
tl.to("#slot-col", {y:-208, duration:0.28, ease:"back.out(1.5)"}, %%TS3%%);
tl.fromTo("#slot", {scale:1}, {scale:1.08, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TS3B%%);
// passagem para a CTA: chicote lateral com desfoque
tl.to("#camF", {scale:1.3, x:-90, filter:"blur(16px)", duration:0.16, ease:"power2.in"}, 10.54);
tl.to(["#t2-l", "#slot"], {x:-120, opacity:0, duration:0.16, ease:"power2.in"}, 10.52);

// ---- CTA (clipe E): mais calma; balão "COMENTA O SEU"; botão com seta para baixo/esquerda em "toca" ----
tl.fromTo("#camE", {scale:1.2, x:110, y:-172, filter:"blur(16px)"}, {scale:1.1, x:0, y:-160, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, 10.7);
tl.to("#camE", {scale:1.125, duration:%%DE1%%, ease:"none"}, 11.0);
tl.to("#camE", {scale:1.15, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camE", {scale:1.165, duration:%%DE2%%, ease:"none"}, %%TTOCA2%%);
tl.fromTo("#bolha", {scale:0.3, opacity:0, transformOrigin:"12% 100%"}, {scale:1, opacity:1, duration:0.6, ease:"elastic.out(1,0.55)"}, 10.94);
tl.fromTo("#bolha", {rotation:0}, {keyframes:[{rotation:-3, duration:0.08}, {rotation:3, duration:0.12}, {rotation:0, duration:0.1}], ease:"none", immediateRender:false}, %%TSEU%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#tq-l", {clipPath:"inset(0% 100% 0% 0% round 40px)"}, {clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.28, ease:"power3.out"}, %%TTOCA1%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA%%);
tl.fromTo("#tq-s", {x:0, y:0}, {x:-7, y:7, duration:0.22, yoyo:true, repeat:%%REP%%, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

BR_S = round(T_QUANDO - 0.02, 3)       # brilho nas tampas em "quando quiser"
THERO = round(T_MARC - 0.05 + 0.62, 3)
TS1 = round(T_LIMPO - 0.1, 3)
TS2 = round(T_VERS - 0.07, 3)
TS3 = round(T_MARC - 0.07, 3)
TP1, TP2, TP3 = round(T_LIMPO - 0.05, 3), round(T_VERS - 0.05, 3), round(T_MARC - 0.05, 3)
TPULSO = round(T_TOCA0 + 0.3, 3)
REP = int(((TOTAL - 0.05) - TPULSO) / 0.22) - 1
REP -= (REP + 1) % 2 == 1  # número par de meias-voltas: termina em x:0
subs = {
    "TOTAL": str(TOTAL), "DOT_HTML": dot_html, "DOT_JS": dot_js, "PUFF_HTML": puff_html, "PUFF_JS": puff_js,
    "BR_T": "400", "BR_H": "430", "BR_S": R(BR_S), "SBRI": R(BR_S + 0.02),
    "DV1": str(DUR_MP3["intro"]), "DV2": str(DUR_MP3["apresentacao"]), "DV3": str(DUR_MP3["cta"]),
    "TPILL": R(t_pal("intro", 3) - 0.02),
    "DF1": R(TP1 - 3.0 - 0.003),
    "TP1": R(TP1), "TP1B": R(TP1 + 0.12), "TP1C": R(TP1 + 0.62), "DF2": R(TP2 - (TP1 + 0.62) - 0.003),
    "TP2": R(TP2), "TP2B": R(TP2 + 0.12), "TP2C": R(TP2 + 0.62), "DF3": R(TP3 - (TP2 + 0.62) - 0.003),
    "TP3": R(TP3), "TP3B": R(TP3 + 0.12),
    "THERO": R(THERO), "THERO2": R(THERO + 0.6), "DF4": R(10.54 - (THERO + 0.6) - 0.003),
    "TKIT": R(T_KIT - 0.05), "TS1": R(TS1), "TS2": R(TS2), "TS3": R(TS3), "TS3B": R(TS3 + 0.2),
    "STIQ1": R(T_LIMPO - 0.14), "STIQ2": R(T_VERS - 0.14),
    "DE1": R(T_TOCA0 - 11.0 - 0.003), "TTOCA": R(T_TOCA0), "TTOCA1": R(T_TOCA0 + 0.08), "TTOCA2": R(T_TOCA0 + 0.24),
    "DE2": R(TOTAL - (T_TOCA0 + 0.24)), "DTOCA": R(TOTAL - T_TOCA0),
    "TSEU": R(T_SEU), "TPULSO": R(TPULSO), "REP": str(REP), "TONDA2": R(T_TOCA0 + 0.95),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
assert THERO + 0.6 < 10.54 and TP3 + 0.62 <= THERO
open(OUT, "w").write(html)
print("ok", OUT, "| kit", T_KIT, "limpo", T_LIMPO, "versátil", T_VERS, "marcante", T_MARC, "brilho", BR_S,
      "| toca", T_TOCA0, "rep", REP)
