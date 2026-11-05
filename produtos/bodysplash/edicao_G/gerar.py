#!/usr/bin/env python3
"""Gera produtos/bodysplash/edicao_G/index.html ("alfaiataria": azul-marinho risca-de-giz / giz / vermelho-gravata,
DM Serif Display + Poppins 800, legenda karaokê em etiqueta costurada). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida>

Lote G ("O último passo da produção"), rotação sem clipe novo. Regra da 3ª violação: o vídeo roda do primeiro ao
último quadro; não há <img>, quadro congelado nem cartão. Trechos (roteiro_G, analise_E/F):
  intro         A 5,55-7,97 s em 0,82x  (frascos sobem entre a fumaça; antes de 5,5 s é proibido)
                G 0,00-0,80 s em 0,8x   (vapor do banho, a mão entra em "falta o quê?")
  apresentação  G 0,80-5,52 s em 0,8x   (dedo aperta a válvula do Enigma -> nuvem de vapor)
                H 0,00-1,79 s em 0,85x  (mão desce até a válvula do Barbarius; PROIBIDO H 2,1-4,9 s)
                H 5,30-7,90 s em 1,0x   (mão já saiu, cortina; 5,0-5,2 ainda tem resto do trecho proibido)
  CTA           I 2,60-6,87 s em 1,0x   (dedos pousam na tampa do Midtown em "toque")
Texto só acima das tampas (y < 545): rótulos (y ~890-1600) nunca ficam sob texto nem sob efeito translúcido.
Transições: painel risca-de-giz opaco de bordas duras (G->H) e lapelas opacas que fecham e abrem (H->I).
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

VOZ = {"intro": 0.15, "apresentacao": 4.25, "cta": 14.8}
DUR_MP3 = {"intro": 3.888, "apresentacao": 10.272, "cta": 3.912}
FIM_FALA = {p: VOZ[p] + falas[p]["palavras"][-1]["fim"] for p in VOZ}
P_FIM = {"intro": 4.05, "apresentacao": 14.55, "cta": round(FIM_FALA["cta"] + 0.45, 2)}
TOTAL = P_FIM["cta"]
T_AG, T_GH, T_HH, T_HI = 2.95, 9.85, 11.95, 14.55      # cortes
VALV = (243, 715)                                       # válvula do Enigma no G (origem do zoom herói)
LEG_TOP = 444

GRUPOS = {
    "intro": [[0, 1], [2, 3], [4, 5], [6, 7, 8]],
    "apresentacao": [[0, 1, 2], [3, 4], [5, 6], [7], [8, 9], [10, 11, 12], [13], [14, 15], [16, 17], [18],
                     [19, 20, 21], [22, 23], [24, 25]],
    "cta": [[0, 1], [2, 3], [4, 5], [6], [7, 8], [9, 10], [11, 12]],
}
CHAVE = {"intro": {6, 8}, "apresentacao": {1, 2, 6, 7, 13, 15, 18, 19, 23}, "cta": {3, 4, 6, 12}}
EXIBE = {("intro", 1): "escolhida,", ("intro", 3): "feita.", ("intro", 5): "aí,", ("intro", 8): "quê?",
         ("apresentacao", 2): "Man,", ("apresentacao", 4): "Primacial:", ("apresentacao", 9): "produção.",
         ("apresentacao", 12): "banho,", ("apresentacao", 13): "borrifou,", ("apresentacao", 18): "ocasião.",
         ("apresentacao", 21): "kit,", ("apresentacao", 25): "dia.",
         ("cta", 3): "visual,", ("cta", 12): "kit."}


def T(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


def TF(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["fim"], 3)


# ---------- legenda karaokê em etiqueta costurada ----------
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = VOZ[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.06, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.06, 3), fim_voz)
        else:
            e = min(fim_voz, P_FIM[parte] - 0.12)
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = round(voz + pal[wi]["inicio"] - 0.02, 3)
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            if wi in CHAVE[parte]:
                spans += (f'<span id="{gid}-{k}" class="pal k"><em class="tx">{txt}</em>'
                          f'<i id="{gid}-{k}u" class="ul"></i></span>')
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.36,color:"#EEE8DA",scale:1}},'
                              f'{{opacity:1,color:"#F04457",scale:1.08,duration:0.1,ease:"power2.out"}},{t});')
                leg_js.append(f'tl.fromTo("#{gid}-{k}u",{{scaleX:0}},{{scaleX:1,duration:0.18,ease:"power2.out"}},{t});')
            else:
                spans += f'<span id="{gid}-{k}" class="pal"><em class="tx">{txt}</em></span>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.36}},{{opacity:1,duration:0.08,ease:"none"}},{t});')
        leg_js.append(f'tl.fromTo("#{gid}-t",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{s});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
                        f'data-track-index="12"><div id="{gid}-t" class="cap" style="top:{LEG_TOP}px">'
                        f'<i class="cst"></i>{spans}</div></div>')

# ---------- tempos-chave ----------
t_escolhida, t_feita = TF("intro", 1), TF("intro", 3)
t_falta = T("intro", 6)
t_o_ult, t_ultimo = T("apresentacao", 5), T("apresentacao", 6)
t_saiu, t_borrifou = T("apresentacao", 10), T("apresentacao", 13)
t_pronto, t_ocasiao = T("apresentacao", 15), T("apresentacao", 18)
t_tres, t_kitf, t_variar, t_dia, t_diaf = (T("apresentacao", 19), TF("apresentacao", 21), T("apresentacao", 23),
                                           T("apresentacao", 25), TF("apresentacao", 25))
t_visual, t_toque, t_produto, t_confira, t_kit_fim = (T("cta", 3), T("cta", 4), T("cta", 6), T("cta", 10),
                                                      TF("cta", 12))

VX, VY = VALV
html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
:root{--marinho:#0F1B30;--giz:#EEE8DA;--gravata:#D3263A;--gravata-claro:#F04457}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0F1B30}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0F1B30;font-family:"Poppins";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camA{transform-origin:50% 0%}
#camG{transform-origin:%%VX%%px %%VY%%px}
#camH1,#camH2{transform-origin:50% 0%}
#camI{transform-origin:9% 50%}
/* tecido risca-de-giz */
.risca{background-color:var(--marinho);
  background-image:repeating-linear-gradient(90deg,rgba(238,232,218,.085) 0 2px,transparent 2px 18px)}
/* títulos: faixas de etiqueta costurada, uma por linha */
.titulo{z-index:6}
.ln{position:absolute;left:44px;display:flex;align-items:flex-start}
.band{position:relative;display:flex;align-items:center;gap:22px;padding:4px 34px 8px 46px;box-shadow:0 8px 22px rgba(6,10,20,.35)}
.band .tab{position:absolute;left:0;top:0;bottom:0;width:18px;display:block;
  background:repeating-linear-gradient(135deg,var(--gravata) 0 10px,#F2E9DA 10px 13px,var(--gravata) 13px 22px)}
.band .st{position:absolute;left:28px;right:10px;top:7px;bottom:7px;display:block;
  border-top:3px dashed rgba(238,232,218,.55);border-bottom:3px dashed rgba(238,232,218,.55)}
.tt{display:block;font-family:"DM Serif Display";font-size:96px;line-height:1;white-space:nowrap;color:var(--giz);letter-spacing:1px}
.tt .s{color:var(--gravata-claro)}
.mask{overflow:hidden}
/* linha de apoio (etiqueta fina) */
.lin{position:absolute;left:44px;top:392px;display:flex}
.lin .band{padding:4px 26px 6px 40px;gap:16px}
.lin .band .tab{width:12px}
.lt{display:block;font-family:"Poppins";font-weight:700;font-size:32px;line-height:1.1;white-space:nowrap;color:var(--giz)}
.lt .s{color:var(--gravata-claro)}
/* caixinha de checklist (giz) com visto vermelho */
.cx{position:relative;flex:0 0 auto;display:block;width:34px;height:34px;border:3px solid rgba(238,232,218,.85);border-radius:4px}
.cx svg{position:absolute;left:-4px;top:-14px;width:50px;height:50px;display:block}
.cx.g{width:62px;height:62px;border-width:5px;border-radius:6px}
.cx.g svg{left:-8px;top:-28px;width:92px;height:92px}
/* transição 1: painel risca-de-giz opaco */
.wipe{z-index:18;overflow:hidden}
#wp1{position:absolute;left:0;top:0;width:1140px;height:1920px;display:block;border-right:16px solid var(--gravata)}
#wp1 i{position:absolute;right:14px;top:0;width:0;height:1920px;display:block;border-right:4px dashed rgba(238,232,218,.7)}
/* transição 2: lapelas */
.lap{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block}
/* brilho nas tampas (faixa acima dos rótulos) */
.brilho{z-index:3}
.br-m{position:absolute;left:0;width:1080px;overflow:hidden;display:block;
  -webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 18%,#000 72%,transparent 100%);mask-image:linear-gradient(to bottom,transparent 0,#000 18%,#000 72%,transparent 100%)}
.br-b{position:absolute;left:0;top:-300px;width:240px;height:1100px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.85) 50%,rgba(255,255,255,0) 100%)}
/* CTA: seta pespontada (fita vermelha + costura de giz) na margem esquerda, ponta para o produto marcado */
#seta{z-index:8}
#gv{position:absolute;left:8px;top:600px;width:80px;height:912px;display:block}
#gv-o{position:absolute;left:-18px;top:1446px;width:80px;height:80px;display:block;border:5px solid var(--gravata-claro);border-radius:50%;opacity:0;
  box-shadow:0 0 0 3px rgba(238,232,218,.7)}
/* legenda karaokê em etiqueta costurada */
.legenda{z-index:9}
.cap{position:absolute;left:44px;display:flex;align-items:flex-start;gap:20px;flex-wrap:nowrap;padding:6px 28px 12px 30px;
  background-color:var(--marinho);background-image:repeating-linear-gradient(90deg,rgba(238,232,218,.085) 0 2px,transparent 2px 18px);
  box-shadow:0 8px 22px rgba(6,10,20,.35)}
.cap .cst{position:absolute;left:8px;right:8px;top:7px;bottom:7px;display:block;border:3px dashed rgba(238,232,218,.4);border-radius:4px}
.pal{position:relative;display:block;font-family:"Poppins";font-weight:800;font-size:76px;line-height:1.06;white-space:nowrap;color:var(--giz);transform-origin:50% 60%}
.tx{display:block;font-style:normal}
.ul{position:absolute;left:2px;right:2px;bottom:4px;height:0;display:block;border-bottom:5px dashed var(--gravata-claro);transform-origin:0 50%}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO 0-2,95: A 5,55-7,97 (0,82x); antes de 5,5 s é proibido -->
  <div id="camA" class="cam"><video id="vA" class="clip full" data-start="0" data-duration="%%TAG%%" data-media-start="5.55" data-playback-rate="0.82" data-track-index="0" src="assets/clipe_A.mp4" muted playsinline></video></div>
  <!-- 2,95-9,85: G 0-5,52 (0,8x), um plano contínuo: vapor -> dedo na válvula -> nuvem de vapor -->
  <div id="camG" class="cam"><video id="vG" class="clip full" data-start="%%TAG%%" data-duration="%%DG%%" data-media-start="0" data-playback-rate="0.8" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <!-- 9,85-11,95: H 0-1,79 (0,85x). H 2,1-4,9 nunca entra. -->
  <div id="camH1" class="cam"><video id="vH1" class="clip full" data-start="%%TGH%%" data-duration="%%DH1%%" data-media-start="0" data-playback-rate="0.85" data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video></div>
  <!-- 11,95-14,55: H 5,3-7,9 (1x), cortina; antes de 5,3 o preto do Enigma ainda está acinzentado -->
  <div id="camH2" class="cam"><video id="vH2" class="clip full" data-start="%%THH%%" data-duration="%%DH2%%" data-media-start="5.3" data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video></div>
  <!-- CTA 14,55-fim: I 2,6-6,87 (1x) -->
  <div id="camI" class="cam"><video id="vI" class="clip full" data-start="%%THI%%" data-duration="%%DI%%" data-media-start="2.6" data-track-index="0" src="assets/clipe_I.mp4" muted playsinline></video></div>

  <!-- produto herói no H2: brilho só na faixa das tampas (y 560-930; rótulos começam em ~950) -->
  <div id="brilho1" class="clip brilho" data-start="%%TBR%%" data-duration="0.85" data-track-index="3"><span class="br-m" style="top:560px;height:370px"><i id="br1" class="br-b"></i></span></div>

  <!-- INTRO: FALTA / O QUÊ? + checklist -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="3.95" data-track-index="6">
    <div class="ln" style="top:168px"><div id="t1-a" class="band risca"><i class="tab"></i><i class="st"></i><span class="tt">FALTA</span></div></div>
    <div class="ln" style="top:280px"><div id="t1-b" class="band risca"><i class="tab"></i><i class="st"></i><span class="tt">O <span class="s">QUÊ?</span></span></div></div>
    <div id="t1-l" class="lin"><div class="band risca"><i class="tab"></i>
      <span class="cx"><svg viewBox="0 0 50 50"><path id="ck1" d="M8 26 L20 38 L44 8" fill="none" stroke="#F04457" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="lt">roupa escolhida</span>
      <span class="cx"><svg viewBox="0 0 50 50"><path id="ck2" d="M8 26 L20 38 L44 8" fill="none" stroke="#F04457" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="lt">barba feita</span>
    </div></div>
  </div>

  <!-- APRESENTAÇÃO: O ÚLTIMO / PASSO (entra em "o último") + linha em "pronto" -->
  <div id="t2" class="clip titulo" data-start="%%TT2%%" data-duration="%%DT2%%" data-track-index="7">
    <div class="ln mask" style="top:168px"><div id="t2-a" class="band risca"><i class="tab"></i><i class="st"></i><span class="tt">O ÚLTIMO</span></div></div>
    <div class="ln mask" style="top:280px"><div id="t2-b" class="band risca"><i class="tab"></i><i class="st"></i><span class="tt"><span class="s">PASSO</span></span></div></div>
    <div id="t2-l" class="lin"><div class="band risca"><i class="tab"></i><span class="lt">pronto pra <span class="s">qualquer ocasião</span></span></div></div>
  </div>

  <!-- CTA: FECHE O / VISUAL + caixinha que ganha o visto no fim; linha em "toque" -->
  <div id="t3" class="clip titulo" data-start="%%THI%%" data-duration="%%DI%%" data-track-index="8">
    <div class="ln mask" style="top:168px"><div id="t3-a" class="band risca"><i class="tab"></i><i class="st"></i><span class="tt">FECHE O</span></div></div>
    <div class="ln mask" style="top:280px"><div id="t3-b" class="band risca"><i class="tab"></i><i class="st"></i><span class="tt"><span class="s">VISUAL</span></span>
      <span class="cx g"><svg viewBox="0 0 50 50"><path id="ck3" d="M8 26 L20 38 L44 8" fill="none" stroke="#F04457" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg></span></div></div>
    <div id="t3-l" class="lin"><div class="band risca"><i class="tab"></i><span class="lt">toque no <span class="s">produto do vídeo</span></span></div></div>
  </div>
  <div id="seta" class="clip" data-start="%%TTOQ%%" data-duration="%%DGRAV%%" data-track-index="11">
    <svg id="gv" viewBox="0 0 80 912">
      <path d="M44 0 L44 828 L16 884" fill="none" stroke="#0F1B30" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M44 0 L44 828 L16 884" fill="none" stroke="#D3263A" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M44 6 L44 828 L16 884" fill="none" stroke="#EEE8DA" stroke-width="4" stroke-dasharray="14 10" stroke-linecap="round"/>
      <path d="M14 830 L14 886 L70 886" fill="none" stroke="#0F1B30" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M14 830 L14 886 L70 886" fill="none" stroke="#D3263A" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M14 836 L14 886 L64 886" fill="none" stroke="#EEE8DA" stroke-width="4" stroke-dasharray="10 8" stroke-linecap="round"/>
    </svg>
    <i id="gv-o"></i>
  </div>

  <div id="wipe1" class="clip wipe" data-start="%%TW1%%" data-duration="0.32" data-track-index="14"><i id="wp1" class="risca"><i></i></i></div>
  <div id="wipe2" class="clip wipe" data-start="%%TW2%%" data-duration="0.34" data-track-index="15">
    <svg id="lapL" class="lap" viewBox="0 0 1080 1920">
      <defs><pattern id="psL" width="18" height="10" patternUnits="userSpaceOnUse"><rect width="18" height="10" fill="#0F1B30"/><rect width="2" height="10" fill="#26324A"/></pattern></defs>
      <path d="M0 0 L560 0 L640 1920 L0 1920 Z" fill="url(#psL)"/>
      <path d="M560 0 L640 1920" stroke="#D3263A" stroke-width="16"/>
      <path d="M532 0 L612 1920" stroke="#EEE8DA" stroke-opacity="0.6" stroke-width="4" stroke-dasharray="18 12"/>
    </svg>
    <svg id="lapR" class="lap" viewBox="0 0 1080 1920">
      <defs><pattern id="psR" width="18" height="10" patternUnits="userSpaceOnUse"><rect width="18" height="10" fill="#0F1B30"/><rect width="2" height="10" fill="#26324A"/></pattern></defs>
      <path d="M520 0 L1080 0 L1080 1920 L440 1920 Z" fill="url(#psR)"/>
      <path d="M520 0 L440 1920" stroke="#D3263A" stroke-width="16"/>
      <path d="M548 0 L468 1920" stroke="#EEE8DA" stroke-opacity="0.6" stroke-width="4" stroke-dasharray="18 12"/>
    </svg>
  </div>

%%LEG%%

  <audio id="voz-intro" data-start="%%V1%%" data-duration="%%DV1%%" data-track-index="16" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="%%V2%%" data-duration="%%DV2%%" data-track-index="16" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="%%V3%%" data-duration="%%DV3%%" data-track-index="16" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="17" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="%%TAG%%" data-duration="0.3" data-track-index="18" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-2" data-start="%%TWH2%%" data-duration="0.3" data-track-index="18" data-volume="0.26" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-3" data-start="%%TWH3%%" data-duration="0.3" data-track-index="18" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="%%TSUB%%" data-duration="%%DSUB%%" data-media-start="%%MSUB%%" data-track-index="18" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOQ%%" data-duration="0.05" data-track-index="17" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%TPOP%%" data-duration="0.09" data-track-index="17" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });
tl.set(["#ck1", "#ck2", "#ck3"], {attr:{"stroke-dasharray":"60 60", "stroke-dashoffset":60}}, 0);

// ---- INTRO (A): punch 1,6 -> 1,38; frascos sobem na fumaça; título bate ----
tl.fromTo("#camA", {scale:1.6}, {scale:1.38, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camA", {scale:1.12, duration:%%D_A%%, ease:"none"}, 0.4);
tl.fromTo("#t1-a", {scale:1.6, opacity:0.7, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.28, ease:"back.out(1.6)"}, 0);
tl.fromTo("#t1-b", {scale:1.9, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.28, ease:"back.out(1.6)"}, 0.12);
tl.fromTo("#t1-l", {opacity:0, x:-24}, {opacity:1, x:0, duration:0.22, ease:"power3.out"}, 0.3);
tl.to("#ck1", {attr:{"stroke-dashoffset":0}, duration:0.18, ease:"power2.out"}, %%TCK1%%);
tl.to("#ck2", {attr:{"stroke-dashoffset":0}, duration:0.18, ease:"power2.out"}, %%TCK2%%);
// corte seco A -> G (2,95, entre "aí" e "falta"): punch no vapor
tl.fromTo("#camG", {scale:1.14}, {scale:1.02, duration:0.3, ease:"power3.out"}, %%TAG%%);
tl.to("#camG", {scale:1.05, duration:%%D_G1%%, ease:"none"}, %%TAG30%%);
tl.fromTo("#t1-b", {scale:1}, {scale:1.07, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}, %%TFALTA%%);
tl.to(["#t1-a", "#t1-b", "#t1-l"], {x:-1000, opacity:0, duration:0.16, stagger:0.03, ease:"power2.in"}, 3.75);

// ---- APRESENTAÇÃO (G): produto herói = dedo apertando a válvula em "o último passo" ----
tl.to("#camG", {scale:1.24, duration:0.36, ease:"power3.inOut"}, %%TZOOM%%);
tl.to("#camG", {scale:1.28, duration:%%D_G2%%, ease:"none"}, %%TZOOM36%%);
tl.fromTo("#t2-a", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, %%TT2%%);
tl.fromTo("#t2-b", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, %%TT2B%%);
tl.set("#t2-l", {opacity:0}, 0);
// "Saiu do banho": recua para a nuvem de vapor
tl.to("#camG", {scale:1.03, duration:0.4, ease:"power3.inOut"}, %%TSAIU%%);
tl.to("#camG", {scale:1.07, duration:%%D_G3%%, ease:"none"}, %%TSAIU40%%);
tl.to("#camG", {scale:1.1, duration:0.14, ease:"power2.out"}, %%TBORR%%);
tl.to("#camG", {scale:1.12, duration:%%D_G4%%, ease:"none"}, %%TBORR14%%);
// passagem G -> H: painel risca-de-giz opaco da esquerda para a direita (cobre tudo no corte)
tl.fromTo("#wp1", {x:-1160}, {x:-30, duration:0.15, ease:"power2.in"}, %%TW1%%);
tl.to("#wp1", {x:1120, duration:0.16, ease:"power2.out"}, %%TGH%%);

// ---- H1: mão desce até o Barbarius ("pronto pra qualquer ocasião") ----
tl.fromTo("#camH1", {scale:1.12}, {scale:1.06, duration:0.3, ease:"power3.out"}, %%TGH%%);
tl.to("#camH1", {scale:1.09, duration:%%D_H1A%%, ease:"none"}, %%TGH30%%);
tl.to("#camH1", {scale:1.12, duration:0.14, ease:"power2.out"}, %%TOCA%%);
tl.to("#camH1", {scale:1.13, duration:%%D_H1B%%, ease:"none"}, %%TOCA14%%);
tl.fromTo("#t2-l", {opacity:0, x:-24}, {opacity:1, x:0, duration:0.22, ease:"power3.out", immediateRender:false}, %%TPRONTO%%);

// ---- H2: "Três no kit" = os três grandes juntos, brilho só nas tampas ----
tl.fromTo("#camH2", {scale:1.14}, {scale:1.05, duration:0.26, ease:"power3.out"}, %%THH%%);
tl.to("#camH2", {scale:1.08, duration:%%D_H2A%%, ease:"none"}, %%THH26%%);
tl.to("#camH2", {scale:1.1, duration:0.14, ease:"power2.out"}, %%TDIA%%);
tl.to("#camH2", {scale:1.11, duration:%%D_H2B%%, ease:"none"}, %%TDIA14%%);
tl.fromTo("#br1", {x:-420, rotation:16}, {x:1300, rotation:16, duration:0.75, ease:"power1.inOut"}, %%TBR%%);
tl.fromTo("#t2-b", {scale:1}, {scale:1.06, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}, %%TVARIAR%%);
tl.to(["#t2-a", "#t2-b"], {yPercent:-110, opacity:0, duration:0.16, ease:"power2.in"}, %%TOUT2%%);
tl.to("#t2-l", {opacity:0, duration:0.14, ease:"none"}, %%TOUT2%%);
// passagem para a CTA: lapelas fecham (cobrem tudo no corte) e abrem
tl.fromTo("#lapL", {x:-720}, {x:0, duration:0.15, ease:"power2.in"}, %%TW2%%);
tl.fromTo("#lapR", {x:720}, {x:0, duration:0.15, ease:"power2.in"}, %%TW2%%);
tl.to("#lapL", {x:-720, duration:0.18, ease:"power2.out"}, %%THI%%);
tl.to("#lapR", {x:720, duration:0.18, ease:"power2.out"}, %%THI%%);

// ---- CTA (I): mais calma; FECHE O VISUAL no respiro; seta pespontada aponta o produto marcado em "toque" ----
tl.fromTo("#camI", {scale:1.03}, {scale:1.0, duration:0.4, ease:"power2.out"}, %%THI%%);
tl.to("#camI", {scale:1.015, duration:%%D_IA%%, ease:"none"}, %%THI40%%);
tl.to("#camI", {scale:1.03, duration:0.3, ease:"power2.out"}, %%TTOQ%%);
tl.fromTo("#t3-a", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, %%TT3%%);
tl.fromTo("#t3-b", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, %%TT3B%%);
tl.fromTo("#t3-b", {scale:1}, {scale:1.05, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}, %%TVISUAL%%);
tl.fromTo("#t3-l", {opacity:0, x:-24}, {opacity:1, x:0, duration:0.22, ease:"power3.out"}, %%TTOQ%%);
tl.fromTo("#gv", {clipPath:"inset(0% 0% 100% 0%)"}, {clipPath:"inset(0% 0% 0% 0%)", duration:0.38, ease:"power2.inOut"}, %%TTOQ%%);
tl.fromTo("#gv-o", {scale:0.5, opacity:0.95}, {scale:1.6, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOQ38%%);
tl.fromTo("#gv", {x:0, y:0}, {x:-4, y:8, duration:0.26, yoyo:true, repeat:%%REPS%%, ease:"sine.inOut", immediateRender:false}, %%TTOQ60%%);
tl.fromTo("#gv-o", {scale:0.5, opacity:0.95}, {scale:1.6, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TCONF%%);
// fecho: a caixinha do VISUAL ganha o visto (checklist da intro completo)
tl.to("#ck3", {attr:{"stroke-dashoffset":0}, duration:0.2, ease:"power2.out"}, %%TPOP%%);

// ---- legenda ----
%%LEGJS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

R = lambda v: str(round(v, 3))
t_zoom = round(t_o_ult - 0.15, 3)
t_t2 = round(t_o_ult - 0.05, 3)
t_br = round(t_kitf + 0.03, 3)
t_out2 = round(T_HI - 0.3, 3)
t_tsub = round(t_diaf + 0.02, 3)
d_sub = round(T_HI - t_tsub, 3)
t_pop = round(t_kit_fim + 0.03, 3)
t_wh2 = round(t_zoom - 0.05, 3)
assert t_wh2 > TF("apresentacao", 4) - 0.01, (t_wh2, TF("apresentacao", 4))
rep = {
    "TOTAL": R(TOTAL), "VX": str(VX), "VY": str(VY),
    "V1": R(VOZ["intro"]), "V2": R(VOZ["apresentacao"]), "V3": R(VOZ["cta"]),
    "DV1": R(DUR_MP3["intro"]), "DV2": R(DUR_MP3["apresentacao"]), "DV3": R(DUR_MP3["cta"]),
    "TAG": R(T_AG), "TAG30": R(T_AG + 0.3), "DG": R(T_GH - T_AG),
    "TGH": R(T_GH), "TGH30": R(T_GH + 0.3), "DH1": R(T_HH - T_GH),
    "THH": R(T_HH), "THH26": R(T_HH + 0.26), "DH2": R(T_HI - T_HH),
    "THI": R(T_HI), "THI40": R(T_HI + 0.4), "DI": R(TOTAL - T_HI),
    "D_A": R(T_AG - 0.4), "TCK1": R(t_escolhida), "TCK2": R(t_feita), "TFALTA": R(t_falta),
    "D_G1": R(t_zoom - T_AG - 0.3), "TZOOM": R(t_zoom), "TZOOM36": R(t_zoom + 0.36),
    "D_G2": R(t_saiu - 0.05 - t_zoom - 0.36), "TSAIU": R(t_saiu - 0.05), "TSAIU40": R(t_saiu + 0.35),
    "D_G3": R(t_borrifou - t_saiu - 0.35), "TBORR": R(t_borrifou), "TBORR14": R(t_borrifou + 0.14),
    "D_G4": R(T_GH - t_borrifou - 0.14),
    "TT2": R(t_t2), "TT2B": R(t_t2 + 0.12), "DT2": R(T_HI - t_t2),
    "TW1": R(T_GH - 0.15), "TWH2": R(t_wh2), "TWH3": R(T_GH - 0.06),
    "D_H1A": R(t_ocasiao - T_GH - 0.3), "TOCA": R(t_ocasiao), "TOCA14": R(t_ocasiao + 0.14),
    "D_H1B": R(T_HH - t_ocasiao - 0.14), "TPRONTO": R(t_pronto),
    "D_H2A": R(t_dia - T_HH - 0.26), "TDIA": R(t_dia), "TDIA14": R(t_dia + 0.14), "D_H2B": R(T_HI - t_dia - 0.14),
    "TBR": R(t_br), "TVARIAR": R(t_variar), "TOUT2": R(t_out2), "TW2": R(T_HI - 0.15),
    "TSUB": R(t_tsub), "DSUB": R(d_sub), "MSUB": R(1.4 - d_sub),
    "TT3": R(T_HI + 0.08), "TT3B": R(T_HI + 0.2), "TVISUAL": R(t_visual),
    "TTOQ": R(t_toque), "TTOQ38": R(t_toque + 0.38), "TTOQ60": R(t_toque + 0.6),
    "D_IA": R(t_toque - T_HI - 0.4), "DGRAV": R(TOTAL - t_toque),
    "REPS": str(int((TOTAL - t_toque - 0.6) / 0.26) - 1), "TCONF": R(t_confira), "TPOP": R(t_pop),
    "LEG": "\n".join(leg_html), "LEGJS": "\n".join(leg_js),
}
for k, v in rep.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, [l for l in html.splitlines() if "%%" in l][:3]
open(OUT, "w").write(html)
print("ok", OUT, "TOTAL", TOTAL, "fim falas", {k: round(v, 3) for k, v in FIM_FALA.items()},
      "toque", t_toque, "zoom", t_zoom, "brilho", t_br, "subida", t_tsub, d_sub, "pop", t_pop)
