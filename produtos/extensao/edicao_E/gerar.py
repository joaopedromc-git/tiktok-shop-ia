#!/usr/bin/env python3
"""Gera produtos/extensao/edicao_E/index.html — teste de formato: cópia do body splash D ("Qual é o seu").
Grafite #101215 / lima #D4FF3A / branco, Anton + Inter 800, legenda sublinhado, letreiro lima que troca no lugar,
balão "COMENTA" e botão com seta na CTA. Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Legenda em y 1440 na intro/apresentação (em 1268 cobria a tipo C), 1268 na CTA (acima do botão).
Regras (analise_E.md + violações 3 e 5): clipe em tela cheia (sem moldura, sem fundo desfocado), vídeo sempre rodando,
nada abaixo de 0,9x, nada tinge a extensão branca (flash/brilho só de passagem).
Linha do tempo (s do vídeo final):
  0,000-1,556   M 0,00-1,40  a 0,9x  (estúdio, névoa, facho; depois de 1,5 s surge 2º cabo: proibido)
  1,556-4,167   O 1,50-3,85  a 0,9x  (dedos giram a extensão; 3,95-4,65 proibido)
  4,167-12,556  N 0,00-7,55  a 0,9x  (dedos empurram; parado só 7,1-7,55 = 0,5 s)
  12,556-16,000 O 4,70-7,80  a 0,9x  (gira de volta até ficar em pé; separado do 1º trecho de O pelo N)
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

TOTAL = 16.0
VOZ = {"intro": 0.15, "apresentacao": 3.62, "cta": 11.75}
FIM_PARTE = {"intro": 3.62, "apresentacao": 11.6, "cta": TOTAL}   # só para limitar a legenda
DV = {"intro": 3.45, "apresentacao": 8.016, "cta": 4.25}          # mp3: 3,48 / 8,016 / 4,272 (cauda muda)
TOPO_LEG = {"intro": 1440, "apresentacao": 1440, "cta": 1268}  # 1440 = abaixo da tipo C/USB; na CTA fica acima do botão

# cortes
R_ = 0.9
CM = (0.0, 1.4)
CO1 = (1.5, 3.85)
CN = (0.0, 7.55)
CO2 = (4.7, 7.8)
T_M = 0.0
T_O1 = round(T_M + (CM[1] - CM[0]) / R_, 3)
T_N = round(T_O1 + (CO1[1] - CO1[0]) / R_, 3)
T_O2 = round(T_N + (CN[1] - CN[0]) / R_, 3)
D_M, D_O1, D_N = round(T_O1 - T_M, 3), round(T_N - T_O1, 3), round(T_O2 - T_N, 3)
D_O2 = round(TOTAL - T_O2, 3)
assert abs(CO2[0] + D_O2 * R_ - CO2[1]) < 0.02, CO2[0] + D_O2 * R_

GRUPOS = {
    "intro": [[0, 1], [2, 3], [4], [5], [6, 7, 8]],
    "apresentacao": [[0], [1, 2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17], [18, 19],
                     [20], [21, 22]],
    "cta": [[0], [1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]],
}
CHAVE = {
    "intro": {3, 8},
    "apresentacao": {5, 9, 13, 19},
    "cta": {0, 4, 6, 8},
}
EXIBE = {("intro", 3): "usa:", ("intro", 4): "tomada,", ("intro", 8): "C?",
         ("apresentacao", 3): "linha:", ("apresentacao", 7): "aparelhos,", ("apresentacao", 13): "C",
         ("apresentacao", 17): "celular,", ("apresentacao", 22): "desliga.",
         ("cta", 12): "extensão."}


def t_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---- legenda sublinhado (igual ao D) ----
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = VOZ[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.04, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.04, 3), fim_voz)
        else:
            e = min(fim_voz, FIM_PARTE[parte])
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
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{TOPO_LEG[parte]}px">{spans}</div></div>'
        )

T_TOMADA = t_pal("intro", 4)
T_USBI = t_pal("intro", 5)
T_TIPOI = t_pal("intro", 7)
T_EXT = t_pal("apresentacao", 0)
T_FILTRO = t_pal("apresentacao", 1)
T_CINCO = t_pal("apresentacao", 4)
T_QUATRO = t_pal("apresentacao", 8)
T_TIPO = t_pal("apresentacao", 12)
T_BOTAO = t_pal("apresentacao", 18)   # "e botão"
T_USA = t_pal("cta", 4)
T_TOCA = t_pal("cta", 6)
T_TOCA0 = round(T_TOCA - 0.03, 3)

# ---- névoa clara por baixo da mão (intro, clipe M): (x, y, largura, deriva x) ----
PUFFS = [(-160, 1560, 660, 140), (250, 1640, 720, -90), (600, 1580, 640, 120),
         (40, 1740, 780, 110), (500, 1750, 760, -130), (820, 1680, 600, -100)]
puff_html = "\n".join(
    f'    <i id="pf{i}" class="puff" style="left:{x}px;top:{y}px;width:{w}px;height:{round(w * 0.62)}px"></i>'
    for i, (x, y, w, dx) in enumerate(PUFFS))
puff_js = "\n".join(
    f'tl.fromTo("#pf{i}",{{x:0,y:0,scale:1,opacity:{0.75 - 0.06 * (i % 3)}}},'
    f'{{x:{dx},y:-{40 + 15 * (i % 3)},scale:1.25,opacity:{0.3 + 0.05 * (i % 2)},duration:{D_M},ease:"none"}},0);'
    for i, (x, y, w, dx) in enumerate(PUFFS))

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
#camM{transform-origin:44% 53%}
#camO1{transform-origin:50% 50%}
#camN{transform-origin:50% 52%}
#camO2{transform-origin:50% 45%}
.sobe{position:absolute;left:0;top:-40px;width:1080px;height:1920px}
/* névoa clara subindo por baixo da mão (intro) */
#fumaca{z-index:3;overflow:hidden}
.puff{position:absolute;display:block;border-radius:50%;
  background:radial-gradient(closest-side,rgba(226,228,234,.40) 0,rgba(226,228,234,.22) 45%,rgba(226,228,234,0) 100%)}
/* luz quente só no alto (eco do facho dourado do clipe M, longe da extensão) */
#leak{z-index:2;overflow:hidden}
#leak-b{position:absolute;left:0;top:-360px;width:760px;height:760px;display:block;border-radius:50%;mix-blend-mode:screen;
  background:radial-gradient(closest-side,rgba(255,196,120,.5) 0,rgba(255,170,90,.2) 45%,rgba(255,170,90,0) 100%)}
/* brilho rápido correndo na extensão (produto herói, "botão liga e desliga") */
#brilho{z-index:2}
#br-m{position:absolute;left:0;top:260px;width:1080px;height:1340px;overflow:hidden;display:block}
#br-b{position:absolute;left:0;top:-300px;width:220px;height:1900px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.5) 50%,rgba(255,255,255,0) 100%)}
.vinheta{z-index:3;background:radial-gradient(ellipse 96% 70% at 50% 50%,rgba(0,0,0,0) 64%,rgba(16,18,21,.42) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(16,18,21,.66) 0,rgba(16,18,21,.34) 13%,rgba(16,18,21,0) 27%)}
.baixo{z-index:3;background:linear-gradient(to top,rgba(16,18,21,.6) 0,rgba(16,18,21,.3) 12%,rgba(16,18,21,0) 24%)}
.flash{z-index:9;background:#FFFFFF;opacity:0}
/* títulos: Anton branco, destaque lima */
.titulo{z-index:6}
.tw{position:absolute;left:50px;width:860px;display:flex;justify-content:center}
.tt{display:block;font-family:"Anton Seu";font-weight:400;line-height:1.02;white-space:nowrap;color:var(--branco);
  letter-spacing:1px;text-shadow:0 6px 22px rgba(0,0,0,.55);text-align:center}
.tt .l{color:var(--lima)}
.tt .ln{display:block}
.mask{position:absolute;left:50px;width:860px;overflow:hidden;display:flex;justify-content:center}
.pill{display:block;white-space:nowrap;background:rgba(16,18,21,.88);color:var(--branco);font-family:"Inter Seu";font-weight:800;
  font-size:40px;line-height:1;padding:16px 30px 18px;border-radius:40px;box-shadow:inset 0 0 0 3px var(--lima),0 10px 24px rgba(0,0,0,.4)}
.pill b{display:inline-block;font-weight:800;color:var(--branco)}
/* letreiro que troca 5 TOMADAS / 4 USB / TIPO C no mesmo lugar (não aponta para porta nenhuma) */
#slot{position:absolute;left:220px;width:520px;height:104px;overflow:hidden;display:block;border-radius:16px;background:var(--lima);
  box-shadow:0 12px 28px rgba(0,0,0,.45)}
#slot-col{display:block}
#slot-col b{display:block;height:104px;font-family:"Anton Seu";font-weight:400;font-size:82px;line-height:104px;text-align:center;
  color:var(--grafite);letter-spacing:3px}
/* balão de comentário da CTA */
#bolha{position:absolute;left:96px;top:150px;display:block;background:var(--lima);border-radius:34px;padding:18px 40px 22px;
  box-shadow:0 14px 30px rgba(0,0,0,.45)}
#bolha b{display:block;font-family:"Anton Seu";font-weight:400;font-size:92px;line-height:1.02;white-space:nowrap;color:var(--grafite);letter-spacing:1px}
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
  <!-- INTRO: M 0-1,40 s a 0,9x (estúdio, névoa, facho) -> O 1,50-3,85 s a 0,9x (dedos giram a extensão) -->
  <div id="camM" class="cam"><video id="vM" class="clip full" data-start="0" data-duration="%%D_M%%" data-media-start="%%CM0%%" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_M.mp4" muted playsinline></video></div>
  <div id="camO1" class="cam"><video id="vO1" class="clip full" data-start="%%T_O1%%" data-duration="%%D_O1%%" data-media-start="%%CO10%%" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_O.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: N 0-7,55 s a 0,9x (dedos empurram a extensão; todas as portas à vista) -->
  <div id="camN" class="cam"><div id="posN" class="sobe"><video id="vN" class="clip full" data-start="%%T_N%%" data-duration="%%D_N%%" data-media-start="%%CN0%%" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_N.mp4" muted playsinline></video></div></div>
  <!-- CTA: O 4,70-7,80 s a 0,9x (gira de volta até ficar em pé) -->
  <div id="camO2" class="cam"><video id="vO2" class="clip full" data-start="%%T_O2%%" data-duration="%%D_O2%%" data-media-start="%%CO20%%" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_O.mp4" muted playsinline></video></div>

  <div id="leak" class="clip" data-start="0" data-duration="%%D_M%%" data-track-index="2"><i id="leak-b"></i></div>
  <div id="brilho" class="clip" data-start="%%BR_S%%" data-duration="0.8" data-track-index="2"><span id="br-m"><i id="br-b"></i></span></div>
  <div id="fumaca" class="clip" data-start="0" data-duration="%%D_M%%" data-track-index="3">
%%PUFF_HTML%%
  </div>
  <div id="baixo" class="clip baixo" data-start="0" data-duration="%%D_M%%" data-track-index="4"></div>
  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="5"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="11"></div>

  <!-- intro: "QUAL VOCÊ / MAIS USA?" bate no quadro 0; a pílula monta tomada • USB • tipo C no tempo da voz -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="%%T_N%%" data-track-index="6">
    <div class="tw" style="top:160px"><div id="t1-l" class="tt" style="font-size:134px"><span class="ln">QUAL VOCÊ</span><span class="ln l">MAIS USA?</span></div></div>
    <div class="tw" style="top:452px"><div id="t1-p" class="pill"><b id="ch1">tomada</b> <b id="ch2">• USB</b> <b id="ch3">• tipo C</b></div></div>
  </div>

  <!-- apresentação: "FILTRO DE LINHA" e o letreiro central que troca no tempo da fala -->
  <div id="t2" class="clip titulo" data-start="%%T_N%%" data-duration="%%D_T2%%" data-track-index="7">
    <div class="mask" style="top:172px;height:128px"><div id="t2-l" class="tt" style="font-size:112px">FILTRO <span class="l">DE LINHA</span></div></div>
    <span id="slot" style="top:318px"><span id="slot-col"><b>5 TOMADAS</b><b>4 USB</b><b>TIPO C</b></span></span>
  </div>

  <!-- CTA: balão "COMENTA QUAL USA" + botão com seta e "e toca no produto" -->
  <div id="t3" class="clip titulo" data-start="%%T_BOLHA%%" data-duration="%%D_BOLHA%%" data-track-index="8">
    <span id="bolha"><b>COMENTA QUAL USA</b><i></i></span>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="10">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#101215" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <span id="tq-l" class="pill">e toca no produto</span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="9"></div>
  <div id="fl2" class="clip flash" data-start="%%T_FL2%%" data-duration="0.12" data-track-index="9"></div>
  <div id="fl3" class="clip flash" data-start="%%T_FL3%%" data-duration="0.14" data-track-index="9"></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="%%V1%%" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="%%V2%%" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="%%V3%%" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="%%SWH%%" data-duration="0.55" data-track-index="15" data-volume="0.36" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="14" data-volume="0.38" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-brilho-1" data-start="%%SBRI%%" data-duration="0.9" data-track-index="14" data-volume="0.3" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-subida-1" data-start="%%SSUB%%" data-duration="0.5" data-media-start="0.9" data-track-index="15" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (M): flash + punch-in + tremor no impacto; névoa clara por baixo; luz quente no alto ----
// flash fraco no quadro 0 (o quadro 0 é a capa: produto e pergunta legíveis)
tl.fromTo("#fl1", {opacity:0.4}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camM", {scale:1.38}, {scale:1.26, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camM", {scale:1.2, duration:%%DM1%%, ease:"none"}, 0.4);
tl.fromTo("#camM", {x:0, y:0}, {keyframes:[{x:16, y:-9, duration:0.05}, {x:-13, y:7, duration:0.06}, {x:9, y:-5, duration:0.06}, {x:-5, y:3, duration:0.07}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, 0.02);
%%PUFF_JS%%
tl.fromTo("#leak-b", {x:-420, opacity:0}, {keyframes:[{x:-160, opacity:1, duration:0.6}, {x:420, opacity:0.7, duration:%%DLEAK%%}], ease:"none"}, 0);
// título bate de 2 -> 1 com desfoque; a pílula abre em "tomada" e cada opção acende em lima no seu tempo
tl.fromTo("#t1-l", {scale:1.5, opacity:1, filter:"blur(5px)", transformOrigin:"50% 55%"}, {scale:1, opacity:1, filter:"blur(0px)", duration:0.32, ease:"back.out(1.7)"}, 0);
tl.fromTo("#t1-p", {clipPath:"inset(0% 100% 0% 0% round 40px)"}, {clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}, %%TPILL%%);
tl.fromTo("#ch1", {color:"#FFFFFF"}, {color:"#D4FF3A", duration:0.12, ease:"none"}, %%TCH1%%);
tl.fromTo("#ch2", {opacity:0.35}, {opacity:1, duration:0.12, ease:"none"}, %%TCH2%%);
tl.fromTo("#ch2", {color:"#FFFFFF"}, {color:"#D4FF3A", duration:0.12, ease:"none", immediateRender:false}, %%TCH2%%);
tl.to("#ch1", {color:"#FFFFFF", duration:0.12, ease:"none"}, %%TCH2%%);
tl.fromTo("#ch3", {opacity:0.35}, {opacity:1, duration:0.12, ease:"none"}, %%TCH3%%);
tl.fromTo("#ch3", {color:"#FFFFFF"}, {color:"#D4FF3A", duration:0.12, ease:"none", immediateRender:false}, %%TCH3%%);
tl.to("#ch2", {color:"#FFFFFF", duration:0.12, ease:"none"}, %%TCH3%%);
// corte seco M -> O com flash curto e punch-in
tl.fromTo("#fl2", {opacity:0}, {keyframes:[{opacity:0.45, duration:0.03}, {opacity:0, duration:0.08}], ease:"none"}, %%T_FL2%%);
tl.fromTo("#camO1", {scale:1.14}, {scale:1.03, duration:0.3, ease:"power3.out"}, %%T_O1%%);
tl.to("#camO1", {scale:1.05, duration:%%DO1%%, ease:"none"}, %%T_O1B%%);
// passagem O -> N: zoom com desfoque (sai) + flash curto
tl.to("#camO1", {scale:1.22, filter:"blur(18px)", duration:0.17, ease:"power2.in"}, %%T_OUT1%%);
tl.to("#t1-l", {scale:1.25, opacity:0, filter:"blur(12px)", duration:0.17, ease:"power2.in"}, %%T_OUT1%%);
tl.to("#t1-p", {opacity:0, y:-20, duration:0.15, ease:"power2.in"}, %%T_OUT1%%);
tl.fromTo("#fl3", {opacity:0}, {keyframes:[{opacity:0.55, duration:0.04}, {opacity:0, duration:0.1}], ease:"none"}, %%T_FL3%%);

// ---- APRESENTAÇÃO (N): entra do desfoque; punch no ritmo de 5 tomadas / 4 USB / tipo C (o quadro inteiro) ----
tl.fromTo("#camN", {scale:1.26, x:0, filter:"blur(18px)"}, {scale:1.05, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%T_N%%);
tl.to("#camN", {scale:1.07, duration:%%DF1%%, ease:"none"}, %%T_N3%%);
tl.to("#camN", {scale:1.12, duration:0.12, ease:"power2.out"}, %%TP1%%);
tl.to("#camN", {scale:1.08, duration:0.5, ease:"power2.inOut"}, %%TP1B%%);
tl.to("#camN", {scale:1.09, duration:%%DF2%%, ease:"none"}, %%TP1C%%);
tl.to("#camN", {scale:1.13, duration:0.12, ease:"power2.out"}, %%TP2%%);
tl.to("#camN", {scale:1.095, duration:0.5, ease:"power2.inOut"}, %%TP2B%%);
tl.to("#camN", {scale:1.1, duration:%%DF3%%, ease:"none"}, %%TP2C%%);
tl.to("#camN", {scale:1.14, duration:0.12, ease:"power2.out"}, %%TP3%%);
tl.to("#camN", {scale:1.105, duration:0.5, ease:"power2.inOut"}, %%TP3B%%);
tl.to("#camN", {scale:1.115, duration:%%DF4%%, ease:"none"}, %%TP3C%%);
// produto herói: a câmera fecha na extensão inteira e um brilho rápido corre por ela em "botão liga e desliga"
tl.to("#camN", {scale:1.2, duration:0.6, ease:"power2.inOut"}, %%THERO%%);
tl.to("#camN", {scale:1.22, duration:%%DF5%%, ease:"none"}, %%THERO2%%);
tl.fromTo("#camN", {x:0, y:0}, {keyframes:[{x:12, y:-6, duration:0.05}, {x:-10, y:5, duration:0.06}, {x:6, y:-3, duration:0.06}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, %%TP3%%);
tl.fromTo("#br-b", {x:-420, rotation:16}, {x:1320, rotation:16, duration:0.72, ease:"power1.inOut"}, %%BR_S%%);
// títulos
tl.fromTo("#t2-l", {yPercent:110, filter:"blur(8px)"}, {yPercent:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%TKIT%%);
tl.fromTo("#slot", {scaleX:0, opacity:0, transformOrigin:"50% 50%"}, {scaleX:1, opacity:1, duration:0.22, ease:"back.out(1.6)"}, %%TS1%%);
tl.fromTo("#slot-col", {y:104}, {y:0, duration:0.26, ease:"back.out(1.5)"}, %%TS1%%);
tl.to("#slot-col", {y:-104, duration:0.28, ease:"back.out(1.5)"}, %%TS2%%);
tl.to("#slot-col", {y:-208, duration:0.28, ease:"back.out(1.5)"}, %%TS3%%);
tl.fromTo("#slot", {scale:1}, {scale:1.08, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TS3B%%);
// fim da apresentação: título e letreiro saem para a esquerda no respiro
tl.to(["#t2-l", "#slot"], {x:-120, opacity:0, duration:0.16, ease:"power2.in"}, %%T_T2OUT%%);
// passagem para o O: chicote lateral com desfoque (o balão fica)
tl.to("#camN", {scale:1.36, x:-90, filter:"blur(16px)", duration:0.16, ease:"power2.in"}, %%T_OUT2%%);

// ---- CTA: balão entra no respiro; O entra em chicote; botão com seta para baixo/esquerda em "toca" ----
tl.fromTo("#bolha", {scale:0.3, opacity:0, transformOrigin:"12% 100%"}, {scale:1, opacity:1, duration:0.6, ease:"elastic.out(1,0.55)"}, %%T_BOLHA%%);
tl.fromTo("#bolha", {rotation:0}, {keyframes:[{rotation:-3, duration:0.08}, {rotation:3, duration:0.12}, {rotation:0, duration:0.1}], ease:"none", immediateRender:false}, %%TUSA%%);
tl.fromTo("#camO2", {scale:1.14, x:110, filter:"blur(16px)"}, {scale:1.02, x:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%T_O2%%);
tl.to("#camO2", {scale:1.035, duration:%%DE1%%, ease:"none"}, %%T_O2B%%);
tl.to("#camO2", {scale:1.05, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camO2", {scale:1.06, duration:%%DE2%%, ease:"none"}, %%TTOCA2%%);
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

T_OUT1 = round(T_N - 0.17, 3)
T_OUT2 = round(T_O2 - 0.16, 3)
TP1, TP2, TP3 = round(T_CINCO - 0.05, 3), round(T_QUATRO - 0.05, 3), round(T_TIPO - 0.05, 3)
THERO = round(T_BOTAO - 0.06, 3)
BR_S = round(T_BOTAO, 3)
TS1, TS2, TS3 = round(T_CINCO - 0.1, 3), round(T_QUATRO - 0.07, 3), round(T_TIPO - 0.07, 3)
T_BOLHA = round(VOZ["cta"] - 0.15, 3)
T_T2OUT = round(VOZ["apresentacao"] + falas["apresentacao"]["palavras"][-1]["fim"] + 0.1, 3)
TPULSO = round(T_TOCA0 + 0.3, 3)
REP = int(((TOTAL - 0.05) - TPULSO) / 0.22) - 1
REP -= (REP + 1) % 2 == 1  # número par de meias-voltas: termina em x:0
subs = {
    "TOTAL": str(TOTAL), "PUFF_HTML": puff_html, "PUFF_JS": puff_js,
    "D_M": R(D_M), "D_O1": R(D_O1), "D_N": R(D_N), "D_O2": R(D_O2),
    "T_O1": R(T_O1), "T_N": R(T_N), "T_O2": R(T_O2),
    "CM0": R(CM[0]), "CO10": R(CO1[0]), "CN0": R(CN[0]), "CO20": R(CO2[0]),
    "DM1": R(D_M - 0.4), "DLEAK": R(D_M - 0.6),
    "TPILL": R(T_TOMADA - 0.04), "TCH1": R(T_TOMADA - 0.02), "TCH2": R(T_USBI - 0.03), "TCH3": R(T_TIPOI - 0.03),
    "T_FL2": R(T_O1 - 0.01), "T_O1B": R(T_O1 + 0.3), "DO1": R(T_OUT1 - (T_O1 + 0.3) - 0.003), "T_OUT1": R(T_OUT1),
    "T_FL3": R(T_N - 0.04),
    "T_N3": R(T_N + 0.3), "DF1": R(TP1 - (T_N + 0.3) - 0.003),
    "TP1": R(TP1), "TP1B": R(TP1 + 0.12), "TP1C": R(TP1 + 0.62), "DF2": R(TP2 - (TP1 + 0.62) - 0.003),
    "TP2": R(TP2), "TP2B": R(TP2 + 0.12), "TP2C": R(TP2 + 0.62), "DF3": R(TP3 - (TP2 + 0.62) - 0.003),
    "TP3": R(TP3), "TP3B": R(TP3 + 0.12), "TP3C": R(TP3 + 0.62), "DF4": R(THERO - (TP3 + 0.62) - 0.003),
    "THERO": R(THERO), "THERO2": R(THERO + 0.6), "DF5": R(T_OUT2 - (THERO + 0.6) - 0.003),
    "BR_S": R(BR_S), "SBRI": R(BR_S + 0.02),
    "TKIT": R(T_FILTRO - 0.03), "TS1": R(TS1), "TS2": R(TS2), "TS3": R(TS3), "TS3B": R(TS3 + 0.2),
    "D_T2": R(T_T2OUT + 0.2 - T_N), "T_T2OUT": R(T_T2OUT), "T_OUT2": R(T_OUT2),
    "T_BOLHA": R(T_BOLHA), "D_BOLHA": R(TOTAL - T_BOLHA), "TUSA": R(T_USA),
    "T_O2B": R(T_O2 + 0.3), "DE1": R(T_TOCA0 - (T_O2 + 0.3) - 0.003),
    "TTOCA": R(T_TOCA0), "TTOCA1": R(T_TOCA0 + 0.08), "TTOCA2": R(T_TOCA0 + 0.24),
    "DE2": R(TOTAL - (T_TOCA0 + 0.24)), "DTOCA": R(TOTAL - T_TOCA0),
    "TPULSO": R(TPULSO), "REP": str(REP), "TONDA2": R(T_TOCA0 + 0.95),
    "V1": R(VOZ["intro"]), "V2": R(VOZ["apresentacao"]), "V3": R(VOZ["cta"]),
    "DV1": R(DV["intro"]), "DV2": R(DV["apresentacao"]), "DV3": R(DV["cta"]),
    "SWH": R(T_N - 0.22), "STIQ1": R(T_CINCO - 0.14), "STIQ2": R(T_QUATRO - 0.14),
    "SSUB": R(T_BOLHA - 0.5),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
assert TP3 + 0.62 < THERO and THERO + 0.6 < T_OUT2, (TP3, THERO, T_OUT2)
assert T_T2OUT + 0.2 < T_BOLHA + 0.1
assert VOZ["intro"] + DV["intro"] <= VOZ["apresentacao"] and VOZ["apresentacao"] + DV["apresentacao"] <= VOZ["cta"]
assert VOZ["cta"] + DV["cta"] <= TOTAL
open(OUT, "w").write(html)
print("ok", OUT, "| cortes M", T_M, "O1", T_O1, "N", T_N, "O2", T_O2, "fim", TOTAL,
      "| cinco", T_CINCO, "quatro", T_QUATRO, "tipo", T_TIPO, "botão", T_BOTAO, "| bolha", T_BOLHA, "toca", T_TOCA0,
      "rep", REP, "| t2 sai", T_T2OUT)
