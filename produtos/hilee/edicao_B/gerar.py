#!/usr/bin/env python3
"""Gera produtos/hilee/edicao_B/index.html — estilo "Porta afora" (manhã de saída, lifestyle editorial).
Musgo-noite #141B15 / mel #FFB13B / linho #FFF4E1 / folha #A9DB6E (só no marca-texto das palavras-chave),
DM Serif Display (títulos) + Bricolage Grotesque 300/700/800 (kicker, etiquetas e legenda "marca-texto de mel").
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra da 3ª violação: o vídeo roda do primeiro ao último quadro; nada de <img>, quadro congelado ou cartão.
Layout "porta": cada clipe roda nítido dentro de uma janela em arco (moldura linho + contorno mel), sobre o próprio
clipe desfocado e tingido de musgo (rodando junto). Garrafa sempre entre y ~450 e ~1345; títulos no alto (y 178-436),
legenda logo abaixo do arco (y 1386-1476), rodapé em 1494: nenhum texto sobre a garrafa.
Regra da 4ª violação: nenhum brilho/reflexo passa sobre a garrafa; trocas de parte com painel opaco de borda dura.
Trechos (analise_B.md):
  intro        D 0,00-2,56 s a 0,80x (vapor branco e fino, garrafa preta aberta)
  apresentação E 0,47-6,13 s a 0,85x (a mão chega na alça em "alça"; roxa)  -> corte seco ->
               D 5,00-7,64 s a 1,00x (vapor fino; detalhe da tampa, em "três tamanhos")
  CTA          F 0,60-5,75 s a 0,92x (mão envolve o corpo em "toque"; nada do fim parado >= 6 s)
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

R = lambda v: str(round(v, 3))

# ---------------- partes ----------------
T_I, T_A, TOTAL = 3.2, 12.5, 18.1
VOZ = {"intro": 0.25, "apresentacao": 3.42, "cta": 12.72}
FIM = {"intro": T_I, "apresentacao": T_A, "cta": TOTAL}
DUR_MP3 = {"intro": 2.66, "apresentacao": 8.93, "cta": 4.99}
T_CUT = 9.86   # E (roxa) -> D (preta): corte seco, entre "em" e "três"


def t_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


def f_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["fim"], 3)


# ---------------- geometria ----------------
# janela em arco (tela): x 160-920, y 300-1370, raio 380 (centro do arco em 540, 680)
AL, AT, AW, AH, AR = 160, 300, 760, 1070, 380
# s = escala do clipe; ts = topo do clipe na tela; (ox, oy) = tampa no clipe (px) = origem dos zooms
# garrafa (clipe): D tampa 360 / base 1625; E alça 400 / base 1640; F tampa 525 / base 1615 -> tela: topo ~450, base ~1344
GEO = {
    "D": {"s": 0.707, "ts": 195, "ox": 550, "oy": 470},
    "E": {"s": 0.72, "ts": 162, "ox": 545, "oy": 560},
    "F": {"s": 0.82, "ts": 20, "ox": 545, "oy": 640},
}
for g in GEO.values():
    g["w"] = round(1080 * g["s"])
    g["h"] = round(1920 * g["s"])
    g["l"] = round(540 - g["w"] / 2) - AL
    g["t"] = g["ts"] - AT
    g["orig"] = f'{round(g["ox"] / 1080 * 100, 2)}% {round(g["oy"] / 1920 * 100, 2)}%'

# (id, clipe, início, duração, media-start, rate)
CORTES = [
    ("D1", "D", 0.0, T_I, 0.00, 0.80),
    ("E1", "E", T_I, round(T_CUT - T_I, 3), 0.47, 0.85),
    ("D2", "D", T_CUT, round(T_A - T_CUT, 3), 5.00, 1.0),
    ("F1", "F", T_A, round(TOTAL - T_A, 3), 0.60, 0.92),
]

# ---------------- legenda "marca-texto de mel" ----------------
GRUPOS = {
    "intro": [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9]],
    "apresentacao": [[0, 1], [2], [3, 4, 5], [6, 7, 8], [9, 10], [11], [12, 13, 14], [15, 16], [17, 18, 19],
                     [20, 21], [22, 23], [24, 25, 26]],
    "cta": [[0, 1], [2, 3], [4, 5, 6], [7, 8], [9, 10, 11], [12]],
}
CHAVE = {
    "intro": {5, 7},
    "apresentacao": {2, 3, 5, 8, 16, 20, 21, 26},
    "cta": {1, 3, 4, 6, 12},
}
EXIBE = {("intro", 9): "dia?",
         ("apresentacao", 2): "Hilee:", ("apresentacao", 8): "fácil.", ("apresentacao", 11): "fabricante,",
         ("apresentacao", 21): "tamanhos,", ("apresentacao", 26): "litro.",
         ("cta", 3): "tamanhos:", ("cta", 12): "disponibilidade."}
TOPO_LEG = 1386
LINHO, MUSGO, MEL, FOLHA = "#FFF4E1", "#141B15", "#FFB13B", "#A9DB6E"
SH_ON, SH_OFF = "0px 4px 14px rgba(0,0,0,0.7)", "0px 4px 14px rgba(0,0,0,0)"

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
            e = min(fim_voz, FIM[parte] - 0.02)
        gid = f"lg-{parte[:3]}-{gi}"
        ems = ""
        for k, i in enumerate(g):
            txt = EXIBE.get((parte, i), pal[i]["palavra"])
            chave = i in CHAVE[parte]
            ems += (f'<em id="{gid}-{k}" class="w"><i id="{gid}-{k}m" class="mk{" kf" if chave else ""}"></i>'
                    f'<b id="{gid}-{k}b">{txt}</b></em>')
            t_on = max(s, t_pal(parte, i) - 0.02)
            if k + 1 < len(g):
                t_off = t_pal(parte, g[k + 1]) - 0.02
            else:
                t_off = min(f_pal(parte, i) + 0.12, e - 0.08)
            t_off = max(t_off, t_on + 0.14)
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.5}},{{opacity:1,duration:0.06,ease:"none"}},{R(t_on)});')
            leg_js.append(f'tl.fromTo("#{gid}-{k}m",{{scaleX:0,opacity:1}},{{scaleX:1,duration:0.08,ease:"power2.out"}},{R(t_on)});')
            leg_js.append(f'tl.fromTo("#{gid}-{k}b",{{color:"{LINHO}",textShadow:"{SH_ON}"}},{{color:"{MUSGO}",textShadow:"{SH_OFF}",duration:0.08,ease:"none"}},{R(t_on)});')
            if chave:
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{scale:1}},{{scale:1.07,duration:0.1,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{R(t_on)});')
            leg_js.append(f'tl.to("#{gid}-{k}m",{{opacity:0,duration:0.05,ease:"none"}},{R(t_off)});')
            leg_js.append(f'tl.to("#{gid}-{k}b",{{color:"{LINHO}",textShadow:"{SH_ON}",duration:0.05,ease:"none"}},{R(t_off)});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div class="cap" style="top:{TOPO_LEG}px"><span id="{gid}-p" class="ctag">{ems}</span></div></div>')
        leg_js.append(f'tl.fromTo("#{gid}-p",{{y:18,opacity:0}},{{y:0,opacity:1,duration:0.14,ease:"power3.out"}},{R(s)});')

T = {
    "garrafa": t_pal("intro", 5), "todo": t_pal("intro", 8),
    "Garrafa": t_pal("apresentacao", 0), "Hilee": t_pal("apresentacao", 2), "alca": t_pal("apresentacao", 3),
    "pra": t_pal("apresentacao", 6), "levar": t_pal("apresentacao", 7), "facil": t_pal("apresentacao", 8), "Segundo": t_pal("apresentacao", 9),
    "vazamentos": t_pal("apresentacao", 16), "tres": t_pal("apresentacao", 20), "ate": t_pal("apresentacao", 22),
    "Confira": t_pal("cta", 0), "tamanhos": t_pal("cta", 3), "toque": t_pal("cta", 4), "produto": t_pal("cta", 6),
    "consulte": t_pal("cta", 10), "disp": t_pal("cta", 12),
}

# ---------------- vídeos ----------------
win_html, bg_html = [], []
for n, (cid, clip, st, du, ms, rate) in enumerate(CORTES):
    g = GEO[clip]
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1.0 else ""
    win_html.append(
        f'      <div id="cw{cid}" class="cw" style="left:{g["l"]}px;top:{g["t"]}px;width:{g["w"]}px;height:{g["h"]}px">'
        f'<div id="mov{cid}" class="mov" style="transform-origin:{g["orig"]}">'
        f'<div id="pun{cid}" class="mov" style="transform-origin:{g["orig"]}">'
        f'<video id="v{cid}" class="clip full" data-start="{st}" data-duration="{du}" data-media-start="{ms}"{rate_attr} '
        f'data-track-index="{n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video></div></div></div>')
    bg_html.append(
        f'    <video id="b{cid}" class="clip full" data-start="{R(max(0, st - 0.001))}" data-duration="{R(du + (0.001 if st > 0 else -0.001))}" '
        f'data-media-start="{ms}"{rate_attr} data-track-index="{2 + n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video>')


def punch(sel, t, peak, rest=1.0, d1=0.1, d2=0.3):
    return (f'tl.to("{sel}",{{scale:{peak},duration:{d1},ease:"power3.out"}},{R(t)});\n'
            f'tl.to("{sel}",{{scale:{rest},duration:{d2},ease:"power2.inOut"}},{R(t + d1)});')


def painel(n, cut):
    """persiana de musgo subindo: cobre a tela inteira por 0,04 s em volta do corte (borda dura, opaca)"""
    return (f'tl.fromTo("#pnl{n}",{{y:1960}},{{keyframes:[{{y:0,duration:0.16,ease:"power2.in"}},{{y:0,duration:0.04}},'
            f'{{y:-1960,duration:0.16,ease:"power2.out"}}]}},{R(cut - 0.18)});')


PAINEIS = [T_I, T_A]
pn_html = "\n".join(
    f'  <div id="pn{n}" class="clip painel" data-start="{R(c - 0.18)}" data-duration="0.36" data-track-index="12">'
    f'<span id="pnl{n}" class="pnl"></span></div>' for n, c in enumerate(PAINEIS))


def reveal(sel, t, d=0.36):
    """sobe por trás de uma linha (a linha-mãe tem overflow hidden)"""
    return f'tl.fromTo("{sel}",{{yPercent:108}},{{yPercent:0,duration:{d},ease:"power3.out"}},{R(t)});'


def slam(sel, t, s0=1.8, d=0.32, o0=0):
    return f'tl.fromTo("{sel}",{{scale:{s0},opacity:{o0}}},{{scale:1,opacity:1,duration:{d},ease:"back.out(1.6)"}},{R(t)});'


def placa(pill, t):
    """placa pendurada no topo do arco: desce e balança até assentar (mesma mecânica em toda parte)"""
    return (f'tl.fromTo("{pill}",{{opacity:0,y:-34,rotation:-7}},{{keyframes:[{{opacity:1,y:0,rotation:4,duration:0.22,ease:"power2.out"}},'
            f'{{rotation:-2,duration:0.16,ease:"sine.inOut"}},{{rotation:0,duration:0.14,ease:"sine.out"}}],transformOrigin:"50% -60px"}},{R(t)});')


def out(sels, t, d=0.14):
    lst = ",".join(f'"{s}"' for s in sels)
    return f'tl.to([{lst}],{{y:-24,opacity:0,duration:{d},ease:"power2.in"}},{R(t)});'


# contorno do arco (mel), 22 px fora da moldura, aberto embaixo
ARC_PATH = "M 138 1300 L 138 680 A 402 402 0 0 1 942 680 L 942 1300"
ARC_LEN = 2510

# botão do "toque": canto inferior esquerdo, fora da garrafa (F: corpo entre x ~400 e ~690)
BX, BY = 52, 1206

HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:"Serif Porta";src:local("DM Serif Display Regular"),local("DMSerifDisplay-Regular"),local("DM Serif Display")}}
@font-face{{font-family:"Bric Porta";font-weight:200 800;src:local("Bricolage Grotesque 96pt ExtraBold"),local("Bricolage Grotesque")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{MUSGO}}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:{MUSGO};font-family:"Bric Porta";font-weight:800}}
.clip{{position:absolute;inset:0}}
.full{{width:100%;height:100%;object-fit:cover}}
/* fundo: o mesmo clipe, desfocado (renderizado pequeno e ampliado 3x) e tingido de musgo */
#bg{{position:absolute;left:0;top:0;width:360px;height:640px;overflow:hidden;transform:scale(3);transform-origin:0 0;
  filter:blur(9px) brightness(.62) saturate(1.1);z-index:1}}
#tint{{position:absolute;inset:0;z-index:2;background:rgba(20,27,21,.56)}}
#glow{{position:absolute;inset:0;z-index:3;background:radial-gradient(ellipse 62% 30% at 50% 22%,rgba(255,177,59,.34) 0,rgba(255,177,59,0) 100%)}}
/* porta: janela em arco com o clipe nítido */
#porta{{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:5}}
#arco{{position:absolute;left:{AL}px;top:{AT}px;width:{AW}px;height:{AH}px;overflow:hidden;background:{MUSGO};
  border-radius:{AR}px {AR}px 26px 26px / {AR}px {AR}px 26px 26px;
  box-shadow:0 0 0 7px {LINHO},0 30px 70px rgba(0,0,0,.55)}}
.cw{{position:absolute;overflow:hidden}}
.mov{{position:absolute;left:0;top:0;width:100%;height:100%}}
/* sombra no alto do arco, só acima da tampa (y < 440): legibilidade dos títulos sobre cortina/folhas */
#scrimA{{position:absolute;left:0;top:0;width:{AW}px;height:140px;
  background:linear-gradient(to bottom,rgba(20,27,21,.84) 0,rgba(20,27,21,.55) 80px,rgba(20,27,21,0) 140px)}}
#linha{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:visible}}
/* títulos */
.titulo{{z-index:8}}
.tg{{position:absolute;left:90px;width:900px}}
.row{{position:absolute;left:90px;width:900px;display:flex;justify-content:center;align-items:flex-end;gap:28px;white-space:nowrap;overflow:hidden;padding:4px 0 8px}}
.sf{{display:block;font-family:"Serif Porta";font-weight:400;line-height:1;color:{LINHO};filter:drop-shadow(0 6px 14px rgba(0,0,0,.6))}}
.sf .m{{color:{MEL}}}
.kk{{display:block;font-family:"Bric Porta";font-weight:300;font-size:44px;line-height:1;letter-spacing:.32em;padding-left:.32em;color:{LINHO};
  filter:drop-shadow(0 4px 10px rgba(0,0,0,.7))}}
.prow{{position:absolute;left:90px;width:900px;display:flex;justify-content:center;align-items:flex-start}}
.pill.dk{{color:{LINHO};background:{MUSGO};border:3px solid {MEL};font-weight:300;letter-spacing:.26em;padding:10px 20px 12px 30px}}
.pill{{display:block;font-family:"Bric Porta";font-weight:700;font-size:36px;line-height:1;white-space:nowrap;color:{MUSGO};
  background:{MEL};border-radius:999px;padding:11px 28px 13px;box-shadow:0 10px 26px rgba(0,0,0,.45)}}
/* rodapé */
#rod{{z-index:9}}
#rod span{{position:absolute;left:60px;top:1494px;display:block;font-family:"Bric Porta";font-weight:700;font-size:30px;line-height:1;
  color:rgba(255,244,225,.88);background:rgba(20,27,21,.7);padding:7px 14px 8px;border-radius:8px}}
/* legenda "marca-texto de mel": a palavra da vez ganha o marca-texto; palavra-chave em folha */
.legenda{{z-index:10}}
.cap{{position:absolute;left:90px;width:900px;display:flex;justify-content:center;align-items:flex-start}}
.ctag{{display:flex;gap:6px;align-items:center;white-space:nowrap}}
.w{{position:relative;display:block;font-style:normal;padding:0 12px 4px}}
.w b{{position:relative;display:block;font-family:"Bric Porta";font-weight:800;font-size:78px;line-height:1.12;color:{LINHO};
  text-shadow:{SH_ON}}}
.mk{{position:absolute;left:0;top:12px;width:100%;height:calc(100% - 16px);display:block;background:{MEL};border-radius:14px;
  transform-origin:0% 50%}}
.mk.kf{{background:{FOLHA}}}
/* CTA */
#toque{{z-index:11}}
#tq-b{{position:absolute;left:{BX}px;top:{BY}px;width:120px;height:120px;display:block;border-radius:50%;background:{MUSGO};
  box-shadow:0 0 0 6px {MEL},0 16px 34px rgba(0,0,0,.55)}}
#tq-b svg{{display:block;width:120px;height:120px}}
.tq-o{{position:absolute;left:{BX}px;top:{BY}px;width:120px;height:120px;display:block;border:6px solid {MEL};border-radius:50%;opacity:0}}
/* persiana de musgo: painel opaco de borda dura (nunca tinge a garrafa) */
.painel{{z-index:12;overflow:hidden}}
.pnl{{position:absolute;left:0;top:-16px;width:1080px;height:1952px;display:block;background:{MUSGO};
  border-top:16px solid {MEL};border-bottom:16px solid {MEL}}}
.flash{{z-index:13;background:{LINHO};opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- fundo desfocado: o mesmo trecho de cada clipe, rodando junto -->
  <div id="bg">
{chr(10).join(bg_html)}
  </div>
  <div id="tint"></div>
  <div id="glow"></div>

  <!-- porta: D 0-2,56 (0,8x) | E 0,47-6,13 (0,85x) | corte seco | D 5,00-7,64 (1x) | F 0,60-5,75 (0,92x) -->
  <div id="porta">
    <svg id="linha" viewBox="0 0 1080 1920"><path id="linha-p" d="{ARC_PATH}" fill="none" stroke="{MEL}" stroke-width="4" stroke-linecap="round" stroke-dasharray="{ARC_LEN}" stroke-dashoffset="{ARC_LEN}"/><circle id="linha-a" cx="138" cy="1300" r="8" fill="{MEL}" opacity="0"/><circle id="linha-b" cx="942" cy="1300" r="8" fill="{MEL}" opacity="0"/></svg>
    <div id="arco">
{chr(10).join(win_html)}
      <div id="scrimA"></div>
    </div>
  </div>

  <!-- INTRO: Garrafa na mão? (uma linha, acima do arco) + placa "todo dia, pra todo lado" pendurada no arco -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="{T_I}" data-track-index="7">
    <div id="t1r" class="row" style="top:146px;height:136px;overflow:visible"><span id="t1a" class="sf" style="font-size:114px">Garrafa</span><span id="t1b" class="sf" style="font-size:114px">na <span class="m">mão?</span></span></div>
    <div class="prow" style="top:318px"><span id="t1p" class="pill" style="opacity:0">todo dia, pra todo lado</span></div>
  </div>

  <!-- APRESENTAÇÃO 1: placa GARRAFA TÉRMICA + Hilee -->
  <div id="t2" class="clip titulo" data-start="{T_I}" data-duration="{R(T["pra"] - T_I)}" data-track-index="8">
    <div id="t2r" class="row" style="top:138px;height:150px"><span id="t2b" class="sf" style="font-size:136px">Hilee</span></div>
    <div class="prow" style="top:318px"><span id="t2a" class="pill dk" style="opacity:0">GARRAFA TÉRMICA</span></div>
  </div>
  <!-- APRESENTAÇÃO 2: Fácil de transportar + placa à prova de vazamentos* -->
  <div id="t3" class="clip titulo" data-start="{R(T["pra"] - 0.06)}" data-duration="{R(T_CUT - T["pra"] + 0.06)}" data-track-index="7">
    <div id="t3r" class="row" style="top:166px;height:112px"><span id="t3a" class="sf" style="font-size:90px"><span class="m">Fácil</span> de</span><span id="t3b" class="sf" style="font-size:90px">transportar</span></div>
    <div class="prow" style="top:318px"><span id="t3p" class="pill" style="opacity:0">à prova de vazamentos*</span></div>
  </div>
  <!-- APRESENTAÇÃO 3 (preta, detalhe da tampa): 3 tamanhos* -->
  <div id="t4" class="clip titulo" data-start="{T_CUT}" data-duration="{R(T_A - T_CUT)}" data-track-index="8">
    <div class="row" style="top:138px;height:150px;overflow:visible"><span id="t4a" class="sf" style="font-size:128px"><span class="m">3</span> tamanhos*</span></div>
  </div>
  <!-- CTA: Cores e tamanhos + placa consulte a disponibilidade -->
  <div id="t5" class="clip titulo" data-start="{T_A}" data-duration="{R(TOTAL - T_A)}" data-track-index="7">
    <div id="t5r" class="row" style="top:156px;height:124px"><span id="t5a" class="sf" style="font-size:102px"><span class="m">Cores</span> e</span><span id="t5b" class="sf" style="font-size:102px">tamanhos</span></div>
    <div class="prow" style="top:318px"><span id="t5p" class="pill" style="opacity:0">consulte a disponibilidade</span></div>
  </div>

  <div id="rod" class="clip" data-start="{T_I}" data-duration="{R(T_A - T_I)}" data-track-index="9"><span id="rod-s">*Dados do fabricante</span></div>

  <div id="toque" class="clip" data-start="{R(T["toque"] - 0.02)}" data-duration="{R(TOTAL - T["toque"] + 0.02)}" data-track-index="11">
    <i id="tq-o1" class="tq-o"></i><i id="tq-o2" class="tq-o"></i><i id="tq-o3" class="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 120 120"><path d="M82 38 L42 78 M40 50 L40 80 L70 80" fill="none" stroke="{LINHO}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

{pn_html}
  <div id="fl0" class="clip flash" data-start="0.034" data-duration="0.1" data-track-index="13"></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{VOZ["intro"]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{VOZ["apresentacao"]}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{VOZ["cta"]}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="3.04" data-duration="0.55" data-track-index="22" data-volume="0.32" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-tique-1" data-start="{R(T["pra"] - 0.04)}" data-duration="0.03" data-track-index="22" data-volume="0.3" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-pop-1" data-start="{R(T["Segundo"] + 0.0)}" data-duration="0.09" data-track-index="22" data-volume="0.25" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="{R(T_CUT - 0.06)}" data-duration="0.3" data-track-index="22" data-volume="0.28" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="12.08" data-duration="0.42" data-media-start="0.97" data-track-index="22" data-volume="0.3" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-2" data-start="{R(T["consulte"] - 0.03)}" data-duration="0.09" data-track-index="22" data-volume="0.25" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-pop-3" data-start="17.6" data-duration="0.09" data-track-index="22" data-volume="0.22" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ================= INTRO: D 0-2,56 s (0,8x), vapor fino =================
tl.fromTo("#fl0", {{opacity:0.45}}, {{opacity:0, duration:0.09, ease:"power1.out"}}, 0.034);
tl.fromTo("#porta", {{scale:1.16}}, {{scale:1.0, duration:0.45, ease:"power3.out", transformOrigin:"50% 43.5%"}}, 0);
tl.fromTo("#linha-p", {{strokeDashoffset:{ARC_LEN}}}, {{strokeDashoffset:0, duration:0.9, ease:"power2.inOut"}}, 0.08);
tl.fromTo(["#linha-a", "#linha-b"], {{opacity:0}}, {{opacity:1, duration:0.1}}, 0.95);
tl.fromTo("#glow", {{opacity:0.55}}, {{opacity:1, duration:{TOTAL}, ease:"none"}}, 0);
tl.fromTo("#movD1", {{scale:1.0}}, {{scale:1.05, duration:{T_I}, ease:"none"}}, 0);
{slam("#t1r", 0, 1.14, 0.34, 1)}
{punch("#punD1", T["garrafa"], 1.06, 1.0, 0.1, 0.35)}
{placa("#t1p", T["todo"] - 0.06)}
{out(["#t1r", "#t1p"], T_I - 0.2)}

{painel(0, T_I)}

// ================= APRESENTAÇÃO: E 0,47-6,13 s (0,85x) -> corte seco -> D 5,00-7,64 s =================
tl.fromTo("#movE1", {{scale:1.07}}, {{scale:1.0, duration:0.45, ease:"power3.out"}}, {T_I});
tl.fromTo("#rod-s", {{opacity:0}}, {{opacity:1, duration:0.2, ease:"power1.out"}}, {R(T_I + 0.1)});
tl.fromTo("#rod-s", {{scale:1}}, {{scale:1.1, duration:0.15, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}}, {R(T["Segundo"])});
{placa("#t2a", T["Garrafa"] - 0.03)}
{reveal("#t2b", T["Hilee"] - 0.05, 0.38)}
// produto herói: a mão chega na alça ("alça na tampa") -> aproximação lenta na tampa, vídeo rodando
tl.to("#movE1", {{scale:1.12, duration:1.7, ease:"power1.inOut"}}, {R(T["alca"] - 0.06)});
{out(["#t2r", "#t2a"], T["pra"] - 0.2)}
{reveal("#t3a", T["pra"] - 0.04)}
{reveal("#t3b", T["levar"] - 0.04)}
tl.to("#movE1", {{scale:1.0, duration:0.55, ease:"power2.inOut"}}, {R(T["Segundo"] - 0.1)});
{placa("#t3p", T["Segundo"] - 0.06)}
{punch("#punE1", T["vazamentos"], 1.035, 1.0)}
{out(["#t3r", "#t3p"], T_CUT - 0.16, 0.12)}
// corte seco para a preta: detalhe da tampa com o vapor
tl.fromTo("#movD2", {{scale:1.24}}, {{scale:1.18, duration:0.3, ease:"power3.out"}}, {T_CUT});
tl.to("#movD2", {{scale:1.24, duration:{R(T_A - T_CUT - 0.3)}, ease:"none"}}, {R(T_CUT + 0.3)});
{slam("#t4a", T["tres"] - 0.04, 1.6, 0.3)}
{punch("#punD2", T["ate"], 1.04, 1.0, 0.1, 0.35)}
{out(["#t4a"], T_A - 0.26)}

{painel(1, T_A)}

// ================= CTA: F 0,60-5,75 s (0,92x), mais calma =================
tl.fromTo("#movF1", {{scale:1.05}}, {{scale:1.0, duration:0.55, ease:"power2.out"}}, {T_A});
tl.to("#movF1", {{scale:1.03, duration:{R(TOTAL - T_A - 0.55)}, ease:"none"}}, {R(T_A + 0.55)});
{reveal("#t5a", T["Confira"] - 0.04)}
{reveal("#t5b", T["tamanhos"] - 0.06)}
// "toque": botão com seta para baixo/esquerda + ondas
tl.fromTo("#tq-b", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(2.2)"}}, {R(T["toque"])});
tl.fromTo("#tq-s", {{x:0, y:0}}, {{x:-7, y:7, duration:0.22, yoyo:true, repeat:11, ease:"sine.inOut"}}, {R(T["toque"] + 0.3)});
tl.fromTo("#tq-o1", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["toque"])});
tl.fromTo("#tq-o2", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["produto"])});
tl.fromTo("#tq-o3", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["disp"])});
{punch("#punF1", T["toque"], 1.04, 1.0, 0.1, 0.4)}
{placa("#t5p", T["consulte"] - 0.06)}
tl.fromTo("#tq-b", {{scale:1}}, {{scale:1.12, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, 17.6);

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT)
