#!/usr/bin/env python3
"""Gera produtos/facas/edicao_B/index.html ("aço frio": azul-noite / azul-gelo, Bricolage Grotesque,
legenda karaokê com contorno). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra número 1 desta edição (3ª violação, quadro estático): o vídeo de fundo roda do primeiro ao último
quadro. Não há <img>, quadro congelado nem cartão; só trechos com movimento da analise_B.md:
  D 0,25-5,35 s em 1,0x | E 0,10-4,51 s em 0,7x | F 0-6,93 s em 0,9x
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 5.1, 0.3), "apresentacao": (5.1, 11.4, 5.3), "cta": (11.4, 19.1, 11.75)}
TOTAL = 19.1
DUR_MP3 = {"intro": 4.68, "apresentacao": 6.09, "cta": 6.93}
TOPO_LEG = {"intro": 1268, "apresentacao": 1268, "cta": 1296}

# CTA: o clipe F tem um cepo de facas desfocado em x 69-100 %, y 20-40 % do quadro original.
# O vídeo fica em escala >= 1,24 ancorada em (20 %, 100 %); a faixa sólida até 572 px cobre até
# y = 43,4 % do quadro original em qualquer escala >= 1,24 (escala maior empurra o cepo para cima).
FAIXA_H = 572

GRUPOS = {
    "intro": [[0, 1, 2], [3, 4], [5, 6], [7, 8], [9], [10, 11, 12]],
    "apresentacao": [[0, 1, 2], [3, 4, 5], [6], [7, 8, 9], [10], [11, 12]],
    "cta": [[0, 1], [2], [3, 4], [5, 6], [7, 8], [9], [10, 11, 12], [13, 14], [15, 16]],
}
CHAVE = {
    "intro": {6, 8, 11, 12},
    "apresentacao": {2, 5, 6, 9, 10, 12},
    "cta": {2, 4, 6, 9, 10, 12, 16},
}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---- legenda karaokê: o grupo entra apagado e cada palavra acende no seu tempo ----
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = P[parte][2]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.05, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.05, 3), fim_voz)
        else:
            e = min(fim_voz, P[parte][1])
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = max(s + 0.02, round(voz + pal[wi]["inicio"] - 0.02, 3))
            chave = wi in CHAVE[parte]
            spans += f'<span id="{gid}-{k}" class="pal">{pal[wi]["palavra"]}</span>'
            cor = "#4FC3F7" if chave else "#FFFFFF"
            leg_js.append(f'tl.to("#{gid}-{k}",{{color:"{cor}",duration:0.07,ease:"none"}},{t});')
            if chave:
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{scale:1}},{{scale:1.08,duration:0.09,yoyo:true,repeat:1,ease:"power2.out"}},{t});')
        leg_js.append(f'tl.fromTo("#{gid}-c",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.1,ease:"power2.out"}},{s});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{TOPO_LEG[parte]}px">{spans}</div></div>'
        )

# ---- apresentação: contador de 6 marcas (uma por peça citada) e moldura de foco ----
T_PECA = [t_pal("apresentacao", i) for i in (0, 3, 6, 7, 10, 12)]  # chefe, carne, cutelo, descascar, tesoura, descascador
pips_html = "".join(f'<b id="pp{i}"><i id="pp{i}-i"></i></b>' for i in range(6))
pips_js = "\n".join(
    f'tl.fromTo("#pp{i}-i",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.2,ease:"power3.out"}},{R(t - 0.02)});'
    for i, t in enumerate(T_PECA))
# Molduras de foco, em coordenadas do clipe E (1080x1920), medidas nos quadros (ver escolhas.md).
# Só nas 4 peças inconfundíveis; faca do chefe e faca de carne não recebem moldura.
# (id, entra, sai, left, top, width, height, deslocamento em x enquanto a peça ainda desliza, duração do deslocamento)
# tempo do clipe = 0,10 + (tempo do vídeo - 5,1) * 0,7
FOCOS = [
    ("fc", 7.36, 8.2, -12, 400, 276, 1100, 37, 0.84),     # cutelo: clipe 1,68 -> 2,27 s (ainda deslizando)
    ("fd", 8.12, 9.55, 684, 632, 146, 888, 0, 0),         # faca de descascar: clipe 2,21 -> 3,22 s
    ("ft", 9.47, 10.31, 815, 422, 249, 624, 0, 0),        # tesoura: clipe 3,16 -> 3,75 s
    ("fp", 10.23, 11.14, 855, 1048, 222, 516, -29, 0.72), # descascador: clipe 3,69 -> 4,33 s (para aos 4,2 s)
]
foco_html = "".join(
    f'<i id="{i}" class="fq" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px"></i>' for i, _, _, l, t, w, h, _, _ in FOCOS)
foco_js = "\n".join(
    f'tl.fromTo("#{i}",{{opacity:0,scale:1.07}},{{opacity:1,scale:1,duration:0.18,ease:"power2.out"}},{a});\n'
    + (f'tl.to("#{i}",{{x:{dx},duration:{dd},ease:"none"}},{a});\n' if dx else "")
    + f'tl.to("#{i}",{{opacity:0,duration:0.18,ease:"power2.in"}},{R(z - 0.18)});'
    for i, a, z, _, _, _, _, dx, dd in FOCOS)
FOCO0, FOCO1 = FOCOS[0][1] - 0.02, FOCOS[-1][2] + 0.02

T_FAQ = t_pal("intro", 8)      # "faqueiro"
T_SEIS = t_pal("intro", 11)    # "seis"
T_OND = t_pal("cta", 4)        # "ondulações"
T_DUR = t_pal("cta", 9)        # "durabilidade"
T_TOCA = t_pal("cta", 10)      # "Toca"
T_CONF = t_pal("cta", 14)      # "confere"

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* O local("Bricolage Grotesque") do fontes.css não carrega no Chromium; o nome completo da fonte variável carrega. */
@font-face{font-family:"Bricolage Display";font-weight:200 800;src:local("Bricolage Grotesque 96pt ExtraBold")}
:root{--base:#0E1B2C;--gelo:#4FC3F7;--texto:#FFFFFF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0E1B2C}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0E1B2C;font-family:"Bricolage Display"}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camD{transform-origin:50% 28%}
#camE{transform-origin:50% 50%}
#camF{transform-origin:20% 100%}
/* moldura de foco: acompanha a peça citada, dentro do enquadramento do clipe E */
#foco{z-index:2}
.fq{position:absolute;display:block;border:5px solid var(--gelo);border-radius:26px;opacity:0;
  box-shadow:0 0 0 2600px rgba(6,12,22,.3),0 0 30px rgba(79,195,247,.6),inset 0 0 26px rgba(79,195,247,.2)}
.vinheta{z-index:3;background:radial-gradient(ellipse 92% 66% at 50% 50%,rgba(0,0,0,0) 62%,rgba(6,12,22,.42) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(14,27,44,.6) 0,rgba(14,27,44,.32) 11%,rgba(14,27,44,0) 23%)}
/* faixa do título na CTA: sólida até %%FAIXA_H%% px, cobre o canto superior direito do clipe F */
#faixa{z-index:5}
#faixa-b{position:absolute;left:0;top:0;width:1080px;height:%%FAIXA_H%%px;display:block;background-color:#0E1B2C;
  background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.035) 0,rgba(255,255,255,.035) 2px,rgba(255,255,255,0) 2px,rgba(255,255,255,0) 28px),
  repeating-linear-gradient(-45deg,rgba(255,255,255,.035) 0,rgba(255,255,255,.035) 2px,rgba(255,255,255,0) 2px,rgba(255,255,255,0) 28px)}
#faixa-l{position:absolute;left:0;bottom:0;width:1080px;height:5px;display:block;
  background:linear-gradient(to right,rgba(79,195,247,0) 0,#4FC3F7 18%,#DDF4FF 50%,#4FC3F7 82%,rgba(79,195,247,0) 100%)}
#faixa-s{position:absolute;left:0;top:%%FAIXA_H%%px;width:1080px;height:46px;display:block;
  background:linear-gradient(to bottom,rgba(14,27,44,.5) 0,rgba(14,27,44,0) 100%)}
/* títulos: Bricolage 800, centralizados na área segura (62-918 px) */
.titulo{z-index:6}
#t3{z-index:4}
.tl{display:block;font-weight:800;color:var(--texto);line-height:1.2;white-space:nowrap;text-align:center;letter-spacing:-.5px;
  text-shadow:0 5px 0 rgba(6,12,22,.6),0 12px 30px rgba(0,0,0,.6)}
.tl.gelo{color:var(--gelo)}
.tl.brilha{text-shadow:none;color:transparent;-webkit-text-fill-color:transparent;-webkit-background-clip:text;background-clip:text;
  background-image:linear-gradient(100deg,#4FC3F7 0%,#4FC3F7 44%,#FFFFFF 50%,#4FC3F7 56%,#4FC3F7 100%);background-size:300% 100%;background-position:0% 0%}
.abs{position:absolute;left:62px;width:856px}
.mask{position:absolute;left:62px;width:856px;overflow:hidden;display:block}
.sub{position:absolute;left:62px;width:856px;display:block;text-align:center;font-weight:600;color:rgba(255,255,255,.9);line-height:1.2;white-space:nowrap;
  text-shadow:0 2px 10px rgba(0,0,0,.8)}
/* etiqueta da intro, à esquerda da faca que sobe */
.lab{position:absolute;left:56px;width:400px;overflow:hidden;display:block}
.lab .tl{text-align:left}
#t2-r{position:absolute;left:56px;top:376px;width:150px;height:7px;border-radius:4px;display:block;background:var(--gelo);
  box-shadow:0 0 16px rgba(79,195,247,.7)}
#t2-6{display:inline-block}
/* contador de peças */
.pips{position:absolute;left:62px;top:318px;width:856px;display:flex;justify-content:center;gap:14px}
.pips b{display:block;width:116px;height:12px;border-radius:3px;overflow:hidden;background:rgba(255,255,255,.26);transform:skewX(-22deg);
  box-shadow:0 2px 8px rgba(0,0,0,.5)}
.pips i{display:block;width:100%;height:100%;background:linear-gradient(to right,#4FC3F7,#BFEAFF)}
/* legenda karaokê com contorno */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start;gap:24px;flex-wrap:nowrap}
.pal{display:block;font-weight:700;font-size:80px;line-height:1.1;color:#93A6BA;white-space:nowrap;
  -webkit-text-stroke:11px #0E1B2C;paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.55)}
.rodape{z-index:7}
.rodape span{position:absolute;left:62px;width:856px;top:1466px;display:block;text-align:center;font-weight:600;font-size:30px;line-height:1;
  letter-spacing:.4px;color:rgba(255,255,255,.8);text-shadow:0 0 6px rgba(0,0,0,.95),0 2px 12px rgba(0,0,0,.9)}
/* CTA: selo com seta para baixo/esquerda */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1394px;width:112px;height:112px;display:block;border-radius:50%;background:var(--gelo);
  box-shadow:0 0 0 5px rgba(14,27,44,.9),0 0 40px rgba(79,195,247,.6),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:112px;height:112px}
#tq-o{position:absolute;left:56px;top:1394px;width:112px;height:112px;display:block;border:6px solid var(--gelo);border-radius:50%;opacity:0}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: clipe D 0,25-5,35 s em 1,0x (tampa sobe até 2 s; faca do chefe sobe 2,5-5 s do clipe) -->
  <div id="camD" class="cam"><video id="vD" class="clip full" data-start="0" data-duration="5.1" data-media-start="0.25" data-track-index="0" src="assets/clipe_D.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: clipe E 0,10-4,51 s em 0,7x (as peças entram deslizando) -->
  <div id="camE" class="cam">
    <video id="vE" class="clip full" data-start="5.1" data-duration="6.3" data-media-start="0.1" data-playback-rate="0.7" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video>
    <div id="foco" class="clip" data-start="%%FOCO0%%" data-duration="%%FOCOD%%" data-track-index="1">%%FOCO_HTML%%</div>
  </div>
  <!-- CTA: clipe F 0-6,93 s em 0,9x (mão fatiando o tomate), escala >= 1,24 ancorada embaixo -->
  <div id="camF" class="cam"><video id="vF" class="clip full" data-start="11.4" data-duration="7.7" data-media-start="0" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>

  <div id="vin" class="clip vinheta" data-start="0" data-duration="11.4" data-track-index="2"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="11.4" data-track-index="3"></div>
  <div id="faixa" class="clip" data-start="11.1" data-duration="8.0" data-track-index="4"><div id="faixa-b"><i id="faixa-l"></i><i id="faixa-s"></i></div></div>

  <!-- títulos -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="1.4" data-track-index="6">
    <div id="t1-g" class="abs" style="top:196px">
      <div id="t1-l0" class="tl" style="font-size:176px;line-height:.98">OLHA O</div>
      <div id="t1-l1" class="tl gelo" style="font-size:176px;line-height:.98">QUE VEM</div>
    </div>
  </div>
  <div id="t2" class="clip titulo" data-start="2.2" data-duration="2.9" data-track-index="6">
    <div class="lab" style="top:196px;height:62px"><div id="t2-l0" class="tl" style="font-size:50px">FAQUEIRO DE</div></div>
    <div class="lab" style="top:254px;height:112px"><div id="t2-l1" class="tl gelo" style="font-size:92px"><b id="t2-6">6</b> PEÇAS</div></div>
    <i id="t2-r"></i>
  </div>
  <div id="t3" class="clip titulo" data-start="5.1" data-duration="6.3" data-track-index="6">
    <div class="mask" style="top:190px;height:116px"><div id="t3-l0" class="tl" style="font-size:96px"><span style="color:#4FC3F7">6</span> PEÇAS NO KIT</div></div>
    <div id="t3-p" class="pips">%%PIPS%%</div>
    <span id="t3-s" class="sub" style="top:342px;font-size:36px">4 facas, tesoura e descascador</span>
  </div>
  <div id="t4" class="clip titulo" data-start="11.4" data-duration="4.92" data-track-index="6">
    <div class="mask" style="top:182px;height:168px"><div id="t4-l0" class="tl" style="font-size:140px">LÂMINA</div></div>
    <div class="mask" style="top:314px;height:168px"><div id="t4-l1" class="tl brilha" style="font-size:140px">ONDULADA</div></div>
    <span id="t4-s" class="sub" style="top:482px;font-size:46px">mais durabilidade*</span>
  </div>
  <div id="t5" class="clip titulo" data-start="16.32" data-duration="2.78" data-track-index="6">
    <div class="mask" style="top:182px;height:168px"><div id="t5-l0" class="tl" style="font-size:140px">TOCA NO</div></div>
    <div class="mask" style="top:314px;height:168px"><div id="t5-l1" class="tl brilha" style="font-size:140px">PRODUTO</div></div>
    <span id="t5-s" class="sub" style="top:482px;font-size:46px">e confere o seu</span>
  </div>
  <div id="rodape" class="clip rodape" data-start="11.4" data-duration="7.7" data-track-index="7"><span id="rodape-s">*Dados do fabricante</span></div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="8">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 112 112"><path d="M76 36 L38 74 M36 46 L36 76 L66 76" fill="none" stroke="#0E1B2C" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.3" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="5.3" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="11.75" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-0" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-pop-1" data-start="2.2" data-duration="0.09" data-track-index="14" data-volume="0.35" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="5.0" data-duration="0.3" data-track-index="14" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="14" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="11.0" data-duration="0.39" data-media-start="1.0" data-track-index="14" data-volume="0.36" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-brilho-1" data-start="13.02" data-duration="0.9" data-track-index="14" data-volume="0.26" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO: caixa com o kit no quadro 0, punch-in, título batendo sobre a tampa; o título sobe junto com a tampa ----
tl.fromTo("#camD", {scale:1.14}, {scale:1, duration:0.45, ease:"power3.out"}, 0);
tl.to("#camD", {scale:1.045, duration:3.2, ease:"none"}, 0.45);
tl.to("#camD", {scale:1.085, duration:0.3, ease:"power2.out"}, %%TSEIS0%%);
tl.to("#camD", {scale:1.1, duration:%%DSEIS%%, ease:"none"}, %%TSEIS1%%);
tl.fromTo("#t1-g", {scale:1.2, transformOrigin:"50% 100%"}, {scale:1, duration:0.32, ease:"back.out(1.9)"}, 0);
tl.to("#t1-g", {y:-330, opacity:0, duration:0.5, ease:"power2.in"}, 0.8);
tl.fromTo("#t2-l0", {yPercent:110}, {yPercent:0, duration:0.26, ease:"power3.out"}, 2.24);
tl.fromTo("#t2-l1", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, 2.3);
tl.fromTo("#t2-r", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.3, ease:"power3.out"}, 2.38);
tl.fromTo("#t2-6", {scale:1, transformOrigin:"50% 60%"}, {scale:1.32, duration:0.14, yoyo:true, repeat:1, ease:"power2.out"}, %%TSEIS%%);
tl.to("#t2-l0", {yPercent:-110, duration:0.16, ease:"power2.in"}, 4.9);
tl.to("#t2-l1", {yPercent:-110, duration:0.16, ease:"power2.in"}, 4.92);
tl.to("#t2-r", {scaleX:0, transformOrigin:"100% 50%", duration:0.16, ease:"power2.in"}, 4.9);

// ---- APRESENTAÇÃO: corte seco + punch; contador de 6 marcas no tempo da fala; moldura de foco nas peças inconfundíveis ----
tl.fromTo("#camE", {scale:1.07}, {scale:1, duration:0.4, ease:"power3.out"}, 5.1);
tl.to("#camE", {scale:1.03, duration:5.9, ease:"none"}, 5.5);
tl.fromTo("#t3-l0", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, 5.13);
tl.fromTo("#t3-p", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.2, ease:"power2.out"}, 5.2);
tl.fromTo("#t3-s", {opacity:0, y:-12}, {opacity:1, y:0, duration:0.22, ease:"power2.out"}, 5.62);
%%PIPS_JS%%
%%FOCO_JS%%

// passagem: a faixa do título desce antes do corte e já está inteira no primeiro quadro do clipe F
tl.fromTo("#faixa-b", {yPercent:-112}, {yPercent:0, duration:0.24, ease:"power3.inOut"}, 11.14);

// ---- CTA: mão fatiando o tomate; a escala nunca fica abaixo de 1,24 (cobertura do canto superior direito) ----
tl.fromTo("#camF", {scale:1.27}, {scale:1.24, duration:0.5, ease:"power2.out"}, 11.4);
tl.to("#camF", {scale:1.255, duration:%%DOND%%, ease:"none"}, 11.9);
tl.to("#camF", {scale:1.285, duration:0.3, ease:"power3.out"}, %%TOND%%);
tl.to("#camF", {scale:1.305, duration:%%DFIM%%, ease:"none"}, %%TOND1%%);
// o rodapé "*Dados do fabricante" não tem animação: fica visível do primeiro ao último quadro da CTA
tl.fromTo("#t4-l0", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, 11.46);
tl.fromTo("#t4-l1", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, 11.54);
tl.fromTo("#t4-l1", {backgroundPosition:"0% 0%"}, {backgroundPosition:"100% 0%", duration:0.7, ease:"power1.inOut", immediateRender:false}, 13.08);
tl.fromTo("#t4-s", {opacity:0, y:-14}, {opacity:1, y:0, duration:0.22, ease:"power2.out"}, %%TDUR%%);
tl.to("#t4-l0", {yPercent:-110, duration:0.16, ease:"power2.in"}, 16.12);
tl.to("#t4-l1", {yPercent:-110, duration:0.16, ease:"power2.in"}, 16.15);
tl.to("#t4-s", {opacity:0, duration:0.14}, 16.12);
tl.fromTo("#t5-l0", {yPercent:110}, {yPercent:0, duration:0.26, ease:"power3.out"}, %%TTOCA%%);
tl.fromTo("#t5-l1", {yPercent:110}, {yPercent:0, duration:0.26, ease:"power3.out"}, %%TTOCA1%%);
tl.fromTo("#t5-l1", {backgroundPosition:"0% 0%"}, {backgroundPosition:"100% 0%", duration:0.7, ease:"power1.inOut", immediateRender:false}, %%TPROD%%);
tl.fromTo("#t5-s", {opacity:0, y:-14}, {opacity:1, y:0, duration:0.22, ease:"power2.out"}, %%TCONF%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:2.1, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA%%);
tl.fromTo("#tq-s", {x:0, y:0}, {x:-7, y:7, duration:0.22, yoyo:true, repeat:9, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:2.1, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:2.1, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA3%%);

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

subs = {
    "TOTAL": str(TOTAL), "FAIXA_H": str(FAIXA_H),
    "FOCO_HTML": foco_html, "FOCO0": R(FOCO0), "FOCOD": R(FOCO1 - FOCO0),
    "FOCO_JS": foco_js, "PIPS": pips_html, "PIPS_JS": pips_js,
    "DV1": str(DUR_MP3["intro"]), "DV2": str(DUR_MP3["apresentacao"]), "DV3": str(DUR_MP3["cta"]),
    "STIQ1": R(T_PECA[2] - 0.08), "STIQ2": R(T_PECA[4] - 0.09),
    "TSEIS": R(T_SEIS), "TSEIS0": R(T_SEIS - 0.03), "TSEIS1": R(T_SEIS + 0.29), "DSEIS": R(5.1 - (T_SEIS + 0.29)),
    "TOND": R(T_OND), "DOND": R(T_OND - 11.9), "TOND1": R(T_OND + 0.32), "DFIM": R(TOTAL - (T_OND + 0.32)),
    "TDUR": R(T_DUR - 0.03),
    "TTOCA": R(T_TOCA - 0.02), "TTOCA1": R(T_TOCA + 0.05), "DTOCA": R(TOTAL - (T_TOCA - 0.02)),
    "TPROD": R(t_pal("cta", 12) - 0.05), "TCONF": R(T_CONF - 0.05),
    "TPULSO": R(T_TOCA + 0.3), "TONDA2": R(T_TOCA + 0.95), "TONDA3": R(T_TOCA + 1.85),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
open(OUT, "w").write(html)
print("ok", OUT)
