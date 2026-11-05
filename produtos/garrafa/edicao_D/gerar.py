#!/usr/bin/env python3
"""Gera produtos/garrafa/edicao_D/index.html ("seco ao toque": giz #F6F4EE / tinta #0F1317 / cobalto #2D5BFF,
Bebas Neue + Inter 800, legenda "etiqueta marca-texto"). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra da 3ª violação: o vídeo de fundo roda do primeiro ao último quadro; nada de <img>, quadro congelado ou cartão.
Trechos (analise_D.md + quadros conferidos em 15/10/2026; PROIBIDO G 1,9-2,4 s e H 3,2-4,3 s):
  intro        G 0,25-1,80 s em 0,92x -> G 2,50-4,28 s em 1,0x (garrafa no alto, mesa seca embaixo)
  apresentação H 0,00-2,97 s em 0,90x -> H 4,40-7,955 s em 0,79x (fogueira o tempo todo) -> G 4,50-6,75 s em 0,85x
  CTA          I 1,00-6,00 s em 0,90x (ondas o tempo todo; mão segura a alça)
Efeitos só por cima do vídeo rodando: punch-ins no ritmo da fala, chicote vertical/lateral, zoom com desfoque,
"passada seca" (faixa de giz que varre a tela) nas trocas de parte, cantoneiras de mira em volta da garrafa inteira,
anel cobalto na tampa, reflexo de luz na garrafa. Nada que pareça gota, água ou poça.
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

TOTAL = 19.5
# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 3.5, 0.20), "apresentacao": (3.5, 13.95, 3.75), "cta": (13.95, TOTAL, 14.20)}
DUR_MP3 = {"intro": 3.24, "apresentacao": 10.128, "cta": 5.256}
TOPO_LEG = 1296  # etiqueta da legenda 1296-1390 (67-72 % da altura): corpo de baixo da garrafa, longe da etiqueta MODUS

GRUPOS = {
    "intro": [[0, 1, 2], [3, 4], [5, 6, 7], [8, 9, 10]],
    "apresentacao": [[0, 1], [2], [3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17],
                     [18, 19, 20], [21, 22], [23, 24], [25, 26]],
    "cta": [[0, 1, 2], [3, 4, 5], [6], [7, 8], [9], [10, 11], [12, 13]],
}
CHAVE = {
    "intro": {2, 4, 8},
    "apresentacao": {2, 5, 9, 13, 15, 17, 22, 26},
    "cta": {2, 6, 8, 11},
}
EXIBE = {("intro", 10): "novo?", ("apresentacao", 2): "MODUS", ("apresentacao", 17): "vazamento,",
         ("apresentacao", 20): "fabricante.", ("apresentacao", 26): "bolsa.", ("cta", 5): "rotina?",
         ("cta", 13): "perto."}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---------------- legenda "etiqueta marca-texto": etiqueta de giz; cada palavra sobe no seu tempo;
# as palavras do grupo ficam apagadas (20 %) e "entintam" no seu tempo; a palavra-chave ganha um bloco cobalto que corre por trás (marca-texto) e fica branca ----------------
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
            e = min(fim_voz, P[parte][1])
        gid = f"lg-{parte[:3]}-{gi}"
        ems = ""
        for k, i in enumerate(g):
            txt = EXIBE.get((parte, i), pal[i]["palavra"])
            t = t_pal(parte, i)
            if i in CHAVE[parte]:
                ems += f'<em id="{gid}-{k}" class="w k"><i id="{gid}-{k}h" class="hl"></i><b id="{gid}-{k}b">{txt}</b></em>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}h",{{scaleX:0}},{{scaleX:1,duration:0.14,ease:"power3.out"}},{R(t)});')
                leg_js.append(f'tl.fromTo("#{gid}-{k}b",{{color:"#0F1317"}},{{color:"#F6F4EE",duration:0.08,ease:"none"}},{R(t + 0.03)});')
            else:
                ems += f'<em id="{gid}-{k}" class="w"><b>{txt}</b></em>'
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.2,y:12}},{{opacity:1,y:0,duration:0.11,ease:"power2.out"}},{R(max(s, t - 0.03))});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div class="cap" style="top:{TOPO_LEG}px"><span id="{gid}-p" class="ctag">{ems}</span></div></div>')
        leg_js.append(f'tl.fromTo("#{gid}-p",{{scale:0.93,y:10}},{{scale:1,y:0,duration:0.15,ease:"back.out(2.2)"}},{R(s)});')


# ---------------- cantoneiras de mira em volta da garrafa inteira (produto herói) ----------------
def cantos(cid, x1, y1, x2, y2, L=78):
    ps = [(f"M{x1} {y1 + L} L{x1} {y1} L{x1 + L} {y1}", -36, -36),
          (f"M{x2 - L} {y1} L{x2} {y1} L{x2} {y1 + L}", 36, -36),
          (f"M{x1} {y2 - L} L{x1} {y2} L{x1 + L} {y2}", -36, 36),
          (f"M{x2 - L} {y2} L{x2} {y2} L{x2} {y2 - L}", 36, 36)]
    h, js = [], []
    for n, (d, dx, dy) in enumerate(ps):
        h.append(f'<g id="{cid}{n}"><path class="cb" d="{d}"/><path class="cf" d="{d}"/></g>')
        js.append((f"#{cid}{n}", dx, dy))
    return "".join(h), js


cH1_h, cH1 = cantos("kH", 330, 396, 902, 1560)
cI_h, cI = cantos("kI", 318, 420, 902, 1646)

T = {
    "garrafa_i": t_pal("intro", 2), "mesa": t_pal("intro", 4), "poca": t_pal("intro", 8), "novo": t_pal("intro", 10),
    "MODUS": t_pal("apresentacao", 2), "isol": t_pal("apresentacao", 3), "nao": t_pal("apresentacao", 8),
    "suar": t_pal("apresentacao", 9), "por": t_pal("apresentacao", 10), "tampa": t_pal("apresentacao", 13),
    "vedacao": t_pal("apresentacao", 15), "vazamento": t_pal("apresentacao", 17), "segundo": t_pal("apresentacao", 18),
    "tranq": t_pal("apresentacao", 22), "bolsa": t_pal("apresentacao", 26),
    "MODUS_c": t_pal("cta", 2), "Toque": t_pal("cta", 6), "no": t_pal("cta", 7), "marcado": t_pal("cta", 9),
    "confira": t_pal("cta", 11), "perto": t_pal("cta", 13),
}


def cantos_js(lista, ini, fim):
    out = []
    for k, (sel, dx, dy) in enumerate(lista):
        out.append(f'tl.fromTo("{sel}",{{x:{dx},y:{dy},opacity:0}},{{x:0,y:0,opacity:1,duration:0.22,ease:"back.out(2)"}},{R(ini + 0.03 * k)});')
    sels = ",".join(f'"{s}"' for s, _, _ in lista)
    out.append(f'tl.to([{sels}],{{opacity:0,duration:0.2,ease:"power1.in"}},{R(fim)});')
    return "\n".join(out)


HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* nomes completos das fontes do container (o local("Bebas Neue") sozinho não carrega no Chromium; Inter é variável) */
@font-face{{font-family:"Bebas Seco";src:local("Bebas Neue Regular"),local("BebasNeue-Regular"),local("Bebas Neue")}}
@font-face{{font-family:"Inter Seco";font-weight:100 900;src:local("Inter Thin"),local("Inter-Thin"),local("Inter")}}
:root{{--giz:#F6F4EE;--tinta:#0F1317;--cob:#2D5BFF}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#0F1317}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:#0F1317;font-family:"Inter Seco";font-weight:800}}
.clip{{position:absolute;inset:0}}
.cam{{position:absolute;inset:0;overflow:hidden;z-index:1}}
.full{{width:100%;height:100%;object-fit:cover}}
/* G1 e G2: origem no alto (a garrafa está perto do topo; o zoom nunca corta a tampa) */
#camG1,#camG2{{transform-origin:50% 0%}}
#camH1,#camG3,#camI{{transform-origin:50% 50%}}
#camH2{{transform-origin:54% 27%}}
.ov{{position:absolute;inset:0}}
.ov svg{{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block;overflow:visible}}
.cb{{fill:none;stroke:#F6F4EE;stroke-width:17;stroke-linecap:round;stroke-linejoin:round;opacity:.9}}
.cf{{fill:none;stroke:#2D5BFF;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}}
.anel-b{{fill:none;stroke:#F6F4EE;stroke-width:15;opacity:.85}}
.anel{{fill:none;stroke:#2D5BFF;stroke-width:8}}
/* reflexo de luz que corre na garrafa (recortado no contorno da garrafa) */
.sw-m{{position:absolute;overflow:hidden;display:block;border-radius:60px}}
.sw-b{{position:absolute;left:-420px;top:-240px;width:220px;height:1800px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.4) 50%,rgba(255,255,255,0) 100%)}}
.vinheta{{z-index:3;background:radial-gradient(ellipse 90% 66% at 50% 50%,rgba(15,19,23,0) 60%,rgba(15,19,23,.34) 100%)}}
/* títulos: etiquetas de giz (Bebas Neue), palavra-chave em etiqueta cobalto */
.titulo{{z-index:6}}
.tag{{display:block;font-family:"Bebas Seco";font-weight:400;line-height:1;white-space:nowrap;background:#F6F4EE;color:#0F1317;
  padding:.12em .2em .02em;border-radius:16px;box-shadow:0 12px 30px rgba(15,19,23,.38)}}
.tag.az{{background:#2D5BFF;color:#F6F4EE}}
.row{{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start;gap:14px}}
.stack{{position:absolute;left:40px;display:flex;flex-direction:column;align-items:flex-start;gap:12px}}
.sub{{display:flex;align-items:center;gap:14px;white-space:nowrap;background:#F6F4EE;color:#0F1317;font-family:"Inter Seco";
  font-weight:800;font-size:36px;line-height:1;padding:12px 26px 14px 16px;border-radius:40px;box-shadow:0 10px 26px rgba(15,19,23,.35)}}
.sub i{{display:block;width:22px;height:22px;border-radius:50%;background:#2D5BFF;box-shadow:0 0 0 5px rgba(45,91,255,.22)}}
/* rodapé de fonte */
#rod{{z-index:7}}
#rod span{{position:absolute;left:40px;top:1468px;display:block;font-family:"Inter Seco";font-weight:600;font-size:30px;line-height:1;
  color:rgba(246,244,238,.88);background:rgba(15,19,23,.5);padding:8px 14px 9px;border-radius:10px}}
/* legenda "etiqueta marca-texto" */
.legenda{{z-index:10}}
.cap{{position:absolute;left:100px;width:840px;display:flex;justify-content:center;align-items:flex-start}}
.ctag{{display:flex;gap:16px;align-items:center;white-space:nowrap;background:rgba(246,244,238,.97);border-radius:22px;
  padding:8px 26px 12px;box-shadow:0 12px 28px rgba(15,19,23,.4)}}
.w{{position:relative;display:block;font-style:normal;font-family:"Inter Seco";font-weight:800;font-size:62px;line-height:1.14;color:#0F1317}}
.w b{{position:relative;font-weight:800}}
.hl{{position:absolute;left:-10px;right:-10px;top:6px;bottom:2px;display:block;background:#2D5BFF;border-radius:10px;transform-origin:0 50%}}
/* CTA: botão cobalto com seta para baixo/esquerda */
#toque{{z-index:11}}
#tq-b{{position:absolute;left:46px;top:1404px;width:120px;height:120px;display:block;border-radius:50%;background:#2D5BFF;
  box-shadow:0 0 0 7px #F6F4EE,0 14px 30px rgba(15,19,23,.45)}}
#tq-b svg{{display:block;width:120px;height:120px}}
.tq-o{{position:absolute;left:46px;top:1404px;width:120px;height:120px;display:block;border:6px solid #F6F4EE;border-radius:50%;opacity:0}}
/* passada seca: faixa de giz que varre a tela na troca de parte */
.wipe{{z-index:12;overflow:hidden}}
.wband{{position:absolute;left:0;top:-200px;width:2600px;height:2320px;display:block;background:#F6F4EE;transform:skewX(-14deg)}}
.wband i{{position:absolute;top:0;width:26px;height:100%;display:block;background:#2D5BFF}}
.flash{{z-index:13;background:#F6F4EE;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- INTRO 1 (0-1,72 s): clipe G 0,25-1,80 s em 0,92x (mão entra e fecha na alça; nada a partir de 1,9 s) -->
  <div id="camG1" class="cam"><video id="vG1" class="clip full" data-start="0" data-duration="1.72" data-media-start="0.25" data-playback-rate="0.92" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>

  <!-- INTRO 2 (1,72-3,5 s): clipe G 2,50-4,28 s em 1,0x (garrafa no alto, inteira; mesa seca embaixo) -->
  <div id="camG2" class="cam"><video id="vG2" class="clip full" data-start="1.72" data-duration="1.78" data-media-start="2.5" data-track-index="1" src="assets/clipe_G.mp4" muted playsinline></video></div>

  <!-- APRESENTAÇÃO 1 (3,5-6,8 s): clipe H 0,00-2,97 s em 0,90x (mão entra, levanta a garrafa; nada a partir de 3,2 s) -->
  <div id="camH1" class="cam"><video id="vH1" class="clip full" data-start="3.5" data-duration="3.3" data-media-start="0" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video>
    <div id="ovH1" class="clip ov" data-start="3.5" data-duration="3.3" data-track-index="2">
      <svg viewBox="0 0 1080 1920">{cH1_h}</svg>
    </div>
  </div>

  <!-- APRESENTAÇÃO 2 (6,8-11,3 s): clipe H 4,40-7,955 s em 0,79x (garrafa de volta na mesa, mão sai, fogueira) -->
  <div id="camH2" class="cam"><video id="vH2" class="clip full" data-start="6.8" data-duration="4.5" data-media-start="4.4" data-playback-rate="0.79" data-track-index="1" src="assets/clipe_H.mp4" muted playsinline></video>
    <div id="ovH2" class="clip ov" data-start="6.8" data-duration="4.5" data-track-index="2">
      <svg viewBox="0 0 1080 1920">
        <rect id="anB" class="anel-b" x="398" y="398" width="380" height="264" rx="36" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <rect id="an" class="anel" x="398" y="398" width="380" height="264" rx="36" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      </svg>
    </div>
  </div>

  <!-- APRESENTAÇÃO 3 (11,3-13,95 s): clipe G 4,50-6,75 s em 0,85x (garrafa desce à mesa, mão solta) -->
  <div id="camG3" class="cam"><video id="vG3" class="clip full" data-start="11.3" data-duration="2.65" data-media-start="4.5" data-playback-rate="0.85" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>

  <!-- CTA (13,95-19,5 s): clipe I 1,00-6,00 s em 0,90x (ondas o tempo todo; a mão entra e segura a alça) -->
  <div id="camI" class="cam"><video id="vI" class="clip full" data-start="13.95" data-duration="5.55" data-media-start="1" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_I.mp4" muted playsinline></video>
    <div id="ovI" class="clip ov" data-start="13.95" data-duration="5.55" data-track-index="2">
      <span id="swI-m" class="sw-m" style="left:338px;top:430px;width:410px;height:1200px"><i id="swI-b" class="sw-b"></i></span>
      <svg viewBox="0 0 1080 1920">{cI_h}</svg>
    </div>
  </div>

  <div id="vin" class="clip vinheta" data-start="0" data-duration="{TOTAL}" data-track-index="3"></div>

  <!-- títulos -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="3.5" data-track-index="7">
    <div class="stack" style="top:196px">
      <div id="t1a" class="tag az" style="font-size:156px">POÇA</div>
      <div id="t1b" class="tag" style="font-size:86px">NA MESA?</div>
      <div id="t1c" class="sub"><i></i>toda vez que apoia</div>
    </div>
  </div>
  <div id="t2" class="clip titulo" data-start="6.86" data-duration="{R(11.3 - 6.86)}" data-track-index="8">
    <div class="row" style="top:186px"><div id="t2a" class="tag az" style="font-size:104px">SEM SUOR</div><div id="t2b" class="tag" style="font-size:104px">POR FORA*</div></div>
    <div class="row" style="top:322px;justify-content:flex-start"><div id="t2c" class="sub"><i></i>tampa com vedação</div></div>
  </div>
  <div id="t3" class="clip titulo" data-start="{R(T["Toque"] - 0.04)}" data-duration="{R(TOTAL - T["Toque"] + 0.04)}" data-track-index="7">
    <div class="row" style="top:186px"><div id="t3a" class="tag az" style="font-size:104px">TOQUE</div><div id="t3b" class="tag" style="font-size:104px">NO PRODUTO</div></div>
    <div class="row" style="top:322px"><div id="t3c" class="sub"><i></i>e confira de perto</div></div>
  </div>

  <div id="rod" class="clip" data-start="3.5" data-duration="10.45" data-track-index="9"><span>*Dados do fabricante</span></div>

  <div id="toque" class="clip" data-start="{R(T["Toque"])}" data-duration="{R(TOTAL - T["Toque"])}" data-track-index="11">
    <i id="tq-o1" class="tq-o"></i><i id="tq-o2" class="tq-o"></i><i id="tq-o3" class="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 120 120"><path d="M80 40 L42 78 M40 50 L40 80 L70 80" fill="none" stroke="#F6F4EE" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

  <div id="wp1" class="clip wipe" data-start="3.32" data-duration="0.36" data-track-index="12"><span id="wb1" class="wband"><i style="left:60px"></i><i style="right:60px"></i></span></div>
  <div id="wp2" class="clip wipe" data-start="13.77" data-duration="0.36" data-track-index="12"><span id="wb2" class="wband"><i style="left:60px"></i><i style="right:60px"></i></span></div>
  <div id="fl0" class="clip flash" data-start="0" data-duration="0.12" data-track-index="13"></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{P["intro"][2]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{P["apresentacao"][2]}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{P["cta"][2]}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="1.6" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="3.2" data-duration="0.55" data-track-index="22" data-volume="0.34" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-brilho-1" data-start="5.1" data-duration="0.9" data-track-index="22" data-volume="0.28" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="6.66" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1" data-start="8.0" data-duration="0.09" data-track-index="22" data-volume="0.28" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whooshc-3" data-start="11.2" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="13.55" data-duration="0.4" data-media-start="1" data-track-index="22" data-volume="0.3" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["Toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-2" data-start="18.0" data-duration="0.09" data-track-index="22" data-volume="0.25" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ================= INTRO 1 (clipe G 0,25-1,80 s) =================
tl.fromTo("#fl0", {{opacity:0.9}}, {{opacity:0, duration:0.1, ease:"power1.out"}}, 0);
tl.fromTo("#camG1", {{scale:1.2}}, {{scale:1.0, duration:0.4, ease:"power3.out"}}, 0);
tl.to("#camG1", {{scale:1.03, duration:{R(T["mesa"] - 0.4)}, ease:"none"}}, 0.4);
tl.to("#camG1", {{scale:1.07, duration:0.1, ease:"power2.out"}}, {R(T["mesa"])});
tl.to("#camG1", {{scale:1.055, duration:0.2, ease:"power2.inOut"}}, {R(T["mesa"] + 0.1)});
// zoom com desfoque (origem no alto: a tampa fica no quadro) e corte
tl.to("#camG1", {{scale:1.2, filter:"blur(14px)", duration:0.12, ease:"power2.in"}}, 1.6);
// título do gancho
tl.fromTo("#t1a", {{scale:2.2, opacity:0, transformOrigin:"0% 50%"}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(1.6)"}}, 0.03);
tl.fromTo("#t1b", {{x:-70, opacity:0}}, {{x:0, opacity:1, duration:0.22, ease:"power3.out"}}, 0.24);
tl.fromTo("#t1c", {{clipPath:"inset(0% 100% 0% 0% round 40px)"}}, {{clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}}, 0.6);

// ================= INTRO 2 (clipe G 2,50-4,28 s): garrafa no alto, mesa seca embaixo =================
// G2 fica sempre >= 1,1x com origem no alto: o MODUS pequeno da base fica abaixo da legenda, nunca cortado por ela
tl.fromTo("#camG2", {{scale:1.24, filter:"blur(14px)"}}, {{scale:1.1, filter:"blur(0px)", duration:0.18, ease:"power3.out"}}, 1.72);
tl.to("#camG2", {{scale:1.11, duration:{R(T["poca"] - 1.9)}, ease:"none"}}, 1.9);
// "poça": punch
tl.to("#camG2", {{scale:1.16, duration:0.1, ease:"power3.out"}}, {R(T["poca"])});
tl.to("#camG2", {{scale:1.14, duration:0.3, ease:"power2.inOut"}}, {R(T["poca"] + 0.1)});
tl.to("#camG2", {{scale:1.15, duration:{R(3.5 - T["poca"] - 0.4)}, ease:"none"}}, {R(T["poca"] + 0.4)});
tl.fromTo("#t1a", {{scale:1.14}}, {{scale:1, duration:0.28, ease:"back.out(2)", immediateRender:false}}, {R(T["poca"])});
tl.to(["#t1a", "#t1b", "#t1c"], {{y:-30, opacity:0, duration:0.14, ease:"power2.in"}}, 3.26);

// passada seca 1 (esquerda -> direita; cobre a tela no corte de 3,5 s)
tl.fromTo("#wb1", {{x:-2900}}, {{x:1400, duration:0.36, ease:"power1.inOut"}}, 3.32);

// ================= APRESENTAÇÃO 1 (clipe H 0-2,97 s) =================
tl.fromTo("#camH1", {{scale:1.1}}, {{scale:1.0, duration:0.4, ease:"power3.out"}}, 3.5);
tl.to("#camH1", {{scale:1.03, duration:{R(T["MODUS"] - 3.9)}, ease:"none"}}, 3.9);
// produto herói: cantoneiras de mira em volta da garrafa inteira no "MODUS" + punch
tl.to("#camH1", {{scale:1.065, duration:0.12, ease:"power2.out"}}, {R(T["MODUS"])});
tl.to("#camH1", {{scale:1.05, duration:0.3, ease:"power2.inOut"}}, {R(T["MODUS"] + 0.12)});
{cantos_js(cH1, T["MODUS"] - 0.04, 5.55)}
tl.to("#camH1", {{scale:1.075, duration:{R(6.66 - T["MODUS"] - 0.42)}, ease:"none"}}, {R(T["MODUS"] + 0.42)});
// zoom com desfoque e corte (pula o giro proibido do H)
tl.to("#camH1", {{scale:1.22, filter:"blur(12px)", duration:0.14, ease:"power2.in"}}, 6.66);

// ================= APRESENTAÇÃO 2 (clipe H 4,40-7,955 s) =================
tl.fromTo("#camH2", {{scale:1.18, filter:"blur(12px)"}}, {{scale:1.0, filter:"blur(0px)", duration:0.22, ease:"power3.out"}}, 6.8);
tl.to("#camH2", {{scale:1.06, duration:0.1, ease:"power3.out"}}, {R(T["suar"] + 0.08)});
tl.to("#camH2", {{scale:1.04, duration:0.3, ease:"power2.inOut"}}, {R(T["suar"] + 0.18)});
tl.fromTo("#t2a", {{scale:1.8, opacity:0, transformOrigin:"50% 55%"}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(1.7)"}}, {R(T["suar"] - 0.04)});
tl.fromTo("#t2b", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:0.22, ease:"power3.out"}}, {R(T["por"] - 0.02)});
tl.to("#camH2", {{scale:1.05, duration:{R(T["vedacao"] - T["suar"] - 0.48)}, ease:"none"}}, {R(T["suar"] + 0.48)});
// "tampa com vedação": anel cobalto desenha em volta da tampa (garrafa parada na mesa) + etiqueta
tl.fromTo("#t2c", {{clipPath:"inset(0% 100% 0% 0% round 40px)"}}, {{clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}}, {R(T["tampa"] - 0.03)});
tl.to(["#anB", "#an"], {{attr:{{"stroke-dashoffset":0}}, duration:0.45, ease:"power2.inOut"}}, {R(T["tampa"])});
tl.to("#camH2", {{scale:1.09, duration:0.1, ease:"power3.out"}}, {R(T["vedacao"])});
tl.to("#camH2", {{scale:1.075, duration:0.3, ease:"power2.inOut"}}, {R(T["vedacao"] + 0.1)});
tl.to("#camH2", {{scale:1.1, duration:0.08, ease:"power3.out"}}, {R(T["vazamento"])});
tl.to("#camH2", {{scale:1.085, duration:0.3, ease:"power2.inOut"}}, {R(T["vazamento"] + 0.08)});
tl.fromTo(["#anB", "#an"], {{opacity:1}}, {{opacity:0, duration:0.2, ease:"power1.in", immediateRender:false}}, 10.0);
tl.to("#camH2", {{scale:1.11, duration:{R(11.18 - T["vazamento"] - 0.38)}, ease:"none"}}, {R(T["vazamento"] + 0.38)});
tl.fromTo("#rod span", {{scale:1.08}}, {{scale:1, duration:0.3, ease:"back.out(2)", transformOrigin:"0% 50%", immediateRender:false}}, {R(T["segundo"])});
tl.to(["#t2a", "#t2b", "#t2c"], {{x:-80, opacity:0, duration:0.14, ease:"power2.in"}}, 11.14);
// chicote lateral e corte
tl.to("#camH2", {{x:-120, scale:1.3, filter:"blur(14px)", duration:0.12, ease:"power2.in"}}, 11.18);

// ================= APRESENTAÇÃO 3 (clipe G 4,50-6,75 s) =================
tl.fromTo("#camG3", {{x:140, scale:1.3, filter:"blur(14px)"}}, {{x:0, scale:1.02, filter:"blur(0px)", duration:0.2, ease:"power3.out"}}, 11.3);
tl.to("#camG3", {{scale:1.04, duration:{R(T["tranq"] - 11.5)}, ease:"none"}}, 11.5);
tl.to("#camG3", {{scale:1.08, duration:0.1, ease:"power3.out"}}, {R(T["tranq"])});
tl.to("#camG3", {{scale:1.065, duration:0.3, ease:"power2.inOut"}}, {R(T["tranq"] + 0.1)});
tl.to("#camG3", {{scale:1.075, duration:{R(T["bolsa"] - T["tranq"] - 0.4)}, ease:"none"}}, {R(T["tranq"] + 0.4)});
tl.to("#camG3", {{scale:1.11, duration:0.1, ease:"power3.out"}}, {R(T["bolsa"])});
tl.to("#camG3", {{scale:1.095, duration:0.3, ease:"power2.inOut"}}, {R(T["bolsa"] + 0.1)});
tl.fromTo("#rod", {{opacity:0}}, {{opacity:1, duration:0.2, ease:"power1.out"}}, 3.55);

// passada seca 2 (direita -> esquerda; cobre a tela no corte de 13,95 s)
tl.fromTo("#wb2", {{x:1400}}, {{x:-2900, duration:0.36, ease:"power1.inOut"}}, 13.77);

// ================= CTA (clipe I 1,00-6,00 s): mais calma =================
tl.fromTo("#camI", {{scale:1.08}}, {{scale:1.0, duration:0.5, ease:"power2.out"}}, 13.95);
tl.to("#camI", {{scale:1.035, duration:{R(T["Toque"] - 14.45)}, ease:"none"}}, 14.45);
{cantos_js(cI, T["MODUS_c"] - 0.04, 15.95)}
tl.fromTo("#swI-b", {{x:0, rotation:16}}, {{x:1100, rotation:16, duration:0.75, ease:"power1.inOut"}}, 15.4);
// "Toque": título + botão com seta para baixo/esquerda + ondas
tl.to("#camI", {{scale:1.065, duration:0.1, ease:"power3.out"}}, {R(T["Toque"])});
tl.to("#camI", {{scale:1.05, duration:0.35, ease:"power2.inOut"}}, {R(T["Toque"] + 0.1)});
tl.to("#camI", {{scale:1.075, duration:{R(TOTAL - T["Toque"] - 0.45)}, ease:"none"}}, {R(T["Toque"] + 0.45)});
tl.fromTo("#t3a", {{scale:1.8, opacity:0, transformOrigin:"50% 55%"}}, {{scale:1, opacity:1, duration:0.26, ease:"back.out(1.7)"}}, {R(T["Toque"] - 0.03)});
tl.fromTo("#t3b", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:0.22, ease:"power3.out"}}, {R(T["no"] - 0.02)});
tl.fromTo("#t3c", {{clipPath:"inset(0% 100% 0% 0% round 40px)"}}, {{clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}}, {R(T["confira"] - 0.05)});
tl.fromTo("#tq-b", {{scale:0.5, opacity:0}}, {{scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}}, {R(T["Toque"])});
tl.fromTo("#tq-s", {{x:0, y:0}}, {{x:-7, y:7, duration:0.22, yoyo:true, repeat:9, ease:"sine.inOut"}}, {R(T["Toque"] + 0.3)});
tl.fromTo("#tq-o1", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["Toque"])});
tl.fromTo("#tq-o2", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["marcado"])});
tl.fromTo("#tq-o3", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["perto"])});

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT)
