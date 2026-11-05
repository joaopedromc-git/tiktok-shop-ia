#!/usr/bin/env python3
"""Gera produtos/garrafa/edicao_B/index.html (outdoor laranja: Anton / Poppins 800,
legenda contorno-pop palavra a palavra, fitas laranja inclinadas tipo placa de trilha).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 4.3, 0.25), "apresentacao": (4.3, 14.6, 4.5), "cta": (14.6, 19.7, 14.9)}
TOTAL = 19.7
LEG_TOP = {"intro": 1130, "apresentacao": 1180, "cta": 1222}
# grupos de palavras (1-3 por vez) e topo especial durante o cartão do produto herói
GRUPOS = {
    "intro": [[0, 1], [2, 3], [4], [5, 6, 7], [8, 9, 10], [11, 12]],
    "apresentacao": [[0, 1], [2], [3, 4], [5, 6], [7, 8], [9], [10, 11], [12, 13, 14], [15, 16], [17, 18],
                     [19, 20, 21], [22, 23], [24, 25]],
    "cta": [[0, 1], [2, 3], [4, 5, 6], [7, 8], [9, 10], [11, 12, 13]],
}
TOPO_GRUPO = {("apresentacao", 2): 1350, ("apresentacao", 3): 1350}
CHAVE = {
    "intro": {3, 4, 7, 12},
    "apresentacao": {2, 4, 6, 11, 16, 18, 21, 23},
    "cta": {3, 4, 6, 10, 13},
}
TEXTO = {
    ("intro", 12): "encher?",
    ("apresentacao", 2): "MODUS:", ("apresentacao", 6): "quatrocentos,", ("apresentacao", 9): "fabricante.",
    ("apresentacao", 16): "trabalho,", ("apresentacao", 21): "acampamento,", ("apresentacao", 25): "carregar.",
    ("cta", 3): "trilha,", ("cta", 13): "Shop.",
}

leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    ini, fim, voz = P[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.03, 3)
        e = round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.03, 3) if gi + 1 < len(grupos) else fim
        gid = f"leg-{parte}-{gi}"
        top = TOPO_GRUPO.get((parte, gi), LEG_TOP[parte])
        spans = ""
        for k, wi in enumerate(g):
            cls = "pal k" if wi in CHAVE[parte] else "pal"
            spans += f'<span id="{gid}-{k}" class="{cls}">{TEXTO.get((parte, wi), pal[wi]["palavra"])}</span>'
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="7"><div class="cap" style="top:{top}px">{spans}</div></div>'
        )
        for k, wi in enumerate(g):
            t = max(s, round(voz + pal[wi]["inicio"] - 0.03, 3))
            alvo = 1
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,scale:0.8}},{{opacity:1,scale:{alvo},duration:0.12,ease:"back.out(2.5)"}},{t});')

# contagem 0,0 -> 2,4 (passos fixos, seek-safe): termina no "quatrocentos" (voz 4.5 + 2.476)
PASSOS = [(6.09, "0,0"), (6.16, "0,3"), (6.23, "0,6"), (6.31, "0,9"), (6.40, "1,2"), (6.50, "1,5"),
          (6.62, "1,8"), (6.76, "2,1"), (6.95, "2,4")]
conta_js = "\n".join(f'tl.set("#num",{{textContent:"{v}"}},{t});' for t, v in PASSOS)

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Anton";src:local("Anton Regular"),local("Anton-Regular"),local("Anton");}
:root{--base:#12140F;--lar:#F28C28;--texto:#FFFFFF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#12140F}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#12140F}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden}
.full{width:100%;height:100%;object-fit:cover}
#camD,#camE1,#camE2,#camF{z-index:1}
/* produto herói: quadro limpo do clipe E congelado, vira cartão com borda laranja sobre ele mesmo desfocado */
#hero{z-index:2;overflow:hidden}
#heroCam{position:absolute;inset:0}
#zBg{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
#zDark{position:absolute;inset:0;opacity:0;background:radial-gradient(ellipse 75% 55% at 50% 58%,rgba(18,20,15,.35) 0,rgba(18,20,15,.82) 100%)}
#card{position:absolute;left:0;top:200px;width:1080px;height:1580px;overflow:hidden;
  box-shadow:0 40px 90px rgba(0,0,0,.6)}
#zImg{position:absolute;left:0;top:-200px;width:1080px;height:1920px;object-fit:cover}
#edge{position:absolute;inset:0;border:8px solid var(--lar);border-radius:inherit;box-shadow:inset 0 0 40px rgba(242,140,40,.35)}
#sweep{position:absolute;inset:0;mix-blend-mode:screen;overflow:hidden}
#sweep i{position:absolute;left:0;top:0;width:100%;height:100%;display:block;
  background:linear-gradient(105deg,rgba(255,214,160,0) 36%,rgba(255,224,180,.45) 50%,rgba(255,214,160,0) 64%)}
/* luz e moldura */
.topo{z-index:3;background:linear-gradient(to bottom,rgba(18,20,15,.62) 0,rgba(18,20,15,.38) 14%,rgba(18,20,15,0) 30%)}
.vinheta{z-index:3;background:radial-gradient(ellipse 85% 62% at 50% 50%,rgba(0,0,0,0) 58%,rgba(0,0,0,.4) 100%)}
.flash{z-index:9;background:#FFFFFF}
#leak{z-index:9;mix-blend-mode:screen;overflow:hidden}
#leak i{position:absolute;left:-40%;top:-10%;width:180%;height:120%;display:block;
  background:radial-gradient(ellipse 38% 46% at 50% 45%,rgba(255,236,200,.95) 0,rgba(242,140,40,.75) 38%,rgba(242,140,40,0) 72%)}
#bloomF{z-index:9;background:radial-gradient(ellipse at 50% 30%,rgba(255,210,150,.8) 0,rgba(242,140,40,.3) 45%,rgba(242,140,40,0) 75%)}
/* títulos: Anton maiúsculo com sombra dura (cartaz de trilha) e fitas laranja inclinadas */
.titulo{z-index:5}
.bloco{position:absolute;left:70px;display:block}
.tl{display:block;font-family:"Anton";color:var(--texto);line-height:.98;white-space:nowrap;text-transform:uppercase;
  text-shadow:7px 7px 0 #12140F,0 10px 34px rgba(0,0,0,.45)}
.tl .lar{color:var(--lar)}
.tl span{display:inline-block}
.fita{position:absolute;display:block;white-space:nowrap}
.fita b{position:absolute;inset:0;display:block;background:var(--lar);transform:skewX(-9deg);box-shadow:7px 7px 0 #12140F}
.fita.esc b{background:#12140F;box-shadow:7px 7px 0 var(--lar)}
.fita span{position:relative;display:block;font-family:"Anton";font-weight:400;color:#12140F;line-height:1.08;padding:4px 30px 6px;
  text-transform:uppercase}
.fita.esc span{color:var(--lar)}
/* cabeçalho do produto herói */
#hh{z-index:5}
#hh-tag{left:410px;top:120px}
#hh-tag span{font-size:58px}
#hh-n{position:absolute;left:0;top:186px;width:1040px;display:flex;justify-content:center;align-items:baseline;gap:22px}
#num{display:block;width:380px;text-align:right;font-family:"Anton";font-size:290px;line-height:1;color:var(--lar);
  text-shadow:8px 8px 0 #12140F,0 0 60px rgba(242,140,40,.35)}
#unid{display:block;font-family:"Anton";font-size:290px;line-height:1;color:var(--texto);text-shadow:8px 8px 0 #12140F}
/* legenda contorno-pop: branco com contorno escuro, palavra-chave em laranja */
.legenda{z-index:7}
.cap{position:absolute;left:30px;width:880px;display:flex;justify-content:center;align-items:baseline;gap:24px;flex-wrap:nowrap}
.pal{display:inline-block;font-family:"Poppins";font-weight:800;font-size:80px;line-height:1.1;color:#FFFFFF;white-space:nowrap;
  -webkit-text-stroke:11px #12140F;paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.45)}
.pal.k{color:var(--lar)}
.rodape{z-index:7}
.rodape span{position:absolute;left:52px;top:1468px;display:block;font-family:"Poppins";font-weight:600;
  font-size:30px;color:rgba(255,255,255,.8);text-shadow:0 2px 8px rgba(0,0,0,.85);background:rgba(18,20,15,.5);padding:4px 16px 6px;border-radius:8px}
/* CTA */
#rip{z-index:6}
.anel{position:absolute;left:390px;top:880px;width:240px;height:240px;display:block;border-radius:50%;border:8px solid var(--lar);
  box-shadow:0 0 30px rgba(242,140,40,.6)}
#cta{z-index:8}
#cta-b{position:absolute;left:56px;top:1352px;display:flex;align-items:center;gap:18px;font-family:"Poppins";font-weight:800;
  font-size:46px;color:#12140F;background:var(--lar);padding:16px 38px 18px 22px;border-radius:999px;
  box-shadow:6px 6px 0 #12140F,0 0 44px rgba(242,140,40,.5)}
#cta-b svg{display:block;width:60px;height:60px}
#onda{position:absolute;left:34px;top:1414px;width:150px;height:150px;display:block;border:5px solid var(--lar);border-radius:50%}
#seta{position:absolute;left:52px;top:1446px;width:104px;height:88px;display:block}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: clipe D (garrafa na pedra da trilha), velocidade normal -->
  <div id="camD" class="cam"><video id="vD" class="clip full" data-start="0" data-duration="4.3" data-media-start="0" data-track-index="0" src="assets/clipe_D.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: clipe E em 0,77x; quadro limpo (1,29 s, sem mão) congelado no "dois litros e quatrocentos" -->
  <div id="camE1" class="cam"><video id="vE1" class="clip full" data-start="4.3" data-duration="1.7" data-media-start="0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <div id="hero" class="clip" data-start="6.0" data-duration="1.95" data-track-index="1">
    <div id="heroCam">
      <img id="zBg" src="assets/e_quadro.jpg" alt="Garrafa MODUS" />
      <div id="zDark"></div>
      <div id="card"><img id="zImg" src="assets/e_quadro.jpg" alt="Garrafa MODUS" /><div id="sweep"><i id="sweep-i"></i></div><div id="edge"></div></div>
    </div>
  </div>
  <div id="camE2" class="cam"><video id="vE2" class="clip full" data-start="7.95" data-duration="6.65" data-media-start="1.309" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <!-- CTA: clipe F em 0,9x (desacelera) -->
  <div id="camF" class="cam"><video id="vF" class="clip full" data-start="14.6" data-duration="5.1" data-media-start="0.3" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>

  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="3"></div>
  <div id="flash0" class="clip flash" data-start="0" data-duration="0.15" data-track-index="4"></div>
  <div id="leak" class="clip" data-start="4.1" data-duration="0.5" data-track-index="4"><i id="leak-i"></i></div>
  <div id="flash1" class="clip flash" data-start="6.0" data-duration="0.2" data-track-index="4"></div>
  <div id="bloomF" class="clip" data-start="14.6" data-duration="0.6" data-track-index="4"></div>

  <!-- títulos -->
  <div id="ti" class="clip titulo" data-start="0" data-duration="2.95" data-track-index="5">
    <div id="ti-b" class="bloco" style="top:176px">
      <div id="ti-l0" class="tl" style="font-size:172px">Acabou</div>
      <div id="ti-l1" class="tl" style="font-size:172px">a <span class="lar">água?</span></div>
    </div>
    <div id="ti-f" class="fita" style="left:78px;top:540px"><b></b><span style="font-size:76px">antes do almoço</span></div>
  </div>
  <div id="ta" class="clip titulo" data-start="4.5" data-duration="1.55" data-track-index="5">
    <div id="ta-l0" class="tl bloco" style="top:196px;font-size:76px">Garrafa Térmica</div>
    <div id="ta-f" class="fita" style="left:78px;top:290px"><b></b><span style="font-size:170px">MODUS</span></div>
  </div>
  <div id="hh" class="clip" data-start="6.0" data-duration="1.95" data-track-index="5">
    <div id="hh-tag" class="fita esc"><b></b><span>MODUS</span></div>
    <div id="hh-n"><span id="num">0,0</span><span id="unid">L</span></div>
  </div>
  <div id="tt" class="clip titulo" data-start="10.72" data-duration="2.25" data-track-index="5">
    <div id="tt-f0" class="fita" style="left:78px;top:200px"><b></b><span style="font-size:112px">do trabalho</span></div>
    <div id="tt-f1" class="fita esc" style="left:140px;top:352px"><b></b><span style="font-size:112px">à trilha</span></div>
  </div>
  <div id="tc" class="clip titulo" data-start="14.66" data-duration="2.95" data-track-index="5">
    <div id="tc-b" class="bloco" style="top:170px">
      <div id="tc-l0" class="tl" style="font-size:162px">Toque na</div>
      <div id="tc-l1" class="tl" style="font-size:162px;color:#F28C28">garrafa</div>
    </div>
  </div>
  <div id="rip" class="clip" data-start="16.34" data-duration="0.8" data-track-index="6"><i id="anel1" class="anel"></i><i id="anel2" class="anel"></i></div>
  <div id="cta" class="clip" data-start="17.7" data-duration="2.0" data-track-index="6">
    <svg id="seta" viewBox="0 0 76 64"><path d="M64 6 L18 50 M16 20 L16 52 L48 52" fill="none" stroke="#F28C28" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>
    <i id="onda"></i>
    <span id="cta-b"><svg viewBox="0 0 60 60"><circle cx="30" cy="30" r="28" fill="#12140F"/><path d="M40 20 L22 38 M21 26 L21 39 L34 39" fill="none" stroke="#F28C28" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>Confira no TikTok Shop</span>
  </div>
  <div id="rodape" class="clip rodape" data-start="4.35" data-duration="10.25" data-track-index="6"><span id="rodape-s">*Dados do fabricante</span></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="4.008" data-track-index="8" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.5" data-duration="10.008" data-track-index="8" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="14.9" data-duration="4.68" data-track-index="8" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-000" data-start="0" data-duration="0.8" data-track-index="9" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-pop-158" data-start="1.58" data-duration="0.09" data-track-index="9" data-volume="0.38" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whooshc-286" data-start="2.86" data-duration="0.3" data-track-index="9" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-410" data-start="4.1" data-duration="0.55" data-track-index="9" data-volume="0.4" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-brilho-596" data-start="5.96" data-duration="0.9" data-track-index="9" data-volume="0.36" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-whooshc-788" data-start="7.88" data-duration="0.3" data-track-index="9" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1068" data-start="10.68" data-duration="0.09" data-track-index="9" data-volume="0.36" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-subida-1418" data-start="14.18" data-duration="0.42" data-media-start="0.97" data-track-index="9" data-volume="0.38" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1636" data-start="16.36" data-duration="0.05" data-track-index="9" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-1770" data-start="17.7" data-duration="0.09" data-track-index="9" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });
const SLAM = (sel, t, from) => tl.fromTo(sel, {scale:from || 1.7, opacity:0}, {scale:1, opacity:1, duration:0.3, ease:"back.out(1.8)"}, t);
const FITA = (sel, t) => tl.fromTo(sel, {x:-70, opacity:0, scaleX:0.6, transformOrigin:"0% 50%"}, {x:0, opacity:1, scaleX:1, duration:0.26, ease:"back.out(1.6)"}, t);
const SAI = (sel, t) => tl.to(sel, {y:-60, opacity:0, duration:0.18, ease:"power2.in"}, t);

// ---- INTRO: gancho. Garrafa inteira já no quadro 0, punch-in 1,08->1 (sem cortar a garrafa), clarão, título grande ----
tl.fromTo("#flash0", {opacity:0.2}, {opacity:0, duration:0.1}, 0);
tl.fromTo("#camD", {scale:1.08}, {scale:1, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camD", {scale:1.012, duration:2.46, ease:"none"}, 0.4);
tl.to("#camD", {scale:1.035, duration:0.22, ease:"power3.out"}, 2.88);
tl.to("#camD", {scale:1.04, duration:1.2, ease:"none"}, 3.1);
tl.fromTo("#ti-b", {scale:1.32, transformOrigin:"0% 0%"}, {scale:1, duration:0.34, ease:"back.out(1.7)"}, 0);
tl.to("#ti-l1 .lar", {scale:1.08, duration:0.14, yoyo:true, repeat:1, ease:"sine.inOut"}, 1.2);
FITA("#ti-f", 1.6);
SAI("#ti-b", 2.76);
SAI("#ti-f", 2.8);

// passagem: luz quente de sol varre a tela e corta seco para o E
tl.fromTo("#leak-i", {xPercent:-45, opacity:0}, {xPercent:10, opacity:1, duration:0.2, ease:"power2.out"}, 4.1);
tl.to("#leak-i", {xPercent:45, opacity:0, duration:0.3, ease:"power2.in"}, 4.3);

// ---- APRESENTAÇÃO ----
tl.fromTo("#camE1", {scale:1.08}, {scale:1, duration:0.45, ease:"power3.out"}, 4.3);
tl.to("#camE1", {scale:1.03, duration:1.25, ease:"none"}, 4.75);
tl.fromTo("#ta-l0", {y:30, opacity:0}, {y:0, opacity:1, duration:0.22, ease:"power3.out"}, 4.52);
SLAM("#ta-f", 4.8, 1.6);
SAI("#ta-l0", 5.86);
SAI("#ta-f", 5.88);
// produto herói: congela, encolhe para cartão com borda laranja, contagem 0,0 -> 2,4 L
tl.fromTo("#flash1", {opacity:0.55}, {opacity:0, duration:0.18}, 6.0);
tl.fromTo("#heroCam", {scale:1.03}, {scale:1, duration:0.3, ease:"power2.out"}, 6.0);
tl.fromTo("#card", {scale:1, x:0, y:0, borderRadius:0}, {scale:0.8, x:-20, y:162, borderRadius:34, duration:0.45, ease:"power3.inOut"}, 6.02);
tl.fromTo("#zBg", {filter:"blur(0px) brightness(1)", scale:1}, {filter:"blur(26px) brightness(0.55)", scale:1.12, duration:0.45, ease:"power2.out"}, 6.02);
tl.fromTo("#zDark", {opacity:0}, {opacity:1, duration:0.4}, 6.05);
tl.fromTo("#edge", {opacity:0}, {opacity:1, duration:0.25}, 6.3);
tl.fromTo("#sweep-i", {xPercent:-120}, {xPercent:120, duration:0.85, ease:"power2.inOut"}, 6.55);
tl.fromTo("#hh-tag", {y:-30, opacity:0}, {y:0, opacity:1, duration:0.22, ease:"power3.out"}, 6.12);
tl.fromTo("#num", {scale:1.5, opacity:0, transformOrigin:"100% 70%"}, {scale:1, opacity:1, duration:0.22, ease:"power3.out"}, 6.07);
%%CONTA_JS%%
tl.fromTo("#num", {scale:1.2}, {scale:1, duration:0.3, ease:"back.out(2.5)", immediateRender:false}, 6.95);
tl.fromTo("#unid", {x:80, opacity:0}, {x:0, opacity:1, duration:0.24, ease:"back.out(1.8)"}, 6.95);
tl.to("#hh-tag", {y:-40, opacity:0, duration:0.18, ease:"power2.in"}, 7.56);
tl.to("#hh-n", {y:-50, opacity:0, duration:0.2, ease:"power2.in"}, 7.56);
tl.to("#edge", {opacity:0, duration:0.15}, 7.56);
tl.to("#card", {scale:1, x:0, y:0, borderRadius:0, duration:0.32, ease:"power3.inOut"}, 7.62);
tl.to("#zBg", {filter:"blur(0px) brightness(1)", scale:1, duration:0.32, ease:"power3.inOut"}, 7.62);
tl.to("#zDark", {opacity:0, duration:0.3}, 7.62);
// volta ao movimento em câmera lenta (zoom máximo 1,10x; nada na linha pequena da etiqueta)
tl.fromTo("#camE2", {scale:1}, {scale:1.04, duration:1.42, ease:"none"}, 7.95);
tl.to("#camE2", {scale:1.07, duration:0.22, ease:"power3.out"}, 9.38);
tl.to("#camE2", {scale:1.08, duration:3.68, ease:"none"}, 9.62);
tl.to("#camE2", {scale:1.09, x:-50, y:60, duration:0.3, ease:"power3.out"}, 13.3);
FITA("#tt-f0", 10.72);
FITA("#tt-f1", 11.55);
SAI("#tt-f0", 12.78);
SAI("#tt-f1", 12.8);
tl.fromTo("#rodape-s", {opacity:0}, {opacity:1, duration:0.2}, 4.35);

// ---- CTA: luz quente, título, toque na garrafa, botão com seta para baixo/esquerda ----
tl.fromTo("#bloomF", {opacity:0.7}, {opacity:0, duration:0.55, ease:"power2.out"}, 14.6);
tl.fromTo("#camF", {scale:1.05}, {scale:1, duration:0.5, ease:"power2.out"}, 14.6);
tl.to("#camF", {scale:1.025, duration:4.6, ease:"none"}, 15.1);
tl.fromTo("#tc-l0", {scale:1.6, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.3, ease:"back.out(1.7)"}, 14.68);
tl.fromTo("#tc-l1", {scale:1.8, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.3, ease:"back.out(1.7)"}, 14.76);
tl.to("#tc-b", {scale:0.93, transformOrigin:"0% 50%", duration:0.08, ease:"power2.in"}, 16.34);
tl.to("#tc-b", {scale:1, duration:0.25, ease:"back.out(3)"}, 16.42);
tl.fromTo("#anel1", {scale:0.2, opacity:1}, {scale:1.3, opacity:0, duration:0.6, ease:"power2.out"}, 16.36);
tl.fromTo("#anel2", {scale:0.2, opacity:0.8}, {scale:1, opacity:0, duration:0.55, ease:"power2.out"}, 16.5);
SAI("#tc-b", 17.5);
tl.fromTo("#cta-b", {scale:0.6, opacity:0, transformOrigin:"15% 50%"}, {scale:1, opacity:1, duration:0.28, ease:"back.out(2.2)"}, 17.7);
tl.to("#cta-b", {scale:1.04, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}, 18.0);
tl.fromTo("#onda", {scale:0.2, opacity:0.95}, {scale:1.6, opacity:0, duration:0.6, ease:"power2.out"}, 17.74);
tl.fromTo("#seta", {opacity:0, x:20, y:-20}, {opacity:1, x:0, y:0, duration:0.25}, 17.85);
tl.to("#seta", {x:-10, y:12, duration:0.36, yoyo:true, repeat:3, ease:"sine.inOut"}, 18.1);

// ---- legenda contorno-pop ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

html = (html.replace("%%TOTAL%%", str(TOTAL)).replace("%%LEG_HTML%%", "\n".join(leg_html))
        .replace("%%LEG_JS%%", "\n".join(leg_js)).replace("%%CONTA_JS%%", conta_js))
open(OUT, "w").write(html)
print("ok", OUT)
