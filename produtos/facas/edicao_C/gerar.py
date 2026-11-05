#!/usr/bin/env python3
"""Gera produtos/facas/edicao_C/index.html ("laço de presente": verde-pinho / rosa-laço / creme,
DM Serif Display + Montserrat 800, legenda contorno-pop). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Combinação cruzada (vídeo C, "presente pra casa nova"). Regra número 1 (3ª violação, quadro estático): o vídeo de
fundo roda do primeiro ao último quadro. Não há <img>, quadro congelado nem cartão. Trechos (analise_C.md):
  intro        F 0,00-4,30 s em 1,0x (mão fatiando o tomate)
  apresentação D 0,50-3,20 s em 1,0x (tampa sobe, faca do chefe sobe) -> E 1,58-4,17 s em 0,7x (tesoura e descascador entram)
  CTA          B 3,60-5,40 s em 1,0x (close do relevo) -> F 4,30-7,00 s em 0,9x (continua de onde a intro parou)
Cepo de facas do clipe F (x 69-100 %, y 20-40 % do quadro original): o vídeo fica em escala >= 1,30 ancorada em
(20 %, 100 %) e a faixa sólida do título vai até FAIXA_H px; cobre até y = 1 - (1920-480)/(1920*1,32) = 43,2 %
(o cepo vai até 40-41 % do quadro original, medido com grade em 1,0/2,0/3,0/4,3/5,5/6,5/7,0 s).
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz). Cortes em múltiplos de 1/30 s.
P = {"intro": (0.0, 4.3, 0.25), "apresentacao": (4.3, 10.7, 4.55), "cta": (10.7, 15.5, 11.0)}
TOTAL = 15.5
CORTE_DE = 7.0   # clipe D -> clipe E (no silêncio entre "completo" e "quatro")
CORTE_BF = 12.5  # clipe B -> clipe F (logo antes de "churrasco")
DUR_MP3 = {"intro": 4.032, "apresentacao": 6.072, "cta": 4.464}
TOPO_LEG = 1286
FAIXA_H = 480
ESC_MIN_F = 1.32  # nunca abaixo disto no clipe F (cobertura do cepo)

GRUPOS = {
    "intro": [[0, 1], [2, 3, 4], [5, 6], [7], [8, 9]],
    "apresentacao": [[0, 1, 2], [3, 4], [5, 6], [7], [8, 9], [10, 11], [12], [13, 14], [15]],
    "cta": [[0], [1, 2], [3, 4, 5], [6, 7], [8], [9, 10]],
}
CHAVE = {
    "intro": {3, 4, 7, 9},
    "apresentacao": {2, 6, 7, 9, 11, 15},
    "cta": {0, 2, 5, 6, 8, 10},
}
EXIBE = {("intro", 4): "nova?"}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---- legenda contorno-pop: cada palavra entra com escala 0,8 -> 1 (0,12 s) no seu tempo; palavra-chave em rosa ----
CORTES = (P["apresentacao"][0], CORTE_DE, P["cta"][0], CORTE_BF)
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
            spans += f'<span id="{gid}-{k}" class="pal{" ch" if chave else ""}">{txt}</span>'
            leg_js.append(
                f'tl.fromTo("#{gid}-{k}",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.12,ease:"back.out(2.4)"}},{t});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{TOPO_LEG}px">{spans}</div></div>'
        )

T_NOVA = t_pal("intro", 4)
T_PRES = t_pal("intro", 7)
T_COZ = t_pal("intro", 9)
T_FAQ = t_pal("apresentacao", 6)
T_TES = t_pal("apresentacao", 11)       # "tesoura"
T_DESC = t_pal("apresentacao", 15)      # "descascador"
T_CHURR = t_pal("cta", 5)
T_TOCA = t_pal("cta", 6)
T_PROD = t_pal("cta", 8)
T_CONF = t_pal("cta", 10)

# Clipe E em 0,7x a partir de 1,58 s: tempo do clipe = 1,58 + (t - 7,0) * 0,7
#   "tesoura" (8,195) -> 2,42 s do clipe (tesoura entrando pela direita)
#   "descascador" (9,586) -> 3,39 s do clipe (descascador chegando ao lugar)
# Zoom no detalhe citado mantendo o ponto P parado: x,y = (P - centro) * (1 - escala)
ESC_E = 1.1
P_TES = (972, 730)    # tesoura: x 82-98 %, y 24-53 % do quadro
P_DESC = (950, 1277)  # descascador: x 80-96 %, y 56-77 % do quadro
txy = lambda p, s: (round((p[0] - 540) * (1 - s), 1), round((p[1] - 960) * (1 - s), 1))
TES_XY = txy(P_TES, ESC_E)
DESC_XY = txy(P_DESC, ESC_E)
DESC_XY2 = txy(P_DESC, 1.13)

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* nomes completos das fontes do container (o local() curto do fontes.css pode não carregar no Chromium) */
@font-face{font-family:"Serif Presente";src:local("DM Serif Display Regular"),local("DMSerifDisplay-Regular"),local("DM Serif Display")}
@font-face{font-family:"Mont Presente";font-weight:100 900;src:local("Montserrat Thin"),local("Montserrat-Thin"),local("Montserrat")}
:root{--pinho:#12291F;--rosa:#FF86A8;--creme:#FFF6E9}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#12291F}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#12291F;font-family:"Mont Presente";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camF1,#camF2{transform-origin:20% 100%}
#camD{transform-origin:52% 43%}
#camE{transform-origin:50% 50%}
#camB{transform-origin:50% 45%}
/* holofote na faca que sobe da caixa (escurece em volta; nada sobre a caixa) */
#holo{z-index:2}
#holo-b{position:absolute;inset:0;display:block;opacity:0;
  background:radial-gradient(ellipse 34% 30% at 52% 43%,rgba(18,41,31,0) 0,rgba(18,41,31,0) 55%,rgba(10,22,16,.55) 100%)}
/* luz que passa pelo relevo das lâminas */
#luz{z-index:2;overflow:hidden}
#luz-b{position:absolute;left:0;top:-400px;width:380px;height:2700px;display:block;
  background:linear-gradient(to right,rgba(255,246,233,0) 0,rgba(255,246,233,.42) 50%,rgba(255,246,233,0) 100%)}
.vinheta{z-index:3;background:radial-gradient(ellipse 94% 68% at 50% 50%,rgba(0,0,0,0) 62%,rgba(10,22,16,.42) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(18,41,31,.62) 0,rgba(18,41,31,.3) 12%,rgba(18,41,31,0) 24%)}
/* faixa de papel de presente: verde-pinho com risca fina, fita rosa na borda de baixo (cobre o cepo do clipe F) */
.faixa{z-index:5}
.fx{position:absolute;left:0;top:0;width:1080px;height:%%FAIXA_H%%px;display:block;background-color:#12291F;
  background-image:repeating-linear-gradient(90deg,rgba(255,246,233,.045) 0,rgba(255,246,233,.045) 3px,rgba(255,246,233,0) 3px,rgba(255,246,233,0) 34px);
  box-shadow:0 14px 30px rgba(0,0,0,.35)}
.fita{position:absolute;left:0;top:%%FITA_T%%px;width:1080px;height:18px;display:block;background-color:#FF86A8;
  background-image:linear-gradient(100deg,rgba(255,255,255,0) 0,rgba(255,255,255,0) 40%,rgba(255,255,255,.55) 50%,rgba(255,255,255,0) 60%,rgba(255,255,255,0) 100%);
  background-size:260% 100%;background-position:100% 0;
  box-shadow:inset 0 3px 0 rgba(255,255,255,.35),inset 0 -3px 0 rgba(150,40,75,.35)}
.filete{position:absolute;left:0;top:%%FILETE_T%%px;width:1080px;height:3px;display:block;background:rgba(255,246,233,.75)}
/* títulos: DM Serif Display creme, palavra de destaque em rosa */
.tt{display:block;font-family:"Serif Presente";font-weight:400;line-height:1;white-space:nowrap;text-align:center;color:var(--creme);
  letter-spacing:.5px;text-shadow:0 6px 18px rgba(0,0,0,.45)}
.tt .r{color:var(--rosa)}
.ta{position:absolute;left:62px;width:856px;display:block}
.mask{position:absolute;left:62px;width:856px;overflow:hidden;display:block}
/* etiqueta de presente: ponta à esquerda com furo, balança no fio */
.tagw{position:absolute;left:62px;width:856px;display:flex;justify-content:center}
.tag{position:relative;display:block;white-space:nowrap;background:var(--rosa);color:var(--pinho);font-family:"Mont Presente";font-weight:800;
  font-size:40px;line-height:1;padding:17px 34px 19px 70px;
  clip-path:polygon(0 50%,34px 0,100% 0,100% 100%,34px 100%);filter:drop-shadow(0 8px 14px rgba(0,0,0,.35))}
.tag i{position:absolute;left:30px;top:50%;width:16px;height:16px;margin-top:-8px;display:block;border-radius:50%;background:var(--pinho)}
.titulo{z-index:6}
/* legenda contorno-pop */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start;gap:22px;flex-wrap:nowrap}
.pal{display:block;font-family:"Mont Presente";font-weight:800;font-size:78px;line-height:1.1;white-space:nowrap;color:#FFFFFF;
  -webkit-text-stroke:10px #12291F;paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.5)}
.pal.ch{color:var(--rosa)}
/* CTA: botão rosa com seta para baixo/esquerda */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border-radius:50%;background:var(--rosa);
  box-shadow:0 0 0 6px rgba(18,41,31,.92),0 0 0 9px rgba(255,246,233,.8),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:116px;height:116px}
#tq-o{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border:7px solid var(--rosa);border-radius:50%;opacity:0}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO (0-4,3 s): clipe F 0-4,3 s em 1,0x, escala >= 1,30 ancorada embaixo à esquerda -->
  <div id="camF1" class="cam"><video id="vF1" class="clip full" data-start="0" data-duration="4.3" data-media-start="0" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO (4,3-10,7 s): clipe D 0,5-3,2 s em 1,0x (tampa sobe, faca do chefe sobe) -->
  <div id="camD" class="cam"><video id="vD" class="clip full" data-start="4.3" data-duration="2.7" data-media-start="0.5" data-track-index="0" src="assets/clipe_D.mp4" muted playsinline></video></div>
  <!-- clipe E 1,58-4,17 s em 0,7x (tesoura e descascador entram deslizando) -->
  <div id="camE" class="cam"><video id="vE" class="clip full" data-start="7" data-duration="3.7" data-media-start="1.58" data-playback-rate="0.7" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <!-- CTA (10,7-15,5 s): clipe B (lote A) 3,6-5,4 s em 1,0x (close do relevo) -->
  <div id="camB" class="cam"><video id="vB" class="clip full" data-start="10.7" data-duration="1.8" data-media-start="3.6" data-track-index="0" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <!-- clipe F 4,3-7,0 s em 0,9x (continua de onde a intro parou) -->
  <div id="camF2" class="cam"><video id="vF2" class="clip full" data-start="12.5" data-duration="3" data-media-start="4.3" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>

  <div id="holo" class="clip" data-start="6.2" data-duration="0.8" data-track-index="1"><i id="holo-b"></i></div>
  <div id="luz" class="clip" data-start="11.2" data-duration="0.95" data-track-index="1"><i id="luz-b"></i></div>
  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"></div>
  <div id="topo" class="clip topo" data-start="4.3" data-duration="8.2" data-track-index="3"></div>

  <!-- faixa da intro: título e etiqueta vão dentro dela -->
  <div id="fa1" class="clip faixa" data-start="0" data-duration="4.56" data-track-index="4">
    <div id="fa1-b" class="fx">
      <i class="filete"></i><i id="fa1-f" class="fita"></i>
      <div id="t1" class="ta" style="top:200px"><div id="t1-l" class="tt" style="font-size:128px">CASA <span id="t1-n" class="r" style="display:inline-block">NOVA?</span></div></div>
      <div class="tagw" style="top:360px"><div id="t1-t" class="tag"><i></i>presente pra cozinha</div></div>
    </div>
  </div>

  <!-- apresentação: título no alto da ardósia do clipe E, acima dos cabos -->
  <div id="t2" class="clip titulo" data-start="7" data-duration="3.7" data-track-index="6">
    <div class="mask" style="top:192px;height:92px"><div id="t2-l" class="tt" style="font-size:74px">FAQUEIRO <span class="r">COMPLETO</span></div></div>
    <div class="tagw" style="top:300px"><div id="t2-t" class="tag" style="font-size:34px;padding:14px 30px 16px 64px"><i></i>6 peças na caixa</div></div>
  </div>

  <!-- faixa da CTA: já inteira no primeiro quadro do clipe F -->
  <div id="fa2" class="clip faixa" data-start="12.24" data-duration="%%FA2D%%" data-track-index="4">
    <div id="fa2-b" class="fx">
      <i class="filete"></i><i id="fa2-f" class="fita"></i>
      <div class="mask" style="top:184px;height:106px"><div id="t3-l0" class="tt" style="font-size:100px">TOCA NO</div></div>
      <div class="mask" style="top:284px;height:106px"><div id="t3-l1" class="tt" style="font-size:100px"><span id="t3-p" class="r" style="display:inline-block">PRODUTO</span></div></div>
      <div class="tagw" style="top:398px"><div id="t3-t" class="tag" style="font-size:32px;padding:12px 30px 14px 62px"><i></i>e confere</div></div>
    </div>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="8">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#12291F" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.55" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="11" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-pop-1" data-start="2.05" data-duration="0.09" data-track-index="14" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="4.22" data-duration="0.3" data-track-index="14" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="6.92" data-duration="0.3" data-track-index="14" data-volume="0.28" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="14" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="10.32" data-duration="0.38" data-media-start="1.0" data-track-index="14" data-volume="0.36" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (clipe F): mão fatiando desde o quadro 0; punch-in, faixa de presente desce, "CASA NOVA?" bate ----
tl.fromTo("#camF1", {scale:1.44}, {scale:1.32, duration:0.42, ease:"power3.out"}, 0);
tl.to("#camF1", {scale:1.345, duration:%%DF1A%%, ease:"none"}, 0.42);
tl.to("#camF1", {scale:1.375, duration:0.25, ease:"power2.out"}, %%TCOZ0%%);
tl.to("#camF1", {scale:1.385, duration:%%DF1B%%, ease:"none"}, %%TCOZ1%%);
tl.fromTo("#fa1-b", {yPercent:-104}, {yPercent:0, duration:0.2, ease:"power3.out"}, 0);
tl.fromTo("#t1-l", {scale:1.55, opacity:0, transformOrigin:"50% 50%"}, {scale:1, opacity:1, duration:0.3, ease:"back.out(1.9)"}, 0.06);
tl.fromTo("#t1-n", {scale:1, transformOrigin:"50% 60%"}, {scale:1.1, duration:0.13, yoyo:true, repeat:1, ease:"power2.out"}, %%TNOVA%%);
tl.fromTo("#fa1-f", {backgroundPosition:"100% 0"}, {backgroundPosition:"0% 0", duration:1.3, ease:"power1.inOut"}, 0.2);
// etiqueta balança no fio, presa pelo furo
tl.fromTo("#t1-t", {opacity:0, rotation:-22, y:-30, transformOrigin:"38px 50%"}, {opacity:1, rotation:0, y:0, duration:0.75, ease:"elastic.out(1,0.45)"}, 2.06);
tl.fromTo("#fa1-f", {backgroundPosition:"100% 0"}, {backgroundPosition:"0% 0", duration:1.2, ease:"power1.inOut", immediateRender:false}, 2.8);
// passagem: a faixa sobe junto com o corte (cobre o cepo até o último quadro do F)
tl.to("#fa1-b", {yPercent:-104, duration:0.24, ease:"power3.in"}, 4.3);

// ---- APRESENTAÇÃO, clipe D: tampa sobe; em "faqueiro completo" a câmera fecha na faca que sobe, holofote ----
tl.fromTo("#camD", {scale:1.1}, {scale:1, duration:0.36, ease:"power3.out"}, 4.3);
tl.to("#camD", {scale:1.03, duration:1.62, ease:"none"}, 4.66);
tl.to("#camD", {scale:1.12, duration:0.5, ease:"power2.out"}, 6.28);
tl.to("#camD", {scale:1.14, duration:0.22, ease:"none"}, 6.78);
tl.fromTo("#holo-b", {opacity:0}, {opacity:1, duration:0.4, ease:"power1.out"}, 6.22);

// ---- APRESENTAÇÃO, clipe E: corte seco; título e etiqueta; zoom na tesoura e no descascador no tempo da fala ----
tl.fromTo("#camE", {scale:1.07, x:0, y:0}, {scale:1, x:0, y:0, duration:0.34, ease:"power3.out"}, 7);
tl.to("#camE", {scale:1.02, duration:%%DE1%%, ease:"none"}, 7.34);
tl.to("#camE", {scale:%%ESC_E%%, x:%%TESX%%, y:%%TESY%%, duration:0.45, ease:"power2.out"}, %%TTES0%%);
tl.to("#camE", {scale:%%ESC_E%%, x:%%DESX%%, y:%%DESY%%, duration:0.45, ease:"power2.inOut"}, %%TDESC0%%);
tl.to("#camE", {scale:1.13, x:%%DESX2%%, y:%%DESY2%%, duration:%%DE2%%, ease:"none"}, %%TDESC1%%);
tl.fromTo("#t2-l", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, 7.02);
tl.fromTo("#t2-t", {opacity:0, rotation:-22, y:-24, transformOrigin:"34px 50%"}, {opacity:1, rotation:0, y:0, duration:0.75, ease:"elastic.out(1,0.45)"}, 7.3);

// ---- CTA, clipe B: close do relevo, luz passando ----
tl.fromTo("#camB", {scale:1.08, x:0}, {scale:1, x:0, duration:0.36, ease:"power3.out"}, 10.7);
tl.to("#camB", {scale:1.04, x:-14, duration:1.44, ease:"none"}, 11.06);
tl.fromTo("#luz-b", {x:-620, rotation:16}, {x:1360, rotation:16, duration:0.9, ease:"power1.inOut"}, 11.22);
// a faixa desce sobre o fim do B e está inteira no primeiro quadro do F
tl.fromTo("#fa2-b", {yPercent:-104}, {yPercent:0, duration:0.22, ease:"power3.out"}, 12.24);
tl.fromTo("#fa2-f", {backgroundPosition:"100% 0"}, {backgroundPosition:"0% 0", duration:1.2, ease:"power1.inOut"}, 12.46);

// ---- CTA, clipe F: mais calmo; "TOCA NO PRODUTO" sobe em "Toca", botão com seta, etiqueta em "confere" ----
tl.fromTo("#camF2", {scale:1.37}, {scale:1.32, duration:0.4, ease:"power2.out"}, 12.5);
tl.to("#camF2", {scale:1.335, duration:%%DF2A%%, ease:"none"}, 12.9);
tl.to("#camF2", {scale:1.36, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camF2", {scale:1.375, duration:%%DF2B%%, ease:"none"}, %%TTOCA2%%);
// o título sobe no silêncio entre "churrasco" e "Toca"
tl.fromTo("#t3-l0", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, %%TT3%%);
tl.fromTo("#t3-l1", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, %%TT31%%);
tl.fromTo("#t3-p", {scale:1, transformOrigin:"50% 60%"}, {scale:1.07, duration:0.13, yoyo:true, repeat:1, ease:"power2.out"}, %%TPROD%%);
tl.fromTo("#t3-t", {opacity:0, rotation:-22, y:-24, transformOrigin:"36px 50%"}, {opacity:1, rotation:0, y:0, duration:0.75, ease:"elastic.out(1,0.45)"}, %%TCONF%%);
tl.fromTo("#fa2-f", {backgroundPosition:"100% 0"}, {backgroundPosition:"0% 0", duration:1.2, ease:"power1.inOut", immediateRender:false}, %%TPROD%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA%%);
tl.fromTo("#tq-s", {x:0, y:0}, {x:-7, y:7, duration:0.22, yoyo:true, repeat:7, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

T_TOCA0 = round(T_TOCA - 0.02, 3)
TTES0 = round(T_TES - 0.08, 3)
TDESC0 = round(T_DESC - 0.12, 3)
subs = {
    "TOTAL": str(TOTAL), "FAIXA_H": str(FAIXA_H), "FITA_T": str(FAIXA_H - 18), "FILETE_T": str(FAIXA_H - 24),
    "FA2D": R(TOTAL - 12.24),
    "DV1": str(DUR_MP3["intro"]), "DV2": str(DUR_MP3["apresentacao"]), "DV3": str(DUR_MP3["cta"]),
    "TNOVA": R(T_NOVA), "TCOZ0": R(T_COZ - 0.04), "TCOZ1": R(T_COZ + 0.22),
    "DF1A": R(T_COZ - 0.05 - 0.42), "DF1B": R(4.3 - (T_COZ + 0.22)),
    "ESC_E": str(ESC_E), "TESX": str(TES_XY[0]), "TESY": str(TES_XY[1]),
    "DESX": str(DESC_XY[0]), "DESY": str(DESC_XY[1]), "DESX2": str(DESC_XY2[0]), "DESY2": str(DESC_XY2[1]),
    "TTES0": R(TTES0), "TDESC0": R(TDESC0), "TDESC1": R(TDESC0 + 0.45),
    "DE1": R(TTES0 - 7.34), "DE2": R(10.7 - (TDESC0 + 0.45)),
    "STIQ1": R(T_TES - 0.09), "STIQ2": R(T_DESC - 0.09),
    "TTOCA": R(T_TOCA0), "TTOCA1": R(T_TOCA0 + 0.07), "TTOCA2": R(T_TOCA0 + 0.24), "DTOCA": R(TOTAL - T_TOCA0),
    "DF2A": R(T_TOCA0 - 12.91), "DF2B": R(TOTAL - (T_TOCA0 + 0.24)),
    "TPROD": R(T_PROD), "TT3": R(T_CHURR + 0.62), "TT31": R(T_CHURR + 0.69), "TCONF": R(T_CONF - 0.05),
    "TPULSO": R(T_TOCA0 + 0.3), "TONDA2": R(T_TOCA0 + 0.95),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
open(OUT, "w").write(html)
print("ok", OUT, "| tesoura", T_TES, "clipe E", round(1.58 + (T_TES - 7) * 0.7, 2),
      "| descascador", T_DESC, "clipe E", round(1.58 + (T_DESC - 7) * 0.7, 2), "| toca", T_TOCA0,
      "| esc E", TES_XY, DESC_XY, DESC_XY2)
