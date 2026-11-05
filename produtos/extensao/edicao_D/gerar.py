#!/usr/bin/env python3
"""Gera produtos/extensao/edicao_D/index.html ("ao alcance da mão": grafite / coral-melancia / creme,
Bricolage Grotesque 800 + Montserrat 800, legenda "adesivo" creme com texto grafite e marca-texto coral).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regra da 3ª violação: o vídeo de fundo roda do primeiro ao último quadro; nada de <img>, quadro congelado ou cartão.
Trechos (analise_D.md + analise_C.md); K REJEITADO, nenhum quadro dele:
  intro        J 0,55-4,47 s em 1,00x (mão encaixa o plugue na 1ª tomada de cima)
  apresentação J 4,47-7,95 s em 0,70x (mão sai, plugue encaixado: callouts 5 tomadas / 4 USB / tipo C)
               G 0,40-4,05 s em 0,85x (dedo no botão sob "onde a mão alcança", LED acende no "Botão")
  CTA          L 0,00-2,80 s em 0,70x (mão pega o celular; nunca depois de 2,8 s)
               G 4,05-5,08 s em 0,85x (continua de onde parou: mão já fora, LED aceso; nunca depois de 5,2 s)
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 3.92, 0.2), "apresentacao": (3.92, 13.18, 4.17), "cta": (13.18, 18.39, 13.53)}
TOTAL = P["cta"][1]
DUR_MP3 = {"intro": 3.696, "apresentacao": 8.952, "cta": 4.752}
# legenda logo abaixo do bloco de título (o produto ocupa o meio e a mão entra por baixo/lados)
TOPO_LEG = {"intro": 356, "apresentacao": 356, "cta": 300}

GRUPOS = {
    "intro": [[0], [1], [2], [3, 4], [5, 6, 7, 8], [9, 10]],
    "apresentacao": [[0], [1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11], [12, 13], [14, 15], [16, 17, 18], [19],
                     [20], [21, 22, 23], [24, 25]],
    "cta": [[0], [1, 2], [3, 4], [5], [6, 7], [8, 9], [10, 11], [12, 13]],
}
CHAVE = {
    "intro": {1, 4, 10},
    "apresentacao": {0, 4, 6, 11, 13, 18, 20, 23},
    "cta": {0, 4, 5, 7, 13},
}
EXIBE = {("intro", 4): "móvel,", ("intro", 10): "joelhos?", ("apresentacao", 3): "linha:",
         ("apresentacao", 5): "tomadas,", ("apresentacao", 11): "C", ("apresentacao", 15): "móvel,",
         ("apresentacao", 19): "alcança.", ("apresentacao", 25): "vista.", ("cta", 4): "mão?",
         ("cta", 13): "confira."}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---------------- legenda "adesivo": cartão creme com borda grafite; palavras acendem no tempo (30% -> 100%);
# palavra-chave ganha marca-texto coral que se desenha por trás ----------------
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
            e = min(fim_voz, P[parte][1] - 0.12)
        gid = f"lg-{parte[:3]}-{gi}"
        ems = ""
        for k, i in enumerate(g):
            txt = EXIBE.get((parte, i), pal[i]["palavra"])
            ti = t_pal(parte, i)
            if i in CHAVE[parte]:
                ems += f'<em id="{gid}-{k}" class="w k"><i id="{gid}-{k}m" class="mk"></i><span>{txt}</span></em>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}m",{{scaleX:0}},{{scaleX:1,duration:0.16,ease:"power3.out"}},{R(ti)});')
            else:
                ems += f'<em id="{gid}-{k}" class="w"><span>{txt}</span></em>'
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0.3}},{{opacity:1,duration:0.08,ease:"power1.out"}},{R(ti - 0.02)});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="20">'
                        f'<div class="cap" style="top:{TOPO_LEG[parte]}px"><span id="{gid}-c" class="card">{ems}</span></div></div>')
        leg_js.append(f'tl.fromTo("#{gid}-c",{{scale:0.86,y:10}},{{scale:1,y:0,duration:0.14,ease:"back.out(2.6)"}},{R(s)});')

T = {
    "escondida": t_pal("intro", 1), "atras": t_pal("intro", 2), "e_la": t_pal("intro", 5), "joelhos": t_pal("intro", 10),
    "extensao": t_pal("apresentacao", 0), "cinco": t_pal("apresentacao", 4), "tomadas": t_pal("apresentacao", 5),
    "quatro": t_pal("apresentacao", 6), "tipo": t_pal("apresentacao", 10), "em": t_pal("apresentacao", 12),
    "onde": t_pal("apresentacao", 16), "botao": t_pal("apresentacao", 20), "desliga": t_pal("apresentacao", 23),
    "vista": t_pal("apresentacao", 25),
    "celular": t_pal("cta", 0), "mao": t_pal("cta", 4), "Toque": t_pal("cta", 5), "aparece": t_pal("cta", 9),
    "confira": t_pal("cta", 13),
}

# J na apresentação: origem 468,1010 (centro da extensão), escala ~1,14 durante os callouts.
# Etiquetas ficam FORA do zoom (aprendizado: dentro do zoom saem pela borda); posição calculada em s=1,14.
S_J = 1.14
jx = lambda x: round(468 + (x - 468) * S_J)
jy = lambda y: round(1010 + (y - 1010) * S_J)

HTML = f'''<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{{font-family:"Bric Alcance";font-weight:200 800;src:local("Bricolage Grotesque 96pt ExtraBold"),local("Bricolage Grotesque")}}
@font-face{{font-family:"Mont Alcance";font-weight:100 900;src:local("Montserrat Thin"),local("Montserrat-Thin"),local("Montserrat")}}
:root{{--graf:#141519;--coral:#FF4D6D;--creme:#FFF7EC}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#141519}}
#root{{width:100%;height:100%;position:relative;overflow:hidden;background:#141519;font-family:"Mont Alcance";font-weight:800}}
.clip{{position:absolute;inset:0}}
.cam{{position:absolute;inset:0;overflow:hidden;z-index:1}}
.full{{width:100%;height:100%;object-fit:cover}}
#camJ1,#camJ2{{transform-origin:468px 1010px}}
#camG1,#camG2{{transform-origin:548px 0px}}
#camL{{transform-origin:540px 0px}}
.ov{{position:absolute;inset:0}}
.ov svg{{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block;overflow:visible}}
.trace{{fill:none;stroke:#FF4D6D;stroke-width:8;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 3px rgba(20,21,25,.9))}}
.anel{{fill:none;stroke:#FF4D6D;stroke-width:6}}
/* etiquetas dos callouts (fora do zoom) */
.chips{{z-index:6}}
.chip{{position:absolute;display:block;white-space:nowrap;background:#FF4D6D;color:#141519;font-family:"Mont Alcance";
  font-weight:800;font-size:44px;line-height:1;padding:12px 22px 14px;border-radius:14px;border:4px solid #141519}}
#m5{{position:absolute;display:flex;flex-direction:column;align-items:center;gap:2px}}
#m5 b{{display:block;font-family:"Bric Alcance";font-weight:800;font-size:150px;line-height:.9;color:#FF4D6D;
  text-shadow:0 6px 0 #141519}}
#m5 span{{display:block;font-family:"Mont Alcance";font-weight:800;font-size:38px;line-height:1;color:#FFF7EC;
  background:#141519;padding:8px 14px 10px;border-radius:10px}}
/* brilho que corre na extensão do G (recortado no contorno da extensão) */
#sw-m{{position:absolute;left:290px;top:485px;width:515px;height:1050px;overflow:hidden;display:block;border-radius:52px}}
#sw-b{{position:absolute;left:0;top:-200px;width:180px;height:1500px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.38) 50%,rgba(255,255,255,0) 100%)}}
.glow{{position:absolute;width:300px;height:300px;display:block;border-radius:50%;
  background:radial-gradient(closest-side,rgba(255,77,109,0) 0,rgba(255,77,109,0) 46%,rgba(255,77,109,.5) 54%,rgba(255,77,109,.14) 74%,rgba(255,77,109,0) 100%)}}
/* bloco de título: placa grafite + aba coral (linha) */
.titulo{{z-index:9}}
.tb{{position:absolute;left:40px;top:170px;width:878px;display:flex;flex-direction:column;align-items:center}}
.slab{{display:block;white-space:nowrap;background:#141519;color:#FFF7EC;font-family:"Bric Alcance";font-weight:800;
  line-height:1;letter-spacing:-1px;padding:14px 32px 20px;border-radius:16px;box-shadow:0 8px 0 rgba(255,77,109,.0)}}
.slab .c{{color:#FF4D6D}}
.aba{{display:block;white-space:nowrap;background:#FF4D6D;color:#141519;font-family:"Mont Alcance";font-weight:800;
  font-size:38px;line-height:1;padding:9px 22px 11px;border-radius:0 0 14px 14px}}
/* legenda "adesivo" */
.legenda{{z-index:10}}
.cap{{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start}}
.card{{display:flex;gap:22px;align-items:center;white-space:nowrap;background:#FFF7EC;border:5px solid #141519;
  border-radius:20px;padding:6px 30px 12px;box-shadow:0 9px 0 #141519}}
.w{{position:relative;display:block;font-style:normal;font-family:"Mont Alcance";font-weight:800;font-size:84px;
  line-height:1.12;color:#141519}}
.w span{{position:relative;display:block}}
.mk{{position:absolute;left:-10px;right:-10px;top:14%;bottom:6%;display:block;background:#FF4D6D;border-radius:10px;
  transform-origin:0% 50%}}
/* painéis de transição: opacos, bordas duras (nunca tingem a extensão) */
.painel{{z-index:14}}
.pn{{position:absolute;inset:0;display:block}}
.flash{{z-index:13;background:#FFF7EC;opacity:0}}
/* CTA: seta lateral apontando a extensão e botão de toque embaixo à esquerda */
#seta{{z-index:11}}
#seta-i{{position:absolute;left:790px;top:640px;width:120px;height:120px;display:block}}
#seta-i svg{{display:block;width:120px;height:120px}}
#toque{{z-index:11}}
#tq-b{{position:absolute;left:56px;top:1380px;width:120px;height:120px;display:block;border-radius:50%;background:#FF4D6D;
  border:6px solid #141519}}
#tq-b svg{{display:block;width:108px;height:108px}}
.tq-o{{position:absolute;left:56px;top:1380px;width:120px;height:120px;display:block;border:6px solid #FF4D6D;border-radius:50%;opacity:0}}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{R(TOTAL)}" data-width="1080" data-height="1920">
  <!-- INTRO (0-3,92 s): J 0,55-4,47 s em 1,00x (a mão encaixa o plugue na 1ª tomada) -->
  <div id="camJ1" class="cam"><video id="vJ1" class="clip full" data-start="0" data-duration="3.92" data-media-start="0.55" data-playback-rate="1" data-track-index="0" src="assets/clipe_J.mp4" muted playsinline></video></div>

  <!-- APRESENTAÇÃO 1 (3,92-8,89 s): J 4,47-7,95 s em 0,70x (mão sai, plugue encaixado) -->
  <div id="camJ2" class="cam"><video id="vJ2" class="clip full" data-start="3.92" data-duration="4.97" data-media-start="4.47" data-playback-rate="0.7" data-track-index="1" src="assets/clipe_J.mp4" muted playsinline></video>
    <div id="ovJ2" class="clip ov" data-start="3.92" data-duration="4.97" data-track-index="2">
      <svg viewBox="0 0 1080 1920">
        <rect id="oJ-tom" class="trace" x="446" y="708" width="206" height="664" rx="26" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <rect id="oJ-usb" class="trace" x="324" y="1008" width="92" height="190" rx="16" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <circle id="oJ-c" class="trace" cx="370" cy="1215" r="32" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      </svg>
    </div>
  </div>
  <div id="chJ" class="clip chips" data-start="3.92" data-duration="4.97" data-track-index="3">
    <div id="m5" style="left:{jx(676)}px;top:{jy(930)}px"><b id="m5n">5</b><span id="m5t">tomadas</span></div>
    <span id="lJ-usb" class="chip" style="right:{1080 - jx(306)}px;top:{jy(1070)}px">4 USB</span>
    <span id="lJ-c" class="chip" style="right:{1080 - jx(326)}px;top:{jy(1186)}px">tipo C</span>
  </div>

  <!-- APRESENTAÇÃO 2 (8,89-13,18 s): G 0,40-4,05 s em 0,85x; dedo no botão sob "onde a mão alcança", LED no "Botão" -->
  <div id="camG1" class="cam"><video id="vG1" class="clip full" data-start="8.89" data-duration="4.29" data-media-start="0.4" data-playback-rate="0.85" data-track-index="1" src="assets/clipe_G.mp4" muted playsinline></video>
    <div id="ovG1" class="clip ov" data-start="8.89" data-duration="4.29" data-track-index="2">
      <span id="sw-m"><i id="sw-b"></i></span>
      <i id="gG1" class="glow" style="left:259px;top:578px"></i>
      <svg viewBox="0 0 1080 1920">
        <circle id="oG-bt" class="trace" cx="409" cy="728" r="88" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <circle id="rpA1" class="anel" cx="409" cy="728" r="88" opacity="0"/>
        <circle id="rpA2" class="anel" cx="409" cy="728" r="88" opacity="0"/>
      </svg>
    </div>
  </div>

  <!-- CTA 1 (13,18-17,18 s): L 0,00-2,80 s em 0,70x (a mão pega o celular; nada depois de 2,8 s) -->
  <div id="camL" class="cam"><video id="vL" class="clip full" data-start="13.18" data-duration="4" data-media-start="0" data-playback-rate="0.7" data-track-index="1" src="assets/clipe_L.mp4" muted playsinline></video>
    <div id="ovL" class="clip ov" data-start="13.18" data-duration="4" data-track-index="2">
      <svg viewBox="0 0 1080 1920">
        <rect id="oL-strip" class="trace" x="402" y="404" width="332" height="646" rx="44" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
      </svg>
    </div>
  </div>

  <!-- CTA 2 (17,18-18,39 s): G 4,05-5,08 s em 0,85x (continua de onde parou: mão fora, LED aceso) -->
  <div id="camG2" class="cam"><video id="vG2" class="clip full" data-start="17.18" data-duration="1.21" data-media-start="4.05" data-playback-rate="0.85" data-track-index="1" src="assets/clipe_G.mp4" muted playsinline></video>
    <div id="ovG2" class="clip ov" data-start="17.18" data-duration="1.21" data-track-index="2">
      <i id="gG2" class="glow" style="left:259px;top:578px"></i>
      <svg viewBox="0 0 1080 1920">
        <rect id="oG2-strip" class="trace" x="286" y="481" width="523" height="1058" rx="54" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
        <circle id="rpB1" class="anel" cx="409" cy="728" r="88" opacity="0"/>
      </svg>
    </div>
  </div>

  <!-- títulos -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="3.86" data-track-index="7">
    <div class="tb"><div id="t1s" class="slab" style="font-size:80px">De joelhos <span class="c">de novo?</span></div><div id="t1a" class="aba">tomada atrás do móvel</div></div>
  </div>
  <div id="t2" class="clip titulo" data-start="{R(T["onde"] - 0.08)}" data-duration="{R(13.1 - T["onde"] + 0.08)}" data-track-index="7">
    <div class="tb"><div id="t2s" class="slab" style="font-size:84px">Ao alcance <span class="c">da mão</span></div><div id="t2a" class="aba">5 tomadas • 4 USB • tipo C</div></div>
  </div>
  <div id="t3" class="clip titulo" data-start="13.24" data-duration="{R(T["Toque"] - 13.24)}" data-track-index="7">
    <div class="tb"><div id="t3s" class="slab" style="font-size:88px">Celular <span class="c">na mão?</span></div></div>
  </div>
  <div id="t4" class="clip titulo" data-start="{R(T["Toque"])}" data-duration="{R(TOTAL - T["Toque"])}" data-track-index="8">
    <div class="tb"><div id="t4s" class="slab" style="font-size:62px">toque na <span class="c">extensão</span> do vídeo</div></div>
  </div>

  <div id="seta" class="clip" data-start="{R(T["Toque"])}" data-duration="{R(17.18 - T["Toque"])}" data-track-index="9">
    <span id="seta-i"><svg id="seta-s" viewBox="0 0 120 120"><circle cx="60" cy="60" r="54" fill="#FF4D6D" stroke="#141519" stroke-width="6"/><path d="M84 60 H34 M54 38 L32 60 L54 82" fill="none" stroke="#141519" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>
  <div id="toque" class="clip" data-start="17.18" data-duration="{R(TOTAL - 17.18)}" data-track-index="9">
    <i id="tq-o1" class="tq-o"></i><i id="tq-o2" class="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 108 108"><path d="M74 34 L38 70 M36 44 L36 72 L64 72" fill="none" stroke="#141519" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

  <!-- transições opacas -->
  <div id="pn1" class="clip painel" data-start="3.74" data-duration="0.36" data-track-index="12"><i id="pn1i" class="pn" style="background:#FF4D6D"></i></div>
  <div id="pn2" class="clip painel" data-start="8.73" data-duration="0.32" data-track-index="12"><i id="pn2i" class="pn" style="background:#141519"></i></div>
  <div id="pn3" class="clip painel" data-start="13.0" data-duration="0.36" data-track-index="12"><i id="pn3i" class="pn" style="background:#FF4D6D"></i></div>
  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="11"></div>
  <div id="fl2" class="clip flash" data-start="17.18" data-duration="0.12" data-track-index="11"></div>

{chr(10).join(leg_html)}

  <audio id="voz-intro" data-start="{P["intro"][2]}" data-duration="{DUR_MP3["intro"]}" data-track-index="21" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="{P["apresentacao"][2]}" data-duration="{DUR_MP3["apresentacao"]}" data-track-index="21" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="{P["cta"][2]}" data-duration="{DUR_MP3["cta"]}" data-track-index="21" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="22" data-volume="0.55" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-pop-1" data-start="{R(T["atras"] - 0.06)}" data-duration="0.09" data-track-index="22" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="3.76" data-duration="0.3" data-track-index="22" data-volume="0.35" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-2" data-start="{R(T["cinco"] - 0.08)}" data-duration="0.09" data-track-index="22" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-tique-1" data-start="{R(T["tipo"] - 0.08)}" data-duration="0.03" data-track-index="22" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="8.74" data-duration="0.3" data-track-index="22" data-volume="0.35" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-brilho-1" data-start="{R(T["botao"] - 0.06)}" data-duration="0.9" data-track-index="22" data-volume="0.28" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-subida-1" data-start="11.78" data-duration="1.4" data-track-index="22" data-volume="0.3" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="{R(T["Toque"])}" data-duration="0.05" data-track-index="22" data-volume="0.45" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-whooshc-3" data-start="17.12" data-duration="0.3" data-track-index="22" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});

// ================= INTRO (J): gancho com flash, punch e título batendo =================
tl.fromTo("#fl1", {{opacity:0.8}}, {{opacity:0, duration:0.1, ease:"power1.out"}}, 0);
tl.fromTo("#camJ1", {{scale:1.34}}, {{scale:1.16, duration:0.4, ease:"power3.out"}}, 0);
tl.to("#camJ1", {{scale:1.19, duration:{R(T["e_la"] - 0.4)}, ease:"none"}}, 0.4);
tl.fromTo("#t1s", {{scale:1.7, opacity:0, rotation:-3}}, {{scale:1, opacity:1, rotation:0, duration:0.3, ease:"back.out(1.8)"}}, 0.03);
tl.fromTo("#t1a", {{clipPath:"inset(0% 100% 0% 0%)"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.28, ease:"power3.out"}}, {R(T["atras"] - 0.05)});
// "e lá vai você": punch
tl.to("#camJ1", {{scale:1.23, duration:0.12, ease:"power2.out"}}, {R(T["e_la"])});
tl.to("#camJ1", {{scale:1.21, duration:0.5, ease:"power2.inOut"}}, {R(T["e_la"] + 0.12)});
// "joelhos": a câmera "ajoelha" (cai e quica) com tremor
tl.fromTo("#camJ1", {{y:0, x:0}}, {{keyframes:[{{y:46, duration:0.1, ease:"power3.in"}}, {{y:28, x:8, duration:0.07}}, {{y:36, x:-7, duration:0.07}}, {{y:30, x:0, duration:0.08}}], immediateRender:false}}, {R(T["joelhos"])});
tl.to("#camJ1", {{scale:1.24, duration:0.12, ease:"power2.out"}}, {R(T["joelhos"])});
tl.to(["#t1s", "#t1a"], {{y:-50, opacity:0, duration:0.12, ease:"power2.in"}}, 3.7);
// painel coral sobe e revela a apresentação
tl.fromTo("#pn1i", {{yPercent:100}}, {{yPercent:0, duration:0.18, ease:"power2.in"}}, 3.74);
tl.to("#pn1i", {{yPercent:-100, duration:0.18, ease:"power2.out"}}, 3.92);

// ================= APRESENTAÇÃO 1 (J): callouts 5 tomadas / 4 USB / tipo C =================
tl.fromTo("#camJ2", {{scale:1.2}}, {{scale:1.12, duration:{R(T["extensao"] - 3.93)}, ease:"power3.out"}}, 3.92);
tl.to("#camJ2", {{scale:1.16, duration:0.12, ease:"power2.out"}}, {R(T["extensao"])});
tl.to("#camJ2", {{scale:1.125, duration:0.5, ease:"power2.inOut"}}, {R(T["extensao"] + 0.12)});
tl.to("#camJ2", {{scale:1.135, duration:{R(T["cinco"] - T["extensao"] - 0.62)}, ease:"none"}}, {R(T["extensao"] + 0.62)});
tl.to("#oJ-tom", {{attr:{{"stroke-dashoffset":0}}, duration:0.36, ease:"power2.out"}}, {R(T["cinco"] - 0.06)});
tl.to("#camJ2", {{scale:1.15, duration:0.12, ease:"power2.out"}}, {R(T["cinco"])});
tl.to("#camJ2", {{scale:1.14, duration:2.6, ease:"none"}}, {R(T["cinco"] + 0.12)});
tl.fromTo("#m5n", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.24, ease:"back.out(2.4)"}}, {R(T["tomadas"] - 0.04)});
tl.fromTo("#m5t", {{y:-16, opacity:0}}, {{y:0, opacity:1, duration:0.18, ease:"power3.out"}}, {R(T["tomadas"] + 0.08)});
tl.to(["#oJ-tom", "#m5"], {{opacity:0, duration:0.14, ease:"power1.in"}}, {R(T["quatro"] - 0.14)});
tl.to("#oJ-usb", {{attr:{{"stroke-dashoffset":0}}, duration:0.3, ease:"power2.out"}}, {R(T["quatro"] - 0.04)});
tl.fromTo("#lJ-usb", {{x:-60, opacity:0}}, {{x:0, opacity:1, duration:0.2, ease:"power3.out"}}, {R(T["quatro"])});
tl.to(["#oJ-usb", "#lJ-usb"], {{opacity:0, duration:0.14, ease:"power1.in"}}, {R(T["tipo"] - 0.16)});
tl.to("#oJ-c", {{attr:{{"stroke-dashoffset":0}}, duration:0.28, ease:"power2.out"}}, {R(T["tipo"] - 0.04)});
tl.fromTo("#lJ-c", {{x:-60, opacity:0}}, {{x:0, opacity:1, duration:0.2, ease:"power3.out"}}, {R(T["tipo"])});
tl.to(["#oJ-c", "#lJ-c"], {{opacity:0, duration:0.14, ease:"power1.in"}}, 8.62);
// painel grafite atravessa da esquerda para a direita
tl.fromTo("#pn2i", {{xPercent:-100}}, {{xPercent:0, duration:0.16, ease:"power2.in"}}, 8.73);
tl.to("#pn2i", {{xPercent:100, duration:0.16, ease:"power2.out"}}, 8.89);

// ================= APRESENTAÇÃO 2 (G): produto herói, dedo alcança o botão, LED acende =================
tl.fromTo("#camG1", {{scale:1.07}}, {{scale:1.0, duration:0.4, ease:"power3.out"}}, 8.89);
tl.to("#camG1", {{scale:1.04, duration:{R(T["botao"] - 9.29)}, ease:"none"}}, 9.29);
tl.fromTo("#sw-b", {{x:-300, rotation:16}}, {{x:680, rotation:16, duration:0.6, ease:"power1.inOut"}}, 8.98);
tl.fromTo("#t2s", {{scale:1.6, opacity:0, rotation:2}}, {{scale:1, opacity:1, rotation:0, duration:0.3, ease:"back.out(1.8)"}}, {R(T["onde"] - 0.08)});
tl.fromTo("#t2a", {{clipPath:"inset(0% 100% 0% 0%)"}}, {{clipPath:"inset(0% 0% 0% 0%)", duration:0.3, ease:"power3.out"}}, {R(T["onde"] + 0.5)});
// "Botão" (LED acende): punch, anel desenha em volta do botão, brilho e ondas
tl.to("#camG1", {{scale:1.08, duration:0.1, ease:"power3.out"}}, {R(T["botao"])});
tl.to("#camG1", {{scale:1.05, duration:0.5, ease:"power2.inOut"}}, {R(T["botao"] + 0.1)});
tl.to("#camG1", {{scale:1.07, duration:{R(13.18 - T["botao"] - 0.6)}, ease:"none"}}, {R(T["botao"] + 0.6)});
tl.to("#oG-bt", {{attr:{{"stroke-dashoffset":0}}, duration:0.34, ease:"power2.out"}}, {R(T["botao"])});
tl.fromTo("#gG1", {{opacity:0, scale:0.7}}, {{keyframes:[{{opacity:1, scale:1, duration:0.18}}, {{opacity:0.4, scale:1.06, duration:0.9}}], ease:"power2.out"}}, {R(T["botao"])});
tl.fromTo("#rpA1", {{attr:{{r:88}}, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{attr:{{r:230}}, opacity:0, duration:0.7}}], ease:"power2.out"}}, {R(T["botao"] + 0.1)});
tl.fromTo("#rpA2", {{attr:{{r:88}}, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{attr:{{r:230}}, opacity:0, duration:0.7}}], ease:"power2.out"}}, {R(T["desliga"])});
tl.to("#camG1", {{y:-6, duration:0.08, yoyo:true, repeat:1, ease:"power1.inOut"}}, {R(T["vista"])});
tl.to(["#t2s", "#t2a"], {{y:-50, opacity:0, duration:0.12, ease:"power2.in"}}, 12.96);
// painel coral desce e revela a CTA
tl.fromTo("#pn3i", {{yPercent:-100}}, {{yPercent:0, duration:0.18, ease:"power2.in"}}, 13.0);
tl.to("#pn3i", {{yPercent:100, duration:0.18, ease:"power2.out"}}, 13.18);

// ================= CTA 1 (L): celular na mão; "Toque" aponta a extensão =================
tl.fromTo("#camL", {{scale:1.16}}, {{scale:1.08, duration:0.4, ease:"power3.out"}}, 13.18);
tl.to("#camL", {{scale:1.12, duration:3.6, ease:"none"}}, 13.58);
tl.fromTo("#t3s", {{scale:1.7, opacity:0, rotation:-2}}, {{scale:1, opacity:1, rotation:0, duration:0.3, ease:"back.out(1.8)"}}, 13.24);
tl.to("#t3s", {{scale:1.06, duration:0.1, yoyo:true, repeat:1, ease:"power1.inOut"}}, {R(T["mao"])});
tl.to("#oL-strip", {{attr:{{"stroke-dashoffset":0}}, duration:0.4, ease:"power2.inOut"}}, {R(T["Toque"])});
tl.fromTo("#t4s", {{scale:0.7, opacity:0}}, {{scale:1, opacity:1, duration:0.22, ease:"back.out(2)"}}, {R(T["Toque"])});
tl.fromTo("#seta-i", {{x:60, opacity:0}}, {{x:0, opacity:1, duration:0.22, ease:"power3.out"}}, {R(T["Toque"] + 0.04)});
tl.fromTo("#seta-s", {{x:0}}, {{x:-14, duration:0.25, yoyo:true, repeat:5, ease:"sine.inOut"}}, {R(T["Toque"] + 0.3)});

// ================= CTA 2 (G): LED aceso, botão de toque embaixo à esquerda =================
tl.fromTo("#fl2", {{opacity:0.55}}, {{opacity:0, duration:0.1, ease:"power1.out"}}, 17.18);
tl.fromTo("#camG2", {{scale:1.12}}, {{scale:1.05, duration:0.3, ease:"power3.out"}}, 17.18);
tl.to("#camG2", {{scale:1.08, duration:{R(TOTAL - 17.48)}, ease:"none"}}, 17.48);
tl.to("#oG2-strip", {{attr:{{"stroke-dashoffset":0}}, duration:0.4, ease:"power2.inOut"}}, 17.22);
tl.fromTo("#gG2", {{opacity:0, scale:0.8}}, {{keyframes:[{{opacity:0.9, scale:1, duration:0.2}}, {{opacity:0.45, scale:1.05, duration:0.9}}], ease:"power2.out"}}, 17.22);
tl.fromTo("#rpB1", {{attr:{{r:88}}, opacity:0}}, {{keyframes:[{{opacity:0.9, duration:0.02}}, {{attr:{{r:220}}, opacity:0, duration:0.7}}], ease:"power2.out"}}, {R(T["confira"])});
tl.fromTo("#tq-b", {{scale:0.5, opacity:0}}, {{scale:1, opacity:1, duration:0.22, ease:"back.out(2.2)"}}, 17.2);
tl.fromTo("#tq-s", {{x:0, y:0}}, {{x:-7, y:7, duration:0.2, yoyo:true, repeat:3, ease:"sine.inOut"}}, 17.45);
tl.fromTo("#tq-o1", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.6}}], ease:"power2.out"}}, 17.2);
tl.fromTo("#tq-o2", {{scale:0.6, opacity:0}}, {{keyframes:[{{opacity:0.95, duration:0.02}}, {{scale:2.0, opacity:0, duration:0.6}}], ease:"power2.out"}}, {R(T["confira"])});

// ================= legenda =================
''' + "\n".join(leg_js) + '''
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

open(OUT, "w").write(HTML)
print("ok", OUT, "total", TOTAL)
