#!/usr/bin/env python3
"""Gera produtos/hilee/edicao_C/index.html — "Placar": time canudo x time direto.
Preto-placar #111214 / vermelho-placar #FF3D2E / creme #FFF4E4; Bebas Neue (placar, títulos, balão) + Montserrat 800
(legenda caixa-palavra, pílulas, rodapé). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regras (analise_C.md + violações 3 e 5): clipe em TELA CHEIA o tempo todo (sem janela, moldura ou fundo desfocado),
nada abaixo de 0,9x, nenhum quadro congelado, H só até 6,0 s, G só até 3,5 s, I só 0,5-6,3 s, nenhum brilho na garrafa,
nenhuma gota/água desenhada, texto fora da tampa, do bocal e da mão.
Linha do tempo (s do vídeo final), tudo a 0,9x:
  0,000-2,778   G 0,00-2,50   (céu; topo aberto inclina para a câmera)                      intro
  2,778-8,683   H 0,60-5,915  (mão entra, tampinha abre em ~2,2 s = 4,56 no "dois"; sobe e desce) apresentação
  8,683-9,905   G 2,40-3,50   (volta a ficar em pé; não colado ao G da intro)                   apresentação
  9,905-16,33   I 0,50-6,28   (roxa levantada pela alça; continua da apresentação até o fim)    apresentação + CTA
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]
R_ = 0.9
R = lambda v: str(round(v, 3))

# ---- tempos ----
T_G1, CG1 = 0.0, (0.0, 2.5)
T_H = round(T_G1 + (CG1[1] - CG1[0]) / R_, 3)                       # 2,778
VOZ = {"intro": 0.15, "apresentacao": round(T_H + 0.15, 3)}
pa = falas["apresentacao"]["palavras"]
T_G2 = round(VOZ["apresentacao"] + pa[15]["inicio"], 3)              # corte H->G2 no início de "fabricante"
CH = (0.6, round(0.6 + (T_G2 - T_H) * R_, 3))
assert CH[1] <= 6.0, CH
CG2 = (2.4, 3.5)
T_I = round(T_G2 + (CG2[1] - CG2[0]) / R_, 3)
T_CTA = round(VOZ["apresentacao"] + pa[-1]["fim"] + 0.3, 3)          # fim da apresentação (respiro 0,3)
VOZ["cta"] = round(T_CTA + 0.154, 3)
TOTAL = round(VOZ["cta"] + falas["cta"]["palavras"][-1]["fim"] + 0.3, 2)
CI = (0.5, round(0.5 + (TOTAL - T_I) * R_, 3))
assert CI[1] <= 6.3, CI
DV = {"intro": 2.664, "apresentacao": 9.0, "cta": round(min(4.296, TOTAL - VOZ["cta"]), 3)}
FIM_PARTE = {"intro": T_H, "apresentacao": T_CTA, "cta": TOTAL}
assert VOZ["intro"] + DV["intro"] <= VOZ["apresentacao"] and VOZ["apresentacao"] + DV["apresentacao"] <= VOZ["cta"]


def t_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


def clipe_em(t):
    if t < T_H: return "G1"
    if t < T_G2: return "H"
    if t < T_I: return "G2"
    return "I"


# ---- legenda caixa-palavra ----
GRUPOS = {
    "intro": [[0, 1, 2], [3, 4], [5, 6], [7, 8]],
    "apresentacao": [[0, 1], [2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12], [13, 14], [15], [16, 17], [18, 19],
                     [20, 21]],
    "cta": [[0], [1, 2], [3, 4, 5], [6, 7], [8, 9], [10, 11]],
}
CHAVE = {"intro": {4, 8}, "apresentacao": {3, 8, 10, 16, 19}, "cta": {0, 2, 3, 7}}
EXIBE = {("intro", 8): "direto?", ("apresentacao", 2): "Hilee:", ("apresentacao", 6): "beber,",
         ("apresentacao", 10): "direto,", ("apresentacao", 12): "preferir.", ("apresentacao", 15): "fabricante,",
         ("apresentacao", 21): "limpar.", ("cta", 2): "direto?", ("cta", 11): "vídeo."}
# altura da legenda por clipe: no G a mão ocupa y 1080-1680 e o bocal inclinado desce até ~900 (legenda entre os dois); no H a mão fica à direita em
# y 480-1170 (legenda abaixo); no I a mão fica no alto (a legenda acompanha a do G para não pular). CTA acima do botão.
TOPO = {"G1": 985, "H": 1290, "G2": 985, "I": 985}
TOPO_CTA = 1250

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
            e = min(fim_voz, FIM_PARTE[parte])
        topo = TOPO_CTA if parte == "cta" else TOPO[clipe_em(s + 0.06)]
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.03, 3)
            chave = wi in CHAVE[parte]
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            spans += f'<span id="{gid}-{k}" class="pal{" k" if chave else ""}">{txt}</span>'
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,scale:0.72,y:14}},'
                          f'{{opacity:1,scale:1,y:0,duration:0.13,ease:"back.out(2.4)"}},{t});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{topo}px">{spans}</div></div>')

# ---- marcos da fala ----
T_CANUDO_I, T_DIRETO_I = t_pal("intro", 4), t_pal("intro", 8)
T_GARRAFA, T_HILEE, T_DOIS = t_pal("apresentacao", 0), t_pal("apresentacao", 2), t_pal("apresentacao", 3)
T_CANUDO_A, T_DIRETO_A, T_COMO = t_pal("apresentacao", 8), t_pal("apresentacao", 10), t_pal("apresentacao", 11)
T_SEGUNDO, T_VEDACAO, T_FACIL = t_pal("apresentacao", 13), t_pal("apresentacao", 16), t_pal("apresentacao", 19)
T_CANUDO_C, T_DIRETO_C = t_pal("cta", 0), t_pal("cta", 2)
T_COMENTA, T_SEU, T_TOCA = t_pal("cta", 3), t_pal("cta", 5), t_pal("cta", 7)
T_TOCA0 = round(T_TOCA - 0.03, 3)
T_ABRE = round(T_H + (2.2 - CH[0]) / R_, 3)          # tampinha começa a abrir (H ~2,2 s)
T_SOBE = round(T_H + (2.7 - CH[0]) / R_, 3)          # garrafa sobe e inclina (H 2,7-4,4 s)
T_DESCE = round(T_H + (4.4 - CH[0]) / R_, 3)
T_T2OUT = round(T_SOBE + 0.2, 3)                     # título "2 JEITOS" sai antes de o topo subir até ele
T_PLACAR = round(T_CANUDO_A - 0.12, 3)
T_BOLHA = round(T_COMENTA - 0.1, 3)

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Bebas Placar";src:local("Bebas Neue Regular"),local("Bebas Neue"),local("BebasNeue-Regular")}
@font-face{font-family:"Mont Placar";font-weight:100 900;src:local("Montserrat Thin"),local("Montserrat-Thin"),local("Montserrat")}
:root{--preto:#111214;--verm:#FF3D2E;--creme:#FFF4E4}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#111214}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#111214;font-family:"Mont Placar";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camG1{transform-origin:50% 21%}
#camH{transform-origin:30% 24%}
#camG2{transform-origin:30% 30%}
#camI{transform-origin:50% 40%}
.vinheta{z-index:3;background:radial-gradient(ellipse 100% 72% at 50% 50%,rgba(0,0,0,0) 66%,rgba(17,18,20,.38) 100%)}
.flash{z-index:9;background:#FFFFFF;opacity:0}
.titulo{z-index:6}
/* placar: peças escuras com filete creme; a peça "acesa" vira vermelho-placar */
.tile{display:flex;align-items:center;justify-content:center;background:rgba(17,18,20,.9);color:var(--creme);
  border-radius:14px;box-shadow:inset 0 0 0 3px rgba(255,244,228,.28),0 12px 28px rgba(0,0,0,.45)}
.tile b{display:block;font-family:"Bebas Placar";font-weight:400;white-space:nowrap;letter-spacing:2px;line-height:1;text-align:center}
.vs{display:flex;align-items:center;justify-content:center;width:84px;height:84px;border-radius:50%;background:var(--creme);
  color:var(--preto);font-family:"Bebas Placar";font-size:46px;letter-spacing:1px;box-shadow:0 10px 24px rgba(0,0,0,.45)}
#t1-row{position:absolute;left:40px;top:196px;width:860px;display:flex;align-items:center;justify-content:center;gap:14px}
#c1,#c2{height:150px;padding:0 26px}
#c1 b,#c2 b{font-size:128px;padding-top:10px}
/* kicker e título da apresentação */
#k2{position:absolute;left:40px;top:214px;width:860px;display:flex;justify-content:center}
#k2 span{display:block;white-space:nowrap;background:rgba(17,18,20,.88);color:var(--creme);font-family:"Mont Placar";font-weight:800;
  font-size:44px;letter-spacing:5px;padding:16px 30px 18px;border-radius:12px;box-shadow:inset 0 -5px 0 var(--verm),0 10px 24px rgba(0,0,0,.4)}
#t2-row{position:absolute;left:40px;top:196px;width:860px;display:flex;justify-content:center;gap:12px;perspective:900px}
#t2a,#t2b{height:130px;padding:0 26px}
#t2a{background:var(--verm);color:#FFFFFF;box-shadow:0 12px 28px rgba(0,0,0,.45)}
#t2a b,#t2b b{font-size:108px;padding-top:8px}
/* placar lateral (à esquerda da garrafa e da alça; x 30-256, y 600-866) */
#pl{position:absolute;left:30px;top:600px;width:226px;perspective:800px}
#pl .tile{position:relative;width:226px;height:126px;margin-bottom:14px}
#pl .tile b{position:absolute;left:0;right:0;top:50%;transform:translateY(-46%)}
.um{font-size:76px}
.dois{font-size:50px;line-height:1.02 !important}
/* balão de comentário da CTA (mesma coluna do placar) */
#bolha{position:absolute;left:30px;top:800px;display:block;background:var(--verm);border-radius:22px;padding:18px 34px 14px;
  box-shadow:0 14px 30px rgba(0,0,0,.45)}
#bolha b{display:block;font-family:"Bebas Placar";font-weight:400;font-size:92px;line-height:.98;white-space:nowrap;color:#FFFFFF;letter-spacing:2px}
#bolha i{position:absolute;left:44px;bottom:-34px;width:58px;height:40px;display:block;background:var(--verm);clip-path:polygon(0 0,100% 0,0 100%)}
/* rodapé de dado do fabricante */
#rod{z-index:6}
#rod span{position:absolute;left:44px;top:1468px;display:block;font-family:"Mont Placar";font-weight:600;font-size:30px;
  color:rgba(255,255,255,.82);text-shadow:0 2px 8px rgba(0,0,0,.75)}
/* legenda caixa-palavra */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:center;gap:12px;flex-wrap:nowrap}
.pal{display:block;font-family:"Mont Placar";font-weight:800;font-size:68px;line-height:1;white-space:nowrap;color:var(--creme);
  background:rgba(17,18,20,.9);padding:14px 22px 18px;border-radius:12px;box-shadow:0 10px 22px rgba(0,0,0,.4)}
.pal.k{background:var(--verm);color:#FFFFFF}
/* CTA: botão com seta para baixo/esquerda + "toca no produto" */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border-radius:50%;background:var(--verm);
  box-shadow:0 0 0 6px rgba(17,18,20,.92),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:116px;height:116px}
#tq-o{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border:7px solid var(--verm);border-radius:50%;opacity:0}
#tq-l{position:absolute;left:196px;top:1428px;display:block;white-space:nowrap;background:rgba(17,18,20,.9);color:var(--creme);
  font-family:"Mont Placar";font-weight:800;font-size:42px;line-height:1;padding:18px 30px 20px;border-radius:40px;
  box-shadow:inset 0 0 0 3px var(--verm),0 10px 24px rgba(0,0,0,.4)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: G 0-2,5 s a 0,9x (topo aberto inclina para a câmera contra o céu) -->
  <div id="camG1" class="cam"><video id="vG1" class="clip full" data-start="0" data-duration="%%D_G1%%" data-media-start="0" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: H 0,6-5,915 s (tampinha abre no "dois"), G 2,4-3,5 s, I 0,5 s em diante (segue na CTA) -->
  <div id="camH" class="cam"><video id="vH" class="clip full" data-start="%%T_H%%" data-duration="%%D_H%%" data-media-start="%%CH0%%" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_H.mp4" muted playsinline></video></div>
  <div id="camG2" class="cam"><video id="vG2" class="clip full" data-start="%%T_G2%%" data-duration="%%D_G2%%" data-media-start="%%CG20%%" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <div id="camI" class="cam"><video id="vI" class="clip full" data-start="%%T_I%%" data-duration="%%D_I%%" data-media-start="%%CI0%%" data-playback-rate="0.9" data-track-index="1" src="assets/clipe_I.mp4" muted playsinline></video></div>

  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="5"></div>

  <!-- intro: placar "CANUDO (OU) DIRETO?" já no quadro 0, acima da tampa; acende a peça dita -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="%%T_H%%" data-track-index="6">
    <div id="t1-row"><span id="c1" class="tile"><b>CANUDO</b></span><span id="vs1" class="vs">OU</span><span id="c2" class="tile"><b>DIRETO?</b></span></div>
  </div>

  <!-- apresentação: kicker "GARRAFA TÉRMICA HILEE" e depois "2 JEITOS DE BEBER" (sai antes de a garrafa subir) -->
  <div id="k2w" class="clip titulo" data-start="%%T_K2%%" data-duration="%%D_K2%%" data-track-index="7">
    <div id="k2"><span id="k2s">GARRAFA TÉRMICA HILEE</span></div>
  </div>
  <div id="t2" class="clip titulo" data-start="%%T_T2%%" data-duration="%%D_T2%%" data-track-index="8">
    <div id="t2-row"><span id="t2a" class="tile"><b>2 JEITOS</b></span><span id="t2b" class="tile"><b>DE BEBER</b></span></div>
  </div>

  <!-- placar lateral: CANUDO | DIRETO -> VEDAÇÃO TOTAL* / FÁCIL DE LIMPAR* -> CANUDO | DIRETO (CTA) -->
  <div id="plw" class="clip titulo" data-start="%%T_PL%%" data-duration="%%D_PL%%" data-track-index="9">
    <div id="pl">
      <span id="p1" class="tile"><b id="p1a" class="um">CANUDO</b><b id="p1b" class="dois" style="opacity:0">VEDAÇÃO<br>TOTAL*</b></span>
      <span id="p2" class="tile"><b id="p2a" class="um">DIRETO</b><b id="p2b" class="dois" style="opacity:0">FÁCIL DE<br>LIMPAR*</b></span>
    </div>
  </div>

  <div id="rod" class="clip" data-start="%%T_H%%" data-duration="%%D_ROD%%" data-track-index="10"><span id="rod-s">*Dados do fabricante</span></div>

  <!-- CTA: balão "COMENTA O SEU" (antes do toque) + botão com seta para baixo/esquerda em "toca" -->
  <div id="t3" class="clip titulo" data-start="%%T_BOLHA%%" data-duration="%%D_BOLHA%%" data-track-index="7">
    <span id="bolha"><b>COMENTA<br>O SEU</b><i></i></span>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="10">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#FFF4E4" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <span id="tq-l">toca no produto</span>
  </div>

  <div id="fl2" class="clip flash" data-start="%%T_FL2%%" data-duration="0.12" data-track-index="11"></div>
  <div id="fl3" class="clip flash" data-start="%%T_FL3%%" data-duration="0.12" data-track-index="11"></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="%%V1%%" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="%%V2%%" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="%%V3%%" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.32" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="%%SWH1%%" data-duration="0.3" data-track-index="15" data-volume="0.38" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%SPOP1%%" data-duration="0.09" data-track-index="14" data-volume="0.36" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="14" data-volume="0.36" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whoosh-2" data-start="%%SWH2%%" data-duration="0.3" data-track-index="15" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-3" data-start="%%STIQ3%%" data-duration="0.03" data-track-index="14" data-volume="0.36" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="%%SSUB%%" data-duration="0.5" data-media-start="0.9" data-track-index="15" data-volume="0.32" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-pop-2" data-start="%%SPOP2%%" data-duration="0.09" data-track-index="14" data-volume="0.36" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });
const V = "#FF3D2E", P = "rgba(17,18,20,0.9)", C = "#FFF4E4";

// ---- INTRO (G): punch-in + tremor no quadro 0, sem flash (o quadro 0 é a capa: garrafa e pergunta limpas) ----
tl.fromTo("#camG1", {scale:1.13}, {scale:1.03, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camG1", {scale:1.045, duration:%%DG1A%%, ease:"none"}, 0.4);
tl.fromTo("#camG1", {x:0, y:0}, {keyframes:[{x:14, y:-8, duration:0.05}, {x:-11, y:6, duration:0.06}, {x:7, y:-4, duration:0.06}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, 0.02);
tl.fromTo("#t1-row", {scale:1.07, transformOrigin:"50% 50%"}, {scale:1, duration:0.3, ease:"back.out(2.2)"}, 0);
tl.fromTo("#vs1", {scale:1}, {scale:1.25, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, 0.1);
// "canudo": peça 1 acende + punch
tl.to("#c1", {backgroundColor:V, color:"#FFFFFF", scale:1.06, duration:0.12, ease:"power2.out"}, %%TC1%%);
tl.to("#c1", {scale:1, duration:0.25, ease:"power2.out"}, %%TC1B%%);
tl.to("#camG1", {scale:1.085, duration:0.12, ease:"power2.out"}, %%TC1%%);
tl.to("#camG1", {scale:1.06, duration:0.45, ease:"power2.inOut"}, %%TC1B%%);
tl.to("#camG1", {scale:1.07, duration:%%DG1B%%, ease:"none"}, %%TC1C%%);
// "direto": peça 2 acende, a 1 apaga + punch
tl.to("#c1", {backgroundColor:P, color:C, duration:0.12, ease:"none"}, %%TC2%%);
tl.to("#c2", {backgroundColor:V, color:"#FFFFFF", scale:1.06, duration:0.12, ease:"power2.out"}, %%TC2%%);
tl.to("#c2", {scale:1, duration:0.25, ease:"power2.out"}, %%TC2B%%);
tl.to("#camG1", {scale:1.1, duration:0.12, ease:"power2.out"}, %%TC2%%);
tl.to("#camG1", {scale:1.08, duration:%%DG1C%%, ease:"power1.out"}, %%TC2B%%);
// saída para o H: zoom com desfoque + flash curto
tl.to("#camG1", {scale:1.2, filter:"blur(16px)", duration:0.16, ease:"power2.in"}, %%T_OUT1%%);
tl.to("#t1-row", {scale:1.2, opacity:0, filter:"blur(10px)", duration:0.16, ease:"power2.in"}, %%T_OUT1%%);
tl.fromTo("#fl2", {opacity:0}, {keyframes:[{opacity:0.4, duration:0.03}, {opacity:0, duration:0.08}], ease:"none"}, %%T_FL2%%);

// ---- APRESENTAÇÃO, H: entra do desfoque; punch na tampinha abrindo ("dois"); câmera fecha no topo enquanto ele sobe ----
tl.fromTo("#camH", {scale:1.18, filter:"blur(16px)"}, {scale:1.02, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%T_H%%);
tl.to("#camH", {scale:1.04, duration:%%DH1%%, ease:"none"}, %%T_H3%%);
tl.to("#camH", {scale:1.1, duration:0.2, ease:"power2.out"}, %%T_DOIS%%);
tl.to("#camH", {scale:1.16, duration:%%DH2%%, ease:"sine.inOut"}, %%T_DOIS2%%);
tl.to("#camH", {scale:1.06, duration:0.5, ease:"power2.inOut"}, %%T_COMO%%);
tl.to("#camH", {scale:1.08, duration:%%DH3%%, ease:"none"}, %%T_COMO2%%);
tl.fromTo("#k2s", {clipPath:"inset(0% 100% 0% 0% round 12px)"}, {clipPath:"inset(0% 0% 0% 0% round 12px)", duration:0.3, ease:"power3.out"}, %%T_K2%%);
tl.to("#k2s", {y:-30, opacity:0, duration:0.14, ease:"power2.in"}, %%T_K2OUT%%);
// "2 JEITOS DE BEBER" vira como placa de placar
tl.fromTo("#t2a", {rotationX:-95, transformOrigin:"50% 0%"}, {rotationX:0, duration:0.34, ease:"back.out(1.8)"}, %%T_T2%%);
tl.fromTo("#t2b", {rotationX:-95, transformOrigin:"50% 0%"}, {rotationX:0, duration:0.34, ease:"back.out(1.8)"}, %%T_T2B%%);
tl.to("#t2-row", {y:-60, opacity:0, duration:0.18, ease:"power2.in"}, %%T_T2OUT%%);
// placar lateral: entra em "canudo"; acende a peça dita; "como preferir" acende as duas
tl.fromTo("#p1", {x:-320}, {x:0, duration:0.3, ease:"power3.out"}, %%T_PL%%);
tl.fromTo("#p2", {x:-320}, {x:0, duration:0.3, ease:"power3.out"}, %%T_PL2%%);
tl.to("#p1", {backgroundColor:V, color:"#FFFFFF", duration:0.1, ease:"none"}, %%TCA%%);
tl.fromTo("#p1", {scale:1}, {scale:1.08, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TCA%%);
tl.to("#p1", {backgroundColor:P, color:C, duration:0.1, ease:"none"}, %%TDA%%);
tl.to("#p2", {backgroundColor:V, color:"#FFFFFF", duration:0.1, ease:"none"}, %%TDA%%);
tl.fromTo("#p2", {scale:1}, {scale:1.08, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TDA%%);
tl.to("#p1", {backgroundColor:V, color:"#FFFFFF", duration:0.1, ease:"none"}, %%TCOMO%%);
tl.to(["#p1", "#p2"], {backgroundColor:P, color:C, duration:0.15, ease:"none"}, %%TSEG%%);
// rodapé: entra com a parte e pulsa em "segundo o fabricante"
tl.fromTo("#rod-s", {opacity:0}, {opacity:1, duration:0.25, ease:"none"}, %%T_H%%);
tl.fromTo("#rod-s", {scale:1, transformOrigin:"0% 50%"}, {scale:1.12, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TSEG%%);

// ---- G2: corte seco com flash; câmera leve (sem invadir a alça do lado esquerdo) ----
tl.fromTo("#fl3", {opacity:0}, {keyframes:[{opacity:0.35, duration:0.03}, {opacity:0, duration:0.08}], ease:"none"}, %%T_FL3%%);
tl.fromTo("#camG2", {scale:1.1}, {scale:1.03, duration:0.28, ease:"power3.out"}, %%T_G2%%);
tl.to("#camG2", {scale:1.055, duration:%%DG2%%, ease:"none"}, %%T_G2B%%);
// "vedação": peça 1 vira VEDAÇÃO TOTAL* (placa de placar)
tl.to("#p1", {rotationX:90, duration:0.09, ease:"power2.in"}, %%TV0%%);
tl.set("#p1a", {opacity:0}, %%TV%%);
tl.set("#p1b", {opacity:1}, %%TV%%);
tl.set("#p1", {backgroundColor:V, color:"#FFFFFF"}, %%TV%%);
tl.fromTo("#p1", {rotationX:-90}, {rotationX:0, duration:0.2, ease:"back.out(2)", immediateRender:false}, %%TV%%);

// ---- I: entra num corte com punch; "fácil de limpar" vira a peça 2 ----
tl.fromTo("#camI", {scale:1.1}, {scale:1.02, duration:0.3, ease:"power3.out"}, %%T_I%%);
tl.to("#camI", {scale:1.045, duration:%%DI1%%, ease:"none"}, %%T_I2%%);
tl.to("#p2", {rotationX:90, duration:0.09, ease:"power2.in"}, %%TF0%%);
tl.set("#p2a", {opacity:0}, %%TF%%);
tl.set("#p2b", {opacity:1}, %%TF%%);
tl.set("#p2", {backgroundColor:V, color:"#FFFFFF"}, %%TF%%);
tl.fromTo("#p2", {rotationX:-90}, {rotationX:0, duration:0.2, ease:"back.out(2)", immediateRender:false}, %%TF%%);
tl.to("#rod-s", {opacity:0, duration:0.15, ease:"none"}, %%T_RODOUT%%);

// ---- CTA: passagem em zoom (subida termina aqui); placar volta para CANUDO | DIRETO; balão; toque ----
tl.to("#camI", {scale:1.11, filter:"blur(6px)", duration:0.13, ease:"power2.in"}, %%T_CTA0%%);
tl.to("#camI", {scale:1.04, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%T_CTA1%%);
tl.to("#camI", {scale:1.06, duration:%%DI2%%, ease:"none"}, %%T_CTA2%%);
tl.to(["#p1", "#p2"], {rotationX:90, duration:0.09, ease:"power2.in", stagger:0.05}, %%TR0%%);
tl.set(["#p1b", "#p2b"], {opacity:0}, %%TR%%);
tl.set(["#p1a", "#p2a"], {opacity:1}, %%TR%%);
tl.set(["#p1", "#p2"], {backgroundColor:P, color:C}, %%TR%%);
tl.fromTo(["#p1", "#p2"], {rotationX:-90}, {rotationX:0, duration:0.2, ease:"back.out(2)", stagger:0.05, immediateRender:false}, %%TR%%);
tl.to("#p1", {backgroundColor:V, color:"#FFFFFF", duration:0.1, ease:"none"}, %%TCC%%);
tl.to("#p1", {backgroundColor:P, color:C, duration:0.1, ease:"none"}, %%TDC%%);
tl.to("#p2", {backgroundColor:V, color:"#FFFFFF", duration:0.1, ease:"none"}, %%TDC%%);
tl.to("#pl", {x:-340, opacity:0, duration:0.16, ease:"power2.in"}, %%T_PLOUT%%);
tl.fromTo("#bolha", {scale:0.3, opacity:0, transformOrigin:"12% 100%"}, {scale:1, opacity:1, duration:0.55, ease:"elastic.out(1,0.55)"}, %%T_BOLHA%%);
tl.fromTo("#bolha", {rotation:0}, {keyframes:[{rotation:-3, duration:0.08}, {rotation:3, duration:0.12}, {rotation:0, duration:0.1}], ease:"none", immediateRender:false}, %%TSEU%%);
tl.to("#camI", {scale:1.08, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camI", {scale:1.09, duration:%%DI3%%, ease:"none"}, %%TTOCA2%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#tq-l", {clipPath:"inset(0% 100% 0% 0% round 40px)"}, {clipPath:"inset(0% 0% 0% 0% round 40px)", duration:0.28, ease:"power3.out"}, %%TTOCA1%%);
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

T_OUT1 = round(T_H - 0.16, 3)
TC1, TC2 = round(T_CANUDO_I - 0.03, 3), round(T_DIRETO_I - 0.03, 3)
T_K2 = round(T_GARRAFA - 0.02, 3)
T_T2 = round(T_DOIS - 0.04, 3)
T_K2OUT = round(T_T2 - 0.14, 3)
T_PL = T_PLACAR
T_PLOUT = round(T_BOLHA - 0.12, 3)
TCA, TDA, TCOMO = round(T_CANUDO_A - 0.03, 3), round(T_DIRETO_A - 0.03, 3), round(T_COMO - 0.03, 3)
TSEG = round(T_SEGUNDO - 0.03, 3)
TV, TF = round(T_VEDACAO - 0.02, 3), round(T_FACIL - 0.02, 3)
T_CTA0 = round(T_CTA - 0.1, 3)
TR = round(T_CTA + 0.02, 3)
TCC, TDC = round(T_CANUDO_C - 0.03, 3), round(T_DIRETO_C - 0.03, 3)
TPULSO = round(T_TOCA0 + 0.3, 3)
REP = int(((TOTAL - 0.05) - TPULSO) / 0.22) - 1
REP -= (REP + 1) % 2 == 1

assert T_T2OUT < T_PL and T_K2OUT > T_K2 + 0.4
assert TCOMO + 0.3 < TSEG < T_G2 < TV < T_I < TF < T_CTA0
assert T_PLOUT > TDC + 0.3

subs = {
    "TOTAL": str(TOTAL),
    "D_G1": R(T_H), "T_H": R(T_H), "D_H": R(T_G2 - T_H), "CH0": R(CH[0]),
    "T_G2": R(T_G2), "D_G2": R(T_I - T_G2), "CG20": R(CG2[0]),
    "T_I": R(T_I), "D_I": R(TOTAL - T_I), "CI0": R(CI[0]),
    "DG1A": R(TC1 - 0.4 - 0.003), "TC1": R(TC1), "TC1B": R(TC1 + 0.12), "TC1C": R(TC1 + 0.57),
    "DG1B": R(TC2 - (TC1 + 0.57) - 0.003), "TC2": R(TC2), "TC2B": R(TC2 + 0.12),
    "DG1C": R(T_OUT1 - (TC2 + 0.12) - 0.003), "T_OUT1": R(T_OUT1), "T_FL2": R(T_H - 0.02),
    "T_H3": R(T_H + 0.3), "DH1": R(T_T2 - (T_H + 0.3) - 0.003),
    "T_DOIS": R(T_T2), "T_DOIS2": R(T_T2 + 0.2), "DH2": R(TCOMO - (T_T2 + 0.2) - 0.003),
    "T_COMO": R(TCOMO), "T_COMO2": R(TCOMO + 0.5), "DH3": R(T_G2 - (TCOMO + 0.5) - 0.003),
    "T_K2": R(T_K2), "D_K2": R(T_K2OUT + 0.16 - T_K2), "T_K2OUT": R(T_K2OUT),
    "T_T2": R(T_T2), "T_T2B": R(T_T2 + 0.1), "D_T2": R(T_T2OUT + 0.2 - T_T2), "T_T2OUT": R(T_T2OUT),
    "T_PL": R(T_PL), "T_PL2": R(T_PL + 0.08), "D_PL": R(T_PLOUT + 0.18 - T_PL),
    "TCA": R(TCA), "TDA": R(TDA), "TCOMO": R(TCOMO), "TSEG": R(TSEG),
    "D_ROD": R(T_CTA - T_H), "T_RODOUT": R(T_CTA - 0.15),
    "T_FL3": R(T_G2 - 0.02), "T_G2B": R(T_G2 + 0.28), "DG2": R(T_I - (T_G2 + 0.28) - 0.003),
    "TV0": R(TV - 0.09), "TV": R(TV),
    "T_I2": R(T_I + 0.3), "DI1": R(T_CTA0 - (T_I + 0.3) - 0.003), "TF0": R(TF - 0.09), "TF": R(TF),
    "T_CTA0": R(T_CTA0), "T_CTA1": R(T_CTA0 + 0.13), "T_CTA2": R(T_CTA0 + 0.43),
    "DI2": R(T_TOCA0 - (T_CTA0 + 0.43) - 0.003),
    "TR0": R(TR - 0.09), "TR": R(TR), "TCC": R(TCC), "TDC": R(TDC), "T_PLOUT": R(T_PLOUT),
    "T_BOLHA": R(T_BOLHA), "D_BOLHA": R(TOTAL - T_BOLHA), "TSEU": R(T_SEU),
    "TTOCA": R(T_TOCA0), "TTOCA1": R(T_TOCA0 + 0.08), "TTOCA2": R(T_TOCA0 + 0.24),
    "DI3": R(TOTAL - (T_TOCA0 + 0.24)), "DTOCA": R(TOTAL - T_TOCA0),
    "TPULSO": R(TPULSO), "REP": str(REP), "TONDA2": R(T_TOCA0 + 0.95),
    "V1": R(VOZ["intro"]), "V2": R(VOZ["apresentacao"]), "V3": R(VOZ["cta"]),
    "DV1": R(DV["intro"]), "DV2": R(DV["apresentacao"]), "DV3": R(DV["cta"]),
    # sons: no máximo ~1 a cada 1,5 s, nunca em cima da palavra-chave
    "STIQ1": R(T_DIRETO_I - 0.2), "SWH1": R(T_H - 0.1), "SPOP1": R(T_DOIS - 0.12),
    "STIQ2": R(T_CANUDO_A - 0.14), "SWH2": R(T_G2 - 0.08), "STIQ3": R(T_FACIL - 0.1),
    "SSUB": R(T_CTA - 0.5), "SPOP2": R(T_COMENTA - 0.13),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
open(OUT, "w").write(html)
print("ok", OUT, "| total", TOTAL, "| H", T_H, CH, "| G2", T_G2, CG2, "| I", T_I, CI,
      "| tampa abre", T_ABRE, "dois", T_DOIS, "sobe", T_SOBE, "desce", T_DESCE,
      "| vedação", T_VEDACAO, "fácil", T_FACIL, "| CTA", T_CTA, "voz", VOZ["cta"], "comenta", T_COMENTA, "toca", T_TOCA0)
