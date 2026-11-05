#!/usr/bin/env python3
"""Gera produtos/hilee/edicao_A/index.html — estilo "Cromo e cobre" (comercial premium).
Obsidiana #0A0C10 / cromo (degradê #FFFFFF-#A7B1BC) / gelo-cromo (#E3F8FF-#7CCBEA) / cobre (#F7B583-#B9612F),
Montserrat 300/900 (títulos) + Poppins 800 (legenda "cartela de comercial").
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra da 3ª violação: o vídeo roda do primeiro ao último quadro; nada de <img>, quadro congelado ou cartão.
Layout "estúdio": cada clipe aparece nítido, reduzido e com bordas esfumadas sobre o próprio clipe desfocado e
escurecido (rodando junto). Garrafa sempre entre y ~470 e ~1366; títulos no alto (y 190-490), legenda logo abaixo da
base da garrafa (y 1366-1476), rodapé em 1490: nenhum texto sobre a garrafa.
Trechos (analise_A.md; A molha a partir de ~1,8 s na borda direita, B parado a partir de 6,5 s):
  intro        A 0,00-1,75 s em 0,70x -> B 0,30-1,25 s em 0,70x (tampa fechada, a mão começa a entrar)
  apresentação C 0,00-3,15 s em 0,70x (mão chega na alça) -> B 1,25-5,69 s em 0,85x (a tampa abre em "Tampa automática")
  CTA          C 3,40-7,00 s em 0,70x (mão segura a alça e sai)
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

R = lambda v: str(round(v, 3))

# ---------------- partes ----------------
T_I, T_A, TOTAL = 3.857, 13.58, 18.72
P = {"intro": (0.0, T_I, 0.20), "apresentacao": (T_I, T_A, T_I + 0.20), "cta": (T_A, TOTAL, T_A + 0.20)}
DUR_MP3 = {"intro": 3.624, "apresentacao": 9.456, "cta": 4.824}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


# ---------------- geometria dos clipes ----------------
# s = escala do clipe; top = topo do clipe na tela; base = y da base da garrafa na tela;
# m0/m1 = início e fim da parte opaca da máscara vertical (fade de 65 px antes de m0 e depois de m1)
GEO = {
    "A": {"s": 0.82, "top": 27, "base": 1354, "m0": 425, "m1": 1440, "m2": 1540},
    "B": {"s": 0.715, "top": 205, "base": 1362, "m0": 430, "m1": 1440, "m2": 1540},
    "C": {"s": 0.645, "top": 262, "base": 1358, "m0": 478, "m1": 1410, "m2": 1505},
}
for g in GEO.values():
    g["w"] = round(1080 * g["s"])
    g["h"] = round(1920 * g["s"])
    g["left"] = round(540 - g["w"] / 2)
    g["oy"] = round((g["base"] - g["top"]) / g["h"] * 100, 2)   # origem dos punches = base da garrafa

# (id, clipe, início, duração, media-start, rate)
CORTES = [
    ("A", "A", 0.0, 2.571, 0.00, 0.70),
    ("B1", "B", 2.571, 1.286, 0.30, 0.70),
    ("C1", "C", T_I, round(8.36 - T_I, 3), 0.00, 0.70),
    ("B2", "B", 8.36, round(T_A - 8.36, 3), 1.25, 0.85),
    ("C2", "C", T_A, round(TOTAL - T_A, 3), 3.40, 0.70),
]

# lupa (detalhe da tampa) — mesmo trecho do B2, ampliado; mesma velocidade
LENS_T0, LENS_T1, LK = 9.62, 12.30, 1.15
LENS = {"x": 44, "y": 760, "d": 340}
LENS_MS = round(1.25 + (LENS_T0 - 8.36) * 0.85, 3)
LID = (560, 560)   # centro da tampa no clipe B (px do clipe)

# ---------------- legenda ----------------
GRUPOS = {
    "intro": [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9], [10, 11, 12]],
    "apresentacao": [[0, 1], [2], [3, 4], [5], [6, 7], [8, 9, 10, 11], [12, 13], [14, 15], [16], [17],
                     [18, 19], [20, 21], [22, 23], [24, 25, 26]],
    "cta": [[0, 1], [2, 3, 4], [5], [6, 7], [8, 9], [10, 11, 12], [13]],
}
# f = gelo-cromo, q = cobre
CHAVE = {
    "intro": {2: "f", 12: "q"},
    "apresentacao": {2: "f", 5: "f", 6: "f", 8: "f", 13: "q", 15: "q", 16: "f", 17: "f", 21: "f", 23: "f", 26: "f"},
    "cta": {1: "f", 4: "q", 5: "f", 13: "f"},
}
EXIBE = {("intro", 5): "e,", ("intro", 7): "almoço,", ("intro", 12): "morna?",
         ("apresentacao", 2): "Hilee:", ("apresentacao", 5): "fabricante,", ("apresentacao", 8): "24",
         ("apresentacao", 9): "", ("apresentacao", 10): "", ("apresentacao", 15): "12.",
         ("apresentacao", 23): "direto,", ("apresentacao", 26): "tudo.",
         ("cta", 4): "sua?", ("cta", 13): "disponibilidade."}
TOPO_LEG = 1366

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
            e = min(fim_voz, P[parte][1] - 0.02)
        gid = f"lg-{parte[:3]}-{gi}"
        ems = ""
        for k, i in enumerate(g):
            txt = EXIBE.get((parte, i), pal[i]["palavra"])
            if txt == "":
                continue
            t = t_pal(parte, i)
            cls = CHAVE[parte].get(i)
            kc = f" k {cls}" if cls else ""
            ems += f'<em id="{gid}-{k}" class="w{kc}"><b>{txt}</b></em>'
            # karaokê: a palavra acende no seu tempo
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.34}},{{opacity:1,duration:0.08,ease:"none"}},{R(max(s, t - 0.02))});')
            if cls:
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{scale:1}},{{scale:1.06,duration:0.1,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{R(max(s, t - 0.02))});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div class="cap" style="top:{TOPO_LEG}px"><span id="{gid}-p" class="ctag">{ems}</span></div></div>')
        leg_js.append(f'tl.fromTo("#{gid}-p",{{y:16,opacity:0}},{{y:0,opacity:1,duration:0.14,ease:"power3.out"}},{R(s)});')

T = {
    "gelo": t_pal("intro", 2), "almoco": t_pal("intro", 7), "agua": t_pal("intro", 9), "morna": t_pal("intro", 12),
    "Garrafa": t_pal("apresentacao", 0), "Hilee": t_pal("apresentacao", 2), "segundo": t_pal("apresentacao", 3),
    "gelada": t_pal("apresentacao", 6), "vinte": t_pal("apresentacao", 8), "quente": t_pal("apresentacao", 13),
    "doze": t_pal("apresentacao", 15), "Tampa": t_pal("apresentacao", 16), "automatica": t_pal("apresentacao", 17),
    "canudo": t_pal("apresentacao", 21), "ou": t_pal("apresentacao", 22), "direto": t_pal("apresentacao", 23),
    "sem": t_pal("apresentacao", 24), "tudo": t_pal("apresentacao", 26),
    "Qual": t_pal("cta", 0), "sua": t_pal("cta", 4), "Toque": t_pal("cta", 5), "produto": t_pal("cta", 7),
    "consulte": t_pal("cta", 11), "disp": t_pal("cta", 13),
}

# ---------------- vídeos ----------------
win_html, bg_html = [], []
for n, (cid, clip, st, du, ms, rate) in enumerate(CORTES):
    g = GEO[clip]
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1.0 else ""
    vmask = (f"linear-gradient(to bottom,transparent {g['m0'] - 65}px,#000 {g['m0']}px,#000 {g['m1']}px,"
             f"transparent {g['m2']}px)")
    win_html.append(
        f'  <div id="vm{cid}" class="vmask" style="-webkit-mask-image:{vmask};mask-image:{vmask}">'
        f'<div id="hm{cid}" class="hmask" style="left:{g["left"]}px;top:{g["top"]}px;width:{g["w"]}px;height:{g["h"]}px">'
        f'<div id="mov{cid}" class="mov" style="transform-origin:50% {g["oy"]}%">'
        f'<div id="pun{cid}" class="mov" style="transform-origin:50% {g["oy"]}%">'
        f'<video id="v{cid}" class="clip full" data-start="{st}" data-duration="{du}" data-media-start="{ms}"{rate_attr} '
        f'data-track-index="{n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video></div></div></div></div>')
    bg_html.append(
        f'    <video id="b{cid}" class="clip full" data-start="{R(max(0, st - 0.001))}" data-duration="{R(du + (0.001 if st > 0 else -0.001))}" '
        f'data-media-start="{ms}"{rate_attr} data-track-index="{2 + n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video>')

LV_W, LV_H = round(1080 * LK), round(1920 * LK)
LV_L = round(LENS["d"] / 2 - LID[0] * LK)
LV_T = round(LENS["d"] / 2 - LID[1] * LK)


def punch(sel, t, peak, rest=1.0, d1=0.1, d2=0.3):
    return (f'tl.to("{sel}",{{scale:{peak},duration:{d1},ease:"power3.out"}},{R(t)});\n'
            f'tl.to("{sel}",{{scale:{rest},duration:{d2},ease:"power2.inOut"}},{R(t + d1)});')


def shutter(n, cut):
    return (f'tl.fromTo("#shl{n}",{{x:-548}},{{keyframes:[{{x:0,duration:0.16,ease:"power2.in"}},{{x:0,duration:0.03}},{{x:-548,duration:0.16,ease:"power2.out"}}]}},{R(cut - 0.175)});\n'
            f'tl.fromTo("#shr{n}",{{x:548}},{{keyframes:[{{x:0,duration:0.16,ease:"power2.in"}},{{x:0,duration:0.03}},{{x:548,duration:0.16,ease:"power2.out"}}]}},{R(cut - 0.175)});')


SHUT = [T_I, T_A]
shut_html = "\n".join(
    f'  <div id="sh{n}" class="clip shut" data-start="{R(c - 0.175)}" data-duration="0.35" data-track-index="12">'
    f'<span id="shl{n}" class="sh-l"></span><span id="shr{n}" class="sh-r"></span></div>' for n, c in enumerate(SHUT))


def reveal(sel, t, d=0.34):
    """sobe por trás de uma linha (a linha-mãe tem overflow hidden)"""
    return f'tl.fromTo("{sel}",{{yPercent:105}},{{yPercent:0,duration:{d},ease:"power3.out"}},{R(t)});'


def shine(sel, t, d=0.7):
    return f'tl.fromTo("{sel}",{{"--sx":"100%"}},{{"--sx":"0%",duration:{d},ease:"power1.inOut"}},{R(t)});'


def out(sels, t, d=0.14):
    lst = ",".join(f'"{s}"' for s in sels)
    return f'tl.to([{lst}],{{y:-26,opacity:0,duration:{d},ease:"power2.in"}},{R(t)});'


CHROME = "linear-gradient(180deg,#FFFFFF 0%,#EEF2F6 38%,#A7B1BC 52%,#DDE3EA 70%,#FFFFFF 100%)"
ICE = "linear-gradient(180deg,#FFFFFF 0%,#E3F8FF 36%,#7CCBEA 53%,#C9F1FF 72%,#FFFFFF 100%)"
COBRE = "linear-gradient(180deg,#FFE6CF 0%,#F7B583 38%,#B9612F 54%,#E99A66 72%,#FFE1C6 100%)"
HL = "linear-gradient(110deg,rgba(255,255,255,0) 42%,rgba(255,255,255,.95) 50%,rgba(255,255,255,0) 58%)"

# botão do "Toque": canto inferior esquerdo, fora da garrafa (C: corpo a partir de x ~420)
BX, BY = 66, 1196

HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:"Mont Cromo";font-weight:100 900;src:local("Montserrat Thin"),local("Montserrat-Thin"),local("Montserrat")}}
@font-face{{font-family:"Pop Cromo";font-weight:800;src:local("Poppins ExtraBold"),local("Poppins-ExtraBold")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0A0C10}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:#0A0C10;font-family:"Pop Cromo";font-weight:800}}
.clip{{position:absolute;inset:0}}
.full{{width:100%;height:100%;object-fit:cover}}
/* fundo: o mesmo clipe, desfocado e escurecido (renderizado pequeno e ampliado 3x) */
#bg{{position:absolute;left:0;top:0;width:360px;height:640px;overflow:hidden;transform:scale(3);transform-origin:0 0;
  filter:blur(9px) brightness(.5) saturate(1.05);z-index:1}}
/* clipe nítido: máscara vertical (tela inteira) + máscara lateral (caixa do clipe), bordas esfumadas */
.vmask{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:5}}
.hmask{{position:absolute;overflow:hidden;
  -webkit-mask-image:linear-gradient(to right,transparent 0,#000 100px,#000 calc(100% - 100px),transparent 100%);
  mask-image:linear-gradient(to right,transparent 0,#000 100px,#000 calc(100% - 100px),transparent 100%)}}
.mov{{position:absolute;left:0;top:0;width:100%;height:100%}}
/* luz de estúdio: escurece o alto (títulos) e os cantos, nunca o meio (garrafa) */
#scrim{{position:absolute;inset:0;z-index:6;pointer-events:none;
  background:linear-gradient(to bottom,rgba(8,9,12,.78) 0,rgba(8,9,12,.5) 300px,rgba(8,9,12,0) 470px),
  radial-gradient(ellipse 85% 62% at 50% 48%,rgba(8,9,12,0) 62%,rgba(8,9,12,.55) 100%)}}
/* brilho que passa na tampa (sobre o vídeo rodando) */
#sweep{{inset:auto;left:380px;top:430px;width:330px;height:340px;overflow:hidden;z-index:6;mix-blend-mode:screen;
  -webkit-mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%);mask-image:radial-gradient(ellipse 50% 50% at 50% 50%,#000 45%,transparent 100%)}}
#sw-bar{{position:absolute;top:0;left:0;width:200px;height:340px;display:block;
  background:linear-gradient(105deg,rgba(255,255,255,0) 30%,rgba(255,255,255,.38) 50%,rgba(255,255,255,0) 70%)}}
/* lupa do detalhe da tampa */
#lens{{position:absolute;left:{LENS["x"]}px;top:{LENS["y"]}px;width:{LENS["d"]}px;height:{LENS["d"]}px;border-radius:50%;overflow:hidden;
  z-index:7;opacity:0;background:#0A0C10;box-shadow:0 0 0 6px #DDE3EA,0 0 0 9px rgba(10,12,16,.7),0 24px 60px rgba(0,0,0,.6)}}
#vL{{position:absolute;left:{LV_L}px;top:{LV_T}px;width:{LV_W}px;height:{LV_H}px;object-fit:cover}}
#lead{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:7;opacity:0;overflow:visible}}
/* títulos */
.titulo{{z-index:8}}
.row{{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-end;gap:26px;white-space:nowrap;overflow:hidden;padding:6px 0 10px}}
.m9,.m3,.m6{{display:block;font-family:"Mont Cromo";line-height:1;filter:drop-shadow(0 6px 10px rgba(0,0,0,.7))}}
.m9{{font-weight:900;letter-spacing:.005em}}
.m3{{font-weight:300;letter-spacing:.3em;padding-left:.3em}}
.m6{{font-weight:700;letter-spacing:.16em;padding-left:.16em}}
.chrome,.ice,.cobre{{color:transparent;-webkit-background-clip:text;background-clip:text;background-repeat:no-repeat;
  background-size:300% 100%,100% 100%;background-position:var(--sx,100%) 0,0 0}}
.chrome{{background-image:{HL},{CHROME}}}
.ice{{background-image:{HL},{ICE}}}
.cobre{{background-image:{HL},{COBRE}}}
.pill{{display:block;font-family:"Mont Cromo";font-weight:800;font-size:36px;line-height:1;letter-spacing:.14em;white-space:nowrap;
  padding:10px 18px 11px 23px;border-radius:10px;color:#FFFFFF;background:rgba(10,12,16,.9);border:2px solid rgba(221,227,234,.55)}}
.pill.q{{color:#0A0C10;background:{COBRE};border:none;padding:12px 20px 13px 25px}}
.stack{{position:relative;display:block}}
.stack .top{{position:absolute;left:0;top:0}}
/* rodapé */
#rod{{z-index:9}}
#rod span{{position:absolute;left:60px;top:1490px;display:block;font-family:"Mont Cromo";font-weight:600;font-size:30px;line-height:1;
  color:rgba(255,255,255,.85);background:rgba(10,12,16,.62);padding:7px 14px 8px;border-radius:8px}}
/* legenda "cartela de comercial": barra obsidiana, palavras acendem no tempo, palavra-chave em metal */
.legenda{{z-index:10}}
.cap{{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start}}
.ctag{{display:flex;gap:24px;align-items:center;white-space:nowrap;background:rgba(10,12,16,.94);border-radius:18px;
  border:2px solid rgba(201,210,220,.3);padding:4px 28px 10px;box-shadow:0 16px 36px rgba(0,0,0,.5)}}
.w{{position:relative;display:block;font-style:normal;font-family:"Pop Cromo";font-weight:800;font-size:84px;line-height:1.12;color:#FFFFFF}}
.w b{{display:block;font-weight:800}}
.w.f b{{color:transparent;-webkit-background-clip:text;background-clip:text;background-image:{ICE}}}
.w.q b{{color:transparent;-webkit-background-clip:text;background-clip:text;background-image:{COBRE}}}
/* CTA */
#toque{{z-index:11}}
#tq-b{{position:absolute;left:{BX}px;top:{BY}px;width:124px;height:124px;display:block;border-radius:50%;background:#0A0C10;
  box-shadow:0 0 0 6px #DDE3EA,0 16px 34px rgba(0,0,0,.55)}}
#tq-b svg{{display:block;width:124px;height:124px}}
.tq-o{{position:absolute;left:{BX}px;top:{BY}px;width:124px;height:124px;display:block;border:6px solid #7CCBEA;border-radius:50%;opacity:0}}
/* cortina de obsidiana: dois painéis opacos de bordas duras com fio cromado */
.shut{{z-index:12;overflow:hidden}}
.sh-l,.sh-r{{position:absolute;top:0;width:544px;height:1920px;display:block;background:#0A0C10}}
.sh-l{{left:0;border-right:5px solid #C9D2DC}}
.sh-r{{left:536px;border-left:5px solid #C9D2DC}}
.flash{{z-index:13;background:#F4F7FA;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- fundo desfocado: o mesmo trecho de cada clipe, rodando junto -->
  <div id="bg">
{chr(10).join(bg_html)}
  </div>

  <!-- clipes nítidos: A 0-1,75 (0,7x) | B 0,30-1,25 (0,7x) | C 0-3,15 (0,7x) | B 1,25-5,69 (0,85x) | C 3,40-7,00 (0,7x) -->
{chr(10).join(win_html)}

  <div id="sweep" class="clip" data-start="9.42" data-duration="0.8" data-track-index="5"><i id="sw-bar"></i></div>
  <div id="scrim"></div>

  <!-- lupa: o mesmo B2 ampliado {LK}x, na tampa -->
  <div id="lens"><video id="vL" class="clip" data-start="{LENS_T0}" data-duration="{R(LENS_T1 - LENS_T0)}" data-media-start="{LENS_MS}" data-playback-rate="0.85" data-track-index="4" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <svg id="lead" viewBox="0 0 1080 1920"><path id="lead-p" d="M 335 815 L 466 650" fill="none" stroke="#DDE3EA" stroke-width="5" stroke-linecap="round" stroke-dasharray="210" stroke-dashoffset="210"/><circle id="lead-d" cx="466" cy="650" r="9" fill="#DDE3EA" opacity="0"/></svg>

  <!-- INTRO: ÁGUA MORNA / DE NOVO? / e nem deu meio-dia -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="{T_I}" data-track-index="7">
    <div class="row" style="top:184px;height:114px"><span id="t1a" class="m9 chrome" style="font-size:96px">ÁGUA</span><span id="t1m" class="stack"><span id="t1m-c" class="m9 chrome" style="font-size:96px">MORNA</span><span id="t1m-q" class="m9 cobre top" style="font-size:96px;opacity:0">MORNA</span></span></div>
    <div class="row" style="top:290px;height:146px"><span id="t1b" class="m9 chrome" style="font-size:128px">DE NOVO?</span></div>
    <div class="row" style="top:426px;height:72px"><span id="t1s" class="pill" style="opacity:0">E NEM DEU MEIO-DIA</span></div>
  </div>

  <!-- APRESENTAÇÃO 1: GARRAFA TÉRMICA / HILEE -->
  <div id="t2" class="clip titulo" data-start="{R(T["Garrafa"] - 0.05)}" data-duration="{R(T["gelada"] - 0.05 - T["Garrafa"] + 0.05)}" data-track-index="8">
    <div class="row" style="top:190px;height:70px"><span id="t2a" class="m3 chrome" style="font-size:50px">GARRAFA TÉRMICA</span></div>
    <div class="row" style="top:258px;height:180px"><span id="t2b" class="m9 chrome" style="font-size:164px;letter-spacing:.06em;padding-left:.06em">HILEE</span></div>
  </div>
  <!-- APRESENTAÇÃO 2: GELADA POR / 24 H* / QUENTE POR 12 HORAS -->
  <div id="t3" class="clip titulo" data-start="{R(T["gelada"] - 0.05)}" data-duration="{R(T["Tampa"] - 0.1 - T["gelada"] + 0.05)}" data-track-index="7">
    <div class="row" style="top:184px;height:110px"><span id="t3a" class="m9 ice" style="font-size:92px">GELADA POR</span></div>
    <div class="row" style="top:282px;height:158px"><span id="t3b" class="m9 ice" style="font-size:140px"><span id="num">24</span> H*</span></div>
    <div class="row" style="top:426px;height:72px"><span id="t3c" class="pill q">QUENTE POR 12 HORAS</span></div>
  </div>
  <!-- APRESENTAÇÃO 3: TAMPA / AUTOMÁTICA -->
  <div id="t4" class="clip titulo" data-start="{R(T["Tampa"] - 0.06)}" data-duration="{R(T["canudo"] - 0.1 - T["Tampa"] + 0.06)}" data-track-index="8">
    <div class="row" style="top:186px;height:118px"><span id="t4a" class="m9 chrome" style="font-size:100px">TAMPA</span></div>
    <div class="row" style="top:296px;height:118px"><span id="t4b" class="m9 chrome" style="font-size:100px">AUTOMÁTICA</span></div>
  </div>
  <!-- APRESENTAÇÃO 4: CANUDO / OU DIRETO -->
  <div id="t5" class="clip titulo" data-start="{R(T["canudo"] - 0.06)}" data-duration="{R(T["sem"] - 0.1 - T["canudo"] + 0.06)}" data-track-index="7">
    <div class="row" style="top:186px;height:118px"><span id="t5a" class="m9 chrome" style="font-size:100px">CANUDO</span></div>
    <div class="row" style="top:296px;height:118px"><span id="t5b" class="m9 ice" style="font-size:100px">OU DIRETO</span></div>
  </div>
  <!-- APRESENTAÇÃO 5: SEM ABRIR / TUDO -->
  <div id="t6" class="clip titulo" data-start="{R(T["sem"] - 0.06)}" data-duration="{R(T_A - 0.12 - T["sem"] + 0.06)}" data-track-index="8">
    <div class="row" style="top:186px;height:118px"><span id="t6a" class="m9 chrome" style="font-size:100px">SEM ABRIR</span></div>
    <div class="row" style="top:290px;height:150px"><span id="t6b" class="m9 ice" style="font-size:136px">TUDO</span></div>
  </div>
  <!-- CTA 1: QUAL COR / É A SUA? -->
  <div id="t7" class="clip titulo" data-start="{R(T["Qual"] - 0.05)}" data-duration="{R(T["consulte"] - 0.1 - T["Qual"] + 0.05)}" data-track-index="7">
    <div class="row" style="top:186px;height:130px"><span id="t7a" class="m9 chrome" style="font-size:112px">QUAL COR</span></div>
    <div class="row" style="top:306px;height:130px"><span id="t7b" class="m9 chrome" style="font-size:112px">É A</span><span id="t7c" class="m9 cobre" style="font-size:112px">SUA?</span></div>
  </div>
  <!-- CTA 2: CONSULTE A / DISPONIBILIDADE -->
  <div id="t8" class="clip titulo" data-start="{R(T["consulte"] - 0.05)}" data-duration="{R(TOTAL - T["consulte"] + 0.05)}" data-track-index="8">
    <div class="row" style="top:204px;height:72px"><span id="t8a" class="m3 chrome" style="font-size:50px">CONSULTE A</span></div>
    <div class="row" style="top:282px;height:96px"><span id="t8b" class="m9 ice" style="font-size:72px">DISPONIBILIDADE</span></div>
  </div>

  <div id="rod" class="clip" data-start="{T_I}" data-duration="{R(T_A - T_I)}" data-track-index="9"><span id="rod-s">*Dados do fabricante</span></div>

  <div id="toque" class="clip" data-start="{R(T["Toque"])}" data-duration="{R(TOTAL - T["Toque"])}" data-track-index="11">
    <i id="tq-o1" class="tq-o"></i><i id="tq-o2" class="tq-o"></i><i id="tq-o3" class="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 124 124"><path d="M84 40 L44 80 M42 52 L42 82 L72 82" fill="none" stroke="#FFFFFF" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

{shut_html}
  <div id="fl0" class="clip flash" data-start="0" data-duration="0.12" data-track-index="13"></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{P["intro"][2]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{R(P["apresentacao"][2])}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{R(P["cta"][2])}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="2.45" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="3.6" data-duration="0.55" data-track-index="22" data-volume="0.34" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-tique-1" data-start="6.72" data-duration="0.03" data-track-index="22" data-volume="0.35" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="8.22" data-duration="0.3" data-track-index="22" data-volume="0.26" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-brilho-1" data-start="9.45" data-duration="0.9" data-track-index="22" data-volume="0.26" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-tique-2" data-start="12.12" data-duration="0.03" data-track-index="22" data-volume="0.33" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="13.19" data-duration="0.39" data-media-start="1.0" data-track-index="22" data-volume="0.3" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["Toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-1" data-start="18.32" data-duration="0.09" data-track-index="22" data-volume="0.25" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ================= INTRO: A 0-1,75 s (0,7x) -> B 0,30-1,25 s (0,7x) =================
tl.fromTo("#fl0", {{opacity:0.9}}, {{opacity:0, duration:0.1, ease:"power1.out"}}, 0);
tl.fromTo("#movA", {{scale:1.1}}, {{scale:1.0, duration:0.42, ease:"power3.out"}}, 0);
tl.to("#movA", {{scale:1.03, duration:2.15, ease:"none"}}, 0.42);
{punch("#punA", T["gelo"], 1.035, 1.0)}
{reveal("#t1a", 0.03)}
{reveal("#t1m", 0.07)}
tl.fromTo("#t1b", {{scale:1.9, opacity:0}}, {{scale:1, opacity:1, duration:0.32, ease:"back.out(1.6)"}}, 0.1);
{shine("#t1b", 0.5, 0.8)}
// corte para o estúdio quente: "MORNA" esquenta (cromo -> cobre)
tl.fromTo("#movB1", {{scale:1.07}}, {{scale:1.0, duration:0.3, ease:"power3.out"}}, 2.571);
tl.to("#movB1", {{scale:1.025, duration:0.98, ease:"none"}}, 2.871);
tl.fromTo("#t1m-q", {{opacity:0}}, {{opacity:1, duration:0.3, ease:"power1.out"}}, 2.571);
tl.fromTo("#t1s", {{opacity:0, scaleX:1.28}}, {{opacity:1, scaleX:1, duration:0.45, ease:"power3.out"}}, 2.62);
tl.fromTo("#t1m", {{scale:1}}, {{scale:1.05, duration:0.12, yoyo:true, repeat:1, ease:"power2.out"}}, {R(T["morna"])});
{shine("#t1m-q", T["morna"], 0.6)}
{out(["#t1a", "#t1m", "#t1b", "#t1s"], 3.62)}

{shutter(0, T_I)}

// ================= APRESENTAÇÃO: C 0-3,15 s (0,7x) -> B 1,25-5,69 s (0,85x) =================
tl.fromTo("#movC1", {{scale:1.0}}, {{scale:1.04, duration:4.5, ease:"none"}}, {T_I});
tl.fromTo("#rod-s", {{opacity:0}}, {{opacity:1, duration:0.2, ease:"power1.out"}}, {R(T_I + 0.08)});
tl.fromTo("#rod-s", {{scale:1}}, {{scale:1.1, duration:0.15, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}}, {R(T["segundo"])});
tl.fromTo("#t2a", {{opacity:0, scaleX:1.28}}, {{opacity:1, scaleX:1, duration:0.45, ease:"power3.out"}}, {R(T["Garrafa"] - 0.03)});
{reveal("#t2b", T["Hilee"] - 0.04, 0.36)}
{shine("#t2b", T["Hilee"] + 0.3, 0.8)}
{out(["#t2a", "#t2b"], T["gelada"] - 0.2)}
// "gelada": título; "vinte e quatro": contagem 0 -> 24
{reveal("#t3a", T["gelada"] - 0.04)}
tl.fromTo("#t3b", {{scale:1.3, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(1.7)"}}, {R(T["vinte"] - 0.03)});
const cnt = {{ n: 0 }};
tl.to(cnt, {{ n: 24, duration: 0.6, ease: "power2.out", onUpdate: () => {{ document.getElementById("num").textContent = String(Math.round(cnt.n)); }} }}, {R(T["vinte"])});
{shine("#t3b", T["vinte"] + 0.62, 0.7)}
{punch("#punC1", T["gelada"], 1.045, 1.0, 0.1, 0.35)}
// corte para o B (a mão volta à tampa)
tl.fromTo("#movB2", {{scale:1.06}}, {{scale:1.0, duration:0.3, ease:"power3.out"}}, 8.36);
tl.fromTo("#t3c", {{opacity:0, scaleX:1.28}}, {{opacity:1, scaleX:1, duration:0.35, ease:"power3.out"}}, {R(T["quente"] - 0.03)});
tl.fromTo("#t3c", {{scale:1}}, {{scale:1.1, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {R(T["doze"])});
{shine("#t3c", T["doze"] + 0.05, 0.6)}
{out(["#t3a", "#t3b", "#t3c"], T["Tampa"] - 0.25)}
// produto herói: a tampa abre (B 2,2-2,6 s = 9,48-9,95 s) -> brilho na tampa + lupa com o detalhe rodando
tl.fromTo("#sw-bar", {{x:-160}}, {{x:380, duration:0.7, ease:"power1.inOut"}}, 9.45);
tl.fromTo("#lens", {{scale:0.2, opacity:0}}, {{scale:1, opacity:1, duration:0.34, ease:"back.out(1.6)"}}, {LENS_T0});
tl.fromTo("#lead", {{opacity:0}}, {{opacity:1, duration:0.05}}, {R(LENS_T0 + 0.2)});
tl.fromTo("#lead-p", {{strokeDashoffset:210}}, {{strokeDashoffset:0, duration:0.25, ease:"power2.out"}}, {R(LENS_T0 + 0.2)});
tl.fromTo("#lead-d", {{opacity:0}}, {{opacity:1, duration:0.08}}, {R(LENS_T0 + 0.43)});
{reveal("#t4a", T["Tampa"] - 0.04)}
{reveal("#t4b", T["automatica"] - 0.04)}
tl.to("#movB2", {{scale:1.03, duration:2.3, ease:"none"}}, 9.7);
{out(["#t4a", "#t4b"], T["canudo"] - 0.22)}
{reveal("#t5a", T["canudo"] - 0.04)}
{reveal("#t5b", T["ou"] - 0.04)}
tl.fromTo("#lens", {{scale:1}}, {{scale:1.06, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {R(T["direto"])});
{out(["#t5a", "#t5b"], T["sem"] - 0.22)}
tl.to("#lens", {{scale:0.2, opacity:0, duration:0.22, ease:"power2.in"}}, {R(LENS_T1 - 0.24)});
tl.to("#lead", {{opacity:0, duration:0.12}}, {R(LENS_T1 - 0.24)});
{reveal("#t6a", T["sem"] - 0.04)}
tl.fromTo("#t6b", {{scale:1.8, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(1.7)"}}, {R(T["tudo"] - 0.03)});
{punch("#punB2", T["tudo"], 1.045, 1.0)}
{out(["#t6a", "#t6b"], T_A - 0.3)}

{shutter(1, T_A)}

// ================= CTA: C 3,40-7,00 s (0,7x), mais calma =================
tl.fromTo("#movC2", {{scale:1.05}}, {{scale:1.0, duration:0.5, ease:"power2.out"}}, {T_A});
tl.to("#movC2", {{scale:1.03, duration:4.6, ease:"none"}}, {R(T_A + 0.5)});
{reveal("#t7a", T["Qual"] - 0.04)}
tl.fromTo(["#t7b", "#t7c"], {{opacity:0, y:40}}, {{opacity:1, y:0, duration:0.3, ease:"back.out(1.8)"}}, {R(T["sua"] - 0.25)});
tl.fromTo("#t7c", {{scale:1}}, {{scale:1.12, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {R(T["sua"])});
{shine("#t7c", T["sua"] + 0.1, 0.6)}
// "Toque": botão com seta para baixo/esquerda + ondas
tl.fromTo("#tq-b", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(2.2)"}}, {R(T["Toque"])});
tl.fromTo("#tq-s", {{x:0, y:0}}, {{x:-7, y:7, duration:0.22, yoyo:true, repeat:11, ease:"sine.inOut"}}, {R(T["Toque"] + 0.3)});
tl.fromTo("#tq-o1", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["Toque"])});
tl.fromTo("#tq-o2", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["produto"])});
tl.fromTo("#tq-o3", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["disp"])});
{punch("#punC2", T["Toque"], 1.04, 1.0, 0.1, 0.4)}
{out(["#t7a", "#t7b", "#t7c"], T["consulte"] - 0.22)}
tl.fromTo("#t8a", {{opacity:0, scaleX:1.28}}, {{opacity:1, scaleX:1, duration:0.45, ease:"power3.out"}}, {R(T["consulte"] - 0.03)});
{reveal("#t8b", T["disp"] - 0.04)}
{shine("#t8b", T["disp"] + 0.4, 0.7)}
tl.fromTo("#tq-b", {{scale:1}}, {{scale:1.12, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, 18.32);

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT)
