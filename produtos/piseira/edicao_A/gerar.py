#!/usr/bin/env python3
"""Gera produtos/piseira/edicao_A/index.html (premium-noir, DM Serif Display / Inter 600, legenda karaokê em pílula)."""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# tempos das partes
P = {"intro": (0.0, 4.55, 0.25), "apresentacao": (4.55, 14.55, 4.80), "cta": (14.55, 19.22, 14.85)}
TOTAL = 19.22
LEG_TOP = {"intro": 1060, "apresentacao": 1290, "cta": 1080}

# grupos (índices de palavras) e palavras-chave; texto exibido (com pontuação mínima)
GRUPOS = {
    "intro": [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9, 10], [11, 12]],
    "apresentacao": [[0, 1], [2, 3], [4, 5], [6, 7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17], [18, 19], [20], [21, 22], [23, 24], [25, 26]],
    "cta": [[0, 1], [2, 3], [4, 5, 6], [7, 8, 9], [10, 11], [12, 13]],
}
CHAVE = {
    "intro": {5, 7, 10},
    "apresentacao": {1, 3, 5, 8, 12, 14, 16, 24, 26},
    "cta": {3, 6, 13},
}
TEXTO = {("intro", 5): "graça?", ("cta", 3): "cor:"}

leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    ini, fim, voz = P[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"], 3)
        e = round(voz + pal[grupos[gi + 1][0]]["inicio"], 3) if gi + 1 < len(grupos) else fim
        gid = f"leg-{parte}-{gi}"
        spans = "".join(
            f'<span id="{gid}-{k}" class="pal">{TEXTO.get((parte, wi), pal[wi]["palavra"])}</span>' for k, wi in enumerate(g)
        )
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="6" style="top:{LEG_TOP[parte]}px"><div id="{gid}-p" class="pilula">{spans}</div></div>'
        )
        leg_js.append(f'tl.fromTo("#{gid}-p",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{s});')
        for k, wi in enumerate(g):
            t = round(voz + pal[wi]["inicio"], 3)
            if wi in CHAVE[parte]:
                leg_js.append(f'tl.to("#{gid}-{k}",{{color:"#C9A86A",scale:1.1,duration:0.12,ease:"back.out(3)"}},{t});')
            else:
                leg_js.append(f'tl.to("#{gid}-{k}",{{color:"#F5F1E8",duration:0.08}},{t});')

SWATCH = ["#1B1B1B", "#1F2A44", "#CDB795", "#EFE3C8", "#F7F5F0", "#6B4A33", "#A8D5C2", "#E3B7B0", "#B5562E"]
sw_html = "".join(f'<span id="sw{i}" class="sw" style="background:{c}"></span>' for i, c in enumerate(SWATCH))
sw_js = "\n".join(
    f'tl.fromTo("#sw{i}",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"back.out(2.5)"}},{round(15.30 + i * 0.045, 3)});'
    for i in range(len(SWATCH))
)

# contagem 0 -> 220 e 0 -> 60
cont = []
for i, n in enumerate([0, 30, 60, 90, 120, 150, 180, 200, 220]):
    cont.append(f'tl.set("#n220",{{textContent:"{n}"}},{round(8.61 + i * 0.075, 3)});')
for i, n in enumerate([0, 10, 20, 30, 40, 50, 60]):
    cont.append(f'tl.set("#n60",{{textContent:"{n}"}},{round(9.67 + i * 0.06, 3)});')

html = f"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
:root{{--base:#0A0A0A;--ouro:#C9A86A;--texto:#F5F1E8}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0A0A0A}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:#0A0A0A}}
.clip{{position:absolute;inset:0}}
.cam{{position:absolute;inset:0;overflow:hidden}}
.cam video{{width:100%;height:100%;object-fit:cover}}
.topo{{z-index:4;background:linear-gradient(to bottom,rgba(10,10,10,.84) 0,rgba(10,10,10,.6) 19%,rgba(10,10,10,0) 40%),
  radial-gradient(ellipse at 50% 55%,rgba(0,0,0,0) 60%,rgba(0,0,0,.35) 100%)}}
.flash{{z-index:9;background:#FFF6E6}}
.bloom{{z-index:9;background:radial-gradient(ellipse at 50% 45%,rgba(255,226,170,.85) 0,rgba(255,214,150,.35) 45%,rgba(255,214,150,0) 75%)}}
.titulo{{z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:flex-start}}
.mask{{display:block;overflow:hidden;padding:0 10px 6px}}
.mask span{{display:block;font-family:"DM Serif Display";color:var(--texto);line-height:1.02;text-align:center;
  text-shadow:0 6px 30px rgba(0,0,0,.55)}}
.mask span b{{font-weight:400;color:var(--ouro)}}
.regua{{display:block;width:220px;height:4px;background:var(--ouro);border-radius:2px;margin-top:22px;transform-origin:center;
  box-shadow:0 0 18px rgba(201,168,106,.6)}}
.legenda{{z-index:7;height:auto;bottom:auto;display:flex;justify-content:center;align-items:flex-start;padding:0 150px 0 90px}}
.pilula{{display:inline-flex;gap:20px;align-items:center;background:rgba(10,10,10,.66);border:2px solid rgba(201,168,106,.45);
  border-radius:999px;padding:12px 36px 16px;box-shadow:0 10px 30px rgba(0,0,0,.35)}}
.pal{{display:inline-block;font-family:"Inter";font-weight:600;font-size:76px;line-height:1.12;color:rgba(245,241,232,.5)}}
.rodape{{z-index:7;height:auto;bottom:auto;top:1478px;display:flex;justify-content:center;align-items:flex-start;padding-right:120px}}
.rodape span{{font-family:"Inter";font-weight:500;font-size:30px;color:rgba(255,255,255,.8);text-shadow:0 2px 8px rgba(0,0,0,.7)}}
#congela{{z-index:2;overflow:hidden}}
#fundo{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;}}
#card{{position:absolute;left:130px;top:430px;width:820px;height:1458px;border:3px solid var(--ouro);border-radius:14px;overflow:hidden;
  box-shadow:0 30px 80px rgba(0,0,0,.65),0 0 60px rgba(201,168,106,.4)}}
#card img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
#reflexo{{position:absolute;top:0;left:0;width:100%;height:100%;
  background:linear-gradient(105deg,rgba(255,240,210,0) 38%,rgba(255,240,210,.38) 50%,rgba(255,240,210,0) 62%)}}
#medidas{{z-index:5;display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:160px}}
#medidas .num{{display:block;font-family:"DM Serif Display";font-size:150px;line-height:1;color:var(--texto);text-shadow:0 6px 30px rgba(0,0,0,.6)}}
#medidas .num b{{font-weight:400;color:var(--ouro)}}
#medidas .sub{{display:block;margin-top:16px;font-family:"Inter";font-weight:600;font-size:40px;letter-spacing:8px;color:var(--ouro)}}
#moldura{{z-index:5}}
#caixa{{position:absolute;left:330px;top:620px;width:560px;height:560px}}
.canto{{position:absolute;width:84px;height:84px;border-color:var(--ouro);border-style:solid;border-width:0;
  filter:drop-shadow(0 0 10px rgba(201,168,106,.8))}}
.c1{{left:0;top:0;border-top-width:7px;border-left-width:7px;border-top-left-radius:10px}}
.c2{{right:0;top:0;border-top-width:7px;border-right-width:7px;border-top-right-radius:10px}}
.c3{{left:0;bottom:0;border-bottom-width:7px;border-left-width:7px;border-bottom-left-radius:10px}}
.c4{{right:0;bottom:0;border-bottom-width:7px;border-right-width:7px;border-bottom-right-radius:10px}}
#cores{{display:flex;gap:18px;margin-top:34px}}
.sw{{display:block;width:62px;height:62px;border-radius:50%;border:3px solid rgba(245,241,232,.9);box-shadow:0 4px 14px rgba(0,0,0,.45)}}
#cta{{z-index:8}}
#cta-b{{position:absolute;left:60px;top:1316px;display:block;font-family:"Inter";font-weight:700;font-size:50px;color:var(--base);
  background:var(--ouro);padding:20px 40px;border-radius:999px;box-shadow:0 0 44px rgba(201,168,106,.55),0 10px 26px rgba(0,0,0,.4)}}
#cta-s{{position:absolute;left:96px;top:1428px;width:90px;height:90px;display:block}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- vídeo: clipe A recortado sem as faixas pretas (a_corte.mp4 = crop 720x1096 a partir de y 90) -->
  <div id="camA1" class="cam"><video id="vA1" class="clip" data-start="0" data-duration="2.4" data-media-start="0" data-track-index="0" src="assets/a_corte.mp4" muted playsinline></video></div>
  <div id="camA2" class="cam"><video id="vA2" class="clip" data-start="2.4" data-duration="2.15" data-media-start="5.6" data-track-index="0" src="assets/a_corte.mp4" muted playsinline></video></div>
  <div id="camB1" class="cam"><video id="vB1" class="clip" data-start="4.55" data-duration="1.4" data-media-start="0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <div id="camB2" class="cam"><video id="vB2" class="clip" data-start="5.95" data-duration="2.3" data-media-start="2.0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <div id="congela" class="clip" data-start="8.25" data-duration="2.8" data-track-index="1">
    <img id="fundo" src="assets/b_fundo.jpg" alt="" />
    <div id="card"><img id="cardimg" src="assets/b_quadro.png" alt="peseira" /><div id="reflexo"></div></div>
  </div>
  <div id="camB3" class="cam"><video id="vB3" class="clip" data-start="11.05" data-duration="3.5" data-media-start="4.8" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <div id="camC" class="cam"><video id="vC" class="clip" data-start="14.55" data-duration="4.67" data-media-start="0" data-playback-rate="0.85" data-track-index="0" src="assets/clipe_C.mp4" muted playsinline></video></div>

  <div id="topo" class="clip topo" data-start="0" data-duration="{TOTAL}" data-track-index="2"></div>
  <div id="flash1" class="clip flash" data-start="0" data-duration="0.2" data-track-index="3"></div>
  <div id="flash2" class="clip flash" data-start="8.25" data-duration="0.3" data-track-index="3"></div>
  <div id="bloom" class="clip bloom" data-start="14.55" data-duration="0.55" data-track-index="3"></div>

  <div id="t1" class="clip titulo" data-start="0" data-duration="2.42" data-track-index="4" style="padding-top:230px">
    <div class="mask"><span id="t1a" style="font-size:156px">Quarto</span></div>
    <div class="mask"><span id="t1b" style="font-size:156px"><b>sem graça?</b></span></div>
    <i id="t1r" class="regua"></i></div>
  <div id="t2" class="clip titulo" data-start="2.42" data-duration="2.13" data-track-index="4" style="padding-top:240px">
    <div class="mask"><span id="t2a" style="font-size:120px">Olha o</span></div>
    <div class="mask"><span id="t2b" style="font-size:120px"><b>pé da cama</b></span></div>
    <i id="t2r" class="regua"></i></div>
  <div id="t3" class="clip titulo" data-start="4.62" data-duration="1.33" data-track-index="4" style="padding-top:240px">
    <div class="mask"><span id="t3a" style="font-size:132px">Peseira</span></div>
    <div class="mask"><span id="t3b" style="font-size:132px"><b>de tricô</b></span></div>
    <i id="t3r" class="regua"></i></div>
  <div id="moldura" class="clip" data-start="6.15" data-duration="2.1" data-track-index="4">
    <div id="caixa"><i class="canto c1"></i><i class="canto c2"></i><i class="canto c3"></i><i class="canto c4"></i></div></div>
  <div id="medidas" class="clip" data-start="8.3" data-duration="2.75" data-track-index="4">
    <span class="num"><b id="n220">0</b><span id="xx"> x </span><b id="n60">0</b><span id="cm"> cm</span></span>
    <span id="sub" class="sub">CASAL OU QUEEN</span></div>
  <div id="t4" class="clip titulo" data-start="14.88" data-duration="4.34" data-track-index="4" style="padding-top:220px">
    <div class="mask"><span id="t4a" style="font-size:132px">Escolha</span></div>
    <div class="mask"><span id="t4b" style="font-size:132px">sua <b>cor</b></span></div>
    <div id="cores">{sw_html}</div></div>
  <div id="cta" class="clip" data-start="16.06" data-duration="3.16" data-track-index="5">
    <span id="cta-b">Toque no produto e confira</span>
    <svg id="cta-s" viewBox="0 0 90 90"><path d="M70 14 L22 62 M22 26 L22 66 L62 66" fill="none" stroke="#C9A86A" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
  <div id="rodape" class="clip rodape" data-start="4.55" data-duration="10.0" data-track-index="5"><span>*Dados do fabricante</span></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="0.25" data-duration="4.224" data-track-index="8" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.8" data-duration="9.624" data-track-index="8" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="14.85" data-duration="4.248" data-track-index="8" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-000" data-start="0" data-duration="0.8" data-track-index="9" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-240" data-start="2.36" data-duration="0.3" data-track-index="9" data-volume="0.35" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-442" data-start="4.42" data-duration="0.55" data-track-index="9" data-volume="0.4" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-pop-595" data-start="5.95" data-duration="0.09" data-track-index="9" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-brilho-825" data-start="8.25" data-duration="0.9" data-track-index="9" data-volume="0.35" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-whooshc-1102" data-start="11.02" data-duration="0.3" data-track-index="9" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-brilho-1455" data-start="14.55" data-duration="0.9" data-track-index="9" data-volume="0.32" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-clique-1606" data-start="16.06" data-duration="0.05" data-track-index="9" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
// ---- INTRO: gancho (punch-in + flash creme + título por máscara) ----
tl.fromTo("#camA1",{{scale:1.22}},{{scale:1,duration:0.4,ease:"power3.out"}},0);
tl.to("#camA1",{{scale:1.07,duration:2.0,ease:"none"}},0.4);
tl.fromTo("#flash1",{{opacity:0.32}},{{opacity:0,duration:0.14}},0);
tl.fromTo("#t1a",{{yPercent:110}},{{yPercent:0,duration:0.38,ease:"power4.out"}},0.04);
tl.fromTo("#t1b",{{yPercent:110}},{{yPercent:0,duration:0.38,ease:"power4.out"}},0.14);
tl.fromTo("#t1r",{{scaleX:0}},{{scaleX:1,duration:0.4,ease:"power3.out"}},0.3);
tl.to("#t1b",{{scale:1.06,duration:0.16,yoyo:true,repeat:1,ease:"sine.inOut"}},1.74);
tl.to(["#t1a","#t1b"],{{yPercent:-110,duration:0.2,ease:"power2.in"}},2.2);
tl.to("#t1r",{{scaleX:0,duration:0.18,ease:"power2.in"}},2.2);
// corte para o close da trança
tl.fromTo("#camA2",{{scale:1.16}},{{scale:1.03,duration:0.3,ease:"power3.out"}},2.4);
tl.to("#camA2",{{scale:1.1,duration:1.55,ease:"none"}},2.7);
tl.to("#camA2",{{scale:1.32,duration:0.3,ease:"power2.in"}},4.25);
tl.fromTo("#t2a",{{yPercent:110}},{{yPercent:0,duration:0.34,ease:"power4.out"}},2.46);
tl.fromTo("#t2b",{{yPercent:110}},{{yPercent:0,duration:0.34,ease:"power4.out"}},2.56);
tl.fromTo("#t2r",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power3.out"}},2.7);
tl.to("#t2b",{{scale:1.06,duration:0.14,yoyo:true,repeat:1,ease:"sine.inOut"}},3.5);
tl.to(["#t2a","#t2b"],{{yPercent:-110,duration:0.18,ease:"power2.in"}},4.32);
tl.to("#t2r",{{scaleX:0,duration:0.16,ease:"power2.in"}},4.32);
// ---- APRESENTAÇÃO ----
tl.fromTo("#camB1",{{scale:1.25}},{{scale:1,duration:0.35,ease:"power3.out"}},4.55);
tl.to("#camB1",{{scale:1.06,duration:1.05,ease:"none"}},4.9);
tl.fromTo("#t3a",{{yPercent:110}},{{yPercent:0,duration:0.36,ease:"power4.out"}},4.66);
tl.fromTo("#t3b",{{yPercent:110}},{{yPercent:0,duration:0.36,ease:"power4.out"}},4.76);
tl.fromTo("#t3r",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power3.out"}},4.9);
tl.to(["#t3a","#t3b"],{{yPercent:-110,duration:0.18,ease:"power2.in"}},5.76);
tl.to("#t3r",{{scaleX:0,duration:0.16,ease:"power2.in"}},5.76);
// zoom no detalhe citado (tranças) + moldura de cantos
tl.fromTo("#camB2",{{scale:1.5,x:-150,y:-280}},{{scale:1.3,x:-150,y:-280,duration:0.3,ease:"power3.out"}},5.95);
tl.to("#camB2",{{scale:1.38,duration:2.0,ease:"none"}},6.25);
tl.fromTo("#caixa",{{scale:1.3,opacity:0}},{{scale:1,opacity:1,duration:0.32,ease:"back.out(2)"}},6.19);
tl.to("#caixa",{{scale:1.04,duration:0.5,yoyo:true,repeat:1,ease:"sine.inOut"}},6.6);
tl.to("#caixa",{{opacity:0,duration:0.2}},7.98);
// produto herói: congelamento vira cartão com contorno dourado
tl.fromTo("#flash2",{{opacity:0.55}},{{opacity:0,duration:0.28}},8.25);
tl.fromTo("#card",{{scale:1.317,y:-199}},{{scale:1,y:0,duration:0.45,ease:"power3.inOut"}},8.27);
tl.to("#card",{{scale:1.035,duration:2.3,ease:"none"}},8.72);
tl.fromTo("#reflexo",{{xPercent:-110}},{{xPercent:110,duration:0.8,ease:"power2.inOut"}},8.55);
tl.fromTo("#n220",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.2}},8.55);
{chr(10).join(cont)}
tl.fromTo("#xx",{{opacity:0}},{{opacity:1,duration:0.15}},9.56);
tl.fromTo("#n60",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.2}},9.62);
tl.fromTo("#cm",{{opacity:0}},{{opacity:1,duration:0.2}},10.17);
tl.fromTo("#sub",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.35,ease:"power2.out"}},10.3);
tl.fromTo("#medidas",{{opacity:1}},{{opacity:0,duration:0.15}},10.9);
// volta ao movimento; quebra em "casal"
tl.fromTo("#camB3",{{scale:1.2}},{{scale:1.08,duration:0.3,ease:"power3.out"}},11.05);
tl.to("#camB3",{{scale:1.12,duration:1.48,ease:"none"}},11.37);
tl.to("#camB3",{{scale:1.22,duration:0.25,ease:"power3.out"}},12.86);
tl.to("#camB3",{{scale:1.26,duration:1.44,ease:"none"}},13.11);
tl.fromTo("#rodape span",{{opacity:0}},{{opacity:1,duration:0.2}},4.6);
// ---- CTA: luz quente, título, cores, botão ----
tl.fromTo("#bloom",{{opacity:0.8}},{{opacity:0,duration:0.5,ease:"power2.out"}},14.55);
tl.fromTo("#camC",{{scale:1.14}},{{scale:1,duration:0.45,ease:"power3.out"}},14.55);
tl.to("#camC",{{scale:1.05,duration:4.2,ease:"none"}},15.0);
tl.fromTo("#t4a",{{yPercent:110}},{{yPercent:0,duration:0.4,ease:"power4.out"}},14.9);
tl.fromTo("#t4b",{{yPercent:110}},{{yPercent:0,duration:0.4,ease:"power4.out"}},15.0);
{sw_js}
tl.fromTo("#cta-b",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.2)"}},16.06);
tl.to("#cta-b",{{scale:1.05,duration:0.4,yoyo:true,repeat:5,ease:"sine.inOut"}},16.5);
tl.fromTo("#cta-s",{{opacity:0,x:20,y:-20}},{{opacity:1,x:0,y:0,duration:0.25}},16.2);
tl.to("#cta-s",{{x:-12,y:14,duration:0.35,yoyo:true,repeat:7,ease:"sine.inOut"}},16.5);
// ---- legenda karaokê ----
{chr(10).join(leg_js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(OUT, "w").write(html)
print("ok", OUT)
