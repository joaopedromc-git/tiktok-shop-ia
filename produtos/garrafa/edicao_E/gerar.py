#!/usr/bin/env python3
"""Gera produtos/garrafa/edicao_E/index.html ("termo duplo": carvão #141110 / brasa #FF5B23 / gelo #8FE3FF / creme #FFF4E6,
DM Serif Display + Inter 800, legenda "etiqueta térmica"). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra da 3ª violação: o vídeo roda do primeiro ao último quadro; nada de <img>, quadro congelado ou cartão.
Layout "vitrine": o clipe aparece nítido numa janela (garrafa inteira, ~90 % da altura da janela) sobre o próprio clipe
desfocado e escurecido, rodando junto. Título no alto (y 150-390), legenda embaixo da janela (y 1378-1488), rodapé 1498:
nenhum texto sobre a garrafa nem sobre a mão. A tinta quente/fria só vai no fundo desfocado, nunca na janela.
Trechos (analise_D.md / analise_B.md; PROIBIDO H 3,2-4,3 s, G 1,9-2,4 s, E 0-2,4 s parado):
  intro        H 0,80-3,078 s em 0,85x -> H 4,45-5,666 s em 0,80x
  apresentação E 2,47-7,979 s em 0,70x -> G 4,60-6,38 s em 1,0x
  CTA          I 1,40-6,08 s em 0,90x
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

TOTAL = 19.05
P = {"intro": (0.0, 4.2, 0.20), "apresentacao": (4.2, 13.85, 4.40), "cta": (13.85, TOTAL, 14.10)}
DUR_MP3 = {"intro": 4.032, "apresentacao": 9.384, "cta": 4.824}

R = lambda v: str(round(v, 3))

# ---------------- janela ----------------
WT, WH, WC = 400, 968, 510   # topo, altura e centro x da janela


def shot(s, top_ext, bot_ext):
    """escala do clipe, largura da janela e topo do clipe dentro da janela (garrafa centrada na altura)"""
    top = (WH - (bot_ext - top_ext) * s) / 2 - top_ext * s
    w = 1080 * s
    return {"s": s, "w": round(w), "left": round(WC - w / 2), "top": round(top), "h": round(1920 * s),
            "oy": round(((top_ext + bot_ext) / 2) / 1920 * 100, 1)}


S = {
    "H": shot(0.728, 420, 1590),   # garrafa em repouso; no levantamento (1,75-2,2 s) a câmera acompanha (+188 px)
    "E": shot(0.57, 70, 1666),     # união do trecho inteiro (sobe até 70 px no alto)
    "G": shot(0.578, 100, 1675),   # união (desce de 100 para 225)
    "I": shot(0.738, 440, 1620),
}

# (id, clipe, início, duração, media-start, rate)
CORTES = [
    ("H1", "H", 0.0, 2.68, 0.80, 0.85),
    ("H2", "H", 2.68, 1.52, 4.45, 0.80),
    ("E", "E", 4.2, 7.87, 2.47, 0.70),
    ("G", "G", 12.07, 1.78, 4.60, 1.0),
    ("I", "I", 13.85, 5.2, 1.40, 0.90),
]

# ---------------- legenda ----------------
GRUPOS = {
    "intro": [[0, 1], [2, 3], [4, 5, 6], [7, 8], [9, 10]],
    "apresentacao": [[0], [1, 2], [3, 4], [5], [6, 7, 8], [9], [10, 11], [12, 13], [14, 15], [16, 17], [18],
                     [19, 20, 21], [22, 23], [24, 25]],
    "cta": [[0, 1, 2], [3], [4, 5], [6], [7, 8], [9, 10], [11, 12]],
}
# q = quente (brasa), f = fria (gelo), n = neutra (carvão)
CHAVE = {
    "intro": {0: "q", 3: "f", 6: "q", 8: "f"},
    "apresentacao": {2: "n", 9: "q", 12: "q", 15: "f", 18: "f", 19: "q", 23: "f"},
    "cta": {0: "f", 2: "q", 4: "n", 10: "n"},
}
EXIBE = {("intro", 1): "acesa,", ("intro", 3): "fria,", ("intro", 10): "novo?",
         ("apresentacao", 5): "fabricante,", ("apresentacao", 12): "12", ("apresentacao", 18): "18.",
         ("apresentacao", 21): "trilha,", ("apresentacao", 25): "trabalho.",
         ("cta", 3): "primeiro?", ("cta", 12): "detalhes."}
TOPO_LEG = 1378


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


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
            t = t_pal(parte, i)
            cls = CHAVE[parte].get(i)
            if cls:
                ems += f'<em id="{gid}-{k}" class="w k {cls}"><i id="{gid}-{k}h" class="hl"></i><b id="{gid}-{k}b">{txt}</b></em>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}h",{{scaleX:0}},{{scaleX:1,duration:0.13,ease:"power3.out"}},{R(max(s, t - 0.02))});')
                if cls == "n":
                    leg_js.append(f'tl.fromTo("#{gid}-{k}b",{{color:"#141110"}},{{color:"#FFF4E6",duration:0.06,ease:"none"}},{R(max(s, t))});')
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{scale:1}},{{scale:1.08,duration:0.09,yoyo:true,repeat:1,ease:"power2.out"}},{R(max(s, t - 0.02))});')
            else:
                ems += f'<em id="{gid}-{k}" class="w"><b>{txt}</b></em>'
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div class="cap" style="top:{TOPO_LEG}px"><span id="{gid}-p" class="ctag">{ems}</span></div></div>')
        leg_js.append(f'tl.fromTo("#{gid}-p",{{scale:0.9,y:12}},{{scale:1,y:0,duration:0.14,ease:"back.out(2.2)"}},{R(s)});')

T = {
    "fria_i": t_pal("intro", 3), "cafe_i": t_pal("intro", 6), "esfriou": t_pal("intro", 8), "novo": t_pal("intro", 10),
    "MODUS": t_pal("apresentacao", 2), "segundo": t_pal("apresentacao", 3), "quente": t_pal("apresentacao", 9),
    "doze": t_pal("apresentacao", 12), "fria_a": t_pal("apresentacao", 15), "dezoito": t_pal("apresentacao", 18),
    "Cafe": t_pal("apresentacao", 19), "agua": t_pal("apresentacao", 22),
    "Praia": t_pal("cta", 0), "trilha_c": t_pal("cta", 2), "Toque": t_pal("cta", 4), "produto": t_pal("cta", 6),
    "confira": t_pal("cta", 10), "detalhes": t_pal("cta", 12),
}

# ---------------- vídeos ----------------
win_html, bg_html = [], []
for n, (cid, clip, st, du, ms, rate) in enumerate(CORTES):
    g = S[clip]
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1.0 else ""
    win_html.append(
        f'    <div id="mov{cid}" class="mov" style="top:{g["top"]}px;width:{g["w"]}px;height:{g["h"]}px;transform-origin:50% {g["oy"]}%">'
        f'<video id="v{cid}" class="clip full" data-start="{st}" data-duration="{du}" data-media-start="{ms}"{rate_attr} '
        f'data-track-index="{n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video></div>')
    bg_html.append(
        f'    <video id="b{cid}" class="clip full" data-start="{R(max(0, st - 0.001))}" data-duration="{R(du + (0.001 if st > 0 else -0.001))}" data-media-start="{ms}"{rate_attr} '
        f'data-track-index="{2 + n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video>')


def win_set(clip, t):
    g = S[clip]
    return f'tl.set("#win",{{left:{g["left"]},width:{g["w"]}}},{R(t)});'


def punch(sel, t, peak, rest, d1=0.1, d2=0.3):
    return (f'tl.to("{sel}",{{scale:{peak},duration:{d1},ease:"power3.out"}},{R(t)});\n'
            f'tl.to("{sel}",{{scale:{rest},duration:{d2},ease:"power2.inOut"}},{R(t + d1)});')


def shutter(n, cut):
    return (f'tl.fromTo("#sht{n}",{{y:-962}},{{keyframes:[{{y:0,duration:0.17,ease:"power2.in"}},{{y:0,duration:0.02}},{{y:-962,duration:0.17,ease:"power2.out"}}]}},{R(cut - 0.18)});\n'
            f'tl.fromTo("#shb{n}",{{y:962}},{{keyframes:[{{y:0,duration:0.17,ease:"power2.in"}},{{y:0,duration:0.02}},{{y:962,duration:0.17,ease:"power2.out"}}]}},{R(cut - 0.18)});')


SHUT = [4.2, 12.07, 13.85]
shut_html = "\n".join(
    f'  <div id="sh{n}" class="clip shut" data-start="{R(c - 0.18)}" data-duration="0.36" data-track-index="12">'
    f'<span id="sht{n}" class="sh-t"></span><span id="shb{n}" class="sh-b"></span></div>' for n, c in enumerate(SHUT))

# botão do "Toque": canto inferior esquerdo da janela do I (areia; a garrafa começa em x ~361)
BX, BY = 140, 1186

HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:"DM Termo";src:local("DM Serif Display Regular"),local("DMSerifDisplay-Regular"),local("DM Serif Display")}}
@font-face{{font-family:"Inter Termo";font-weight:100 900;src:local("Inter Thin"),local("Inter-Thin"),local("Inter")}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#141110}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:#141110;font-family:"Inter Termo";font-weight:800}}
.clip{{position:absolute;inset:0}}
.full{{width:100%;height:100%;object-fit:cover}}
/* fundo: o mesmo clipe, desfocado e escurecido (renderizado pequeno e ampliado 3x) */
#bg{{position:absolute;left:0;top:0;width:360px;height:640px;overflow:hidden;transform:scale(3);transform-origin:0 0;
  filter:blur(7px) brightness(.42) saturate(1.1);z-index:1}}
#bg video{{transform:none}}
.tint{{position:absolute;inset:0;z-index:2;opacity:0}}
#tw{{background:radial-gradient(ellipse 120% 70% at 15% 80%,rgba(255,91,35,.42) 0,rgba(255,91,35,0) 70%),
  linear-gradient(to bottom,rgba(20,17,16,.15),rgba(60,20,8,.35))}}
#tc{{background:radial-gradient(ellipse 120% 70% at 85% 25%,rgba(143,227,255,.32) 0,rgba(143,227,255,0) 70%),
  linear-gradient(to bottom,rgba(8,30,44,.35),rgba(20,17,16,.15))}}
/* janela nítida */
#win{{position:absolute;top:{WT}px;height:{WH}px;left:{S["H"]["left"]}px;width:{S["H"]["w"]}px;overflow:hidden;border-radius:40px;z-index:5;
  background:#141110;box-shadow:0 26px 60px rgba(0,0,0,.55)}}
.mov{{position:absolute;left:0}}
#frame{{position:absolute;inset:0;display:block;border-radius:40px;border:7px solid #FFF4E6;z-index:3}}
#glow{{position:absolute;inset:0;display:block;border-radius:40px;border:7px solid #FF5B23;z-index:4;opacity:0}}
/* régua térmica na margem esquerda (longe da garrafa) */
#gauge{{z-index:4}}
#g-tube{{position:absolute;left:38px;top:540px;width:44px;height:700px;display:block;border-radius:22px;border:5px solid #FFF4E6;
  background:rgba(20,17,16,.55);overflow:hidden}}
#g-fill{{position:absolute;left:5px;right:5px;bottom:5px;height:680px;display:block;border-radius:14px;background:#FF5B23;transform-origin:50% 100%}}
.g-tk{{position:absolute;left:88px;width:18px;height:5px;display:block;border-radius:3px;background:#FFF4E6;opacity:.8}}
#g-bulb{{position:absolute;left:30px;top:1232px;width:60px;height:60px;display:block;border-radius:50%;border:5px solid #FFF4E6;background:#FF5B23}}
/* títulos */
.titulo{{z-index:6}}
.row{{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-end;gap:22px;white-space:nowrap}}
.dm{{display:block;font-family:"DM Termo";font-weight:400;line-height:1;color:#FFF4E6;text-shadow:0 6px 0 rgba(20,17,16,.85),0 0 30px rgba(20,17,16,.6)}}
.dm.q{{color:#FF5B23}} .dm.f{{color:#8FE3FF}}
.pill{{display:flex;align-items:center;gap:12px;white-space:nowrap;font-family:"Inter Termo";font-weight:800;font-size:40px;line-height:1;
  padding:12px 24px 14px;border-radius:40px;background:#FFF4E6;color:#141110;box-shadow:0 8px 0 rgba(20,17,16,.6)}}
.pill.q{{background:#FF5B23}} .pill.f{{background:#8FE3FF}}
.pill b{{font-weight:900}}
/* rodapé */
#rod{{z-index:7}}
#rod span{{position:absolute;left:60px;top:1498px;display:block;font-family:"Inter Termo";font-weight:600;font-size:30px;line-height:1;
  color:rgba(255,244,230,.85);background:rgba(20,17,16,.6);padding:7px 14px 8px;border-radius:10px}}
/* legenda "etiqueta térmica" */
.legenda{{z-index:10}}
.cap{{position:absolute;left:40px;width:880px;display:flex;justify-content:center;align-items:flex-start}}
.ctag{{display:flex;gap:18px;align-items:center;white-space:nowrap;background:#FFF4E6;border-radius:26px;
  padding:6px 24px 10px;box-shadow:0 10px 0 rgba(20,17,16,.7),0 18px 34px rgba(0,0,0,.45)}}
.w{{position:relative;display:block;font-style:normal;font-family:"Inter Termo";font-weight:800;font-size:84px;line-height:1.1;color:#141110}}
.w b{{font-weight:800}}
.w.k{{padding:0 14px 4px}}
.w b{{position:relative}}
.hl{{position:absolute;inset:0;display:block;border-radius:16px;transform-origin:0 50%}}
.w.q .hl{{background:#FF5B23}} .w.f .hl{{background:#8FE3FF}} .w.n .hl{{background:#141110}}
/* CTA */
#toque{{z-index:11}}
#tq-b{{position:absolute;left:{BX}px;top:{BY}px;width:124px;height:124px;display:block;border-radius:50%;background:#FF5B23;
  box-shadow:0 0 0 8px #FFF4E6,0 14px 30px rgba(0,0,0,.5)}}
#tq-b svg{{display:block;width:124px;height:124px}}
.tq-o{{position:absolute;left:{BX}px;top:{BY}px;width:124px;height:124px;display:block;border:7px solid #8FE3FF;border-radius:50%;opacity:0}}
/* obturador quente/frio: dois painéis opacos de bordas duras */
.shut{{z-index:12;overflow:hidden}}
.sh-t,.sh-b{{position:absolute;left:0;width:1080px;height:962px;display:block}}
.sh-t{{top:0;background:#FF5B23;border-bottom:10px solid #141110}}
.sh-b{{top:958px;background:#8FE3FF;border-top:10px solid #141110}}
.flash{{z-index:13;background:#FFF4E6;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- fundo desfocado: o mesmo trecho de cada clipe, rodando junto -->
  <div id="bg">
{chr(10).join(bg_html)}
  </div>
  <div id="tw" class="tint"></div>
  <div id="tc" class="tint"></div>

  <!-- janela nítida: H 0,80-3,078 (0,85x) | H 4,45-5,666 (0,80x) | E 2,47-7,979 (0,70x) | G 4,60-6,38 | I 1,40-6,08 (0,90x) -->
  <div id="win">
{chr(10).join(win_html)}
    <i id="frame"></i><i id="glow"></i>
  </div>

  <div id="gauge" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="4">
    <div id="g-in">
      <span id="g-tube"><i id="g-fill"></i></span><span id="g-bulb"></span>
      <i class="g-tk" style="top:600px"></i><i class="g-tk" style="top:740px"></i><i class="g-tk" style="top:880px"></i><i class="g-tk" style="top:1020px"></i><i class="g-tk" style="top:1160px"></i>
    </div>
  </div>

  <!-- títulos (faixa do alto, acima da janela) -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="4.2" data-track-index="7">
    <div class="row" style="top:150px;height:86px"><span id="t1a" class="dm" style="font-size:86px">O CAFÉ</span></div>
    <div class="row" style="top:150px;height:86px"><span id="t1s" class="pill">e a noite nem começou</span></div>
    <div class="row" style="top:236px;height:156px"><span id="t1b" class="dm q" style="font-size:156px">ESFRIOU?</span></div>
  </div>
  <div id="t2" class="clip titulo" data-start="{R(T["quente"] - 0.04)}" data-duration="{R(13.85 - T["quente"] + 0.04)}" data-track-index="8">
    <div class="row" style="top:166px;height:116px"><span id="t2a" class="dm q" style="font-size:116px">QUENTE</span><span id="t2b" class="dm" style="font-size:72px;padding-bottom:10px">ou</span><span id="t2c" class="dm f" style="font-size:116px">FRIA*</span></div>
    <div class="row" style="top:304px;height:68px"><span id="t2d" class="pill q"><b>12 h</b> quente</span><span id="t2e" class="pill f"><b>18 h</b> fria</span></div>
  </div>
  <div id="t3" class="clip titulo" data-start="{R(T["Praia"] - 0.06)}" data-duration="{R(TOTAL - T["Praia"] + 0.06)}" data-track-index="7">
    <div class="row" style="top:150px;height:68px"><span id="t3s" class="pill">praia ou trilha?</span></div>
    <div class="row" style="top:250px;height:104px"><span id="t3a" class="dm" style="font-size:98px">TOQUE</span><span id="t3b" class="dm f" style="font-size:98px">E CONFIRA</span></div>
  </div>

  <div id="rod" class="clip" data-start="4.2" data-duration="9.65" data-track-index="9"><span id="rod-s">*Dados do fabricante</span></div>

  <div id="toque" class="clip" data-start="{R(T["Toque"])}" data-duration="{R(TOTAL - T["Toque"])}" data-track-index="11">
    <i id="tq-o1" class="tq-o"></i><i id="tq-o2" class="tq-o"></i><i id="tq-o3" class="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 124 124"><path d="M84 40 L44 80 M42 52 L42 82 L72 82" fill="none" stroke="#141110" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

{shut_html}
  <div id="fl0" class="clip flash" data-start="0" data-duration="0.12" data-track-index="13"></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{P["intro"][2]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{P["apresentacao"][2]}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{P["cta"][2]}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="2.6" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="3.98" data-duration="0.55" data-track-index="22" data-volume="0.34" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-brilho-1" data-start="5.92" data-duration="0.9" data-track-index="22" data-volume="0.24" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-tique-1" data-start="9.29" data-duration="0.03" data-track-index="22" data-volume="0.35" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="11.99" data-duration="0.3" data-track-index="22" data-volume="0.28" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="13.45" data-duration="0.4" data-media-start="1" data-track-index="22" data-volume="0.3" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["Toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-1" data-start="18.62" data-duration="0.09" data-track-index="22" data-volume="0.25" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ---------- tinta do fundo (só no fundo desfocado): quente até o corte do G, fria depois ----------
tl.set("#tw", {{opacity:1}}, 0);
tl.set("#tc", {{opacity:0}}, 0);
tl.set("#tw", {{opacity:0}}, 12.07);
tl.set("#tc", {{opacity:1}}, 12.07);
// largura da janela por clipe (troca escondida pelo obturador)
{win_set("H", 0)}
{win_set("E", 4.2)}
{win_set("G", 12.07)}
{win_set("I", 13.85)}

// ================= INTRO: H 0,80-3,078 s (0,85x) =================
tl.fromTo("#fl0", {{opacity:0.9}}, {{opacity:0, duration:0.1, ease:"power1.out"}}, 0);
tl.fromTo("#win", {{scale:1.12}}, {{scale:1.0, duration:0.4, ease:"power3.out"}}, 0);
tl.fromTo("#movH1", {{scale:1.0, y:0}}, {{scale:1.02, duration:2.56, ease:"none"}}, 0);
// a mão levanta a garrafa (1,75-2,2 s do clipe): a câmera acompanha para a tampa nunca sair da janela
tl.to("#movH1", {{y:188, duration:0.6, ease:"sine.inOut"}}, 1.08);
{punch("#win", T["fria_i"], 1.035, 1.0)}
// corte com desfoque (pula o giro proibido 3,2-4,3 s)
tl.to("#movH1", {{filter:"blur(14px)", duration:0.12, ease:"power2.in"}}, 2.56);
tl.fromTo("#movH2", {{y:24, scale:1.04, filter:"blur(14px)"}}, {{y:24, scale:1.0, filter:"blur(0px)", duration:0.18, ease:"power3.out"}}, 2.68);
tl.to("#movH2", {{scale:1.025, duration:1.3, ease:"none"}}, 2.86);
// título do gancho
tl.fromTo("#t1a", {{y:-40, opacity:0}}, {{y:0, opacity:1, duration:0.24, ease:"power3.out"}}, 0.02);
tl.fromTo("#t1b", {{scale:2.1, opacity:0}}, {{scale:1, opacity:1, duration:0.32, ease:"back.out(1.6)"}}, 0.05);
tl.fromTo("#t1s", {{opacity:0}}, {{opacity:0, duration:0.01}}, 0);
// "esfriou": a palavra gela (brasa -> gelo) e treme; a régua despenca
tl.to("#t1b", {{color:"#8FE3FF", duration:0.25, ease:"power1.out"}}, {R(T["esfriou"])});
tl.fromTo("#t1b", {{x:0}}, {{x:7, duration:0.04, yoyo:true, repeat:7, ease:"sine.inOut"}}, {R(T["esfriou"] + 0.02)});
tl.to("#t1a", {{y:-30, opacity:0, duration:0.16, ease:"power2.in"}}, {R(T["novo"] - 0.1)});
tl.fromTo("#t1s", {{y:30, opacity:0}}, {{y:0, opacity:1, duration:0.22, ease:"back.out(2)", immediateRender:false}}, {R(T["novo"] + 0.06)});
tl.to(["#t1b", "#t1s"], {{y:-30, opacity:0, duration:0.14, ease:"power2.in"}}, 3.98);

// régua térmica
tl.fromTo("#g-in", {{x:-120}}, {{x:0, duration:0.35, ease:"power3.out"}}, 0.1);
tl.fromTo("#g-fill", {{scaleY:0.05, backgroundColor:"#FF5B23"}}, {{scaleY:0.88, duration:0.5, ease:"power2.out"}}, 0.15);
tl.fromTo("#g-bulb", {{backgroundColor:"#FF5B23"}}, {{backgroundColor:"#8FE3FF", duration:0.3, ease:"power1.out"}}, {R(T["esfriou"])});
tl.to("#g-fill", {{scaleY:0.16, backgroundColor:"#8FE3FF", duration:0.5, ease:"power2.in"}}, {R(T["esfriou"])});

{shutter(0, 4.2)}

// ================= APRESENTAÇÃO: E 2,47-7,979 s (0,70x) =================
tl.fromTo("#movE", {{scale:1.0}}, {{scale:1.025, duration:7.7, ease:"none"}}, 4.2);
tl.fromTo("#win", {{scale:1.06}}, {{scale:1.0, duration:0.35, ease:"power3.out", immediateRender:false}}, 4.2);
tl.fromTo("#rod-s", {{opacity:0}}, {{opacity:1, duration:0.2, ease:"power1.out"}}, 4.25);
// produto herói no "MODUS": a janela cresce e o contorno acende em brasa (sobre o vídeo rodando)
tl.to("#win", {{scale:1.06, duration:0.14, ease:"power3.out"}}, {R(T["MODUS"])});
tl.to("#win", {{scale:1.035, duration:0.5, ease:"power2.inOut"}}, {R(T["MODUS"] + 0.14)});
tl.fromTo("#glow", {{opacity:0}}, {{keyframes:[{{opacity:1, duration:0.12}}, {{opacity:1, duration:0.6}}, {{opacity:0, duration:0.3}}]}}, {R(T["MODUS"])});
tl.to("#win", {{scale:1.0, duration:0.6, ease:"power1.inOut"}}, {R(T["segundo"] + 0.2)});
tl.fromTo("#rod-s", {{scale:1.1}}, {{scale:1, duration:0.3, ease:"back.out(2)", transformOrigin:"0% 50%", immediateRender:false}}, {R(T["segundo"])});
// "quente": título; régua sobe em brasa
tl.fromTo("#t2a", {{scale:1.9, opacity:0}}, {{scale:1, opacity:1, duration:0.28, ease:"back.out(1.7)"}}, {R(T["quente"] - 0.03)});
tl.fromTo(["#t2b", "#t2c"], {{opacity:0}}, {{opacity:0, duration:0.01}}, {R(T["quente"] - 0.03)});
tl.to("#g-fill", {{scaleY:1, backgroundColor:"#FF5B23", duration:0.4, ease:"power2.out"}}, {R(T["quente"])});
tl.to("#g-bulb", {{backgroundColor:"#FF5B23", duration:0.2}}, {R(T["quente"])});
{punch("#win", T["quente"], 1.03, 1.0)}
tl.fromTo("#t2d", {{y:30, opacity:0}}, {{y:0, opacity:1, duration:0.22, ease:"back.out(2)"}}, {R(T["doze"] - 0.03)});
tl.fromTo("#t2e", {{y:30, opacity:0}}, {{y:0, opacity:1, duration:0.22, ease:"back.out(2)"}}, {R(T["dezoito"] - 0.03)});
// "fria"
tl.to(["#t2b"], {{opacity:1, duration:0.15}}, {R(T["fria_a"] - 0.2)});
tl.fromTo("#t2c", {{scale:1.9, opacity:0}}, {{scale:1, opacity:1, duration:0.28, ease:"back.out(1.7)", immediateRender:false}}, {R(T["fria_a"] - 0.03)});
tl.to("#g-fill", {{backgroundColor:"#8FE3FF", duration:0.3}}, {R(T["fria_a"])});
tl.to("#g-bulb", {{backgroundColor:"#8FE3FF", duration:0.2}}, {R(T["fria_a"])});
{punch("#win", T["fria_a"], 1.03, 1.0)}
// "Café na trilha": a etiqueta 12 h pulsa, régua em brasa
tl.to("#g-fill", {{backgroundColor:"#FF5B23", duration:0.25}}, {R(T["Cafe"])});
tl.to("#g-bulb", {{backgroundColor:"#FF5B23", duration:0.2}}, {R(T["Cafe"])});
tl.fromTo("#t2d", {{scale:1}}, {{scale:1.14, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {R(T["Cafe"])});
{punch("#win", T["Cafe"], 1.03, 1.0)}

{shutter(1, 12.07)}

// G 4,60-6,38 s: "água fria no trabalho"
tl.fromTo("#movG", {{scale:1.0}}, {{scale:1.025, duration:1.78, ease:"none"}}, 12.07);
tl.to("#g-fill", {{backgroundColor:"#8FE3FF", duration:0.25}}, {R(T["agua"])});
tl.to("#g-bulb", {{backgroundColor:"#8FE3FF", duration:0.2}}, {R(T["agua"])});
tl.fromTo("#t2e", {{scale:1}}, {{scale:1.14, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, {R(T["agua"])});
{punch("#win", T["agua"], 1.03, 1.0)}
tl.to(["#t2a", "#t2b", "#t2c", "#t2d", "#t2e"], {{y:-30, opacity:0, duration:0.14, ease:"power2.in"}}, 13.6);

{shutter(2, 13.85)}

// ================= CTA: I 1,40-6,08 s (0,90x), mais calma =================
tl.fromTo("#movI", {{scale:1.0}}, {{scale:1.03, duration:5.2, ease:"none"}}, 13.85);
tl.fromTo("#win", {{scale:1.05}}, {{scale:1.0, duration:0.5, ease:"power2.out", immediateRender:false}}, 13.85);
tl.fromTo("#t3s", {{y:-30, opacity:0}}, {{y:0, opacity:1, duration:0.24, ease:"power3.out"}}, {R(T["Praia"] - 0.04)});
tl.to("#g-fill", {{scaleY:0.6, backgroundColor:"#8FE3FF", duration:0.3}}, {R(T["Praia"])});
tl.to("#g-fill", {{backgroundColor:"#FF5B23", duration:0.25}}, {R(T["trilha_c"])});
tl.to("#g-bulb", {{backgroundColor:"#FF5B23", duration:0.2}}, {R(T["trilha_c"])});
tl.to("#g-in", {{x:-140, opacity:0, duration:0.25, ease:"power2.in"}}, {R(T["Toque"] - 0.2)});
// "Toque": título + botão com seta para baixo/esquerda + ondas
tl.fromTo("#t3a", {{scale:1.8, opacity:0}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(1.7)"}}, {R(T["Toque"] - 0.03)});
tl.fromTo("#t3b", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:0.24, ease:"power3.out"}}, {R(T["confira"] - 0.04)});
{punch("#win", T["Toque"], 1.035, 1.0, 0.1, 0.4)}
tl.fromTo("#tq-b", {{scale:0.4, opacity:0}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(2.2)"}}, {R(T["Toque"])});
tl.fromTo("#tq-s", {{x:0, y:0}}, {{x:-7, y:7, duration:0.22, yoyo:true, repeat:9, ease:"sine.inOut"}}, {R(T["Toque"] + 0.3)});
tl.fromTo("#tq-o1", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["Toque"])});
tl.fromTo("#tq-o2", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["produto"])});
tl.fromTo("#tq-o3", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["detalhes"])});
tl.fromTo("#tq-b", {{scale:1}}, {{scale:1.12, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, 18.62);

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT)
