#!/usr/bin/env python3
"""Gera produtos/bodysplash/edicao_F/index.html ("manual de uso": tinta-petróleo / gelo / água / laranja-sinal,
Archivo Black + Montserrat 800, legenda "etiqueta técnica"). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida>

Lote F ("Tá borrifando certo?"), clipes G/H/I com mão. Regra da 3ª violação: o vídeo roda do primeiro ao último
quadro; não há <img>, quadro congelado nem cartão. Trechos (analise_F.md):
  intro         G 0,00-4,00 s em 1,0x  (mão aperta a válvula do Enigma)
  apresentação  H 0,00-1,96 s em 0,8x  (mão desce até a válvula do Barbarius; PROIBIDO H 2,1-4,9 s)
                G 4,00-7,96 s em 0,8x  (nuvem de vapor; punch na válvula do Enigma sem tampa)
                H 5,00-7,85 s em 0,95x (mão já saiu, cortina)
  CTA           I 1,40-6,80 s em 1,0x  (mão escolhe e apoia os dedos na tampa do Midtown)
Texto só acima das tampas (y < 530): os rótulos (y ~920-1600) nunca ficam sob texto nem sob efeito translúcido.
Transições: painel opaco de bordas duras (cobre a tela inteira por um instante, nunca tinge).
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

TOTAL = 19.8
P = {"intro": (0.0, 4.0, 0.25), "apresentacao": (4.0, 14.4, 4.2), "cta": (14.4, TOTAL, 14.7)}
DUR_MP3 = {"intro": 3.75, "apresentacao": 10.128, "cta": 4.992}
T_HG, T_GH = 6.45, 11.4  # cortes dentro da apresentação
VALV = (243, 748)       # válvula do Enigma (G), centro do alvo e origem do zoom
LEG_TOP = 456

GRUPOS = {
    "intro": [[0, 1], [2, 3], [4, 5, 6], [7, 8], [9, 10]],
    "apresentacao": [[0, 1, 2], [3, 4, 5], [6, 7], [8, 9], [10, 11, 12], [13], [14, 15], [16, 17], [18, 19],
                     [20], [21, 22], [23, 24], [25, 26]],
    "cta": [[0, 1], [2, 3, 4], [5], [6, 7, 8], [9], [10, 11], [12, 13]],
}
CHAVE = {"intro": {1, 6, 9}, "apresentacao": {6, 9, 12, 13, 15, 19, 20, 22}, "cta": {4, 6, 13}}
EXIBE = {("intro", 6): "certo,", ("intro", 10): "jeito?", ("apresentacao", 2): "Man:",
         ("apresentacao", 5): "fabricante,", ("apresentacao", 9): "pele,", ("apresentacao", 13): "centímetros,",
         ("apresentacao", 19): "revelar.", ("apresentacao", 20): "Leve,", ("apresentacao", 26): "dia.",
         ("cta", 5): "começar.", ("cta", 13): "perto."}


def T(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


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
            e = min(fim_voz, P[parte][1] - 0.1)
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.03, 3)
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            if wi in CHAVE[parte]:
                spans += f'<span id="{gid}-{k}" class="pal k"><i id="{gid}-{k}b" class="kb"></i><em class="tx">{txt}</em></span>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}b",{{scaleX:0}},{{scaleX:1,duration:0.14,ease:"power3.out"}},{t});')
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.1,ease:"power2.out"}},{t});')
            else:
                spans += f'<span id="{gid}-{k}" class="pal"><em class="tx">{txt}</em></span>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.12,ease:"power2.out"}},{t});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
                        f'data-track-index="12"><div class="cap" style="top:{LEG_TOP}px">{spans}</div></div>')

# tempos-chave
t_pele, t_na = T("apresentacao", 9), T("apresentacao", 8)
t_uns, t_quinze, t_cm_fim = T("apresentacao", 11), T("apresentacao", 12), round(P["apresentacao"][2] + falas["apresentacao"]["palavras"][13]["fim"], 3)
t_e, t_espere = T("apresentacao", 14), T("apresentacao", 15)
t_leve, t_reap, t_dia = T("apresentacao", 20), T("apresentacao", 22), T("apresentacao", 26)
t_certo, t_ou = T("intro", 6), T("intro", 7)
t_toca, t_conf, t_perto = T("cta", 6), T("cta", 11), T("cta", 13)
t_tres = T("cta", 4)

VX, VY = VALV
html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
:root{--tinta:#0C2430;--gelo:#F2FAFC;--agua:#7FD8F0;--sinal:#FF4F2E}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0C2430}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0C2430;font-family:"Montserrat";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camG1,#camG2{transform-origin:%%VX%%px %%VY%%px}
#camH1,#camH2,#camI{transform-origin:50% 30%}
/* papel milimetrado só na faixa do alto (acima das tampas) */
#grade{z-index:2;height:540px;bottom:auto;opacity:.55;
  background-image:repeating-linear-gradient(0deg,rgba(12,36,48,.10) 0 2px,transparent 2px 60px),repeating-linear-gradient(90deg,rgba(12,36,48,.10) 0 2px,transparent 2px 60px);
  -webkit-mask-image:linear-gradient(to bottom,#000 0,#000 60%,transparent 100%);mask-image:linear-gradient(to bottom,#000 0,#000 60%,transparent 100%)}
.flash{z-index:20;background:#F2FAFC;opacity:0}
/* títulos: tinta com contorno gelo, alinhados à esquerda como num manual */
.titulo{z-index:6}
.ln{position:absolute;left:44px;width:880px;height:118px;overflow:hidden;display:flex;align-items:center;gap:18px;padding-left:12px}
.tt{display:block;font-family:"Archivo Black";font-size:96px;line-height:1;white-space:nowrap;color:var(--tinta);
  -webkit-text-stroke:14px var(--gelo);paint-order:stroke fill;letter-spacing:-1px}
.tt .s{color:var(--sinal);-webkit-text-stroke:14px var(--tinta)}
.chip{position:relative;flex:0 0 76px;width:76px;height:76px;display:block;border-radius:50%;background:var(--gelo);
  box-shadow:inset 0 0 0 6px var(--tinta),0 4px 12px rgba(12,36,48,.25)}
.chip b,.chip i{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;border-radius:50%;
  font-family:"Archivo Black";font-weight:400;font-style:normal;font-size:42px;line-height:1}
.chip b{color:var(--tinta)}
.chip i{background:var(--sinal);color:var(--gelo);box-shadow:inset 0 0 0 6px var(--tinta);transform:scale(0)}
/* régua 0-15 */
#regua{position:absolute;left:150px;top:404px;width:720px;height:48px;display:block;filter:drop-shadow(0 0 2px #F2FAFC) drop-shadow(0 0 2px #F2FAFC)}
#rg-l{position:absolute;left:0;top:30px;width:540px;height:6px;display:block;background:var(--tinta)}
#rg-t{position:absolute;left:0;top:14px;width:544px;height:16px;display:block;
  background:repeating-linear-gradient(90deg,var(--tinta) 0 4px,transparent 4px 36px)}
#rg-0,#rg-15{position:absolute;top:0;width:6px;height:36px;display:block;background:var(--sinal)}
#rg-0{left:0}#rg-15{left:536px}
#rg-n{position:absolute;left:560px;top:4px;display:block;font-size:36px;line-height:1;color:var(--sinal);white-space:nowrap}
/* linha de passo (3) e linha da CTA */
.passo{position:absolute;left:56px;top:400px;display:flex;align-items:center;gap:14px}
.passo .chip{flex-basis:52px;width:52px;height:52px;box-shadow:inset 0 0 0 5px var(--tinta)}
.passo .chip b,.passo .chip i{font-size:28px}
.passo .chip i{box-shadow:inset 0 0 0 5px var(--tinta);transform:scale(1)}
.pt{display:block;font-size:38px;line-height:1;white-space:nowrap;color:var(--tinta);-webkit-text-stroke:8px var(--gelo);paint-order:stroke fill}
.pt .s{display:inline-block;color:var(--gelo);-webkit-text-stroke:0;background:var(--sinal);padding:4px 10px 6px;border-radius:6px;box-shadow:0 0 0 3px var(--gelo)}
/* rodapé ao lado do asterisco */
#rodape{z-index:7}
#rd{position:absolute;left:748px;top:300px;display:block;font-family:"Montserrat";font-weight:700;font-size:28px;line-height:1.15;
  color:var(--tinta);-webkit-text-stroke:6px rgba(242,250,252,.92);paint-order:stroke fill}
/* alvo na válvula (intro) */
#alvo{z-index:5}
#av{position:absolute;left:%%AVL%%px;top:%%AVT%%px;width:170px;height:170px;display:block}
#av-c{position:absolute;inset:0;display:block;border-radius:50%;border:6px solid var(--sinal);box-shadow:0 0 0 3px rgba(242,250,252,.85),inset 0 0 0 3px rgba(242,250,252,.85)}
.avt{position:absolute;display:block;background:var(--sinal);box-shadow:0 0 0 2px rgba(242,250,252,.85)}
/* transições: painel opaco de bordas duras com régua na borda de ataque */
.wipe{z-index:18;overflow:hidden}
#wp1{position:absolute;left:0;top:0;width:1120px;height:1920px;display:block;background:var(--tinta);
  border-right:14px solid var(--sinal)}
#wp1 i{position:absolute;right:0;top:0;width:60px;height:1920px;display:block;
  background:repeating-linear-gradient(0deg,var(--agua) 0 4px,transparent 4px 40px)}
#wp2{position:absolute;left:0;top:0;width:1080px;height:1960px;display:block;background:var(--tinta);
  border-top:14px solid var(--sinal)}
#wp2 i{position:absolute;left:0;top:0;width:1080px;height:60px;display:block;
  background:repeating-linear-gradient(90deg,var(--agua) 0 4px,transparent 4px 40px)}
/* CTA: linha de chamada descendo pela margem esquerda até o produto marcado */
#guia{z-index:8}
#gd-l{position:absolute;left:24px;top:468px;width:8px;height:1040px;display:block;transform-origin:50% 0;
  background:repeating-linear-gradient(180deg,var(--sinal) 0 26px,transparent 26px 40px);box-shadow:0 0 0 2px rgba(242,250,252,.6)}
#gd-s{position:absolute;left:0;top:1484px;width:56px;height:56px;display:block}
#gd-o{position:absolute;left:-2px;top:1482px;width:60px;height:60px;display:block;border:6px solid var(--sinal);border-radius:50%;opacity:0}
/* brilho nas tampas (faixa y 540-880, acima dos rótulos) */
#brilho{z-index:3}
#br-m{position:absolute;left:0;top:540px;width:1080px;height:340px;overflow:hidden;display:block}
#br-b{position:absolute;left:0;top:-300px;width:240px;height:940px;display:block;
  background:linear-gradient(to right,rgba(255,255,255,0) 0,rgba(255,255,255,.7) 50%,rgba(255,255,255,0) 100%)}
/* legenda "etiqueta técnica" */
.legenda{z-index:9}
.cap{position:absolute;left:56px;width:862px;display:flex;justify-content:flex-start;align-items:flex-start;gap:16px;flex-wrap:nowrap}
.pal{position:relative;display:block;font-family:"Montserrat";font-weight:800;font-size:60px;line-height:1.1;white-space:nowrap}
.tx{position:relative;display:block;font-style:normal;color:var(--tinta);-webkit-text-stroke:11px var(--gelo);paint-order:stroke fill}
.pal.k{padding:0 14px}
.pal.k .tx{color:var(--gelo);-webkit-text-stroke:0}
.kb{position:absolute;left:0;top:4px;right:0;bottom:2px;display:block;background:var(--sinal);border-radius:8px;transform-origin:0 50%;
  box-shadow:0 0 0 4px var(--gelo),0 6px 14px rgba(12,36,48,.3)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO 0-4,0: G 0-4,0 (mão aperta a válvula do Enigma) -->
  <div id="camG1" class="cam"><video id="vG1" class="clip full" data-start="0" data-duration="4" data-media-start="0" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO 4,0-14,4: H 0-1,96 (0,8x) | G 4,0-7,96 (0,8x) | H 5,0-7,85 (0,95x). H 2,1-4,9 nunca entra. -->
  <div id="camH1" class="cam"><video id="vH1" class="clip full" data-start="4" data-duration="2.45" data-media-start="0" data-playback-rate="0.8" data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video></div>
  <div id="camG2" class="cam"><video id="vG2" class="clip full" data-start="6.45" data-duration="4.95" data-media-start="4" data-playback-rate="0.8" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <div id="camH2" class="cam"><video id="vH2" class="clip full" data-start="11.4" data-duration="3" data-media-start="5" data-playback-rate="0.95" data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video></div>
  <!-- CTA 14,4-19,8: I 1,4-6,8 -->
  <div id="camI" class="cam"><video id="vI" class="clip full" data-start="14.4" data-duration="5.4" data-media-start="1.4" data-track-index="0" src="assets/clipe_I.mp4" muted playsinline></video></div>

  <div id="grade" class="clip" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"></div>
  <div id="brilho" class="clip" data-start="%%TCONF%%" data-duration="0.9" data-track-index="3"><span id="br-m"><i id="br-b"></i></span></div>

  <!-- intro: alvo na válvula + BORRIFA / CERTO? -->
  <div id="alvo" class="clip" data-start="0.9" data-duration="2.7" data-track-index="4"><span id="av"><i id="av-c"></i>
    <i class="avt" style="left:82px;top:-26px;width:6px;height:34px"></i><i class="avt" style="left:82px;top:162px;width:6px;height:34px"></i>
    <i class="avt" style="left:-26px;top:82px;width:34px;height:6px"></i><i class="avt" style="left:162px;top:82px;width:34px;height:6px"></i></span></div>
  <div id="t1" class="clip titulo" data-start="0" data-duration="3.96" data-track-index="6">
    <div class="ln" style="top:190px"><div id="t1-a" class="tt">BORRIFA</div></div>
    <div class="ln" style="top:290px"><div id="t1-b" class="tt"><span class="s">CERTO?</span></div></div>
  </div>

  <!-- apresentação: 1 NA PELE, / 2 A 15 CM* + régua; passo 3 = linha do roteiro -->
  <div id="t2" class="clip titulo" data-start="4" data-duration="10.36" data-track-index="7">
    <div class="ln" style="top:190px"><span id="c1" class="chip"><b data-layout-allow-occlusion data-layout-allow-overlap>1</b><i id="c1f">1</i></span><div id="t2-a" class="tt">NA PELE,</div></div>
    <div class="ln" style="top:290px"><span id="c2" class="chip"><b data-layout-allow-occlusion data-layout-allow-overlap>2</b><i id="c2f">2</i></span><div id="t2-b" class="tt">A <span class="s">15 CM</span>*</div></div>
    <span id="regua"><i id="rg-t"></i><i id="rg-l"></i><i id="rg-0"></i><i id="rg-15"></i><b id="rg-n">15 cm</b></span>
    <div id="p3" class="passo"><span class="chip"><b data-layout-allow-occlusion data-layout-allow-overlap>3</b><i>3</i></span><span class="pt">e espera o cheiro <span class="s">se revelar</span></span></div>
  </div>
  <div id="rodape" class="clip" data-start="4" data-duration="10.36" data-track-index="10"><span id="rd">*Dados do<br>fabricante</span></div>

  <!-- CTA: QUAL / PRIMEIRO? + linha de chamada até o produto marcado -->
  <div id="t3" class="clip titulo" data-start="14.4" data-duration="5.4" data-track-index="8">
    <div class="ln" style="top:190px"><div id="t3-a" class="tt">QUAL</div></div>
    <div class="ln" style="top:290px"><div id="t3-b" class="tt"><span class="s">PRIMEIRO?</span></div></div>
    <div id="p4" class="passo"><span class="pt">toque no <span class="s">produto marcado</span></span></div>
  </div>
  <div id="guia" class="clip" data-start="%%TTOCA%%" data-duration="%%DGUIA%%" data-track-index="11">
    <i id="gd-l"></i><i id="gd-o"></i>
    <span id="gd-s"><svg viewBox="0 0 56 56" width="56" height="56"><path d="M40 16 L14 42 M12 22 L12 44 L34 44" fill="none" stroke="#F2FAFC" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/><path d="M40 16 L14 42 M12 22 L12 44 L34 44" fill="none" stroke="#FF4F2E" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="13"></div>
  <div id="wipe1" class="clip wipe" data-start="3.84" data-duration="0.32" data-track-index="14"><i id="wp1"><i></i></i></div>
  <div id="wipe2" class="clip wipe" data-start="14.24" data-duration="0.32" data-track-index="15"><i id="wp2"><i></i></i></div>

%%LEG%%

  <audio id="voz-intro" data-start="0.25" data-duration="%%DV1%%" data-track-index="16" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.2" data-duration="%%DV2%%" data-track-index="16" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="14.7" data-duration="%%DV3%%" data-track-index="16" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="17" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="3.84" data-duration="0.3" data-track-index="18" data-volume="0.36" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-2" data-start="6.33" data-duration="0.3" data-track-index="18" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%TUNS%%" data-duration="0.03" data-track-index="17" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%TPOP%%" data-duration="0.09" data-track-index="17" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whoosh-3" data-start="11.3" data-duration="0.3" data-track-index="18" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="13.8" data-duration="0.6" data-media-start="0.8" data-track-index="18" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="17" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-brilho-1" data-start="%%TCONF%%" data-duration="0.9" data-track-index="17" data-volume="0.3" src="assets/sfx/brilho.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (G): flash + punch 1,2 -> 1,0 na válvula; título bate; alvo na válvula quando o dedo aperta ----
tl.fromTo("#fl1", {opacity:0.9}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camG1", {scale:1.2}, {scale:1.0, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camG1", {scale:1.04, duration:%%D_G1A%%, ease:"none"}, 0.4);
tl.to("#camG1", {scale:1.08, duration:0.14, ease:"power2.out"}, %%TCERTO%%);
tl.to("#camG1", {scale:1.1, duration:%%D_G1B%%, ease:"none"}, %%TCERTO14%%);
tl.fromTo("#t1-a", {scale:1.8, opacity:0, transformOrigin:"0% 60%"}, {scale:1, opacity:1, duration:0.28, ease:"back.out(1.7)"}, 0.03);
tl.fromTo("#t1-b", {yPercent:110}, {yPercent:0, duration:0.26, ease:"power3.out"}, 0.2);
tl.fromTo("#av", {scale:1.7, opacity:0, rotation:-45}, {scale:1, opacity:1, rotation:0, duration:0.24, ease:"back.out(1.8)"}, 0.9);
tl.fromTo("#av", {scale:1}, {scale:1.14, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TCERTO%%);
tl.to("#av", {opacity:0, scale:0.8, duration:0.18, ease:"power2.in"}, 3.4);
tl.fromTo("#t1-b", {scale:1}, {scale:1.08, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 60%", immediateRender:false}, %%TCERTO%%);
tl.to(["#t1-a", "#t1-b"], {yPercent:-110, duration:0.16, ease:"power2.in"}, 3.8);
// passagem: painel tinta entra pela esquerda, cobre tudo no corte (4,0) e sai pela direita
tl.fromTo("#wp1", {x:-1140}, {x:-20, duration:0.16, ease:"power2.in"}, 3.84);
tl.to("#wp1", {x:1100, duration:0.16, ease:"power2.out"}, 4.0);

// ---- APRESENTAÇÃO 1 (H 0-1,96): mão desce até a válvula do Barbarius ----
tl.fromTo("#camH1", {scale:1.1}, {scale:1.03, duration:0.3, ease:"power3.out"}, 4.0);
tl.to("#camH1", {scale:1.07, duration:2.15, ease:"none"}, 4.3);
tl.fromTo("#t2-a", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, 4.12);
tl.fromTo("#t2-b", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, 4.24);
tl.fromTo(["#c1", "#c2"], {scale:0.3, opacity:0}, {scale:1, opacity:1, duration:0.24, stagger:0.12, ease:"back.out(2)"}, 4.12);
tl.fromTo("#rd", {opacity:0}, {opacity:1, duration:0.25, ease:"none"}, 4.45);
tl.set("#regua", {opacity:1, clipPath:"inset(0% 100% 0% 0%)"}, 0);
tl.set("#p3", {opacity:0}, 0);
tl.set("#p4", {opacity:0}, 0);

// ---- APRESENTAÇÃO 2 (G 4,0-7,96): corte em "borrife" direto no detalhe (válvula), recua em "quinze" ----
tl.fromTo("#camG2", {scale:1.46}, {scale:1.34, duration:0.26, ease:"power3.out"}, %%THG%%);
tl.to("#camG2", {scale:1.28, duration:%%D_G2A%%, ease:"none"}, %%THG26%%);
tl.fromTo("#c1f", {scale:0}, {scale:1, duration:0.2, ease:"back.out(2.4)"}, %%TNA%%);
tl.fromTo("#c1", {scale:1}, {scale:1.2, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TNA%%);
tl.fromTo("#c2f", {scale:0}, {scale:1, duration:0.2, ease:"back.out(2.4)"}, %%TUNS%%);
tl.fromTo("#c2", {scale:1}, {scale:1.2, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TUNS%%);
tl.to("#camG2", {scale:1.04, duration:0.36, ease:"power3.inOut"}, %%TQUINZE%%);
tl.to("#camG2", {scale:1.08, duration:%%D_G2B%%, ease:"none"}, %%TQUINZE36%%);
tl.to("#regua", {clipPath:"inset(0% 0% 0% 0%)", duration:%%D_REG%%, ease:"power1.inOut"}, %%TQUINZE%%);
// "e espere": régua sai, passo 3 entra; push-in lento enquanto o vapor se abre
tl.to("#regua", {opacity:0, y:-10, duration:0.16, ease:"power2.in"}, %%TE08%%);
tl.fromTo("#p3", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.24, ease:"power3.out"}, %%TE%%);
tl.to("#camG2", {scale:1.13, duration:0.2, ease:"power2.out"}, %%TE%%);
tl.to("#camG2", {scale:1.18, duration:%%D_G2C%%, ease:"none"}, %%TE20%%);

// ---- APRESENTAÇÃO 3 (H 5,0-7,85): "Leve, pra reaplicar ao longo do dia" ----
tl.fromTo("#camH2", {scale:1.1}, {scale:1.04, duration:0.26, ease:"power3.out"}, %%TGH%%);
tl.to("#camH2", {scale:1.07, duration:%%D_H2A%%, ease:"none"}, %%TGH26%%);
tl.to("#camH2", {scale:1.1, duration:0.14, ease:"power2.out"}, %%TREAP%%);
tl.to("#camH2", {scale:1.12, duration:%%D_H2B%%, ease:"none"}, %%TREAP14%%);
tl.to("#camH2", {scale:1.14, duration:0.14, ease:"power2.out"}, %%TDIA%%);
tl.to("#camH2", {scale:1.15, duration:%%D_H2C%%, ease:"none"}, %%TDIA14%%);
tl.fromTo("#p3", {scale:1}, {scale:1.05, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}, %%TLEVE%%);
tl.to(["#t2-a", "#t2-b"], {yPercent:-110, duration:0.16, ease:"power2.in"}, 14.2);
tl.to(["#c1", "#c2", "#p3", "#rd"], {opacity:0, duration:0.14, ease:"none"}, 14.2);
// passagem para a CTA: painel tinta sobe de baixo, cobre no corte (14,4) e sai pelo alto
tl.fromTo("#wp2", {y:1960}, {y:-20, duration:0.16, ease:"power2.in"}, 14.24);
tl.to("#wp2", {y:-1990, duration:0.16, ease:"power2.out"}, 14.4);

// ---- CTA (I): mais calma; QUAL PRIMEIRO? no respiro; linha de chamada em "Toca" ----
tl.fromTo("#camI", {scale:1.08}, {scale:1.0, duration:0.4, ease:"power2.out"}, 14.4);
tl.to("#camI", {scale:1.03, duration:%%D_IA%%, ease:"none"}, 14.8);
tl.to("#camI", {scale:1.05, duration:0.3, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camI", {scale:1.08, duration:%%D_IB%%, ease:"none"}, %%TTOCA30%%);
tl.fromTo("#t3-a", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, 14.5);
tl.fromTo("#t3-b", {yPercent:110}, {yPercent:0, duration:0.3, ease:"power3.out"}, 14.62);
tl.fromTo("#t3-b", {scale:1}, {scale:1.06, duration:0.14, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 60%", immediateRender:false}, %%TTRES%%);
tl.fromTo("#p4", {opacity:0, x:-30}, {opacity:1, x:0, duration:0.24, ease:"power3.out"}, %%TTOCA%%);
tl.fromTo("#gd-l", {scaleY:0}, {scaleY:1, duration:0.4, ease:"power2.inOut"}, %%TTOCA%%);
tl.fromTo("#gd-s", {scale:0, opacity:0}, {scale:1, opacity:1, duration:0.2, ease:"back.out(2.4)"}, %%TTOCA36%%);
tl.fromTo("#gd-o", {scale:0.6, opacity:0.95}, {scale:2, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA36%%);
tl.fromTo("#gd-s", {x:0, y:0}, {x:-6, y:6, duration:0.24, yoyo:true, repeat:%%REPS%%, ease:"sine.inOut", immediateRender:false}, %%TTOCA60%%);
tl.fromTo("#gd-o", {scale:0.6, opacity:0.95}, {scale:2, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TPERTO%%);
tl.fromTo("#br-b", {x:-400, rotation:14}, {x:1300, rotation:14, duration:0.75, ease:"power1.inOut"}, %%TCONF%%);

// ---- legenda ----
%%LEGJS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

R = lambda v: str(round(v, 3))
t_g2a_fim = t_quinze
rep = {
    "TOTAL": R(TOTAL), "VX": str(VX), "VY": str(VY), "AVL": str(VX - 85), "AVT": str(VY - 85),
    "DV1": R(DUR_MP3["intro"]), "DV2": R(DUR_MP3["apresentacao"]), "DV3": R(DUR_MP3["cta"]),
    "TCERTO": R(t_certo), "TCERTO14": R(t_certo + 0.14),
    "D_G1A": R(t_certo - 0.4), "D_G1B": R(4.0 - t_certo - 0.14),
    "THG": R(T_HG), "THG26": R(T_HG + 0.26), "D_G2A": R(t_quinze - T_HG - 0.26),
    "TNA": R(t_na), "TUNS": R(t_uns), "TQUINZE": R(t_quinze), "TQUINZE36": R(t_quinze + 0.36),
    "D_G2B": R(t_e - t_quinze - 0.36), "D_REG": R(t_cm_fim - t_quinze),
    "TE": R(t_e), "TE08": R(t_e - 0.08), "TE20": R(t_e + 0.2), "D_G2C": R(T_GH - t_e - 0.2),
    "TPOP": R(t_e - 0.04),
    "TGH": R(T_GH), "TGH26": R(T_GH + 0.26), "D_H2A": R(t_reap - T_GH - 0.26),
    "TREAP": R(t_reap), "TREAP14": R(t_reap + 0.14), "D_H2B": R(t_dia - t_reap - 0.14),
    "TDIA": R(t_dia), "TDIA14": R(t_dia + 0.14), "D_H2C": R(14.4 - t_dia - 0.14), "TLEVE": R(t_leve),
    "TTOCA": R(t_toca), "TTOCA30": R(t_toca + 0.3), "TTOCA36": R(t_toca + 0.36), "TTOCA60": R(t_toca + 0.6),
    "D_IA": R(t_toca - 14.8), "D_IB": R(TOTAL - t_toca - 0.3), "DGUIA": R(TOTAL - t_toca),
    "REPS": str(int((TOTAL - t_toca - 0.6) / 0.24) - 1), "TPERTO": R(t_perto), "TTRES": R(t_tres),
    "TCONF": R(t_conf),
    "LEG": "\n".join(leg_html), "LEGJS": "\n".join(leg_js),
}
for k, v in rep.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, [l for l in html.splitlines() if "%%" in l][:3]
open(OUT, "w").write(html)
print("ok", OUT, "TOTAL", TOTAL, "toca", t_toca, "quinze", t_quinze, "e", t_e)
