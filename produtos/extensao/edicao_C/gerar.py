#!/usr/bin/env python3
"""Gera produtos/extensao/edicao_C/index.html ("um toque só": índigo-noite / lavanda-luar / branco,
Poppins 900 + Inter 800, legenda "interruptor"). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra da 3ª violação: o vídeo de fundo roda do primeiro ao último quadro; nada de <img>, quadro congelado ou cartão.
Trechos (analise_C.md, conferidos quadro a quadro em 15/10/2026):
  intro        H 0,00-2,39 s em 0,70x  (mão pega o cabo; a 2ª mão por baixo aparece ~2,45 s: nunca mostrar)
  apresentação I 0,00-4,56 s em 0,88x  (sombras de folhas, tela do celular acende) -> G 0,40-2,82 s em 0,70x
               (dedo aperta o botão; o LED vermelho acende ~2,0 s = no "toque" da fala)
  CTA          I 4,70-6,33 s em 0,85x  -> G 2,82-5,08 s em 0,72x (mão sai, LED aceso; continua de onde parou)
Efeitos só por cima do vídeo rodando: punch-in no ritmo, revelação em círculo a partir do botão, ondas do toque,
brilho correndo na extensão, estrelas leves nas cenas de noite, vinheta índigo nas bordas (nunca sobre a extensão).
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

TOTAL = 16.6
# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 3.42, 0.15), "apresentacao": (3.42, 11.53, 3.75), "cta": (11.53, TOTAL, 11.78)}
DUR_MP3 = {"intro": 3.552, "apresentacao": 7.704, "cta": 4.704}
TOPO_LEG = 1437  # pílula da legenda 1437-1539 (77 % da altura): fica na borda lisa de baixo da extensão

GRUPOS = {
    "intro": [[0, 1], [2], [3, 4, 5], [6, 7, 8], [9]],
    "apresentacao": [[0], [1, 2, 3], [4, 5], [6], [7, 8], [9, 10], [11, 12], [13, 14], [15, 16], [17, 18],
                     [19, 20], [21, 22]],
    "cta": [[0, 1], [2, 3, 4], [5, 6], [7, 8], [9, 10], [11, 12]],
}
CHAVE = {
    "intro": {2, 3, 4, 5, 8, 9},
    "apresentacao": {0, 5, 6, 7, 8, 11, 12, 16, 18, 20, 22},
    "cta": {4, 5, 7, 8, 12},
}
EXIBE = {("intro", 8): "dormir?", ("intro", 9): "Cansa.", ("apresentacao", 6): "tomadas,",
         ("apresentacao", 12): "C.", ("apresentacao", 16): "desligar,", ("apresentacao", 22): "botão.",
         ("cta", 4): "usar?", ("cta", 12): "detalhes."}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---------------- legenda "interruptor": pílula índigo que afunda e volta (0,92 -> 1) a cada grupo; as palavras
# acendem no seu tempo; palavra-chave em lavanda com brilho ----------------
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = P[parte][2]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.03, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.03, 3), fim_voz)
        else:
            e = min(fim_voz, P[parte][1])
        gid = f"lg-{parte[:3]}-{gi}"
        ems = ""
        for k, i in enumerate(g):
            txt = EXIBE.get((parte, i), pal[i]["palavra"])
            cls = "w k" if i in CHAVE[parte] else "w"
            ems += f'<em id="{gid}-{k}" class="{cls}">{txt}</em>'
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.32,scale:0.94}},{{opacity:1,scale:1,duration:0.1,ease:"power2.out"}},{R(t_pal(parte, i) - 0.02)});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div class="cap" style="top:{TOPO_LEG}px"><span id="{gid}-p" class="cpill">{ems}</span></div></div>')
        leg_js.append(f'tl.fromTo("#{gid}-p",{{scale:0.92}},{{scale:1,duration:0.16,ease:"back.out(2.4)"}},{R(s)});')

# ---------------- estrelas (só nas cenas de noite): posições fixas, longe da extensão ----------------
EST = [(70, 120, 5), (170, 300, 4), (250, 80, 6), (360, 210, 4), (600, 60, 5), (690, 250, 4),
       (790, 140, 6), (880, 330, 4), (960, 90, 5), (60, 520, 4), (150, 760, 5), (900, 600, 5)]


def estrelas(eid, ini, dur, trilha):
    h = [f'  <div id="{eid}" class="clip estrelas" data-start="{R(ini)}" data-duration="{R(dur)}" data-track-index="{trilha}">']
    js = []
    for n, (x, y, d) in enumerate(EST):
        h.append(f'    <i id="{eid}-{n}" class="st" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px"></i>')
        pico = round(0.45 + 0.5 * ((n * 37) % 10) / 10, 2)
        fase = round(((n * 53) % 10) / 10 * 0.6, 2)
        dx = ((n * 29) % 7 - 3) * 6
        js.append(f'tl.fromTo("#{eid}-{n}",{{opacity:0,x:0,y:0}},{{keyframes:[{{opacity:{pico},duration:{R(0.25 + fase)}}},'
                  f'{{opacity:{round(pico * 0.35, 2)},x:{dx / 2},y:-10,duration:0.55}},{{opacity:{pico},x:{dx},y:-22,duration:0.6}},'
                  f'{{opacity:{round(pico * 0.5, 2)},x:{dx * 1.5},y:-34,duration:{R(max(0.2, dur - 1.4 - fase))}}}],ease:"sine.inOut"}},{R(ini)});')
    h.append('  </div>')
    return h, js


st1_h, st1_js = estrelas("st1", 2.15, P["intro"][1] - 2.15, 6)
st2_h, st2_js = estrelas("st2", 8.08, 11.53 - 8.08, 6)
st3_h, st3_js = estrelas("st3", 13.45, TOTAL - 13.45, 6)

# tempos-chave (abs)
T = {
    "tomada": t_pal("intro", 2), "um1": t_pal("intro", 3), "por": t_pal("intro", 4), "um2": t_pal("intro", 5),
    "antes": t_pal("intro", 6), "dormir": t_pal("intro", 8), "cansa": t_pal("intro", 9),
    "extensao": t_pal("apresentacao", 0), "com": t_pal("apresentacao", 4), "cinco": t_pal("apresentacao", 5),
    "quatro": t_pal("apresentacao", 7), "e": t_pal("apresentacao", 9), "tipo": t_pal("apresentacao", 11),
    "na": t_pal("apresentacao", 13), "desligar": t_pal("apresentacao", 16), "toque": t_pal("apresentacao", 20),
    "botao": t_pal("apresentacao", 22),
    "ja": t_pal("cta", 0), "Toque": t_pal("cta", 5), "marcado": t_pal("cta", 8),
}

HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* nomes completos das fontes do container (Poppins-Black.ttf; Inter é variável) */
@font-face{{font-family:"Poppins Noite";font-weight:900;src:local("Poppins Black"),local("Poppins-Black")}}
@font-face{{font-family:"Inter Seu";font-weight:100 900;src:local("Inter Thin"),local("Inter-Thin"),local("Inter")}}
:root{{--indigo:#110E26;--lav:#B9A7FF;--luz:#F5F2FF}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#110E26}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:#110E26;font-family:"Inter Seu";font-weight:800}}
.clip{{position:absolute;inset:0}}
.cam{{position:absolute;inset:0;overflow:hidden;z-index:1}}
.full{{width:100%;height:100%;object-fit:cover}}
/* H e G: origem abaixo do centro da extensão (o alto não sobe sobre o título, o pé não desce sobre a legenda) */
#camH,#camG1,#camG2{{transform-origin:38% 62%}}
#camI1,#camI2{{transform-origin:53% 50%}}
.ov{{position:absolute;inset:0}}
.ov svg{{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block;overflow:visible}}
.trace{{fill:none;stroke:#B9A7FF;stroke-width:7;stroke-linecap:round;filter:drop-shadow(0 0 10px rgba(185,167,255,.95))}}
.anel{{fill:none;stroke:#B9A7FF;stroke-width:6}}
.rv{{fill:none;stroke:#F5F2FF;stroke-width:10;filter:drop-shadow(0 0 16px rgba(185,167,255,1))}}
/* números das tomadas (à direita da extensão, dentro da zona segura) */
.num{{position:absolute;left:784px;width:56px;height:56px;display:block;border-radius:50%;background:rgba(17,14,38,.9);
  box-shadow:inset 0 0 0 3px #B9A7FF,0 0 16px rgba(185,167,255,.55);font-family:"Poppins Noite";font-weight:900;
  font-size:30px;line-height:56px;text-align:center;color:#B9A7FF;font-style:normal}}
.lab{{position:absolute;display:block;white-space:nowrap;background:rgba(17,14,38,.9);color:#F5F2FF;font-family:"Inter Seu";
  font-weight:800;font-size:42px;line-height:1;padding:12px 26px 14px;border-radius:40px;box-shadow:inset 0 0 0 3px #B9A7FF}}
.lab b{{color:#B9A7FF}}
/* halo do botão: só em volta do anel (centro transparente: a cor do botão não muda) */
.halo{{position:absolute;width:420px;height:420px;display:block;border-radius:50%;
  background:radial-gradient(closest-side,rgba(185,167,255,0) 0,rgba(185,167,255,0) 40%,rgba(185,167,255,.55) 48%,rgba(185,167,255,.18) 70%,rgba(185,167,255,0) 100%)}}
/* brilho que corre na extensão do G (recortado no contorno da extensão) */
#sw-m{{position:absolute;left:290px;top:490px;width:520px;height:1046px;overflow:hidden;display:block;border-radius:52px}}
#sw-b{{position:absolute;left:0;top:-200px;width:200px;height:1500px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.42) 50%,rgba(255,255,255,0) 100%)}}
/* noite: vinheta índigo nas bordas (centro livre onde está a extensão) */
#noite{{z-index:4;background:radial-gradient(ellipse 70% 52% at 50% 52%,rgba(17,14,38,0) 64%,rgba(17,14,38,.88) 100%)}}
#borda{{z-index:4;background:linear-gradient(to left,rgba(17,14,38,.92) 0,rgba(17,14,38,.6) 70px,rgba(17,14,38,0) 150px)}}
.topo{{z-index:5;background:linear-gradient(to bottom,rgba(17,14,38,.82) 0,rgba(17,14,38,.5) 13%,rgba(17,14,38,0) 24%)}}
.estrelas{{z-index:6}}
.st{{position:absolute;display:block;border-radius:50%;background:#F1EDFF;box-shadow:0 0 10px 3px rgba(185,167,255,.75)}}
.flash{{z-index:12;background:#EDE8FF;opacity:0}}
/* títulos: Poppins 900, branco com destaque lavanda */
.titulo{{z-index:9}}
.tw{{position:absolute;left:30px;width:858px;display:flex;justify-content:center;align-items:flex-start}}
.mask{{position:absolute;left:30px;width:858px;overflow:hidden;display:flex;justify-content:center;align-items:flex-start}}
.tt{{display:block;font-family:"Poppins Noite";font-weight:900;line-height:1.08;white-space:nowrap;color:#FFFFFF;
  letter-spacing:-2px;text-shadow:0 6px 26px rgba(17,14,38,.85),0 0 2px rgba(17,14,38,.6)}}
.tt .l{{color:#B9A7FF}}
.pill{{display:flex;align-items:center;gap:14px;white-space:nowrap;background:#B9A7FF;color:#110E26;font-family:"Inter Seu";
  font-weight:800;font-size:42px;line-height:1;padding:11px 30px 13px 16px;border-radius:40px;box-shadow:0 10px 26px rgba(17,14,38,.55)}}
.pill svg{{display:block;width:40px;height:40px}}
/* legenda "interruptor" */
.legenda{{z-index:10}}
.cap{{position:absolute;left:40px;width:838px;display:flex;justify-content:center;align-items:flex-start}}
.cpill{{display:flex;gap:18px;align-items:center;white-space:nowrap;background:rgba(17,14,38,.88);border-radius:52px;
  padding:10px 32px 12px;box-shadow:inset 0 0 0 3px rgba(185,167,255,.55),0 0 26px rgba(185,167,255,.28),0 10px 24px rgba(0,0,0,.4)}}
.w{{display:block;font-style:normal;font-family:"Inter Seu";font-weight:800;font-size:70px;line-height:1.14;color:#FFFFFF}}
.w.k{{color:#B9A7FF;text-shadow:0 0 18px rgba(185,167,255,.75)}}
/* CTA: botão lavanda com seta para baixo/esquerda */
#toque{{z-index:11}}
#tq-b{{position:absolute;left:52px;top:1300px;width:116px;height:116px;display:block;border-radius:50%;background:#B9A7FF;
  box-shadow:0 0 0 6px rgba(17,14,38,.92),0 0 30px rgba(185,167,255,.8)}}
#tq-b svg{{display:block;width:116px;height:116px}}
.tq-o{{position:absolute;left:52px;top:1300px;width:116px;height:116px;display:block;border:6px solid #B9A7FF;border-radius:50%;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
  <!-- INTRO (0-3,42 s): clipe H 0,00-2,39 s em 0,70x (mão pega o cabo; nada depois de 2,40 s) -->
  <div id="camH" class="cam"><video id="vH" class="clip full" data-start="0" data-duration="3.42" data-media-start="0" data-playback-rate="0.7" data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video></div>

  <!-- APRESENTAÇÃO 1 (3,18-8,36 s): clipe I 0,00-4,56 s em 0,88x; revela em círculo a partir do botão -->
  <div id="camI1" class="cam"><video id="vI1" class="clip full" data-start="3.18" data-duration="5.18" data-media-start="0" data-playback-rate="0.88" data-track-index="1" src="assets/clipe_I.mp4" muted playsinline></video>
    <div id="ovI1" class="clip ov" data-start="3.18" data-duration="5.18" data-track-index="2">
      <svg viewBox="0 0 1080 1920">
        <circle id="rv1" class="rv" cx="472" cy="652" r="0"/>
        <rect id="oI-strip" class="trace" x="380" y="462" width="390" height="776" rx="44" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <rect id="oI-tom" class="trace" x="546" y="572" width="192" height="614" rx="28" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <rect id="oI-usb" class="trace" x="430" y="850" width="92" height="220" rx="20" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <circle id="oI-c" class="trace" cx="475" cy="1087" r="34" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      </svg>
      <i id="n1" class="num" style="top:592px">1</i>
      <i id="n2" class="num" style="top:704px">2</i>
      <i id="n3" class="num" style="top:817px">3</i>
      <i id="n4" class="num" style="top:927px">4</i>
      <i id="n5" class="num" style="top:1092px">5</i>
      <span id="lI-usb" class="lab" style="right:672px;top:928px"><b>4</b> USB</span>
      <span id="lI-c" class="lab" style="right:640px;top:1055px">tipo <b>C</b></span>
    </div>
  </div>

  <!-- APRESENTAÇÃO 2 (8,08-11,53 s): clipe G 0,40-2,82 s em 0,70x; o LED acende no "toque" -->
  <div id="camG1" class="cam"><video id="vG1" class="clip full" data-start="8.08" data-duration="3.45" data-media-start="0.4" data-playback-rate="0.7" data-track-index="1" src="assets/clipe_G.mp4" muted playsinline></video>
    <div id="ovG1" class="clip ov" data-start="8.08" data-duration="3.45" data-track-index="2">
      <span id="sw-m"><i id="sw-b"></i></span>
      <i id="hG1" class="halo" style="left:198px;top:533px"></i>
      <svg viewBox="0 0 1080 1920">
        <circle id="rv2" class="rv" cx="408" cy="743" r="0"/>
        <circle id="rpA1" class="anel" cx="408" cy="743" r="84" opacity="0"/>
        <circle id="rpA2" class="anel" cx="408" cy="743" r="84" opacity="0"/>
        <circle id="rpA3" class="anel" cx="408" cy="743" r="84" opacity="0"/>
      </svg>
    </div>
  </div>

  <!-- CTA 1 (11,53-13,45 s): clipe I 4,70-6,33 s em 0,85x (tela do celular acesa, sombras balançando) -->
  <div id="camI2" class="cam"><video id="vI2" class="clip full" data-start="11.53" data-duration="1.92" data-media-start="4.7" data-playback-rate="0.85" data-track-index="1" src="assets/clipe_I.mp4" muted playsinline></video></div>

  <!-- CTA 2 (13,45-16,6 s): clipe G 2,82-5,08 s em 0,72x (continua de onde parou: mão sai, LED aceso) -->
  <div id="camG2" class="cam"><video id="vG2" class="clip full" data-start="13.45" data-duration="3.15" data-media-start="2.815" data-playback-rate="0.72" data-track-index="1" src="assets/clipe_G.mp4" muted playsinline></video>
    <div id="ovG2" class="clip ov" data-start="13.45" data-duration="3.15" data-track-index="2">
      <i id="hG2" class="halo" style="left:198px;top:533px"></i>
      <svg viewBox="0 0 1080 1920">
        <circle id="rpB1" class="anel" cx="408" cy="743" r="84" opacity="0"/>
        <circle id="rpB2" class="anel" cx="408" cy="743" r="84" opacity="0"/>
      </svg>
    </div>
  </div>

  <div id="noite" class="clip" data-start="0" data-duration="{TOTAL}" data-track-index="3"></div>
  <div id="borda" class="clip" data-start="0" data-duration="3.42" data-track-index="4"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="{TOTAL}" data-track-index="5"></div>
{chr(10).join(st1_h + st2_h + st3_h)}

  <!-- títulos -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="3.42" data-track-index="7">
    <div class="tw" style="top:186px"><div id="t1a" class="tt" style="font-size:132px">Um por <span class="l">um?</span></div></div>
    <div class="tw" style="top:186px"><div id="t1b" class="tt" style="font-size:132px;opacity:0"><span class="l">Cansa.</span></div></div>
    <div class="tw" style="top:352px"><div id="t1p" class="pill"><svg viewBox="0 0 40 40"><path d="M20 6 V19 M12.5 11.5 A12 12 0 1 0 27.5 11.5" fill="none" stroke="#110E26" stroke-width="4.5" stroke-linecap="round"/></svg>antes de dormir</div></div>
  </div>
  <div id="t2" class="clip titulo" data-start="8.3" data-duration="3.23" data-track-index="8">
    <div class="mask" style="top:186px;height:156px"><div id="t2a" class="tt" style="font-size:128px">Um toque <span class="l">só</span></div></div>
    <div class="tw" style="top:352px"><div id="t2p" class="pill"><svg viewBox="0 0 40 40"><path d="M20 6 V19 M12.5 11.5 A12 12 0 1 0 27.5 11.5" fill="none" stroke="#110E26" stroke-width="4.5" stroke-linecap="round"/></svg>liga/desliga • 5 tomadas</div></div>
  </div>
  <div id="t3" class="clip titulo" data-start="11.53" data-duration="{R(TOTAL - 11.53)}" data-track-index="7">
    <div class="tw" style="top:190px"><div id="t3a" class="tt" style="font-size:112px">Onde vai <span class="l">usar?</span></div></div>
    <div class="tw" style="top:352px"><div id="t3p" class="pill"><svg viewBox="0 0 40 40"><path d="M20 6 V19 M12.5 11.5 A12 12 0 1 0 27.5 11.5" fill="none" stroke="#110E26" stroke-width="4.5" stroke-linecap="round"/></svg>toque no produto marcado</div></div>
  </div>

  <div id="toque" class="clip" data-start="{R(T["Toque"])}" data-duration="{R(TOTAL - T["Toque"])}" data-track-index="9">
    <i id="tq-o1" class="tq-o"></i><i id="tq-o2" class="tq-o"></i><i id="tq-o3" class="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#110E26" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.14" data-track-index="11"></div>
  <div id="fl2" class="clip flash" data-start="13.45" data-duration="0.14" data-track-index="11"></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{P["intro"][2]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{P["apresentacao"][2]}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{P["cta"][2]}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="3.38" data-duration="0.3" data-track-index="22" data-volume="0.35" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1" data-start="5.12" data-duration="0.09" data-track-index="22" data-volume="0.32" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-tique-1" data-start="6.2" data-duration="0.03" data-track-index="22" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="8.08" data-duration="0.3" data-track-index="22" data-volume="0.35" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-brilho-1" data-start="9.53" data-duration="0.9" data-track-index="22" data-volume="0.3" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="11.36" data-duration="0.55" data-track-index="22" data-volume="0.34" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["Toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-2" data-start="15.1" data-duration="0.09" data-track-index="22" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ================= INTRO (clipe H) =================
tl.fromTo("#fl1", {{opacity:0.85}}, {{opacity:0, duration:0.12, ease:"power1.out"}}, 0);
tl.fromTo("#camH", {{scale:1.2}}, {{scale:1.0, duration:0.4, ease:"power3.out"}}, 0);
tl.to("#camH", {{scale:1.03, duration:{R(T["tomada"] - 0.4)}, ease:"none"}}, 0.4);
// punch em "tomada"
tl.to("#camH", {{scale:1.07, duration:0.12, ease:"power2.out"}}, {R(T["tomada"])});
tl.to("#camH", {{scale:1.045, duration:0.4, ease:"power2.inOut"}}, {R(T["tomada"] + 0.12)});
// três toques no ritmo de "um / por / um"
tl.to("#camH", {{scale:1.065, duration:0.07, ease:"power2.out"}}, {R(T["um1"])});
tl.to("#camH", {{scale:1.05, duration:0.1, ease:"power1.inOut"}}, {R(T["um1"] + 0.075)});
tl.to("#camH", {{scale:1.075, duration:0.07, ease:"power2.out"}}, {R(T["por"])});
tl.to("#camH", {{scale:1.06, duration:0.1, ease:"power1.inOut"}}, {R(T["por"] + 0.07)});
tl.to("#camH", {{scale:1.085, duration:0.07, ease:"power2.out"}}, {R(T["um2"])});
tl.to("#camH", {{scale:1.07, duration:0.3, ease:"power1.inOut"}}, {R(T["um2"] + 0.07)});
tl.to("#camH", {{scale:1.085, duration:{R(T["cansa"] - T["um2"] - 0.37)}, ease:"none"}}, {R(T["um2"] + 0.37)});
// "Cansa.": impacto com tremor
tl.to("#camH", {{scale:1.12, duration:0.1, ease:"power3.out"}}, {R(T["cansa"])});
tl.fromTo("#camH", {{x:0, y:0}}, {{keyframes:[{{x:14, y:-8, duration:0.05}}, {{x:-11, y:6, duration:0.06}}, {{x:7, y:-4, duration:0.06}}, {{x:0, y:0, duration:0.07}}], ease:"none", immediateRender:false}}, {R(T["cansa"] + 0.02)});
// título
tl.fromTo("#t1a", {{scale:2, opacity:0, filter:"blur(14px)", transformOrigin:"50% 55%"}}, {{scale:1, opacity:1, filter:"blur(0px)", duration:0.32, ease:"back.out(1.7)"}}, 0.04);
tl.fromTo("#t1p", {{clipPath:"inset(0% 100% 0% 0% round 40px)"}}, {{clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}}, 0.5);
tl.to("#t1a", {{y:-40, opacity:0, filter:"blur(10px)", duration:0.12, ease:"power2.in"}}, {R(T["cansa"] - 0.1)});
tl.fromTo("#t1b", {{scale:1.7, rotation:-4, opacity:0, transformOrigin:"50% 55%"}}, {{scale:1, rotation:0, opacity:1, duration:0.22, ease:"back.out(2)"}}, {R(T["cansa"])});
tl.to(["#t1b", "#t1p"], {{opacity:0, scale:1.15, filter:"blur(8px)", duration:0.16, ease:"power2.in"}}, 3.26);
// "antes de dormir": a luz baixa (bordas índigo) e aparecem as estrelas
tl.fromTo("#noite", {{opacity:0.3}}, {{opacity:0.92, duration:0.6, ease:"power2.inOut"}}, {R(T["dormir"])});

// ================= APRESENTAÇÃO 1 (clipe I): revelação em círculo a partir do botão =================
tl.fromTo("#camI1", {{clipPath:"circle(0px at 472px 652px)"}}, {{clipPath:"circle(1500px at 472px 652px)", duration:0.24, ease:"power2.in"}}, 3.18);
tl.fromTo("#rv1", {{attr:{{r:0}}, opacity:1}}, {{attr:{{r:1490}}, opacity:0.5, duration:0.24, ease:"power2.in"}}, 3.18);
tl.to("#noite", {{opacity:0.25, duration:0.3, ease:"power1.out"}}, 3.3);
tl.fromTo("#camI1", {{scale:1.08}}, {{scale:1.0, duration:0.45, ease:"power3.out", immediateRender:false}}, 3.18);
tl.to("#camI1", {{scale:1.035, duration:{R(T["cinco"] - 3.64)}, ease:"none"}}, 3.64);
// produto inteiro: contorno lavanda desenha em volta da extensão
tl.to("#oI-strip", {{attr:{{"stroke-dashoffset":0}}, duration:0.55, ease:"power2.inOut"}}, {R(T["extensao"])});
tl.to("#oI-strip", {{opacity:0, duration:0.2, ease:"power1.in"}}, 5.0);
// "cinco tomadas": colchete na coluna das tomadas + números 1-5
tl.to("#oI-tom", {{attr:{{"stroke-dashoffset":0}}, duration:0.4, ease:"power2.out"}}, 5.12);
tl.to("#camI1", {{scale:1.065, duration:0.12, ease:"power2.out"}}, {R(T["cinco"])});
tl.to("#camI1", {{scale:1.05, duration:0.4, ease:"power2.inOut"}}, {R(T["cinco"] + 0.12)});
''' + "\n".join(
    f'tl.fromTo("#n{k}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.2, ease:"back.out(2.5)"}}, {R(T["cinco"] + 0.05 + 0.09 * (k - 1))});'
    for k in range(1, 6)) + f'''
tl.to(["#oI-tom", "#n1", "#n2", "#n3", "#n4", "#n5"], {{opacity:0, duration:0.15, ease:"power1.in"}}, 6.2);
// "quatro USB"
tl.to("#oI-usb", {{attr:{{"stroke-dashoffset":0}}, duration:0.3, ease:"power2.out"}}, 6.2);
tl.fromTo("#lI-usb", {{x:40, opacity:0}}, {{x:0, opacity:1, duration:0.2, ease:"power3.out"}}, {R(T["quatro"])});
tl.to("#camI1", {{scale:1.08, duration:0.12, ease:"power2.out"}}, {R(T["quatro"])});
tl.to("#camI1", {{scale:1.065, duration:0.4, ease:"power2.inOut"}}, {R(T["quatro"] + 0.12)});
tl.to(["#oI-usb", "#lI-usb"], {{opacity:0, duration:0.15, ease:"power1.in"}}, {R(T["tipo"] - 0.12)});
// "tipo C"
tl.to("#oI-c", {{attr:{{"stroke-dashoffset":0}}, duration:0.3, ease:"power2.out"}}, {R(T["tipo"] - 0.05)});
tl.fromTo("#lI-c", {{x:40, opacity:0}}, {{x:0, opacity:1, duration:0.2, ease:"power3.out"}}, {R(T["tipo"])});
tl.to("#camI1", {{scale:1.095, duration:0.12, ease:"power2.out"}}, {R(T["tipo"])});
tl.to("#camI1", {{scale:1.08, duration:0.4, ease:"power2.inOut"}}, {R(T["tipo"] + 0.12)});

// ================= APRESENTAÇÃO 2 (clipe G): revelação a partir do botão; dedo aperta; LED acende no "toque" =================
tl.fromTo("#camG1", {{clipPath:"circle(0px at 408px 743px)"}}, {{clipPath:"circle(1500px at 408px 743px)", duration:0.26, ease:"power2.in"}}, 8.08);
tl.fromTo("#rv2", {{attr:{{r:0}}, opacity:1}}, {{attr:{{r:1490}}, opacity:0.5, duration:0.26, ease:"power2.in"}}, 8.08);
tl.to("#noite", {{opacity:0.75, duration:0.4, ease:"power1.out"}}, 8.2);
tl.fromTo("#camG1", {{scale:1.08}}, {{scale:1.0, duration:0.45, ease:"power3.out", immediateRender:false}}, 8.08);
tl.to("#camG1", {{scale:1.06, duration:{R(T["toque"] + 0.09 - 8.53)}, ease:"none"}}, 8.53);
tl.fromTo("#t2a", {{yPercent:110, filter:"blur(8px)"}}, {{yPercent:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}}, {R(T["na"] - 0.04)});
tl.fromTo("#t2p", {{clipPath:"inset(0% 100% 0% 0% round 40px)"}}, {{clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}}, {R(T["desligar"])});
// brilho correndo na extensão (no silêncio depois de "desligar")
tl.fromTo("#sw-b", {{x:-320, rotation:18}}, {{x:700, rotation:18, duration:0.7, ease:"power1.inOut"}}, 9.53);
// LED acende (G 2,0 s) junto do "toque": punch, ondas e halo em volta do anel
tl.to("#camG1", {{scale:1.1, duration:0.1, ease:"power3.out"}}, {R(T["toque"] + 0.09)});
tl.to("#camG1", {{scale:1.075, duration:0.5, ease:"power2.inOut"}}, {R(T["toque"] + 0.19)});
''' + "\n".join(
    f'tl.fromTo("#rpA{k}", {{attr:{{r:84}}, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{attr:{{r:330}}, opacity:0, duration:0.73}}], ease:"power2.out"}}, {R(T["toque"] + 0.09 + 0.14 * (k - 1))});'
    for k in range(1, 4)) + f'''
tl.fromTo("#hG1", {{opacity:0, scale:0.7}}, {{keyframes:[{{opacity:1, scale:1, duration:0.18}}, {{opacity:0.35, scale:1.08, duration:0.9}}], ease:"power2.out"}}, {R(T["toque"] + 0.09)});
tl.to("#hG1", {{opacity:0, duration:0.25}}, 11.1);
// passagem para a CTA: mergulho com desfoque
tl.to("#camG1", {{scale:1.24, filter:"blur(16px)", duration:0.16, ease:"power2.in"}}, 11.37);
tl.to(["#t2a", "#t2p"], {{x:-90, opacity:0, duration:0.15, ease:"power2.in"}}, 11.36);

// ================= CTA 1 (clipe I) =================
tl.fromTo("#camI2", {{scale:1.2, filter:"blur(16px)"}}, {{scale:1.03, filter:"blur(0px)", duration:0.3, ease:"power3.out"}}, 11.53);
tl.to("#camI2", {{scale:1.07, duration:1.62, ease:"none"}}, 11.83);
tl.to("#noite", {{opacity:0.25, duration:0.3, ease:"power1.out"}}, 11.53);
tl.fromTo("#t3a", {{scale:1.6, opacity:0, filter:"blur(12px)", transformOrigin:"50% 55%"}}, {{scale:1, opacity:1, filter:"blur(0px)", duration:0.3, ease:"back.out(1.7)"}}, 11.6);

// ================= CTA 2 (clipe G): volta para a noite; toque no produto marcado =================
tl.fromTo("#fl2", {{opacity:0.4}}, {{opacity:0, duration:0.12, ease:"power1.out"}}, 13.45);
tl.fromTo("#camG2", {{scale:1.1}}, {{scale:1.02, duration:0.3, ease:"power3.out"}}, 13.45);
tl.to("#camG2", {{scale:1.07, duration:{R(TOTAL - 13.75)}, ease:"none"}}, 13.75);
tl.to("#noite", {{opacity:0.8, duration:0.3, ease:"power1.out"}}, 13.45);
tl.fromTo("#t3p", {{clipPath:"inset(0% 100% 0% 0% round 40px)"}}, {{clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.3, ease:"power3.out"}}, {R(T["Toque"] + 0.06)});
tl.fromTo("#tq-b", {{scale:0.5, opacity:0}}, {{scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}}, {R(T["Toque"])});
tl.fromTo("#tq-s", {{x:0, y:0}}, {{x:-7, y:7, duration:0.22, yoyo:true, repeat:9, ease:"sine.inOut"}}, {R(T["Toque"] + 0.3)});
tl.fromTo("#tq-o1", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["Toque"])});
tl.fromTo("#tq-o2", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, {R(T["marcado"])});
tl.fromTo("#tq-o3", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.63}}], ease:"power2.out"}}, 15.1);
// final: o botão da extensão (LED aceso) pulsa junto com o último toque
tl.fromTo("#rpB1", {{attr:{{r:84}}, opacity:0}}, {{keyframes:[{{opacity:0.9, duration:0.02}}, {{attr:{{r:300}}, opacity:0, duration:0.78}}], ease:"power2.out"}}, 15.1);
tl.fromTo("#rpB2", {{attr:{{r:84}}, opacity:0}}, {{keyframes:[{{opacity:0.9, duration:0.02}}, {{attr:{{r:300}}, opacity:0, duration:0.78}}], ease:"power2.out"}}, 15.26);
tl.fromTo("#hG2", {{opacity:0, scale:0.75}}, {{keyframes:[{{opacity:0.9, scale:1, duration:0.2}}, {{opacity:0.3, scale:1.06, duration:1.2}}], ease:"power2.out"}}, 15.1);

// ================= estrelas =================
''' + "\n".join(st1_js + st2_js + st3_js) + '''

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT)
