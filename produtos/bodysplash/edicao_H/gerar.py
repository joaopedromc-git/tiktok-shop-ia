#!/usr/bin/env python3
"""Gera produtos/bodysplash/edicao_H/index.html — estilo "Rodízio" (não precisa escolher, alterna).
Ameixa #1A1022 / magenta #FF3D9A / névoa #F8F2FB. Anton (títulos, uma linha, tarja) + Bebas Neue (legenda em
pilha, trilho seletor ENIGMA · MIDTOWN · BARBARIUS, linhas).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regras da 5ª violação (28/10/2026): clipe em TELA CHEIA o tempo todo (sem janela/moldura/cartão); texto leve só no
terço de cima (faixa y 196-524, coluna esquerda x 56-~380 para a legenda); nada sobre rótulo; nenhum brilho, partícula
ou flash sobre o produto; trocas por corte seco + "giro de carrossel" (o clipe novo entra deslizando 56 px, coberto,
sem transparência); nenhum quadro congelado; velocidade 0,9-1,1x.
Geometria medida nos quadros: J sobe o Midtown em x >= 385 (rótulo a partir de y ~150-530); L levanta o Enigma em
x >= 310 (tampa a partir de y ~200) e devolve em x 114-398 (tampa >= 412). Por isso a legenda fica na coluna
esquerda (x <= ~370) e, na CTA depois do "Toque", só em uma linha (y 326-416).
Trechos (analise_H.md / analise_F.md):
  intro        J 0,40-3,90 (1x)    mão entra e levanta o Midtown
  apresentação G 0,40-3,88 (1x)    dedo aperta a válvula do Enigma (lote F)  -> herói: zoom na válvula em "Enigma"
               H 0,10-1,71 (1x)    mão desce até a válvula do Barbarius (lote F, só 0-2,0 s)
               J 3,90-7,56 (0,9x)  Midtown desce e volta à fileira, mão solta
               K 6,40-7,95 (1,04x) Barbarius volta ao lugar, mão na válvula (K 1,0-6,3 tem Barbarius DUPLICADO)
  CTA          L 3,20-7,60 (1x)    mão levanta o Enigma e devolve (proibido antes de 3,2)
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

R = lambda v: str(round(v, 3))

# ---------------- partes ----------------
T_I, T_A, TOTAL = 3.5, 14.15, 18.55
VOZ = {"intro": 0.3, "apresentacao": 3.65, "cta": 14.45}
FIM = {"intro": T_I, "apresentacao": T_A, "cta": TOTAL}
DUR_MP3 = {"intro": 3.024, "apresentacao": 10.488, "cta": 3.432}


def t_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


def f_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["fim"], 3)


# (id, clipe, início, duração, media-start, rate, origem do zoom lento, direção do giro)
CORTES = [
    ("J1", "J", 0.0, 3.5, 0.40, 1.0, "50% 62%", 0),
    ("G1", "G", 3.5, 3.48, 0.40, 1.0, "50% 60%", 1),
    ("H1", "H", 6.98, 1.61, 0.10, 1.0, "50% 62%", -1),
    ("J2", "J", 8.59, 4.07, 3.90, 0.9, "50% 62%", 1),
    ("K1", "K", 12.66, 1.49, 6.40, 1.04, "88% 60%", -1),
    ("L1", "L", 14.15, 4.40, 3.20, 1.0, "40% 55%", 1),
]
for c in CORTES:   # trechos dentro do permitido
    fim_src = c[4] + c[3] * c[5]
    assert 0.9 <= c[5] <= 1.1, c
    lim = {"J": 8.0, "G": 4.0, "H": 2.0, "K": 7.95, "L": 7.6}[c[1]]
    assert fim_src <= lim + 0.005, (c, fim_src)

T = {
    "Tres_i": t_pal("intro", 0), "voce_i": t_pal("intro", 3), "escolher_i": t_pal("intro", 8),
    "Kit": t_pal("apresentacao", 0), "Enigma": t_pal("apresentacao", 5), "Midtown": t_pal("apresentacao", 6),
    "Barbarius": t_pal("apresentacao", 8), "juntos": t_pal("apresentacao", 9), "Perfis": t_pal("apresentacao", 10),
    "do": t_pal("apresentacao", 14), "fresco": t_pal("apresentacao", 15), "marcante": t_pal("apresentacao", 17),
    "marcante_f": f_pal("apresentacao", 17), "Em": t_pal("apresentacao", 18), "escolher": t_pal("apresentacao", 21),
    "voce": t_pal("apresentacao", 22), "alterna": t_pal("apresentacao", 23), "alterna_f": f_pal("apresentacao", 23),
    "Quer": t_pal("cta", 0), "tres": t_pal("cta", 2), "vez": t_pal("cta", 5), "Toque": t_pal("cta", 6),
    "produto": t_pal("cta", 8), "video": t_pal("cta", 10),
}

AMEIXA, MAGENTA, NEVOA = "#1A1022", "#FF3D9A", "#F8F2FB"

# ---------------- legenda "pilha de rodízio" (karaokê) ----------------
# cada grupo = lista de linhas; cada linha = índices de palavras. Linhas <= ~9 caracteres (coluna esquerda).
GRUPOS = {
    "intro": [[[0], [1]], [[2, 3], [4]], [[5, 6, 7], [8]], [[9, 10]]],
    "apresentacao": [[[0], [1, 2]], [[3], [4]], [[5]], [[6]], [[7], [8]], [[9]], [[10], [11, 12]], [[13]],
                     [[14, 15]], [[16], [17]], [[18, 19], [20]], [[21]], [[22], [23]]],
    "cta": [[[0], [1, 2]], [[3, 4], [5]], [[6, 7, 8]], [[9, 10]]],
}
CHAVE = {"intro": {0, 8, 9, 10}, "apresentacao": {5, 6, 8, 15, 17, 23}, "cta": {2, 6, 8}}
EXIBE = {("intro", 4): "curte,", ("intro", 10): "um?",
         ("apresentacao", 4): "Primacial:", ("apresentacao", 5): "Enigma,", ("apresentacao", 9): "juntos.",
         ("apresentacao", 13): "completam,", ("apresentacao", 17): "marcante.", ("apresentacao", 21): "escolher,",
         ("apresentacao", 23): "alterna.", ("cta", 5): "vez?", ("cta", 10): "vídeo."}
LEG_TOP = 326

leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = VOZ[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        idx = [i for linha in g for i in linha]
        s = round(voz + pal[idx[0]]["inicio"] - 0.05, 3)
        fim_voz = round(voz + pal[idx[-1]]["fim"] + 0.35, 3)
        if gi + 1 < len(grupos):
            prox = grupos[gi + 1][0][0]
            e = min(round(voz + pal[prox]["inicio"] - 0.05, 3), fim_voz)
        else:
            e = min(fim_voz, FIM[parte] - 0.03)
        gid = f"lg-{parte[:3]}-{gi}"
        rows = ""
        k = 0
        for linha in g:
            ems = ""
            for i in linha:
                txt = EXIBE.get((parte, i), pal[i]["palavra"]).upper()
                chave = i in CHAVE[parte]
                ems += f'<em id="{gid}-{k}" class="w"><b id="{gid}-{k}b">{txt}</b></em>'
                t_on = max(s + 0.02, t_pal(parte, i) - 0.02)
                leg_js.append(f'tl.to("#{gid}-{k}b",{{opacity:1,duration:0.05,ease:"none"}},{R(t_on)});')
                if chave:
                    leg_js.append(f'tl.to("#{gid}-{k}",{{backgroundColor:"{MAGENTA}",duration:0.06,ease:"none"}},{R(t_on)});')
                    leg_js.append(f'tl.to("#{gid}-{k}b",{{color:"{AMEIXA}",duration:0.06,ease:"none"}},{R(t_on)});')
                    leg_js.append(f'tl.fromTo("#{gid}-{k}",{{scale:1}},{{scale:1.1,duration:0.1,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{R(t_on)});')
                k += 1
            rows += f'<div class="lrow">{ems}</div>'
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div id="{gid}-p" class="pilha" style="top:{LEG_TOP}px">{rows}</div></div>')
        # rodízio: o grupo entra girando de baixo (rolodex) e sai girando para cima
        leg_js.append(f'tl.fromTo("#{gid}-p",{{rotationX:-80,y:34,opacity:0}},{{rotationX:0,y:0,opacity:1,duration:0.16,ease:"power3.out"}},{R(s)});')
        if e - s > 0.3:
            leg_js.append(f'tl.to("#{gid}-p",{{rotationX:70,y:-26,opacity:0,duration:0.09,ease:"power2.in"}},{R(e - 0.09)});')

# ---------------- vídeos (tela cheia) ----------------
vid_html = []
for n, (cid, clip, st, du, ms, rate, orig, _d) in enumerate(CORTES):
    rate_attr = f' data-playback-rate="{rate}"' if rate != 1.0 else ""
    vid_html.append(
        f'  <div id="cw{cid}" class="cw"><div id="mov{cid}" class="mov" style="transform-origin:{orig}">'
        f'<div id="pun{cid}" class="mov" style="transform-origin:{orig}">'
        f'<video id="v{cid}" class="clip full" data-start="{st}" data-duration="{du}" data-media-start="{ms}"{rate_attr} '
        f'data-track-index="{n % 2}" src="assets/clipe_{clip}.mp4" muted playsinline></video></div></div></div>')

video_js = []
for cid, clip, st, du, ms, rate, orig, d in CORTES:
    # zoom lento contínuo
    video_js.append(f'tl.fromTo("#mov{cid}",{{scale:1.0}},{{scale:1.05,duration:{R(du)},ease:"none"}},{R(st)});')
    if d:
        # giro de carrossel: o clipe novo entra deslizando (escala 1,12 cobre o deslocamento: nunca aparece borda)
        video_js.append(f'tl.fromTo("#cw{cid}",{{x:{56 * d},scale:1.12}},{{x:0,scale:1.0,duration:0.3,ease:"power3.out"}},{R(st)});')


def punch(sel, t, peak, rest=1.0, d1=0.1, d2=0.32):
    return (f'tl.to("{sel}",{{scale:{peak},duration:{d1},ease:"power3.out"}},{R(t)});\n'
            f'tl.to("{sel}",{{scale:{rest},duration:{d2},ease:"power2.inOut"}},{R(t + d1)});')


def slam(sel, t, s0=1.5, d=0.3, o0=0):
    return f'tl.fromTo("{sel}",{{scale:{s0},opacity:{o0}}},{{scale:1,opacity:1,duration:{d},ease:"back.out(1.7)"}},{R(t)});'


def rola_sai(sel, t, d=0.14):
    return f'tl.to("{sel}",{{rotationX:75,y:-30,opacity:0,duration:{d},ease:"power2.in"}},{R(t)});'


def rola_entra(sel, t, d=0.18):
    return f'tl.fromTo("{sel}",{{rotationX:-80,y:30,opacity:0}},{{rotationX:0,y:0,opacity:1,duration:{d},ease:"power3.out"}},{R(t)});'


# ---------------- trilho seletor ENIGMA · MIDTOWN · BARBARIUS ----------------
CELL = [180, 200, 244]
NOMES = ["ENIGMA", "MIDTOWN", "BARBARIUS"]
PAD = 8
CX = [PAD + sum(CELL[:i]) for i in range(3)]
RAIL_W = PAD * 2 + sum(CELL)


def sel_html(n, st, du):
    cells = "".join(f'<span id="s{n}n{i}" class="nm" style="left:{CX[i]}px;width:{CELL[i]}px">{NOMES[i]}</span>' for i in range(3))
    return (f'  <div id="sel{n}" class="clip trilho" data-start="{R(st)}" data-duration="{R(du)}" data-track-index="8">'
            f'<div id="s{n}r" class="rail" style="width:{RAIL_W}px"><i id="s{n}c" class="cap" style="width:{CELL[0]}px"></i>{cells}</div></div>')


def sel_vai(n, t, alvo, d=0.16):
    """cápsula magenta desliza até o nome 'alvo' (0,1,2) ou cobre os três ('todos')"""
    if alvo == "todos":
        x, w = CX[0], sum(CELL)
        on = [0, 1, 2]
    else:
        x, w, on = CX[alvo], CELL[alvo], [alvo]
    js = [f'tl.to("#s{n}c",{{x:{x - CX[0]},width:{w},duration:{d},ease:"power3.inOut"}},{R(t)});']
    for i in range(3):
        cor = AMEIXA if i in on else "rgba(248,242,251,0.5)"
        js.append(f'tl.to("#s{n}n{i}",{{color:"{cor}",duration:0.04,ease:"none"}},{R(t + (0.03 if i in on else 0))});')
    return "\n".join(js)


SEL = [
    (0, T["Enigma"] - 0.2, T["juntos"] + 0.62 - (T["Enigma"] - 0.2)),
    (1, T["Em"] - 0.1, T_A - 0.06 - (T["Em"] - 0.1)),
]
sel_divs = "\n".join(sel_html(n, st, du) for n, st, du in SEL)

sel_js = []
# 1: um nome por vez no tempo da fala; "juntos" = os três acesos
s0 = SEL[0][1]
sel_js.append(rola_entra("#s0r", s0))
sel_js.append(f'tl.to("#s0c",{{opacity:1,duration:0.06}},{R(T["Enigma"] - 0.02)});')
sel_js.append(sel_vai(0, T["Enigma"] - 0.04, 0, 0.01))
sel_js.append(sel_vai(0, T["Midtown"] - 0.06, 1))
sel_js.append(sel_vai(0, T["Barbarius"] - 0.06, 2))
sel_js.append(sel_vai(0, T["juntos"] - 0.04, "todos", 0.2))
sel_js.append(rola_sai("#s0r", SEL[0][1] + SEL[0][2] - 0.15))
# 2: "Em vez de escolher" hesita; "você alterna" = rodízio rápido, termina nos três
s1 = SEL[1][1]
sel_js.append(rola_entra("#s1r", s1))
sel_js.append(f'tl.to("#s1c",{{opacity:1,duration:0.06}},{R(T["Em"] + 0.1)});')
sel_js.append(sel_vai(1, T["Em"] + 0.08, 0, 0.01))
sel_js.append(sel_vai(1, T["escolher"] - 0.04, 1, 0.22))
sel_js.append(sel_vai(1, T["escolher"] + 0.3, 0, 0.18))
seq = [1, 2, 0, 1, 2]
for j, alvo in enumerate(seq):
    sel_js.append(sel_vai(1, T["voce"] + 0.02 + j * 0.18, alvo, 0.12))
sel_js.append(sel_vai(1, T["alterna_f"] - 0.05, "todos", 0.18))
sel_js.append(rola_sai("#s1r", T_A - 0.2))

HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:{AMEIXA}}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:{AMEIXA}}}
.clip{{position:absolute;inset:0}}
.full{{width:100%;height:100%;object-fit:cover}}
/* clipes em tela cheia */
.cw{{position:absolute;left:0;top:0;width:1080px;height:1920px;overflow:hidden;z-index:1}}
.mov{{position:absolute;left:0;top:0;width:100%;height:100%}}
/* títulos: Anton numa tarja ameixa, uma linha, faixa y 196-312 */
.titulo{{z-index:7;perspective:700px}}
.tt{{position:absolute;left:56px;top:196px;display:block;white-space:nowrap;font-family:"Anton";font-weight:400;font-size:100px;line-height:1;
  color:{NEVOA};background:{AMEIXA};padding:8px 24px 10px;border-radius:14px;transform-origin:0% 50%;box-shadow:0 12px 30px rgba(0,0,0,.35)}}
.tt .m{{font-style:normal;color:{MAGENTA}}}
/* trilho seletor (y 200-270) */
.trilho{{z-index:8;perspective:700px}}
.rail{{position:absolute;left:56px;top:200px;height:70px;display:block;background:{AMEIXA};border-radius:14px;
  box-shadow:0 12px 30px rgba(0,0,0,.35);transform-origin:50% 100%}}
.cap{{position:absolute;left:{CX[0]}px;top:8px;height:54px;display:block;background:{MAGENTA};border-radius:10px;opacity:0}}
.nm{{position:absolute;top:0;display:block;text-align:center;font-family:"Bebas Neue";font-size:54px;line-height:72px;letter-spacing:.03em;
  color:rgba(248,242,251,0.5)}}
/* linha "do fresco ao marcante" */
.linha{{z-index:8;perspective:700px}}
.lt{{position:absolute;left:56px;top:200px;display:block;white-space:nowrap;font-family:"Bebas Neue";font-size:54px;line-height:1;letter-spacing:.04em;
  color:{NEVOA};background:{AMEIXA};padding:9px 20px 7px;border-radius:14px;transform-origin:50% 100%;box-shadow:0 12px 30px rgba(0,0,0,.35)}}
.lt .m{{font-style:normal;color:{MAGENTA}}}
.lbar{{position:absolute;left:20px;right:20px;bottom:-12px;height:8px;display:block;border-radius:4px;background:{MAGENTA};transform-origin:0% 50%}}
/* legenda: pilha na coluna esquerda */
.legenda{{z-index:10;perspective:600px}}
.pilha{{position:absolute;left:56px;display:flex;flex-direction:column;align-items:flex-start;gap:4px;transform-origin:0% 100%}}
.lrow{{display:flex;gap:6px;align-items:flex-start}}
.w{{display:block;font-style:normal;background:{AMEIXA};border-radius:12px;padding:6px 14px 0;transform-origin:0% 50%}}
.w b{{display:block;font-family:"Bebas Neue";font-weight:400;font-size:84px;line-height:84px;letter-spacing:.02em;color:{NEVOA};opacity:0.42}}
/* CTA */
.cta{{z-index:9;perspective:700px}}
.pill{{position:absolute;left:56px;top:200px;height:72px;display:flex;align-items:center;gap:12px;white-space:nowrap;background:{MAGENTA};border-radius:14px;
  padding:0 22px 0 12px;font-family:"Bebas Neue";font-size:52px;line-height:1;letter-spacing:.03em;color:{AMEIXA};
  box-shadow:0 12px 30px rgba(0,0,0,.35);transform-origin:0% 50%}}
.pill svg{{display:block;width:56px;height:56px}}
.onda{{position:absolute;left:62px;top:204px;width:64px;height:64px;display:block;border:5px solid {MAGENTA};border-radius:50%;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- clipes em tela cheia: J 0,40-3,90 | G 0,40-3,88 | H 0,10-1,71 | J 3,90-7,56 (0,9x) | K 6,40-7,95 (1,04x) | L 3,20-7,60 -->
{chr(10).join(vid_html)}

  <!-- títulos (uma linha, faixa do alto) -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="1.12" data-track-index="7">
    <span id="t1a" class="tt" style="font-size:104px">ESCOLHER <i class="m">SÓ UM?</i></span></div>
  <div id="t2" class="clip titulo" data-start="{T_I}" data-duration="{R(T["Enigma"] - 0.2 - T_I)}" data-track-index="7">
    <span id="t2a" class="tt"><i class="m">OS TRÊS</i> NO KIT</span></div>
  <div id="t3" class="clip titulo" data-start="{T_A}" data-duration="{R(T["Toque"] - 0.08 - T_A)}" data-track-index="7">
    <span id="t3a" class="tt" style="font-size:84px"><i class="m">OS TRÊS</i> DE UMA VEZ</span></div>

  <!-- trilho seletor -->
{sel_divs}
  <div id="ln1" class="clip linha" data-start="{R(T["do"] - 0.12)}" data-duration="{R(T["Em"] - 0.1 - (T["do"] - 0.12))}" data-track-index="9">
    <span id="ln1a" class="lt">DO <i class="m">FRESCO</i> AO <i class="m">MARCANTE</i><i id="ln1b" class="lbar"></i></span></div>

  <!-- CTA: toque no produto do vídeo, seta para baixo/esquerda (produto marcado) -->
  <div id="cta1" class="clip cta" data-start="{R(T["Toque"] - 0.04)}" data-duration="{R(TOTAL - T["Toque"] + 0.04)}" data-track-index="9">
    <i id="on1" class="onda"></i><i id="on2" class="onda"></i>
    <span id="pl1" class="pill"><svg id="pls" viewBox="0 0 56 56"><path d="M42 14 L16 40 M15 21 L15 41 L35 41" fill="none" stroke="{AMEIXA}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>TOQUE NO PRODUTO DO VÍDEO</span></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{VOZ["intro"]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{VOZ["apresentacao"]}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{VOZ["cta"]}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="0.94" data-duration="0.3" data-track-index="22" data-volume="0.25" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="{R(T_I - 0.04)}" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="{R(T["Enigma"] - 0.2)}" data-duration="0.03" data-track-index="22" data-volume="0.3" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-pop-1" data-start="{R(T["juntos"] - 0.02)}" data-duration="0.09" data-track-index="22" data-volume="0.25" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-tique-2" data-start="{R(T["do"] - 0.12)}" data-duration="0.03" data-track-index="22" data-volume="0.25" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-3" data-start="{R(T["Em"] - 0.1)}" data-duration="0.03" data-track-index="22" data-volume="0.28" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="{R(T_A - 0.4)}" data-duration="0.4" data-media-start="0.99" data-track-index="22" data-volume="0.3" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["Toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-2" data-start="17.95" data-duration="0.09" data-track-index="22" data-volume="0.22" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ================= vídeo: zoom lento contínuo + giro de carrossel em cada troca =================
''' + "\n".join(video_js) + f'''

// ================= INTRO: J 0,40-3,90 (mão levanta o Midtown) =================
tl.fromTo("#punJ1", {{scale:1.2}}, {{scale:1.0, duration:0.42, ease:"power3.out"}}, 0);
{slam("#t1a", 0, 1.22, 0.3, 1)}
{rola_sai("#t1a", 0.96)}
{punch("#punJ1", T["escolher_i"], 1.04, 1.0, 0.1, 0.4)}

// ================= APRESENTAÇÃO =================
{slam("#t2a", T_I + 0.04, 1.15, 0.26)}
{rola_sai("#t2a", T["Enigma"] - 0.36)}
// produto herói: em "Enigma", aproxima na válvula com o dedo apertando (vídeo rodando)
tl.fromTo("#punG1", {{scale:1.0}}, {{scale:1.22, duration:0.55, ease:"power2.inOut", transformOrigin:"238px 720px"}}, {R(T["Enigma"] - 0.08)});
{rola_entra("#ln1a", T["do"] - 0.12)}
tl.fromTo("#ln1b", {{scaleX:0}}, {{scaleX:1, duration:{R(T["marcante_f"] - T["do"])}, ease:"power1.inOut"}}, {R(T["do"])});
{punch("#punJ2", T["marcante"], 1.05, 1.0, 0.1, 0.35)}
{rola_sai("#ln1a", T["Em"] - 0.24)}
''' + "\n".join(sel_js) + f'''
{punch("#punK1", T["alterna"], 1.05, 1.0, 0.1, 0.35)}

// ================= CTA: L 3,20-7,60 (mão levanta o Enigma e devolve), mais calma =================
{slam("#t3a", T["Quer"] - 0.06, 1.15, 0.26)}
{punch("#punL1", T["tres"], 1.03, 1.0, 0.1, 0.4)}
{rola_sai("#t3a", T["Toque"] - 0.22)}
tl.fromTo("#pl1", {{scale:0.5, opacity:0}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(2)"}}, {R(T["Toque"] - 0.04)});
tl.fromTo("#pls", {{x:0, y:0}}, {{x:-5, y:5, duration:0.24, yoyo:true, repeat:9, ease:"sine.inOut"}}, {R(T["Toque"] + 0.3)});
tl.fromTo("#on1", {{scale:0.7, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.1, opacity:0, duration:0.62}}], ease:"power2.out"}}, {R(T["Toque"])});
tl.fromTo("#on2", {{scale:0.7, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.1, opacity:0, duration:0.62}}], ease:"power2.out"}}, {R(T["produto"])});
{punch("#punL1", T["Toque"], 1.04, 1.0, 0.1, 0.4)}
tl.fromTo("#pl1", {{scale:1}}, {{scale:1.08, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}}, 17.95);

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT)
