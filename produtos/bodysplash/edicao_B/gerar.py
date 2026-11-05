#!/usr/bin/env python3
"""Gera produtos/bodysplash/edicao_B/index.html (luxo noir dourado: DM Serif Display / Bricolage Grotesque,
legenda karaokê em fita com sublinhado dourado, títulos em "foco" letra a letra).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 4.85, 0.25), "apresentacao": (4.85, 15.5, 5.05), "cta": (15.5, 20.05, 15.8)}
TOTAL = 20.05
LEG_TOP = {"intro": 1296, "apresentacao": 1336, "cta": 1222}

GRUPOS = {
    "intro": [[0, 1], [2, 3, 4], [5, 6], [7], [8, 9], [10, 11], [12, 13]],
    "apresentacao": [[0, 1, 2], [3], [4, 5], [6, 7], [8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18], [19],
                     [20], [21, 22], [23, 24, 25]],
    "cta": [[0, 1], [2, 3, 4], [5, 6], [7, 8, 9], [10, 11], [12, 13]],
}
CHAVE = {
    "intro": {6, 9, 10, 13},
    "apresentacao": {3, 7, 9, 12, 15, 18, 20},
    "cta": {1, 6, 7, 13},
}
TEXTO = {
    ("intro", 6): "ele?", ("intro", 9): "meia.", ("intro", 13): "cheiro.",
    ("apresentacao", 2): "Man:", ("apresentacao", 5): "splashes,", ("apresentacao", 7): "fresco,",
    ("apresentacao", 12): "marcante.", ("apresentacao", 19): "dele.", ("apresentacao", 22): "cada,",
    ("apresentacao", 25): "fabricante.",
    ("cta", 6): "presente:", ("cta", 13): "kit.",
}
CREME, OURO = "#F5F1E8", "#C9A86A"

leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    ini, fim, voz = P[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"], 3)
        e = round(voz + pal[grupos[gi + 1][0]]["inicio"], 3) if gi + 1 < len(grupos) else fim
        gid = f"leg-{parte}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            sub = f'<i id="{gid}-{k}-s" class="sub"></i>' if wi in CHAVE[parte] else ""
            spans += f'<span id="{gid}-{k}" class="pal">{TEXTO.get((parte, wi), pal[wi]["palavra"])}{sub}</span>'
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="7" style="top:{LEG_TOP[parte]}px"><div id="{gid}-f" class="fita">{spans}</div></div>'
        )
        leg_js.append(f'tl.fromTo("#{gid}-f",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{s});')
        for k, wi in enumerate(g):
            t = round(voz + pal[wi]["inicio"], 3)
            if wi in CHAVE[parte]:
                leg_js.append(f'tl.to("#{gid}-{k}",{{color:"{OURO}",scale:1.1,duration:0.12,ease:"back.out(3)"}},{t});')
                leg_js.append(f'tl.fromTo("#{gid}-{k}-s",{{scaleX:0}},{{scaleX:1,duration:0.22,ease:"power3.out"}},{round(t + 0.04, 3)});')
            else:
                leg_js.append(f'tl.to("#{gid}-{k}",{{color:"{CREME}",duration:0.08}},{t});')


def letras(txt):
    return "".join(f'<span class="l">{"&nbsp;" if c == " " else c}</span>' for c in txt)


def linha(lid, palavras, size):
    """palavras: lista de (texto, classe extra)."""
    ws = " ".join(f'<span class="w {cls}">{letras(t)}</span>' for t, cls in palavras)
    return f'<div id="{lid}" class="tl" style="font-size:{size}px">{ws}</div>'


ORN = ('<div id="{id}" class="orn"><i class="ln ln-l"></i><svg class="dia" viewBox="0 0 20 20">'
       '<polygon points="10,1 19,10 10,19 1,10" fill="#C9A86A"/></svg><i class="ln ln-r"></i></div>')

T1 = (linha("t1-l0", [("Presente", "")], 138) + linha("t1-l1", [("pra", ""), ("ele?", "ouro")], 138)
      + ORN.replace("{id}", "t1-o"))
T2 = (linha("t2-l0", [("Esquece", ""), ("a meia", "risk")], 116)).replace(
    '<span class="w risk">', '<span id="t2-risk" class="w risk"><i id="t2-risco" class="risco"></i>') + ORN.replace("{id}", "t2-o")
T3 = linha("t3-l0", [("Kit", ""), ("Body", "ouro"), ("Man", "ouro")], 124) + ORN.replace("{id}", "t3-o")
T4 = (linha("t4-l0", [("Pra", ""), ("você", "ouro")], 118) + linha("t4-l1", [("ou", ""), ("presente", "ouro")], 118)
      + ORN.replace("{id}", "t4-o"))
SW = {"sf": "Fresco", "se": "elegante", "sm": "marcante"}

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
:root{--base:#0A0A0A;--ouro:#C9A86A;--texto:#F5F1E8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0A0A0A}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:visible}
.full{width:100%;height:100%;object-fit:cover}
/* intro: quadrado nítido sobre o próprio clipe desfocado */
#camDf{z-index:1}
#camD{z-index:2}
#vD{inset:auto;left:75px;top:492px;width:929px;height:927px;object-fit:cover}
#molD{inset:auto;left:75px;top:492px;width:929px;height:927px;border:2px solid rgba(201,168,106,.9);border-radius:4px;
  box-shadow:0 34px 90px rgba(0,0,0,.7),0 0 70px rgba(201,168,106,.22),inset 0 0 0 1px rgba(245,241,232,.08)}
#veuD{z-index:1;background:radial-gradient(ellipse 70% 42% at 50% 50%,rgba(201,168,106,.16) 0,rgba(10,10,10,.35) 60%,rgba(10,10,10,.72) 100%)}
#camE1,#camE2,#camZ,#camF{z-index:2}
/* faixa escura do alto: cobre o "bodyman" inventado do clipe E e dá apoio ao título */
.topo{z-index:4;background:linear-gradient(to bottom,#0A0A0A 0,#0A0A0A 120px,rgba(10,10,10,.82) 210px,rgba(10,10,10,.45) 330px,rgba(10,10,10,0) 470px)}
.vinheta{z-index:3;background:radial-gradient(ellipse 80% 60% at 50% 48%,rgba(0,0,0,0) 55%,rgba(0,0,0,.42) 100%)}
.flash{z-index:9;background:#FFF8EC}
.bloom{z-index:9;background:radial-gradient(ellipse at 50% 40%,rgba(235,240,255,.85) 0,rgba(200,215,240,.35) 42%,rgba(200,215,240,0) 72%)}
#spot{z-index:3;background:radial-gradient(ellipse 52% 40% at 50% 47%,rgba(0,0,0,0) 50%,rgba(0,0,0,.62) 100%)}
#varre{z-index:3;mix-blend-mode:screen;overflow:hidden}
#varre i{position:absolute;top:0;left:0;width:100%;height:100%;display:block;
  background:linear-gradient(105deg,rgba(255,236,200,0) 36%,rgba(255,236,200,.42) 50%,rgba(255,236,200,0) 64%)}
.brilho{position:absolute;width:120px;height:120px;display:block}
/* títulos: letras entram em foco (desfoque + espaçamento largo -> nítido) */
.titulo{z-index:5;height:auto;bottom:auto;display:flex;flex-direction:column;align-items:center;justify-content:flex-start}
.tl{display:block;font-family:"DM Serif Display";color:var(--texto);line-height:1.0;text-align:center;white-space:nowrap;
  text-shadow:0 6px 34px rgba(0,0,0,.7)}
.w{display:inline-block;position:relative}
.w.ouro{color:var(--ouro)}
.l{display:inline-block}
.risco{position:absolute;left:-4%;top:52%;width:108%;height:9px;display:block;background:var(--ouro);border-radius:5px;
  transform-origin:left center;box-shadow:0 0 16px rgba(201,168,106,.7)}
.orn{display:flex;align-items:center;gap:16px;margin-top:20px}
.ln{display:block;width:150px;height:2px;background:var(--ouro);box-shadow:0 0 12px rgba(201,168,106,.6)}
.ln-l{transform-origin:right center}
.ln-r{transform-origin:left center}
.dia{display:block;width:18px;height:18px}
#troca{z-index:5;height:auto;bottom:auto}
.slot{position:absolute;left:0;width:1080px;top:0;display:flex;align-items:center;justify-content:center;gap:26px}
.slot .tl{font-size:112px}
.slot .dia{width:16px;height:16px}
#ml{z-index:5;height:auto;bottom:auto;display:flex;flex-direction:column;align-items:center}
#ml .tl b{font-weight:400;color:var(--ouro)}
#cada{display:block;margin-top:6px;font-family:"Bricolage Grotesque";font-weight:600;font-size:46px;letter-spacing:14px;
  color:var(--texto);text-shadow:0 3px 18px rgba(0,0,0,.7)}
/* legenda karaokê em fita escura; palavra-chave acende em dourado com sublinhado que se desenha */
.legenda{z-index:7;height:auto;bottom:auto}
.fita{display:flex;justify-content:center;align-items:center;gap:22px;padding:12px 170px 18px 70px;
  background:linear-gradient(90deg,rgba(10,10,10,0) 0,rgba(10,10,10,.62) 16%,rgba(10,10,10,.62) 78%,rgba(10,10,10,0) 100%)}
.pal{display:inline-block;position:relative;font-family:"Bricolage Grotesque";font-weight:700;font-size:74px;line-height:1.1;
  color:rgba(245,241,232,.42);text-shadow:0 3px 14px rgba(0,0,0,.6)}
.sub{position:absolute;left:2px;right:2px;bottom:2px;height:6px;display:block;background:var(--ouro);border-radius:3px;
  transform-origin:left center;box-shadow:0 0 10px rgba(201,168,106,.6)}
.rodape{z-index:7;height:auto;bottom:auto;top:1480px;display:flex;justify-content:center;padding-right:150px}
.rodape span{display:block;font-family:"Bricolage Grotesque";font-weight:500;font-size:30px;color:rgba(255,255,255,.8);
  text-shadow:0 2px 8px rgba(0,0,0,.8)}
/* CTA */
#cta{z-index:8}
#cta-b{position:absolute;left:58px;top:1372px;display:flex;align-items:center;gap:18px;font-family:"Bricolage Grotesque";
  font-weight:700;font-size:48px;color:var(--base);background:var(--ouro);padding:18px 40px 20px 26px;border-radius:999px;
  box-shadow:0 0 46px rgba(201,168,106,.55),0 10px 26px rgba(0,0,0,.45)}
#cta-b svg{display:block;width:58px;height:58px}
#onda{position:absolute;left:52px;top:1440px;width:120px;height:120px;display:block;border:4px solid var(--ouro);border-radius:50%}
#seta{position:absolute;left:70px;top:1478px;width:70px;height:56px;display:block}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO (clipe D, trecho limpo 4,1-7,93 s em 0,79x): fundo = o próprio clipe desfocado; quadrado nítido com moldura dourada -->
  <div id="camDf" class="cam"><video id="vDf" class="clip full" data-start="0" data-duration="4.85" data-media-start="4.1" data-playback-rate="0.79" data-track-index="0" src="assets/d_fundo.mp4" muted playsinline></video></div>
  <div id="veuD" class="clip" data-start="0" data-duration="4.85" data-track-index="2"></div>
  <div id="camD" class="cam">
    <video id="vD" class="clip" data-start="0" data-duration="4.85" data-media-start="4.1" data-playback-rate="0.79" data-track-index="1" src="assets/d_quadrado.mp4" muted playsinline></video>
    <div id="molD" class="clip" data-start="0" data-duration="4.85" data-track-index="3"></div>
  </div>
  <!-- APRESENTAÇÃO (clipe E em 0,77x; quadro de 5,58 s congelado no meio). O "bodyman" inventado (alto à esquerda) fica fora do quadro pelo enquadramento e ainda sob a faixa escura -->
  <div id="camE1" class="cam"><video id="vE1" class="clip full" data-start="4.85" data-duration="7.25" data-media-start="0" data-playback-rate="0.77" data-track-index="1" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <div id="camZ" class="cam">
    <img id="zImg" class="clip full" data-start="12.1" data-duration="1.75" data-track-index="1" src="assets/e_quadro.png" alt="Kit Body Man" />
    <svg id="b1" class="clip brilho" data-start="12.1" data-duration="1.75" data-track-index="3" style="inset:auto;left:198px;top:648px" viewBox="0 0 120 120"><path d="M60 0 C64 46 74 56 120 60 C74 64 64 74 60 120 C56 74 46 64 0 60 C46 56 56 46 60 0Z" fill="#FFF3DA"/></svg>
    <svg id="b2" class="clip brilho" data-start="12.1" data-duration="1.75" data-track-index="3" style="inset:auto;left:483px;top:645px" viewBox="0 0 120 120"><path d="M60 0 C64 46 74 56 120 60 C74 64 64 74 60 120 C56 74 46 64 0 60 C46 56 56 46 60 0Z" fill="#FFF3DA"/></svg>
    <svg id="b3" class="clip brilho" data-start="12.1" data-duration="1.75" data-track-index="3" style="inset:auto;left:760px;top:652px" viewBox="0 0 120 120"><path d="M60 0 C64 46 74 56 120 60 C74 64 64 74 60 120 C56 74 46 64 0 60 C46 56 56 46 60 0Z" fill="#FFF3DA"/></svg>
  </div>
  <div id="camE2" class="cam"><video id="vE2" class="clip full" data-start="13.85" data-duration="1.65" data-media-start="5.5825" data-playback-rate="0.77" data-track-index="1" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <!-- CTA (clipe F em 0,90x, desacelerando) -->
  <div id="camF" class="cam"><video id="vF" class="clip full" data-start="15.5" data-duration="4.55" data-media-start="0.3" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_F.mp4" muted playsinline></video></div>

  <div id="vin" class="clip vinheta" data-start="4.85" data-duration="15.2" data-track-index="2"></div>
  <div id="spot" class="clip" data-start="12.1" data-duration="1.75" data-track-index="3"></div>
  <div id="varre" class="clip" data-start="12.3" data-duration="1.1" data-track-index="3"><i id="varre-i"></i></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="4"></div>
  <div id="flash2" class="clip flash" data-start="12.1" data-duration="0.3" data-track-index="5"></div>
  <div id="bloom" class="clip bloom" data-start="15.5" data-duration="0.6" data-track-index="5"></div>

  <div id="t1" class="clip titulo" data-start="0" data-duration="1.86" data-track-index="6" style="top:168px">%%T1%%</div>
  <div id="t2" class="clip titulo" data-start="1.86" data-duration="1.3" data-track-index="6" style="top:236px">%%T2%%</div>
  <div id="t3" class="clip titulo" data-start="4.92" data-duration="1.12" data-track-index="6" style="top:170px">%%T3%%</div>
  <div id="troca" class="clip" data-start="7.3" data-duration="2.66" data-track-index="6" style="top:180px">
    <div id="sf" class="slot">%%SF%%</div><div id="se" class="slot">%%SE%%</div><div id="sm" class="slot">%%SM%%</div></div>
  <div id="ml" class="clip" data-start="12.12" data-duration="1.73" data-track-index="6" style="top:150px">
    <div id="ml-l" class="tl" style="font-size:150px"><b id="ml-200">200 ml</b></div><span id="cada">%%CADA%%</span></div>
  <div id="t4" class="clip titulo" data-start="15.56" data-duration="2.2" data-track-index="6" style="top:176px">%%T4%%</div>
  <div id="cta" class="clip" data-start="17.78" data-duration="2.27" data-track-index="6">
    <svg id="seta" viewBox="0 0 70 56"><path d="M58 6 L16 44 M14 18 L14 46 L42 46" fill="none" stroke="#C9A86A" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <i id="onda"></i>
    <span id="cta-b"><svg viewBox="0 0 58 58"><circle cx="29" cy="29" r="27" fill="#0A0A0A"/><path d="M38 20 L21 37 M20 26 L20 38 L32 38" fill="none" stroke="#C9A86A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>Toque no produto e confira</span></div>
  <div id="rodape" class="clip rodape" data-start="4.85" data-duration="10.65" data-track-index="6"><span id="rodape-s">*Dados do fabricante</span></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="4.608" data-track-index="8" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="5.05" data-duration="10.392" data-track-index="8" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="15.8" data-duration="4.176" data-track-index="8" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-000" data-start="0" data-duration="0.8" data-track-index="9" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-182" data-start="1.82" data-duration="0.3" data-track-index="9" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-462" data-start="4.62" data-duration="0.55" data-track-index="9" data-volume="0.4" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-tique-728" data-start="7.28" data-duration="0.03" data-track-index="9" data-volume="0.35" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whooshc-998" data-start="9.98" data-duration="0.3" data-track-index="9" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-brilho-1208" data-start="12.08" data-duration="0.9" data-track-index="9" data-volume="0.35" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-subida-1490" data-start="14.9" data-duration="0.6" data-media-start="0.8" data-track-index="9" data-volume="0.35" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1780" data-start="17.8" data-duration="0.05" data-track-index="9" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });
const FOCO_IN = (sel, t, dur, stg) => {
  tl.fromTo(sel, {opacity:0, filter:"blur(14px)", y:22, scale:1.18},
    {opacity:1, filter:"blur(0px)", y:0, scale:1, duration:dur, stagger:stg, ease:"power3.out"}, t);
};
const FOCO_OUT = (sel, t) => {
  tl.to(sel, {opacity:0, filter:"blur(10px)", y:-14, duration:0.2, stagger:0.008, ease:"power2.in"}, t);
};
// "tracking": cada letra parte afastada do centro da linha e fecha (só transform, sem letter-spacing)
const TRACK = (sel, t, dur, k) => {
  tl.fromTo(sel, {x:(i, el, arr) => (i - (arr.length - 1) / 2) * (k || 16)}, {x:0, duration:dur, ease:"power3.out"}, t);
};
const ORN_IN = (id, t) => {
  tl.fromTo(id + " .ln", {scaleX:0}, {scaleX:1, duration:0.4, ease:"power3.out"}, t);
  tl.fromTo(id + " .dia", {scale:0, opacity:0}, {scale:1, opacity:1, duration:0.3, ease:"back.out(3)"}, t);
};
const ORN_OUT = (id, t) => {
  tl.to(id + " .ln", {scaleX:0, duration:0.18, ease:"power2.in"}, t);
  tl.to(id + " .dia", {scale:0, opacity:0, duration:0.18}, t);
};

// ---- INTRO: gancho (punch-in do quadrado + clarão + título em foco) ----
tl.fromTo("#camD", {scale:1.14, transformOrigin:"540px 955px"}, {scale:1, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camD", {scale:1.03, duration:2.79, ease:"none"}, 0.4);
tl.to("#camD", {scale:1.07, duration:0.25, ease:"back.out(2)"}, 3.19);
tl.to("#camD", {scale:1.09, duration:1.16, ease:"none"}, 3.44);
tl.to("#camD", {scale:1.3, opacity:0, duration:0.25, ease:"power2.in"}, 4.6);
tl.fromTo("#camDf", {scale:1.12}, {scale:1.0, duration:0.5, ease:"power3.out"}, 0);
tl.to("#camDf", {scale:1.08, duration:4.1, ease:"none"}, 0.5);
tl.fromTo("#t1 .l", {opacity:0.85, filter:"blur(5px)", scale:1.22}, {opacity:1, filter:"blur(0px)", scale:1, duration:0.36, stagger:0.012, ease:"power3.out"}, 0);
TRACK("#t1-l0 .l", 0, 0.5);
TRACK("#t1-l1 .l", 0, 0.5);
ORN_IN("#t1-o", 0.3);
tl.to("#t1-l1 .ouro", {scale:1.08, duration:0.16, yoyo:true, repeat:1, ease:"sine.inOut"}, 1.29);
FOCO_OUT("#t1 .l", 1.64);
ORN_OUT("#t1-o", 1.64);
// "Esquece a meia": entra em foco; "a meia" é riscada em dourado
FOCO_IN("#t2 .l", 1.88, 0.34, 0.018);
TRACK("#t2-l0 .l", 1.88, 0.45, 12);
ORN_IN("#t2-o", 2.05);
tl.fromTo("#t2-risco", {scaleX:0}, {scaleX:1, duration:0.26, ease:"power3.inOut"}, 2.62);
tl.to("#t2-risk", {opacity:0.55, duration:0.2}, 2.75);
FOCO_OUT("#t2 .l", 2.94);
tl.to("#t2-risco", {opacity:0, duration:0.18}, 2.94);
ORN_OUT("#t2-o", 2.94);

// ---- APRESENTAÇÃO ----
// enquadramento com origem no alto: o canto superior esquerdo do clipe E (texto inventado) fica sempre fora do quadro
tl.fromTo("#camE1", {transformOrigin:"50% 0%", scale:1.22, x:-30, y:-230}, {scale:1.08, y:-150, duration:0.35, ease:"power3.out"}, 4.85);
tl.to("#camE1", {scale:1.1, y:-160, duration:0.85, ease:"none"}, 5.2);
tl.to("#camE1", {scale:1.15, y:-195, duration:0.3, ease:"power3.out"}, 6.05);
tl.to("#camE1", {scale:1.18, y:-215, duration:3.6, ease:"none"}, 6.35);
tl.to("#camE1", {scale:1.26, y:-300, duration:0.25, ease:"power3.out"}, 10.0);
tl.to("#camE1", {scale:1.3, y:-330, duration:1.85, ease:"none"}, 10.25);
FOCO_IN("#t3 .l", 4.95, 0.4, 0.02);
TRACK("#t3-l0 .l", 4.95, 0.55);
ORN_IN("#t3-o", 5.2);
FOCO_OUT("#t3 .l", 5.86);
ORN_OUT("#t3-o", 5.86);
// fresco / elegante / marcante: trocam no mesmo lugar, no tempo da fala (sem ligar a nenhum frasco)
FOCO_IN("#sf .l", 7.32, 0.3, 0.018);
tl.fromTo("#sf .dia", {scale:0}, {scale:1, duration:0.25, ease:"back.out(3)"}, 7.36);
FOCO_OUT("#sf .l", 8.1);
tl.to("#sf .dia", {scale:0, duration:0.15}, 8.1);
FOCO_IN("#se .l", 8.24, 0.3, 0.018);
tl.fromTo("#se .dia", {scale:0}, {scale:1, duration:0.25, ease:"back.out(3)"}, 8.28);
FOCO_OUT("#se .l", 8.98);
tl.to("#se .dia", {scale:0, duration:0.15}, 8.98);
FOCO_IN("#sm .l", 9.12, 0.3, 0.018);
tl.fromTo("#sm .dia", {scale:0}, {scale:1, duration:0.25, ease:"back.out(3)"}, 9.16);
FOCO_OUT("#sm .l", 9.74);
tl.to("#sm .dia", {scale:0, duration:0.15}, 9.74);
// produto herói: congela, abre do close para os três frascos, luz varre, brilho no aro cromado de cada um
tl.fromTo("#flash2", {opacity:0.5}, {opacity:0, duration:0.28}, 12.1);
tl.fromTo("#camZ", {transformOrigin:"50% 0%", scale:1.3, x:-30, y:-330}, {scale:1.1, y:-170, duration:0.42, ease:"power3.inOut"}, 12.1);
tl.to("#camZ", {scale:1.12, y:-182, duration:1.33, ease:"none"}, 12.52);
tl.fromTo("#spot", {opacity:0}, {opacity:1, duration:0.4}, 12.2);
tl.fromTo("#varre-i", {xPercent:-110}, {xPercent:110, duration:0.95, ease:"power2.inOut"}, 12.35);
tl.fromTo("#ml-l", {opacity:0, filter:"blur(16px)", scale:1.3}, {opacity:1, filter:"blur(0px)", scale:1, duration:0.4, ease:"power3.out"}, 12.17);
tl.fromTo("#cada .l", {opacity:0, x:(i, el, arr) => (i - (arr.length - 1) / 2) * 40}, {opacity:1, x:0, duration:0.45, ease:"power3.out"}, 13.36);
tl.fromTo("#b1", {scale:0, rotation:-45, opacity:0}, {scale:1, rotation:0, opacity:1, duration:0.22, ease:"back.out(2)"}, 13.36);
tl.to("#b1", {scale:0, opacity:0, duration:0.25}, 13.6);
tl.fromTo("#b2", {scale:0, rotation:-45, opacity:0}, {scale:1, rotation:0, opacity:1, duration:0.22, ease:"back.out(2)"}, 13.44);
tl.to("#b2", {scale:0, opacity:0, duration:0.25}, 13.68);
tl.fromTo("#b3", {scale:0, rotation:-45, opacity:0}, {scale:1, rotation:0, opacity:1, duration:0.22, ease:"back.out(2)"}, 13.52);
tl.to("#b3", {scale:0, opacity:0, duration:0.25}, 13.76);
tl.to("#ml", {opacity:0, duration:0.15}, 13.72);
// volta ao movimento
tl.fromTo("#camE2", {transformOrigin:"50% 0%", scale:1.2, x:-30, y:-250}, {scale:1.12, y:-185, duration:0.3, ease:"power3.out"}, 13.85);
tl.to("#camE2", {scale:1.15, y:-205, duration:1.35, ease:"none"}, 14.15);
tl.fromTo("#rodape-s", {opacity:0}, {opacity:1, duration:0.2}, 4.9);

// ---- CTA: luz fria do refletor, título, toque ----
tl.fromTo("#bloom", {opacity:0.75}, {opacity:0, duration:0.55, ease:"power2.out"}, 15.5);
tl.fromTo("#camF", {scale:1.12}, {scale:1, duration:0.55, ease:"power2.out"}, 15.5);
tl.to("#camF", {scale:1.04, duration:4.0, ease:"none"}, 16.05);
FOCO_IN("#t4 .l", 15.6, 0.42, 0.016);
TRACK("#t4-l0 .l", 15.6, 0.6);
TRACK("#t4-l1 .l", 15.6, 0.6);
ORN_IN("#t4-o", 15.9);
FOCO_OUT("#t4 .l", 17.52);
ORN_OUT("#t4-o", 17.52);
tl.fromTo("#cta-b", {scale:0.6, opacity:0, transformOrigin:"20% 50%"}, {scale:1, opacity:1, duration:0.3, ease:"back.out(2.2)"}, 17.8);
tl.to("#cta-b", {scale:1.04, duration:0.55, yoyo:true, repeat:3, ease:"sine.inOut"}, 18.2);
tl.fromTo("#onda", {scale:0.2, opacity:0.95}, {scale:1.6, opacity:0, duration:0.6, ease:"power2.out"}, 17.82);
tl.fromTo("#seta", {opacity:0, x:18, y:-18}, {opacity:1, x:0, y:0, duration:0.25}, 17.95);
tl.to("#seta", {x:-10, y:12, duration:0.4, yoyo:true, repeat:4, ease:"sine.inOut"}, 18.2);

// ---- legenda karaokê ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""


def slot(sid, txt):
    dia = '<svg class="dia" viewBox="0 0 20 20"><polygon points="10,1 19,10 10,19 1,10" fill="#C9A86A"/></svg>'
    return dia + linha(f"{sid}-l", [(txt, "")], 112) + dia


html = (html.replace("%%TOTAL%%", str(TOTAL)).replace("%%T1%%", T1).replace("%%T2%%", T2).replace("%%T3%%", T3)
        .replace("%%T4%%", T4).replace("%%SF%%", slot("sf", SW["sf"])).replace("%%SE%%", slot("se", SW["se"]))
        .replace("%%SM%%", slot("sm", SW["sm"])).replace("%%LEG_HTML%%", "\n".join(leg_html))
        .replace("%%CADA%%", letras("CADA")).replace("%%LEG_JS%%", "\n".join(leg_js)))
open(OUT, "w").write(html)
print("ok", OUT)
