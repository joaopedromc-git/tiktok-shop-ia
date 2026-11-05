#!/usr/bin/env python3
"""Gera produtos/extensao/edicao_F/index.html — "Giro de 90°" (ângulo "Em pé ou deitada?").
Tinta-azul #0F1733 / tangerina #FF8A1F / creme #FFF5E6; Archivo Black (títulos, letreiro) + Poppins 800 (legenda).
Motivo: tudo gira 90°. Mostrador com ponteiro que vai de 12 h a 3 h junto com o clipe O (e volta na CTA),
transições "ponteiro de relógio" (painel opaco que gira 90° em torno de um canto, borda dura tangerina),
letreiro que vira 90° (rotationX) a cada corte, palavra-chave da legenda numa etiqueta que "deita" (-90° -> 0°).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regras: tudo a 1,0x, clipe em tela cheia (sem moldura), vídeo sempre rodando, nada desenhado sobre portas,
nada translúcido sobre a extensão (o degradê do topo para em 22 % da altura), sem rodapé.
Linha do tempo (s do vídeo final) — ver os prints no fim.
  O 1,50-3,90 (intro, gira até deitar) | N 0,90-x (empurra, sobe/desce) | G 0,60-2,40 (botão, LED ~2,0)
  | J 1,50-3,15 (plugue na 1ª tomada) | O 4,70-7,83 (gira de volta até ficar em pé)
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]
R = lambda v: str(round(v, 3))
P = lambda parte, i: falas[parte]["palavras"][i]

# ---------------- cortes (tudo a 1,0x) ----------------
V1 = 0.15
CO1 = (1.5, 3.9)
T_N = round(CO1[1] - CO1[0], 3)                     # 2.4
V2 = 2.68                                           # respiro de 0,24 s depois de "horizontal" (fim 2,44)
CN0 = 0.9
T_G = round(V2 + 2.5, 3)                            # entre "USB" (fim V2+2,25) e "Botão" (V2+2,58)
CG = (0.6, 2.4)
T_J = round(T_G + CG[1] - CG[0], 3)                 # LED (G 2,0) cai em T_G+1,4, dentro de "desliga"
CJ = (1.5, 3.15)
T_O2 = round(T_J + CJ[1] - CJ[0], 3)
V3 = round(T_O2 + 0.08, 3)
CO2 = (4.7, 7.83)                                   # o arquivo tem 7,85 s: para 0,02 s antes do fim
TOTAL = round(T_O2 + CO2[1] - CO2[0], 3)
D_O1, D_N, D_G, D_J, D_O2 = T_N, round(T_G - T_N, 3), round(T_J - T_G, 3), round(T_O2 - T_J, 3), round(TOTAL - T_O2, 3)
CN1 = round(CN0 + D_N, 3)
assert CN1 <= 7.0, CN1
VOZ = {"intro": V1, "apresentacao": V2, "cta": V3}
FIM_PARTE = {"intro": T_N, "apresentacao": T_O2, "cta": TOTAL}
DV = {"intro": round(V2 - V1 - 0.05, 3), "apresentacao": 5.976, "cta": round(TOTAL - V3, 3)}
for p in VOZ:
    assert VOZ[p] + falas[p]["palavras"][-1]["fim"] < FIM_PARTE[p] + 0.06, p
assert V2 + DV["apresentacao"] <= V3 and V1 + DV["intro"] <= V2


def t(parte, i):
    return round(VOZ[parte] + P(parte, i)["inicio"], 3)


T_VERT, T_HORIZ = t("intro", 2), t("intro", 4)
T_EXT, T_FILTRO, T_USB = t("apresentacao", 0), t("apresentacao", 1), t("apresentacao", 5)
T_BOTAO, T_DESL, T_CINCO = t("apresentacao", 6), t("apresentacao", 9), t("apresentacao", 10)
T_QUAL, T_TOCA = t("cta", 1), t("cta", 4)
T_LED = round(T_G + 2.0 - CG[0], 3)
T_TOCA0 = round(T_TOCA - 0.03, 3)

# ---------------- legenda "etiqueta que deita" ----------------
GRUPOS = {
    "intro": [[0, 1], [2], [3, 4]],
    "apresentacao": [[0], [1, 2, 3], [4, 5], [6], [7, 8, 9], [10, 11]],
    "cta": [[0], [1, 2], [3, 4], [5, 6], [7, 8]],
}
CHAVE = {"intro": {2, 4}, "apresentacao": {5, 9, 11}, "cta": {0, 4}}
EXIBE = {("intro", 4): "horizontal?", ("apresentacao", 5): "USB.", ("apresentacao", 9): "desliga.",
         ("apresentacao", 11): "tomadas.", ("cta", 8): "conferir."}
CAIXA = {"intro": (40, 878), "apresentacao": (40, 878), "cta": (196, 722)}   # na CTA o botão fica à esquerda
TOPO_LEG = 1450

leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz, pal = VOZ[parte], falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.04, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.04, 3), fim_voz)
        else:
            e = min(fim_voz, FIM_PARTE[parte])
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            tt = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.03, 3)
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            if wi in CHAVE[parte]:
                spans += (f'<span id="{gid}-{k}" class="pal ch"><i id="{gid}-{k}-t" class="tag"></i>'
                          f'<em class="tx">{txt}</em></span>')
                leg_js.append(f'tl.fromTo("#{gid}-{k}-t",{{rotation:-90}},{{rotation:0,duration:0.2,ease:"back.out(1.6)"}},{tt});')
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0}},{{opacity:1,duration:0.06,ease:"none"}},{tt});')
            else:
                spans += f'<span id="{gid}-{k}" class="pal"><em class="tx">{txt}</em></span>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:16}},{{opacity:1,y:0,duration:0.11,ease:"power2.out"}},{tt});')
        x, w = CAIXA[parte]
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="12">'
            f'<div id="{gid}-c" class="cap" style="left:{x}px;width:{w}px;top:{TOPO_LEG}px">{spans}</div></div>')

# ---------------- transições "ponteiro de relógio" ----------------
# (instante do corte, canto-pivô, sentido) — o painel cobre a tela inteira só ~1 quadro no corte
SWEEPS = [(T_N, "bl", 1), (T_G, "tr", 1), (T_J, "bl", 1), (T_O2, "bl", -1)]
sw_html, sw_js = [], []
for i, (tc, piv, sent) in enumerate(SWEEPS, 1):
    s = round(tc - 0.17, 3)
    sw_html.append(f'  <div id="sw{i}" class="clip sw" data-start="{s}" data-duration="0.34" data-track-index="{8 + i % 2}">'
                   f'<i id="sw{i}-p" class="pan {piv}"></i></div>')
    sw_js.append(f'tl.fromTo("#sw{i}-p",{{rotation:{-90 * sent}}},{{rotation:0,duration:0.15,ease:"power2.in"}},{s});')
    sw_js.append(f'tl.to("#sw{i}-p",{{rotation:{90 * sent},duration:0.15,ease:"power2.out"}},{R(tc + 0.02)});')

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Archivo Giro";src:local("Archivo Black Regular"),local("ArchivoBlack-Regular"),local("Archivo Black")}
@font-face{font-family:"Pop Giro";font-weight:800;src:local("Poppins ExtraBold"),local("Poppins-ExtraBold")}
:root{--tinta:#0F1733;--tang:#FF8A1F;--creme:#FFF5E6}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0F1733}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0F1733;font-family:"Pop Giro";font-weight:800}
.clip{position:absolute;inset:0}
.lay{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camO1{transform-origin:50% 45%}
#camN{transform-origin:35% 58%}
#camG{transform-origin:35% 41%}
#camJ{transform-origin:60% 42%}
#camO2{transform-origin:50% 45%}
/* degradê só no alto (para em 22 %: não tinge a extensão) */
.topo{z-index:3;background:linear-gradient(to bottom,rgba(15,23,51,.62) 0,rgba(15,23,51,.3) 12%,rgba(15,23,51,0) 22%)}
.flash{z-index:13;background:#FFFFFF;opacity:0}
/* transição: painel opaco gira 90° em torno de um canto, borda dura tangerina */
.sw{z-index:9;overflow:hidden}
.pan{position:absolute;display:block;width:2400px;height:2400px;background:var(--tinta);box-shadow:inset 0 0 0 26px var(--tang)}
.pan.bl{left:0;top:-480px;transform-origin:0 2400px}
.pan.tr{left:-1320px;top:0;transform-origin:2400px 0}
/* títulos */
.titulo{z-index:10}
.tt{position:absolute;display:block;font-family:"Archivo Giro";font-weight:400;line-height:1;white-space:nowrap;color:var(--creme);
  -webkit-text-stroke:10px var(--tinta);paint-order:stroke fill;text-shadow:0 8px 22px rgba(0,0,0,.45);letter-spacing:1px}
.tt .t{color:var(--tang)}
.mask{position:absolute;left:50px;width:868px;overflow:hidden;display:flex;justify-content:center;padding-top:6px}
.pill{position:absolute;display:block;white-space:nowrap;background:var(--tinta);color:var(--creme);font-family:"Pop Giro";font-weight:800;
  font-size:34px;line-height:1;padding:12px 26px 14px;border-radius:12px;box-shadow:inset 0 0 0 4px var(--tang),0 10px 24px rgba(0,0,0,.4)}
.pill b{font-weight:800;color:var(--tang)}
/* mostrador 90° */
.dial{position:absolute;display:block}
.dial svg{display:block;width:100%;height:100%;overflow:visible}
/* letreiro que vira 90° a cada corte */
#slot{position:absolute;left:164px;top:322px;width:640px;height:98px;display:block;border-radius:14px;background:var(--tang);
  box-shadow:0 0 0 6px var(--tinta),0 14px 30px rgba(0,0,0,.45);overflow:hidden}
#slot b{position:absolute;left:0;top:0;width:640px;height:98px;display:block;font-family:"Archivo Giro";font-weight:400;font-size:64px;
  line-height:98px;text-align:center;color:var(--tinta);letter-spacing:2px;opacity:0}
/* CTA: chips da enquete + botão com seta para baixo/esquerda */
.chip{position:absolute;top:276px;display:block;background:var(--tinta);color:var(--creme);font-family:"Archivo Giro";font-weight:400;
  font-size:50px;line-height:1;padding:16px 28px 18px;border-radius:14px;box-shadow:inset 0 0 0 5px var(--tang),0 12px 26px rgba(0,0,0,.45)}
#toque{z-index:12}
#tq-b{position:absolute;left:56px;top:1410px;width:116px;height:116px;display:block;border-radius:50%;background:var(--tang);
  box-shadow:0 0 0 7px var(--tinta),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:116px;height:116px}
#tq-o{position:absolute;left:56px;top:1410px;width:116px;height:116px;display:block;border:8px solid var(--tang);border-radius:50%;opacity:0}
/* legenda: branco com contorno tinta; palavra-chave numa etiqueta tangerina que deita (-90° -> 0°) */
.legenda{z-index:11}
.cap{position:absolute;display:flex;justify-content:center;align-items:flex-start;gap:20px;flex-wrap:nowrap}
.pal{position:relative;display:block;font-family:"Pop Giro";font-weight:800;font-size:74px;line-height:1.12;white-space:nowrap;color:#FFFFFF;
  -webkit-text-stroke:8px var(--tinta);paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.5)}
.pal.ch{color:var(--tinta);-webkit-text-stroke:0;text-shadow:none;padding:0 14px}
.tag{position:absolute;left:0;right:0;top:6px;bottom:2px;display:block;border-radius:12px;background:var(--tang);transform-origin:0% 100%;
  box-shadow:0 0 0 5px var(--tinta),0 10px 22px rgba(0,0,0,.45)}
.tx{position:relative;z-index:1;display:block;font-style:normal}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: O 1,50-3,90 (dedos giram a extensão de em pé até deitada) -->
  <div id="camO1" class="cam"><video id="vO1" class="clip full" data-start="0" data-duration="%%D_O1%%" data-media-start="%%CO10%%" data-track-index="0" src="assets/clipe_O.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: N (empurra, sobe/desce) -> G (botão, LED) -> J (plugue na 1ª tomada) -->
  <div id="camN" class="cam"><video id="vN" class="clip full" data-start="%%T_N%%" data-duration="%%D_N%%" data-media-start="%%CN0%%" data-track-index="1" src="assets/clipe_N.mp4" muted playsinline></video></div>
  <div id="camG" class="cam"><video id="vG" class="clip full" data-start="%%T_G%%" data-duration="%%D_G%%" data-media-start="%%CG0%%" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <div id="camJ" class="cam"><video id="vJ" class="clip full" data-start="%%T_J%%" data-duration="%%D_J%%" data-media-start="%%CJ0%%" data-track-index="1" src="assets/clipe_J.mp4" muted playsinline></video></div>
  <!-- CTA: O 4,70-7,83 (gira de volta até ficar em pé; separado do 1º trecho de O pela apresentação) -->
  <div id="camO2" class="cam"><video id="vO2" class="clip full" data-start="%%T_O2%%" data-duration="%%D_O2%%" data-media-start="%%CO20%%" data-track-index="0" src="assets/clipe_O.mp4" muted playsinline></video></div>

  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"></div>
%%SW_HTML%%

  <!-- intro: "EM PÉ / OU DEITADA?" no quadro 0; o ponteiro do mostrador vai de 12 h a 3 h junto com a extensão -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="%%T_N%%" data-track-index="3">
    <div id="t1-b" class="lay">
      <div id="t1-a" class="tt" style="left:60px;top:150px;font-size:150px">EM PÉ</div>
      <span id="d1" class="dial" style="left:668px;top:162px;width:132px;height:132px"><svg viewBox="0 0 132 132">
        <circle cx="66" cy="66" r="56" fill="#0F1733" stroke="#FF8A1F" stroke-width="10"/>
        <circle cx="66" cy="10" r="6" fill="#FFF5E6"/><circle cx="122" cy="66" r="6" fill="#FFF5E6"/>
        <g id="d1-h"><path d="M66 66 L66 26" stroke="#FFF5E6" stroke-width="12" stroke-linecap="round"/></g>
        <circle cx="66" cy="66" r="9" fill="#FF8A1F"/></svg></span>
      <div id="t1-c" class="tt" style="left:60px;top:322px;font-size:100px">OU <span class="t">DEITADA?</span></div>
    </div>
  </div>

  <!-- apresentação: título + linha + letreiro que vira a cada corte -->
  <div id="t2" class="clip titulo" data-start="%%T_N%%" data-duration="%%D_T2%%" data-track-index="4">
    <div id="t2-b" class="lay">
      <div class="mask" style="top:160px;height:92px"><div id="t2-a" class="tt" style="position:relative;font-size:72px">EXTENSÃO <span class="t">COM USB</span></div></div>
      <div style="position:absolute;left:50px;width:868px;top:256px;display:flex;justify-content:center"><span id="t2-p" class="pill" style="position:relative;font-size:34px;padding:10px 24px 12px">tipo C <b>•</b> liga/desliga</span></div>
      <span id="slot"><b id="s1">4 USB</b><b id="s2">LIGA/DESLIGA</b><b id="s3">5 TOMADAS</b></span>
    </div>
  </div>

  <!-- CTA: "COMENTA A SUA", enquete EM PÉ / DEITADA com o ponteiro voltando, "e toca no produto" -->
  <div id="t3" class="clip titulo" data-start="%%T_O2%%" data-duration="%%D_O2%%" data-track-index="5">
    <div class="mask" style="top:150px;height:104px"><div id="t3-a" class="tt" style="position:relative;font-size:86px">COMENTA <span class="t">A SUA</span></div></div>
    <span id="c1" class="chip" style="left:150px">EM PÉ</span>
    <span id="d2" class="dial" style="left:418px;top:268px;width:104px;height:104px"><svg viewBox="0 0 132 132">
      <circle cx="66" cy="66" r="56" fill="#0F1733" stroke="#FF8A1F" stroke-width="10"/>
      <circle cx="66" cy="10" r="6" fill="#FFF5E6"/><circle cx="122" cy="66" r="6" fill="#FFF5E6"/>
      <g id="d2-h"><path d="M66 66 L66 26" stroke="#FFF5E6" stroke-width="12" stroke-linecap="round"/></g>
      <circle cx="66" cy="66" r="9" fill="#FF8A1F"/></svg></span>
    <span id="c2" class="chip" style="left:546px">DEITADA</span>
    <div style="position:absolute;left:50px;width:868px;top:282px;display:flex;justify-content:center"><span id="t3-p" class="pill" style="position:relative;font-size:44px;padding:12px 28px 14px;opacity:0">e <b>toca</b> no produto</span></div>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="6">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#0F1733" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="7"></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="%%V1%%" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="%%V2%%" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="%%V3%%" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-wc-1" data-start="%%SW1%%" data-duration="0.4" data-track-index="15" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-wc-2" data-start="%%SW2%%" data-duration="0.4" data-track-index="14" data-volume="0.36" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-wc-3" data-start="%%SW3%%" data-duration="0.4" data-track-index="15" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="%%SSUB%%" data-duration="0.5" data-media-start="0.9" data-track-index="14" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="15" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (O 1,50-3,90): flash fraco + punch-in + tremor no quadro 0; título bate; ponteiro 12 h -> 3 h ----
tl.fromTo("#fl1", {opacity:0.25}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camO1", {scale:1.18}, {scale:1.0, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camO1", {scale:1.045, duration:%%DO1A%%, ease:"none"}, 0.4);
tl.fromTo("#camO1", {x:0, y:0}, {keyframes:[{x:16, y:-9, duration:0.05}, {x:-13, y:7, duration:0.06}, {x:9, y:-5, duration:0.06}, {x:-5, y:3, duration:0.07}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, 0.02);
tl.fromTo("#t1-a", {scale:1.08, transformOrigin:"0% 60%"}, {scale:1, duration:0.3, ease:"back.out(1.7)"}, 0);
tl.fromTo("#t1-c", {x:-24}, {x:0, duration:0.28, ease:"power3.out"}, 0);
tl.fromTo("#d1", {scale:0.8}, {scale:1, duration:0.32, ease:"back.out(1.8)"}, 0);
tl.fromTo("#d1-h", {rotation:0, svgOrigin:"66 66"}, {rotation:90, svgOrigin:"66 66", duration:%%DHAND1%%, ease:"sine.inOut"}, 0.12);
tl.fromTo("#t1-a", {scale:1}, {scale:1.08, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TVERT%%);
tl.fromTo("#t1-c", {scale:1, transformOrigin:"0% 60%"}, {scale:1.08, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%THORIZ%%);
tl.to("#t1-b", {rotation:12, x:60, opacity:0, duration:0.15, ease:"power2.in", transformOrigin:"0% 0%"}, %%T1OUT%%);

// ---- transições: painel gira 90° em torno do canto ----
%%SW_JS%%

// ---- APRESENTAÇÃO ----
// N: entra levemente aberta; punch no "USB"
tl.fromTo("#camN", {scale:1.08}, {scale:1.02, duration:0.3, ease:"power3.out"}, %%T_N%%);
tl.to("#camN", {scale:1.05, duration:%%DN1%%, ease:"none"}, %%T_N3%%);
tl.to("#camN", {scale:1.11, duration:0.13, ease:"power2.out"}, %%TPUSB%%);
tl.to("#camN", {scale:1.08, duration:0.4, ease:"power2.inOut"}, %%TPUSB2%%);
tl.to("#camN", {scale:1.09, duration:%%DN2%%, ease:"none"}, %%TPUSB3%%);
// G (produto herói): a câmera fecha no botão e no LED; punch quando o LED acende, no "desliga"
tl.fromTo("#camG", {scale:1.03}, {scale:1.1, duration:%%DGA%%, ease:"power2.inOut"}, %%T_G%%);
tl.to("#camG", {scale:1.13, duration:%%DG1%%, ease:"none"}, %%TBOTAO2%%);
tl.to("#camG", {scale:1.21, duration:0.14, ease:"power2.out"}, %%TLEDP%%);
tl.to("#camG", {scale:1.19, duration:%%DG2%%, ease:"none"}, %%TLEDP2%%);
// J: punch no "Cinco"
tl.fromTo("#camJ", {scale:1.08}, {scale:1.02, duration:0.2, ease:"power3.out"}, %%T_J%%);
tl.to("#camJ", {scale:1.04, duration:%%DJ1%%, ease:"none"}, %%T_J3%%);
tl.to("#camJ", {scale:1.1, duration:0.13, ease:"power2.out"}, %%TPCINCO%%);
tl.to("#camJ", {scale:1.08, duration:%%DJ2%%, ease:"power2.out"}, %%TPCINCO2%%);
// título, linha e letreiro (vira 90° em cada corte)
tl.fromTo("#t2-a", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, %%TT2%%);
tl.fromTo("#t2-p", {clipPath:"inset(0% 100% 0% 0% round 12px)"}, {clipPath:"inset(0% 0% 0% 0% round 12px)", duration:0.28, ease:"power3.out"}, %%TFILTRO%%);
tl.fromTo("#slot", {rotation:-90, opacity:0, transformOrigin:"0% 100%"}, {rotation:0, opacity:1, duration:0.26, ease:"back.out(1.5)"}, %%TS1%%);
tl.fromTo("#s1", {opacity:0}, {opacity:1, duration:0.05, ease:"none"}, %%TS1%%);
tl.to("#s1", {rotationX:90, transformPerspective:600, duration:0.12, ease:"power2.in"}, %%TS2A%%);
tl.fromTo("#s2", {opacity:1, rotationX:-90, transformPerspective:600}, {opacity:1, rotationX:0, duration:0.2, ease:"back.out(1.6)", immediateRender:false}, %%TS2%%);
tl.set("#s1", {opacity:0}, %%TS2%%);
tl.to("#s2", {rotationX:90, transformPerspective:600, duration:0.12, ease:"power2.in"}, %%TS3A%%);
tl.fromTo("#s3", {opacity:1, rotationX:-90, transformPerspective:600}, {opacity:1, rotationX:0, duration:0.2, ease:"back.out(1.6)", immediateRender:false}, %%TS3%%);
tl.set("#s2", {opacity:0}, %%TS3%%);
tl.fromTo("#slot", {scale:1}, {scale:1.07, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TSCINCO%%);
tl.to("#t2-b", {rotation:-10, x:-80, opacity:0, duration:0.15, ease:"power2.in", transformOrigin:"0% 0%"}, %%T2OUT%%);

// ---- CTA (O 4,70-7,83): título, enquete com ponteiro voltando a 12 h, botão em "toca" ----
tl.fromTo("#camO2", {scale:1.07}, {scale:1.0, duration:0.3, ease:"power3.out"}, %%T_O2%%);
tl.to("#camO2", {scale:1.03, duration:%%DE1%%, ease:"none"}, %%T_O2B%%);
tl.to("#camO2", {scale:1.05, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camO2", {scale:1.06, duration:%%DE2%%, ease:"none"}, %%TTOCA2%%);
tl.fromTo("#t3-a", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, %%TT3%%);
tl.fromTo("#c1", {rotation:-90, opacity:0, transformOrigin:"0% 100%"}, {rotation:0, opacity:1, duration:0.24, ease:"back.out(1.6)"}, %%TQUAL%%);
tl.fromTo("#d2", {scale:0.4, opacity:0}, {scale:1, opacity:1, duration:0.22, ease:"back.out(2)"}, %%TQUAL1%%);
tl.fromTo("#c2", {rotation:-90, opacity:0, transformOrigin:"0% 100%"}, {rotation:0, opacity:1, duration:0.24, ease:"back.out(1.6)"}, %%TQUAL2%%);
tl.fromTo("#d2-h", {rotation:90, svgOrigin:"66 66"}, {rotation:0, svgOrigin:"66 66", duration:%%DHAND2%%, ease:"sine.inOut"}, %%T_O2%%);
tl.to(["#c1", "#d2", "#c2"], {rotationX:90, transformPerspective:600, duration:0.12, ease:"power2.in"}, %%TROWOUT%%);
tl.set(["#c1", "#d2", "#c2"], {opacity:0}, %%TTOCA%%);
tl.fromTo("#t3-p", {opacity:1, rotationX:-90, transformPerspective:600}, {opacity:1, rotationX:0, duration:0.22, ease:"back.out(1.6)", immediateRender:false}, %%TTOCA%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA%%);
tl.fromTo("#tq-s", {x:0, y:0}, {x:-7, y:7, duration:0.22, yoyo:true, repeat:%%REP%%, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

TPUSB = round(T_USB - 0.04, 3)
TLEDP = round(T_LED - 0.04, 3)
TPCINCO = round(T_CINCO - 0.04, 3)
TS1, TS2, TS3 = round(T_USB - 0.06, 3), round(T_G + 0.05, 3), round(T_J + 0.05, 3)
T2OUT = round(T_O2 - 0.17, 3)
TPULSO = round(T_TOCA0 + 0.3, 3)
REP = int(((TOTAL - 0.05) - TPULSO) / 0.22) - 1
REP -= (REP + 1) % 2 == 1
subs = {
    "TOTAL": R(TOTAL), "SW_HTML": "\n".join(sw_html), "SW_JS": "\n".join(sw_js),
    "D_O1": R(D_O1), "D_N": R(D_N), "D_G": R(D_G), "D_J": R(D_J), "D_O2": R(D_O2),
    "T_N": R(T_N), "T_G": R(T_G), "T_J": R(T_J), "T_O2": R(T_O2),
    "CO10": R(CO1[0]), "CN0": R(CN0), "CG0": R(CG[0]), "CJ0": R(CJ[0]), "CO20": R(CO2[0]),
    "DO1A": R(T_N - 0.6), "DHAND1": R(T_N - 0.25), "TVERT": R(T_VERT - 0.03), "THORIZ": R(T_HORIZ - 0.03),
    "T1OUT": R(T_N - 0.17),
    "T_N3": R(T_N + 0.3), "DN1": R(TPUSB - (T_N + 0.3) - 0.003),
    "TPUSB": R(TPUSB), "TPUSB2": R(TPUSB + 0.13), "TPUSB3": R(TPUSB + 0.53), "DN2": R(T_G - (TPUSB + 0.53)),
    "DGA": R(T_BOTAO + 0.46 - T_G), "TBOTAO2": R(T_BOTAO + 0.46), "DG1": R(TLEDP - (T_BOTAO + 0.46) - 0.003),
    "TLEDP": R(TLEDP), "TLEDP2": R(TLEDP + 0.14), "DG2": R(T_J - (TLEDP + 0.14)),
    "T_J3": R(T_J + 0.2), "DJ1": R(TPCINCO - (T_J + 0.2) - 0.003),
    "TPCINCO": R(TPCINCO), "TPCINCO2": R(TPCINCO + 0.13), "DJ2": R(T_O2 - (TPCINCO + 0.13)),
    "TT2": R(T_EXT - 0.04), "TFILTRO": R(T_FILTRO - 0.03),
    "TS1": R(TS1), "TS2A": R(TS2 - 0.12), "TS2": R(TS2), "TS3A": R(TS3 - 0.12), "TS3": R(TS3),
    "TSCINCO": R(T_CINCO - 0.02), "T2OUT": R(T2OUT),
    "T_O2B": R(T_O2 + 0.3), "DE1": R(T_TOCA0 - (T_O2 + 0.3) - 0.003),
    "TTOCA": R(T_TOCA0), "TTOCA1": R(T_TOCA0 + 0.08), "TTOCA2": R(T_TOCA0 + 0.24), "DE2": R(TOTAL - (T_TOCA0 + 0.24)),
    "DTOCA": R(TOTAL - T_TOCA0), "TPULSO": R(TPULSO), "REP": str(REP), "TONDA2": R(T_TOCA0 + 0.95),
    "TT3": R(T_O2 + 0.06), "TQUAL": R(T_QUAL - 0.04), "TQUAL1": R(T_QUAL + 0.1), "TQUAL2": R(T_QUAL + 0.2),
    "DHAND2": R(T_TOCA0 - 0.15 - T_O2), "TROWOUT": R(T_TOCA0 - 0.12),
    "D_T2": R(T_O2 - T_N),
    "V1": R(V1), "V2": R(V2), "V3": R(V3), "DV1": R(DV["intro"]), "DV2": R(DV["apresentacao"]), "DV3": R(DV["cta"]),
    "SW1": R(T_N + 0.0), "SW2": R(T_G - 0.12), "SW3": R(T_J - 0.02), "SSUB": R(T_O2 - 0.5),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
for nome, d in (("DN1", TPUSB - (T_N + 0.3)), ("DG1", TLEDP - (T_BOTAO + 0.46)), ("DJ1", TPCINCO - (T_J + 0.2))):
    assert d > 0.05, (nome, d)
open(OUT, "w").write(html)
print(f"TOTAL {TOTAL} | O1 0-{T_N} (O {CO1[0]}-{CO1[1]}) | N {T_N}-{T_G} (N {CN0}-{CN1}) | G {T_G}-{T_J} (G {CG[0]}-{CG[1]}, LED {T_LED})"
      f" | J {T_J}-{T_O2} (J {CJ[0]}-{CJ[1]}) | O2 {T_O2}-{TOTAL} (O {CO2[0]}-{CO2[1]})")
print(f"voz {V1}/{V2}/{V3} | horizontal fim {round(V1 + P('intro', 4)['fim'], 3)} | USB {T_USB} | Botão {T_BOTAO} | desliga {T_DESL}-"
      f"{round(V2 + P('apresentacao', 9)['fim'], 3)} | Cinco {T_CINCO} | tomadas fim {round(V2 + P('apresentacao', 11)['fim'], 3)}"
      f" | toca {T_TOCA} | conferir fim {round(V3 + P('cta', 8)['fim'], 3)} | rep {REP}")
