#!/usr/bin/env python3
"""Gera produtos/bodysplash/edicao_E/index.html ("pirâmide de notas": tabaco / bergamota / cedro,
Bricolage Grotesque 800 + Inter 800, legenda névoa). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Combinação cruzada (vídeo E, "do cítrico ao amadeirado"), sem crédito para clipe novo. Regra número 1 (3ª violação,
quadro estático): o vídeo de fundo roda do primeiro ao último quadro. Não há <img>, quadro congelado nem cartão.
Trechos (analise_E.md):
  intro        F 0,00-3,85 s em 1,0x   (mãos trazendo a bandeja)
  apresentação A 5,55-7,95 s em 0,77x  (frascos subindo da caixa entre fumaça; enquadrado nos frascos)
               D 4,95-7,95 s em 0,9x   (quadro nítido y 420-1498 sobre o próprio clipe desfocado; antes de ~5 s
                                        o reflexo ainda clareia o Midtown e o Barbarius)
               E 2,00-5,50 s em 1,0x   (ancorado no alto, escala >= 1,1 e y -150: "bodyman" sempre fora do quadro)
  CTA          F 4,00-7,83 s em 0,85x  (continua de onde a intro parou)
Nenhuma nota ligada a frasco: as notas aparecem só no alto (título, régua TOPO/MEIO/FUNDO, pílula) e na legenda;
nada é desenhado perto dos frascos e nenhum efeito passa sobre os rótulos (luzes só acima das tampas).
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 3.85, 0.25), "apresentacao": (3.85, 13.8, 4.05), "cta": (13.8, 18.3, 14.1)}
TOTAL = 18.3
DUR_MP3 = {"intro": 3.552, "apresentacao": 9.696, "cta": 4.152}
TOPO_LEG = 1290
# cortes da apresentação
T_AD = 6.97   # A -> D (entre "cítricas" e "terminam")
T_DE = 10.3   # D -> E (entre "meio" e "flor")

GRUPOS = {
    "intro": [[0, 1], [2, 3], [4], [5, 6, 7]],
    "apresentacao": [[0, 1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14, 15], [16, 17, 18],
                     [19, 20, 21], [22], [23, 24], [25, 26]],
    "cta": [[0, 1], [2, 3], [4, 5, 6], [7, 8], [9, 10]],
}
# família de cada palavra-chave: ci = cítrico (bergamota), ma = madeira (cedro), me = meio (degradê), br = marca
CHAVE = {
    "intro": {1: "ci", 4: "ma", 7: "br"},
    "apresentacao": {1: "br", 2: "br", 8: "ci", 12: "ma", 13: "ma", 15: "ma", 18: "me", 19: "me", 21: "me",
                     22: "me", 26: "me"},
    "cta": {1: "me", 4: "ma"},
}
EXIBE = {("intro", 4): "amadeirado:", ("intro", 7): "kit?", ("apresentacao", 2): "Man:",
         ("apresentacao", 12): "madeira,", ("apresentacao", 15): "musk.", ("apresentacao", 18): "meio:",
         ("apresentacao", 21): "laranjeira,", ("apresentacao", 22): "especiarias", ("apresentacao", 26): "doce.",
         ("cta", 3): "prefere?", ("cta", 10): "três."}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---- legenda névoa: cada palavra se condensa do desfoque no seu tempo; palavra-chave na cor da sua nota ----
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
            t = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.04, 3)
            fam = CHAVE[parte].get(wi, "")
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            over = f'<em class="gx" aria-hidden="true">{txt}</em>' if fam == "me" else ""
            spans += f'<span id="{gid}-{k}" class="pal {fam}"><em class="tx">{txt}</em>{over}</span>'
            leg_js.append(
                f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:14,scale:1.08,filter:"blur(10px)"}},'
                f'{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:0.16,ease:"power2.out"}},{t});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{TOPO_LEG}px">{spans}</div></div>'
        )

# ---- partículas de "notas" subindo só na faixa do alto (acima das tampas): (x, y, tamanho, opacidade) ----
# cor sólida + box-shadow (sem radial-gradient: o lint avisa que muitos overlays "pesados" podem dar quadro preto)
DOTS = [(90, 300, 12, .6), (190, 140, 8, .55), (300, 380, 14, .45), (420, 90, 9, .55), (520, 330, 7, .6),
        (610, 200, 13, .5), (700, 360, 9, .6), (790, 110, 15, .4), (870, 260, 10, .55), (960, 380, 12, .5),
        (1010, 170, 8, .55), (360, 240, 10, .5)]
CICLO = 3.0
dot_html, dot_js = [], []
for nome, cor in (("m", "#A6F0C8"), ("c", "#DE8A50")):
    dot_html.append(f'  <div id="nt-{nome}" class="clip notas" data-start="0" data-duration="{TOTAL}" data-track-index="2"><span id="nt-{nome}-in" class="ntin">')
    for i, (x, y, sz, o) in enumerate(DOTS):
        if (i % 2 == 0) != (nome == "m"):
            continue
        dot_html.append(f'    <i id="nt-{nome}{i}" class="dot" style="left:{x}px;top:{y}px;width:{sz}px;height:{sz}px;'
                        f'background:{cor};box-shadow:0 0 {sz}px {round(sz / 2)}px {cor}"></i>')
        off = round((i * 0.37) % CICLO, 2)
        rep = int((TOTAL - off) / CICLO) + 1
        dot_js.append(
            f'tl.fromTo("#nt-{nome}{i}",{{x:0,y:0,opacity:0}},{{keyframes:[{{opacity:{o},duration:0.6}},'
            f'{{x:{(-1) ** i * (14 + 5 * (i % 4))},y:-{90 + 10 * (i % 5)},opacity:{round(o * 0.5, 2)},duration:1.8}},'
            f'{{opacity:0,duration:0.6}}],repeat:{rep},ease:"none"}},{off});')
    dot_html.append("  </span></div>")

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* nomes completos das fontes do container (Bricolage e Inter são variáveis) */
@font-face{font-family:"Bricolage Notas";font-weight:200 800;src:local("Bricolage Grotesque 96pt ExtraBold")}
@font-face{font-family:"Inter Notas";font-weight:100 900;src:local("Inter Thin"),local("Inter-Thin"),local("Inter")}
:root{--tabaco:#1E140E;--berg:#A6F0C8;--cedro:#DE8A50;--marfim:#FBF6EE;
  --degrade:linear-gradient(90deg,#A6F0C8 0%,#D9D4A0 48%,#DE8A50 100%)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#1E140E}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#1E140E;font-family:"Inter Notas";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camF1{transform-origin:50% 10%}
#camA{transform-origin:50% 0%}
#camE{transform-origin:50% 0%}
#camF2{transform-origin:50% 50%}
/* clipe D: cópia desfocada e escurecida enchendo a tela + quadro nítido (y 420-1498) com moldura em degradê */
#camDb{transform-origin:50% 50%}
#vDb{filter:blur(34px) brightness(.48) saturate(1.15)}
#camDf{position:absolute;inset:0;z-index:1;transform-origin:50% 959px}
#dqwin{position:absolute;left:0;top:420px;width:1080px;height:1078px;overflow:hidden;display:block}
#vDf{position:absolute;left:0;top:-420px;width:1080px;height:1920px;object-fit:cover}
#dqf{z-index:1}
#dqb{position:absolute;left:-8px;top:412px;width:1096px;height:1094px;display:block;transform-origin:548px 547px;
  border:8px solid transparent;border-image:linear-gradient(160deg,#A6F0C8 0%,#D9D4A0 45%,#DE8A50 100%) 1;
  box-shadow:0 30px 60px rgba(0,0,0,.55)}
/* luzes só na faixa do alto (acima das tampas), nunca sobre os rótulos */
#luzes{z-index:2;overflow:hidden;height:440px;bottom:auto;
  -webkit-mask-image:linear-gradient(to bottom,#000 0,#000 55%,transparent 100%);mask-image:linear-gradient(to bottom,#000 0,#000 55%,transparent 100%)}
.lz{position:absolute;display:block;border-radius:50%;mix-blend-mode:screen}
#lzM{left:-260px;top:-420px;width:820px;height:820px;background:radial-gradient(closest-side,rgba(166,240,200,.55) 0,rgba(166,240,200,.2) 45%,rgba(166,240,200,0) 100%)}
#lzC{left:520px;top:-420px;width:820px;height:820px;background:radial-gradient(closest-side,rgba(222,138,80,.6) 0,rgba(222,138,80,.22) 45%,rgba(222,138,80,0) 100%)}
.notas{z-index:2;overflow:hidden}
.ntin{position:absolute;inset:0;display:block}
.dot{position:absolute;display:block;border-radius:50%}
/* névoa da passagem intro -> apresentação */
#nevoa{z-index:8;overflow:hidden}
#nv-b{position:absolute;left:-200px;top:0;width:1480px;height:900px;display:block;border-radius:50%;
  background:radial-gradient(closest-side,rgba(240,250,244,.95) 0,rgba(214,244,228,.7) 40%,rgba(214,244,228,0) 100%)}
/* virada de nota (A -> D): faixa opaca de bordas duras (cobre os rótulos, nunca tinge) */
#virada{z-index:8;overflow:hidden}
#vr-b{position:absolute;left:-700px;top:-200px;width:520px;height:2320px;display:block;
  background:linear-gradient(90deg,#A6F0C8 0,#A6F0C8 50%,#DE8A50 50%,#DE8A50 100%)}
/* brilho correndo nas tampas (CTA, só a faixa das tampas) */
#brilho{z-index:2}
#br-m{position:absolute;left:0;top:%%BR_T%%px;width:1080px;height:%%BR_H%%px;overflow:hidden;display:block}
#br-b{position:absolute;left:0;top:-300px;width:280px;height:1000px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,252,246,.82) 50%,rgba(255,255,255,0) 100%)}
.vinheta{z-index:3;background:radial-gradient(ellipse 96% 72% at 50% 50%,rgba(0,0,0,0) 62%,rgba(30,20,14,.5) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(30,20,14,.72) 0,rgba(30,20,14,.42) 14%,rgba(30,20,14,0) 28%)}
.baixo{z-index:3;background:linear-gradient(to top,rgba(30,20,14,.7) 0,rgba(30,20,14,.35) 12%,rgba(30,20,14,0) 24%)}
.flash{z-index:9;background:#FBF6EE;opacity:0}
/* títulos: Bricolage 800, centralizados na área segura (40-918 px) */
.titulo{z-index:6}
.tw{position:absolute;left:40px;width:878px;display:flex;justify-content:center;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}
.mask{position:absolute;left:40px;width:878px;overflow:hidden;display:flex;justify-content:center;filter:drop-shadow(0 6px 18px rgba(0,0,0,.6))}
.tt{display:block;font-family:"Bricolage Notas";font-weight:800;line-height:1.0;white-space:nowrap;color:var(--marfim);letter-spacing:-2px}
.tt .b{color:var(--berg)}
.tt .c{color:var(--cedro)}
.tt .g{background:var(--degrade);-webkit-background-clip:text;background-clip:text;color:transparent}
/* régua da pirâmide: TOPO / MEIO / FUNDO */
.regua{position:absolute;left:119px;width:720px;height:70px;display:block}
.rg-bar{position:absolute;left:0;top:10px;width:720px;height:10px;display:block;border-radius:5px;background:var(--degrade);
  transform-origin:0 50%;box-shadow:0 4px 14px rgba(0,0,0,.45)}
.rg-p{position:absolute;top:2px;width:26px;height:26px;margin-left:-13px;display:block;border-radius:50%;
  background:var(--tabaco);box-shadow:inset 0 0 0 4px var(--marfim)}
.rg-p i{position:absolute;inset:5px;display:block;border-radius:50%;opacity:0}
.rg-l{position:absolute;top:38px;width:160px;margin-left:-80px;display:block;text-align:center;font-family:"Inter Notas";font-weight:800;
  font-size:24px;letter-spacing:4px;color:var(--marfim);opacity:.55;text-shadow:0 2px 8px rgba(0,0,0,.8)}
/* pílula da linha secundária */
.pill{display:block;white-space:nowrap;background:rgba(30,20,14,.86);color:var(--marfim);font-family:"Inter Notas";font-weight:800;
  font-size:38px;line-height:1;padding:15px 28px 17px;border-radius:40px;box-shadow:0 10px 24px rgba(0,0,0,.4)}
.pill .b{color:var(--berg)}
.pill .c{color:var(--cedro)}
.pill .it{display:inline-block;opacity:.28}
.pill .sep{opacity:.5;padding:0 10px}
.pill.borda{box-shadow:inset 0 0 0 3px rgba(251,246,238,.0),0 10px 24px rgba(0,0,0,.4);border:3px solid transparent;
  background:linear-gradient(rgba(30,20,14,.9),rgba(30,20,14,.9)) padding-box,var(--degrade) border-box}
/* rodapé */
#rodape{z-index:7}
#rd{position:absolute;left:40px;top:1466px;display:block;font-family:"Inter Notas";font-weight:700;font-size:30px;line-height:1;
  color:rgba(255,255,255,.82);background:rgba(30,20,14,.55);padding:8px 14px 10px;border-radius:10px}
/* legenda névoa */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start;gap:18px;flex-wrap:nowrap}
.pal{position:relative;display:block;font-family:"Inter Notas";font-weight:800;font-size:70px;line-height:1.12;white-space:nowrap}
.tx{position:relative;display:block;font-style:normal;color:var(--marfim);-webkit-text-stroke:8px var(--tabaco);paint-order:stroke fill;
  text-shadow:0 8px 20px rgba(0,0,0,.6)}
.pal.ci .tx{color:var(--berg)}
.pal.ma .tx{color:var(--cedro)}
.pal.br .tx{color:var(--marfim)}
.gx{position:absolute;left:0;top:0;display:block;font-style:normal;background:var(--degrade);-webkit-background-clip:text;background-clip:text;color:transparent}
/* CTA: botão em degradê com seta para baixo/esquerda + "toca no produto" */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border-radius:50%;background:var(--degrade);
  box-shadow:0 0 0 6px rgba(30,20,14,.92),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:116px;height:116px}
#tq-o{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border:7px solid var(--cedro);border-radius:50%;opacity:0}
#tq-l{position:absolute;left:196px;top:1426px;display:block}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO (0-3,85 s): clipe F 0-3,85 s, mãos trazendo a bandeja -->
  <div id="camF1" class="cam"><video id="vF1" class="clip full" data-start="0" data-duration="3.85" data-media-start="0" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO 1 (3,85-6,97 s): clipe A (lote A) 5,55-7,95 s em 0,77x, frascos subindo da caixa -->
  <div id="camA" class="cam"><video id="vA" class="clip full" data-start="3.85" data-duration="3.12" data-media-start="5.55" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_A.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO 2 (6,97-10,3 s): clipe D 4,95-7,95 s em 0,9x; fundo = o próprio clipe desfocado, quadro nítido por cima -->
  <div id="camDb" class="cam"><video id="vDb" class="clip full" data-start="6.97" data-duration="3.36" data-media-start="4.92" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_D.mp4" muted playsinline></video></div>
  <div id="camDf"><span id="dqwin"><video id="vDf" class="clip" data-start="6.97" data-duration="3.33" data-media-start="4.95" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_D.mp4" muted playsinline></video></span></div>
  <div id="dqf" class="clip" data-start="6.97" data-duration="3.33" data-track-index="3"><i id="dqb"></i></div>
  <!-- APRESENTAÇÃO 3 (10,3-13,8 s): clipe E 2,0-5,5 s, ancorado no alto (escala >= 1,1, y -150): "bodyman" fora -->
  <div id="camE" class="cam"><video id="vE" class="clip full" data-start="10.3" data-duration="3.5" data-media-start="2" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <!-- CTA (13,8-18,3 s): clipe F 4,0-7,83 s em 0,85x -->
  <div id="camF2" class="cam"><video id="vF2" class="clip full" data-start="13.8" data-duration="4.5" data-media-start="4" data-playback-rate="0.85" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>

  <div id="luzes" class="clip" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"><i id="lzM" class="lz"></i><i id="lzC" class="lz"></i></div>
%%DOT_HTML%%
  <div id="brilho" class="clip" data-start="%%BR_S%%" data-duration="0.8" data-track-index="4"><span id="br-m"><i id="br-b"></i></span></div>
  <div id="baixo" class="clip baixo" data-start="0" data-duration="%%TOTAL%%" data-track-index="4"></div>
  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="5"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="11"></div>

  <!-- intro: "DO CÍTRICO" bate; a régua em degradê se desenha em "termina"; "À MADEIRA" sobe em "amadeirado" -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="3.85" data-track-index="6">
    <div id="t1-g" style="position:absolute;left:0;top:0;width:1080px;height:600px;display:block">
      <div class="tw" style="top:196px"><div id="t1-a" class="tt" style="font-size:124px">DO <span class="b">CÍTRICO</span></div></div>
      <span id="t1-r" class="rg-bar" style="left:159px;top:338px;width:640px"></span>
      <div class="mask" style="top:362px;height:132px"><div id="t1-b" class="tt" style="font-size:124px">À <span class="c">MADEIRA</span></div></div>
    </div>
    <div class="tw" style="top:448px"><div id="t1-p" class="pill borda">conhece esse kit?</div></div>
  </div>

  <!-- apresentação: título que troca + régua TOPO / MEIO / FUNDO + pílula (nada aponta para frasco) -->
  <div id="t2" class="clip titulo" data-start="3.85" data-duration="9.95" data-track-index="7">
    <div id="t2-g" style="position:absolute;left:0;top:0;width:1080px;height:600px;display:block">
      <div class="mask" style="top:190px;height:132px"><div id="t2-a" class="tt" style="font-size:118px">TOPO <span class="b">CÍTRICO</span></div></div>
      <div class="mask" style="top:190px;height:132px"><div id="t2-b" class="tt" style="font-size:118px">O MEIO <span class="g">MUDA</span></div></div>
      <span id="rg" class="regua" style="top:326px">
        <i id="rg-bar" class="rg-bar"></i>
        <i id="rg-p1" class="rg-p" style="left:0"><i id="rg-p1i" style="background:#A6F0C8"></i></i>
        <i id="rg-p2" class="rg-p" style="left:360px"><i id="rg-p2i" style="background:linear-gradient(90deg,#A6F0C8,#DE8A50)"></i></i>
        <i id="rg-p3" class="rg-p" style="left:720px"><i id="rg-p3i" style="background:#DE8A50"></i></i>
        <b id="rg-l1" class="rg-l" style="left:0">TOPO</b>
        <b id="rg-l2" class="rg-l" style="left:360px">MEIO</b>
        <b id="rg-l3" class="rg-l" style="left:720px">FUNDO</b>
      </span>
    </div>
    <div class="tw" style="top:418px"><div id="t2-p" class="pill">fundo: <span class="c">madeira, âmbar e musk</span></div></div>
    <div class="tw" style="top:418px"><div id="t2-q" class="pill borda"><span id="it1" class="it">flor</span><span class="sep">•</span><span id="it2" class="it">especiarias</span><span class="sep">•</span><span id="it3" class="it">doce</span></div></div>
  </div>
  <div id="rodape" class="clip" data-start="3.85" data-duration="9.95" data-track-index="10"><span id="rd">*Notas olfativas do fabricante</span></div>

  <!-- CTA: "QUAL NOTA / É A SUA?" no silêncio; botão com seta para baixo/esquerda em "Toca" -->
  <div id="t3" class="clip titulo" data-start="13.86" data-duration="4.44" data-track-index="8">
    <div class="mask" style="top:186px;height:130px"><div id="t3-a" class="tt" style="font-size:118px">QUAL <span class="g">NOTA</span></div></div>
    <div class="mask" style="top:312px;height:130px"><div id="t3-b" class="tt" style="font-size:118px">É A SUA?</div></div>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="9">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#1E140E" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <span id="tq-l" class="pill">toca no produto</span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="13"></div>
  <div id="nevoa" class="clip" data-start="3.62" data-duration="0.5" data-track-index="13"><i id="nv-b"></i></div>
  <div id="virada" class="clip" data-start="6.84" data-duration="0.36" data-track-index="14"><i id="vr-b"></i></div>
  <div id="fl2" class="clip flash" data-start="10.28" data-duration="0.12" data-track-index="15"></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="%%DV1%%" data-track-index="16" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.05" data-duration="%%DV2%%" data-track-index="16" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="14.1" data-duration="%%DV3%%" data-track-index="16" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="17" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%SPOP%%" data-duration="0.09" data-track-index="17" data-volume="0.36" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="3.6" data-duration="0.55" data-track-index="18" data-volume="0.36" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-whoosh-2" data-start="6.84" data-duration="0.3" data-track-index="18" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-3" data-start="10.16" data-duration="0.3" data-track-index="18" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="13.2" data-duration="0.6" data-media-start="0.8" data-track-index="18" data-volume="0.36" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="17" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-brilho-1" data-start="%%SBRI%%" data-duration="0.9" data-track-index="17" data-volume="0.3" src="assets/sfx/brilho.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (clipe F): flash + punch-in no impacto; "DO CÍTRICO" bate; régua; "À MADEIRA" sobe ----
tl.fromTo("#fl1", {opacity:0.9}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camF1", {scale:1.24, filter:"blur(0px)"}, {scale:1.05, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camF1", {scale:1.08, duration:%%DFA%%, ease:"none"}, 0.4);
tl.to("#camF1", {scale:1.12, duration:0.14, ease:"power2.out"}, %%TAMA%%);
tl.to("#camF1", {scale:1.1, duration:%%DFB%%, ease:"none"}, %%TAMA2%%);
tl.fromTo("#t1-a", {scale:1.7, opacity:0, filter:"blur(14px)", transformOrigin:"50% 60%"}, {scale:1, opacity:1, filter:"blur(0px)", duration:0.3, ease:"back.out(1.7)"}, 0.04);
tl.fromTo("#t1-r", {scaleX:0}, {scaleX:1, duration:%%DREG%%, ease:"power1.inOut"}, %%TREG%%);
tl.fromTo("#t1-b", {yPercent:110, filter:"blur(8px)"}, {yPercent:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%TAMA%%);
// em "conhece": o título recolhe para o alto e a pílula abre
tl.fromTo("#t1-g", {scale:1, transformOrigin:"50% 196px"}, {scale:0.8, duration:0.3, ease:"power3.inOut"}, %%TPILL%%);
tl.fromTo("#t1-p", {clipPath:"inset(0% 50% 0% 50% round 40px)", opacity:0}, {clipPath:"inset(0% 0% 0% 0% round 40px)", opacity:1, duration:0.3, ease:"power3.out"}, %%TPILL2%%);
// luzes: bergamota no cítrico, cedro sobe no amadeirado
tl.fromTo("#lzM", {opacity:0, x:-120}, {opacity:1, x:60, duration:1.2, ease:"power1.out"}, 0);
tl.fromTo("#lzC", {opacity:0, x:120}, {opacity:0.85, x:-40, duration:1.2, ease:"power1.out"}, %%TAMA%%);
tl.to("#lzM", {opacity:0.4, duration:1.0, ease:"none"}, %%TAMA%%);
// passagem: névoa clara sobe pela tela; F sai com zoom e desfoque
tl.to("#camF1", {scale:1.3, filter:"blur(16px)", duration:0.18, ease:"power2.in"}, 3.67);
tl.to("#t1-g", {opacity:0, y:-30, duration:0.18, ease:"power2.in"}, 3.66);
tl.to("#t1-p", {opacity:0, duration:0.15, ease:"power2.in"}, 3.66);
tl.fromTo("#nv-b", {y:1500, opacity:0.85}, {y:-1000, opacity:0.85, duration:0.48, ease:"power1.inOut"}, 3.62);

// ---- APRESENTAÇÃO 1 (clipe A): entra da névoa; câmera acompanha os frascos subindo; punch em "os três" ----
tl.fromTo("#camA", {scale:1.5, x:0, filter:"blur(16px)"}, {scale:1.38, filter:"blur(0px)", duration:0.32, ease:"power3.out"}, 3.85);
tl.to("#camA", {scale:1.28, duration:%%DA1%%, ease:"none"}, 4.17);
tl.to("#camA", {scale:1.33, duration:0.14, ease:"power2.out"}, %%TTRES%%);
tl.to("#camA", {scale:1.16, duration:%%DA2%%, ease:"power1.inOut"}, %%TTRES2%%);
tl.to("#lzM", {opacity:1, x:0, duration:0.6, ease:"power1.out"}, 3.85);
tl.to("#lzC", {opacity:0.15, x:80, duration:0.6, ease:"power1.out"}, 3.85);
// títulos e régua
tl.fromTo("#t2-a", {yPercent:110, filter:"blur(8px)"}, {yPercent:0, filter:"blur(0px)", duration:0.32, ease:"power3.out"}, 3.95);
tl.fromTo("#rg-bar", {scaleX:0}, {scaleX:1, duration:0.5, ease:"power2.out"}, 4.12);
tl.fromTo(["#rg-p1", "#rg-p2", "#rg-p3", "#rg-l1", "#rg-l2", "#rg-l3"], {opacity:0, y:8}, {opacity:1, y:0, duration:0.22, stagger:0.06, ease:"power2.out"}, 4.3);
tl.set(["#rg-l1", "#rg-l2", "#rg-l3"], {opacity:0.55}, 4.7);
tl.fromTo("#rd", {opacity:0}, {opacity:1, duration:0.3, ease:"none"}, 3.95);
// TOPO acende em "cítricas"
tl.fromTo("#rg-p1i", {opacity:0, scale:0.3}, {opacity:1, scale:1, duration:0.2, ease:"back.out(2)"}, %%TCIT%%);
tl.fromTo("#rg-p1", {scale:1}, {scale:1.35, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TCIT%%);
tl.fromTo("#rg-l1", {opacity:0.55}, {opacity:1, duration:0.2, ease:"none", immediateRender:false}, %%TCIT%%);
// passagem A -> D: virada de nota (faixa bergamota -> cedro atravessa)
tl.to("#camA", {scale:1.3, x:-60, filter:"blur(14px)", duration:0.15, ease:"power2.in"}, 6.82);
tl.fromTo("#vr-b", {x:0}, {x:1900, duration:0.36, ease:"power2.inOut"}, 6.84);

// ---- APRESENTAÇÃO 2 (clipe D): quadro nítido entra e respira; fundo desfocado do próprio clipe ----
tl.fromTo("#camDb", {scale:2.05}, {scale:1.85, duration:3.33, ease:"none"}, 6.97);
tl.fromTo(["#camDf", "#dqb"], {scale:0.7, rotation:-3, filter:"blur(10px)"}, {scale:0.9, rotation:0, filter:"blur(0px)", duration:0.34, ease:"back.out(1.5)"}, 6.97);
tl.to(["#camDf", "#dqb"], {scale:0.92, duration:%%DD1%%, ease:"none"}, 7.31);
tl.to(["#camDf", "#dqb"], {scale:0.96, duration:0.14, ease:"power2.out"}, %%TMAD%%);
tl.to(["#camDf", "#dqb"], {scale:0.95, duration:%%DD2%%, ease:"none"}, %%TMAD2%%);
tl.to(["#camDf", "#dqb"], {scale:0.98, duration:0.14, ease:"power2.out"}, %%TMUDA%%);
tl.to(["#camDf", "#dqb"], {scale:0.975, duration:%%DD3%%, ease:"none"}, %%TMUDA2%%);
tl.to("#lzC", {opacity:1, x:0, duration:0.5, ease:"power1.out"}, 6.97);
tl.to("#lzM", {opacity:0.12, x:-80, duration:0.5, ease:"power1.out"}, 6.97);
tl.fromTo("#t2-p", {clipPath:"inset(0% 50% 0% 50% round 40px)", opacity:0}, {clipPath:"inset(0% 0% 0% 0% round 40px)", opacity:1, duration:0.3, ease:"power3.out"}, 7.0);
// FUNDO acende em "madeira"
tl.fromTo("#rg-p3i", {opacity:0, scale:0.3}, {opacity:1, scale:1, duration:0.2, ease:"back.out(2)"}, %%TMAD%%);
tl.fromTo("#rg-p3", {scale:1}, {scale:1.35, duration:0.16, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TMAD%%);
tl.fromTo("#rg-l3", {opacity:0.55}, {opacity:1, duration:0.2, ease:"none", immediateRender:false}, %%TMAD%%);
// "O MEIO MUDA": título rola; MEIO acende; pílula troca para as notas do meio
tl.to("#t2-a", {yPercent:-110, duration:0.28, ease:"power3.in"}, %%TSWAP%%);
tl.fromTo("#t2-b", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, %%TSWAP2%%);
tl.fromTo("#rg-p2i", {opacity:0, scale:0.3}, {opacity:1, scale:1, duration:0.2, ease:"back.out(2)"}, %%TMUDA%%);
tl.fromTo("#rg-p2", {scale:1}, {scale:1.45, duration:0.18, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TMUDA%%);
tl.fromTo("#rg-l2", {opacity:0.55}, {opacity:1, duration:0.2, ease:"none", immediateRender:false}, %%TMUDA%%);
tl.to(["#rg-l1", "#rg-l3"], {opacity:0.4, duration:0.2, ease:"none"}, %%TMUDA%%);
tl.to(["#rg-p1i", "#rg-p3i"], {opacity:0.35, duration:0.2, ease:"none"}, %%TMUDA%%);
tl.to("#t2-p", {opacity:0, y:-12, duration:0.18, ease:"power2.in"}, %%TSWAP%%);
tl.fromTo("#t2-q", {clipPath:"inset(0% 50% 0% 50% round 40px)", opacity:0}, {clipPath:"inset(0% 0% 0% 0% round 40px)", opacity:1, duration:0.3, ease:"power3.out"}, %%TQ%%);
// passagem D -> E: o quadro abre até encher a tela
tl.to(["#camDf", "#dqb"], {scale:1.25, filter:"blur(12px)", duration:0.16, ease:"power2.in"}, 10.14);
tl.to("#dqb", {opacity:0, duration:0.16, ease:"power2.in"}, 10.14);
tl.fromTo("#fl2", {opacity:0}, {keyframes:[{opacity:0.45, duration:0.04}, {opacity:0, duration:0.08}], ease:"none"}, 10.28);

// ---- APRESENTAÇÃO 3 (clipe E): ancorado no alto; punch leve em cada nota do meio (os três juntos) ----
tl.fromTo("#camE", {scale:1.24, y:-150, filter:"blur(12px)"}, {scale:1.1, y:-150, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, 10.3);
tl.to("#camE", {scale:1.115, duration:%%DE1%%, ease:"none"}, 10.6);
tl.to("#camE", {scale:1.14, duration:0.14, ease:"power2.out"}, %%TESP%%);
tl.to("#camE", {scale:1.13, duration:%%DE2%%, ease:"none"}, %%TESP2%%);
tl.to("#camE", {scale:1.16, duration:0.14, ease:"power2.out"}, %%TDOCE%%);
tl.to("#camE", {scale:1.155, duration:%%DE3%%, ease:"none"}, %%TDOCE2%%);
tl.to("#lzM", {opacity:0.35, x:40, duration:0.5, ease:"power1.out"}, 10.3);
// no E a régua já cumpriu o papel: sai, e a pílula das notas do meio sobe para o lugar dela (menos coisa sobre as tampas)
tl.to("#rg", {opacity:0, y:-10, duration:0.2, ease:"power2.in"}, 10.16);
tl.to("#t2-q", {y:-88, duration:0.3, ease:"power3.out"}, 10.3);
tl.to("#lzC", {opacity:0.35, x:-40, duration:0.5, ease:"power1.out"}, 10.3);
tl.to("#it1", {opacity:1, duration:0.18, ease:"none"}, %%TFLOR%%);
tl.to("#it2", {opacity:1, duration:0.18, ease:"none"}, %%TESP%%);
tl.to("#it3", {opacity:1, duration:0.18, ease:"none"}, %%TDOCE%%);
tl.fromTo("#t2-q", {scale:1}, {scale:1.05, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TDOCE%%);
// passagem para a CTA: mergulho com desfoque
tl.to("#camE", {scale:1.32, filter:"blur(16px)", duration:0.16, ease:"power2.in"}, 13.64);
tl.to("#t2-g", {opacity:0, y:-24, duration:0.16, ease:"power2.in"}, 13.62);
tl.to("#t2-q", {opacity:0, duration:0.14, ease:"power2.in"}, 13.62);
tl.to("#rd", {opacity:0, duration:0.14, ease:"none"}, 13.62);

// ---- CTA (clipe F): mais calma; pergunta no silêncio; botão em "Toca"; brilho nas tampas em "os três" ----
tl.fromTo("#camF2", {scale:1.2, filter:"blur(14px)"}, {scale:1.04, filter:"blur(0px)", duration:0.32, ease:"power3.out"}, 13.8);
tl.to("#camF2", {scale:1.07, duration:%%DC1%%, ease:"none"}, 14.12);
tl.to("#camF2", {scale:1.1, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camF2", {scale:1.12, duration:%%DC2%%, ease:"none"}, %%TTOCA2%%);
tl.to(["#lzM", "#lzC"], {opacity:0.5, x:0, duration:0.6, ease:"power1.out"}, 13.8);
tl.fromTo("#t3-a", {yPercent:110, filter:"blur(8px)"}, {yPercent:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, 13.9);
tl.fromTo("#t3-b", {yPercent:110, filter:"blur(8px)"}, {yPercent:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, 14.02);
tl.fromTo("#t3-a", {scale:1}, {scale:1.06, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false, transformOrigin:"50% 60%"}, %%TNOTA%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#tq-l", {clipPath:"inset(0% 100% 0% 0% round 40px)"}, {clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.28, ease:"power3.out"}, %%TTOCA1%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA%%);
tl.fromTo("#tq-s", {x:0, y:0}, {x:-7, y:7, duration:0.22, yoyo:true, repeat:%%REP%%, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);
tl.fromTo("#br-b", {x:-400, rotation:16}, {x:1300, rotation:16, duration:0.72, ease:"power1.inOut"}, %%BR_S%%);

// ---- partículas de notas ----
tl.fromTo("#nt-m-in", {opacity:1}, {keyframes:[{opacity:1, duration:%%TAMA%%}, {opacity:0.45, duration:0.6}, {opacity:1, duration:0.6}], ease:"none"}, 0);
tl.to("#nt-m-in", {opacity:0.15, duration:0.4, ease:"none"}, 6.97);
tl.to("#nt-m-in", {opacity:0.8, duration:0.4, ease:"none"}, 10.3);
tl.fromTo("#nt-c-in", {opacity:0.1}, {opacity:0.9, duration:0.8, ease:"none"}, %%TAMA%%);
tl.to("#nt-c-in", {opacity:0.25, duration:0.4, ease:"none"}, 3.85);
tl.to("#nt-c-in", {opacity:1, duration:0.4, ease:"none"}, 6.97);
tl.to("#nt-c-in", {opacity:0.8, duration:0.4, ease:"none"}, 10.3);
%%DOT_JS%%

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

T_AMA = t_pal("intro", 4)          # "amadeirado"
T_TERM = t_pal("intro", 3)         # "termina"
T_CONH = t_pal("intro", 5)         # "conhece"
T_TRES = t_pal("apresentacao", 3)  # "os três"
T_CIT = t_pal("apresentacao", 8)   # "cítricas"
T_MAD = t_pal("apresentacao", 12)  # "madeira"
T_MUDA = t_pal("apresentacao", 16)
T_FLOR = t_pal("apresentacao", 19)
T_ESP = t_pal("apresentacao", 22)
T_DOCE = t_pal("apresentacao", 26)
T_NOTA = t_pal("cta", 1)
T_TOCA0 = round(t_pal("cta", 4) - 0.03, 3)
T_OSTRES = t_pal("cta", 9)

TPULSO = round(T_TOCA0 + 0.3, 3)
REP = int(((TOTAL - 0.05) - TPULSO) / 0.22) - 1
REP -= (REP + 1) % 2 == 1  # número par de meias-voltas: termina em x:0
BR_S = round(T_OSTRES - 0.05, 3)
TAMA = round(T_AMA - 0.06, 3)
TTRES = round(T_TRES - 0.05, 3)
TMAD = round(T_MAD - 0.05, 3)
TMUDA = round(T_MUDA - 0.05, 3)
TESP = round(T_ESP - 0.05, 3)
TDOCE = round(T_DOCE - 0.05, 3)
TSWAP = round(T_MUDA - 0.12, 3)
subs = {
    "TOTAL": str(TOTAL), "DOT_HTML": "\n".join(dot_html), "DOT_JS": "\n".join(dot_js),
    "BR_T": "450", "BR_H": "390", "BR_S": R(BR_S), "SBRI": R(BR_S),
    "DV1": str(DUR_MP3["intro"]), "DV2": str(DUR_MP3["apresentacao"]), "DV3": str(DUR_MP3["cta"]),
    "DFA": R(TAMA - 0.4 - 0.003), "TAMA": R(TAMA), "TAMA2": R(TAMA + 0.14), "DFB": R(3.67 - (TAMA + 0.14) - 0.003),
    "TREG": R(T_TERM - 0.04), "DREG": R(T_AMA + 0.5 - T_TERM),
    "TPILL": R(T_CONH - 0.1), "TPILL2": R(T_CONH - 0.02), "SPOP": R(T_CONH - 0.12),
    "DA1": R(TTRES - 4.17 - 0.003), "TTRES": R(TTRES), "TTRES2": R(TTRES + 0.14), "DA2": R(6.82 - (TTRES + 0.14) - 0.003),
    "TCIT": R(T_CIT - 0.05),
    "DD1": R(TMAD - 7.31 - 0.003), "TMAD": R(TMAD), "TMAD2": R(TMAD + 0.14), "DD2": R(TMUDA - (TMAD + 0.14) - 0.003),
    "TMUDA": R(TMUDA), "TMUDA2": R(TMUDA + 0.14), "DD3": R(10.14 - (TMUDA + 0.14) - 0.003),
    "TSWAP": R(TSWAP), "TSWAP2": R(TSWAP + 0.1), "TQ": R(TSWAP + 0.16),
    "DE1": R(TESP - 10.6 - 0.003), "TESP": R(TESP), "TESP2": R(TESP + 0.14), "DE2": R(TDOCE - (TESP + 0.14) - 0.003),
    "TDOCE": R(TDOCE), "TDOCE2": R(TDOCE + 0.14), "DE3": R(13.64 - (TDOCE + 0.14) - 0.003),
    "TFLOR": R(T_FLOR - 0.05),
    "DC1": R(T_TOCA0 - 14.12 - 0.003), "TTOCA": R(T_TOCA0), "TTOCA1": R(T_TOCA0 + 0.08), "TTOCA2": R(T_TOCA0 + 0.24),
    "DC2": R(TOTAL - (T_TOCA0 + 0.24)), "DTOCA": R(TOTAL - T_TOCA0),
    "TNOTA": R(T_NOTA - 0.03), "TPULSO": R(TPULSO), "REP": str(REP), "TONDA2": R(T_TOCA0 + 0.95),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
assert 6.892 + 4.05 - 4.05 < T_AD and T_DE < T_FLOR
open(OUT, "w").write(html)
print("ok", OUT, "| amadeirado", T_AMA, "conhece", T_CONH, "três", T_TRES, "cítricas", T_CIT, "madeira", T_MAD,
      "muda", T_MUDA, "flor", T_FLOR, "especiarias", T_ESP, "doce", T_DOCE, "| toca", T_TOCA0, "brilho", BR_S, "rep", REP)
