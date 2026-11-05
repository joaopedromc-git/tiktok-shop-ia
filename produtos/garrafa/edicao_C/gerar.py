#!/usr/bin/env python3
"""Gera produtos/garrafa/edicao_C/index.html ("placa de estrada": asfalto / amarelo de sinalização,
Archivo Black + Inter 800, legenda caixa-palavra). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Combinação cruzada (vídeo C, "pé na estrada"). Regra número 1 (3ª violação, quadro estático): o vídeo de fundo
roda do primeiro ao último quadro. Não há <img>, quadro congelado nem cartão. Trechos da analise_C.md:
  D 4,00-5,60 s em 1,0x | A 2,20-5,20 s em 1,0x | E 1,88-7,97 s em 0,7x | F 2,50-7,10 s em 1,0x
A garrafinha de plástico do clipe A não é o produto: nenhuma moldura, brilho ou callout sobre ela.
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz). Cortes em múltiplos de 1/30 s.
P = {"intro": (0.0, 4.6, 0.25), "apresentacao": (4.6, 13.3, 4.9), "cta": (13.3, 17.9, 13.6)}
TOTAL = 17.9
CORTE_DA = 1.6  # dentro da intro: clipe D -> clipe A, no silêncio entre "estrada?" e "Água"
DUR_MP3 = {"intro": 4.272, "apresentacao": 8.352, "cta": 4.2}
TOPO_LEG = 1256

GRUPOS = {
    "intro": [[0, 1], [2], [3, 4, 5], [6, 7], [8], [9]],
    "apresentacao": [[0, 1], [2], [3, 4], [5, 6], [7], [8, 9], [10, 11], [12, 13, 14], [15, 16], [17, 18], [19]],
    "cta": [[0, 1], [2], [3, 4], [5, 6], [7], [8, 9], [10, 11]],
}
CHAVE = {
    "intro": {2, 5, 8},
    "apresentacao": {4, 7, 11, 13, 14, 16},
    "cta": {4, 5, 7, 11},
}
EXIBE = {("intro", 2): "estrada?"}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


R = lambda v: str(round(v, 3))

# ---- legenda caixa-palavra: cada palavra é uma plaquinha de asfalto que salta no seu tempo; a palavra-chave é amarela ----
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
        if s < CORTE_DA < e:  # a legenda não atravessa o corte D -> A
            e = CORTE_DA
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.03, 3)
            chave = wi in CHAVE[parte]
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            spans += f'<span id="{gid}-{k}" class="pal{" ch" if chave else ""}">{txt}</span>'
            esc = "1.06" if chave else "1"
            leg_js.append(
                f'tl.fromTo("#{gid}-{k}",{{opacity:0,scale:0.6}},{{opacity:1,scale:{esc},duration:0.14,ease:"back.out(2.2)"}},{t});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{TOPO_LEG}px">{spans}</div></div>'
        )

T_ESTRADA = t_pal("intro", 2)
T_PAINEL = t_pal("intro", 4)       # "no (painel)"
T_ESQ = t_pal("intro", 8)          # "esquenta"
T_ALCA = t_pal("apresentacao", 4)  # "alça"
T_GARRAFA = t_pal("apresentacao", 5)
T_MODUS = t_pal("apresentacao", 7)
T_PAREDE = t_pal("apresentacao", 8)
T_DOIS = t_pal("apresentacao", 13)
T_QUATRO = t_pal("apresentacao", 16)
T_TOCA = t_pal("cta", 5)
T_PRODUTO = t_pal("cta", 7)
T_CONF = t_pal("cta", 9)

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Archivo Black";src:local("Archivo Black"),local("Archivo Black Regular"),local("ArchivoBlack-Regular")}
@font-face{font-family:"Inter";font-weight:100 900;src:local("Inter"),local("Inter Regular")}
:root{--asf:#14161A;--ama:#FFD21F;--txt:#FFFFFF}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#14161A}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#14161A;font-family:"Inter";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camD{transform-origin:55% 48%}
#camA{transform-origin:50% 42%}
#camE{transform-origin:30% 45%}
#camF{transform-origin:45% 50%}
/* calor no painel (quadro inteiro, nada em volta da garrafinha de plástico) e luz que varre a tela quando a garrafa sobe */
#calor{z-index:2}
#calor-b{position:absolute;inset:0;display:block;opacity:0;
  background:linear-gradient(to bottom,rgba(255,170,40,.36) 0,rgba(255,120,30,.2) 45%,rgba(255,90,20,.06) 100%)}
#luz{z-index:2;overflow:hidden}
#luz-b{position:absolute;left:0;top:-340px;width:430px;height:2600px;display:block;
  background:linear-gradient(to right,rgba(255,244,205,0) 0,rgba(255,244,205,.6) 50%,rgba(255,244,205,0) 100%)}
.vinheta{z-index:3;background:radial-gradient(ellipse 94% 68% at 50% 50%,rgba(0,0,0,0) 62%,rgba(10,11,13,.4) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(20,22,26,.5) 0,rgba(20,22,26,.24) 12%,rgba(20,22,26,0) 24%)}
/* títulos grandes (gancho e CTA): Archivo Black, branco + amarelo de sinalização, contorno de asfalto */
.titulo{z-index:6}
.tg{position:absolute;left:62px;top:196px;width:856px;display:block}
.tt{display:block;font-family:"Archivo Black";font-weight:400;font-size:128px;line-height:1;letter-spacing:-1px;text-align:center;white-space:nowrap;
  color:var(--txt);-webkit-text-stroke:14px #14161A;paint-order:stroke fill;text-shadow:0 9px 0 #14161A,0 18px 30px rgba(0,0,0,.45)}
.tt.am{color:var(--ama)}
/* faixa de estrada: tira de asfalto com tracejado amarelo correndo */
.road{position:absolute;left:170px;top:472px;width:640px;height:26px;display:block;border-radius:7px;background:#14161A;overflow:hidden;
  box-shadow:0 6px 14px rgba(0,0,0,.4)}
.dash{position:absolute;left:0;top:9px;width:640px;height:8px;display:block;
  background-image:linear-gradient(to right,#FFD21F 0,#FFD21F 58px,rgba(255,210,31,0) 58px,rgba(255,210,31,0) 96px);
  background-size:96px 8px;background-repeat:repeat-x;background-position:0px 0px}
/* placas: asfalto com filete branco (informação) e amarela com filete de asfalto (o dado que importa) */
.placas{z-index:6}
.pl{position:absolute;display:block;border-radius:18px;white-space:nowrap;text-align:center;
  box-shadow:inset 0 0 0 5px #14161A,inset 0 0 0 8px rgba(255,255,255,.92),0 10px 24px rgba(0,0,0,.42)}
.pl.esc{background:#14161A;color:var(--txt)}
.pl.ama{background:var(--ama);color:#14161A;box-shadow:inset 0 0 0 5px #FFD21F,inset 0 0 0 8px #14161A,0 10px 24px rgba(0,0,0,.42)}
.pl span{display:block;white-space:nowrap}
#pa-a{left:62px;top:204px;padding:21px 34px 21px;font-size:44px;line-height:1;letter-spacing:1px}
#pa-b{left:62px;top:300px;padding:19px 36px 21px;font-family:"Archivo Black";font-weight:400;font-size:104px;line-height:1;letter-spacing:-1px}
#pm-a{left:28px;top:196px;width:288px;height:110px;padding-top:15px}
#pm-a .k{font-size:22px;line-height:24px;letter-spacing:1.4px;color:rgba(255,255,255,.86)}
#pm-m{margin-top:3px;font-family:"Archivo Black";font-weight:400;font-size:62px;line-height:62px;letter-spacing:.5px;color:var(--ama)}
#pm-b{left:28px;top:314px;width:288px;height:120px;padding-top:16px;font-size:40px;line-height:44px}
#pm-c{left:28px;top:314px;width:288px;height:142px;padding-top:10px}
#pm-n{font-family:"Archivo Black";font-weight:400;font-size:94px;line-height:84px;letter-spacing:-1px}
#pm-c .un{font-family:"Archivo Black";font-weight:400;font-size:38px;line-height:42px;letter-spacing:1px}
.subw{position:absolute;left:62px;top:514px;width:856px;display:flex;justify-content:center}
#t3-s{position:relative;padding:17px 30px 19px;font-size:42px;line-height:1}
/* legenda caixa-palavra */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:flex-start;gap:14px;flex-wrap:nowrap}
.pal{display:block;font-family:"Inter";font-weight:800;font-size:68px;line-height:1.1;white-space:nowrap;color:var(--txt);background:#14161A;
  padding:11px 22px 15px;border-radius:14px;box-shadow:inset 0 0 0 4px #14161A,inset 0 0 0 6px rgba(255,255,255,.8),0 8px 18px rgba(0,0,0,.4)}
.pal.ch{background:var(--ama);color:#14161A;box-shadow:inset 0 0 0 4px #FFD21F,inset 0 0 0 6px #14161A,0 8px 18px rgba(0,0,0,.4)}
.rodape{z-index:7}
.rodape span{position:absolute;left:28px;top:1457px;display:block;white-space:nowrap;font-weight:600;font-size:28px;line-height:28px;
  letter-spacing:.4px;color:rgba(255,255,255,.8);background:rgba(20,22,26,.62);padding:8px 14px;border-radius:10px}
/* CTA: placa redonda amarela com seta para baixo/esquerda */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1392px;width:120px;height:120px;display:block;border-radius:50%;background:var(--ama);
  box-shadow:inset 0 0 0 5px #FFD21F,inset 0 0 0 9px #14161A,0 0 0 5px rgba(20,22,26,.92),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:120px;height:120px}
#tq-o{position:absolute;left:56px;top:1392px;width:120px;height:120px;display:block;border:7px solid var(--ama);border-radius:50%;opacity:0}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO (0-4,6 s), dois clipes. Abertura: clipe D 4,0-5,6 s em 1,0x (garrafa verde na trilha, grande e nítida) -->
  <div id="camD" class="cam"><video id="vD" class="clip full" data-start="0" data-duration="1.6" data-media-start="4" data-track-index="0" src="assets/clipe_D.mp4" muted playsinline></video></div>
  <!-- corte seco em 1,6 s: clipe A 2,2-5,2 s em 1,0x (painel do carro; poeira subindo e paisagem andando) -->
  <div id="camA" class="cam"><video id="vA" class="clip full" data-start="1.6" data-duration="3" data-media-start="2.2" data-track-index="0" src="assets/clipe_A.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO (4,6-13,3 s): clipe E 1,88-7,97 s em 0,7x (mão entra aos 6,2 s, fecha na alça aos 7,1 s, levanta de 8,3 a 9,8 s) -->
  <div id="camE" class="cam"><video id="vE" class="clip full" data-start="4.6" data-duration="8.7" data-media-start="1.88" data-playback-rate="0.7" data-track-index="0" src="assets/clipe_E.mp4" muted playsinline></video></div>
  <!-- CTA (13,3-17,9 s): clipe F 2,5-7,1 s em 1,0x -->
  <div id="camF" class="cam"><video id="vF" class="clip full" data-start="13.3" data-duration="4.6" data-media-start="2.5" data-track-index="0" src="assets/clipe_F.mp4" muted playsinline></video></div>

  <div id="calor" class="clip" data-start="1.6" data-duration="3" data-track-index="1"><i id="calor-b"></i></div>
  <div id="luz" class="clip" data-start="8.4" data-duration="0.95" data-track-index="1"><i id="luz-b"></i></div>
  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="2"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="3"></div>

  <!-- gancho: atravessa o corte D -> A e sai antes da placa do painel -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="2.2" data-track-index="6">
    <div id="t1-g" class="tg">
      <div id="t1-l0" class="tt">VAI PEGAR</div>
      <div id="t1-l1" class="tt am">ESTRADA?</div>
    </div>
    <i id="t1-r" class="road"><i id="t1-d" class="dash"></i></i>
  </div>
  <!-- painel: placas sobre o céu, à esquerda do retrovisor -->
  <div id="pa" class="clip placas" data-start="2.2" data-duration="2.4" data-track-index="6">
    <div id="pa-a" class="pl esc">ÁGUA NO PAINEL</div>
    <div id="pa-b" class="pl ama">ESQUENTA</div>
  </div>
  <!-- apresentação: placas no canto superior esquerdo, ao lado da tampa (não cobrem a garrafa) -->
  <div id="pm" class="clip placas" data-start="%%PM0%%" data-duration="%%PMD%%" data-track-index="6">
    <div id="pm-a" class="pl esc"><span class="k">GARRAFA TÉRMICA</span><span id="pm-m">MODUS</span></div>
    <div id="pm-b" class="pl esc"><span id="pm-b0">parede dupla</span><span id="pm-b1">a vácuo</span></div>
    <div id="pm-c" class="pl ama"><span id="pm-n">2,4</span><span class="un">LITROS*</span></div>
  </div>
  <div id="rodape" class="clip rodape" data-start="4.6" data-duration="8.7" data-track-index="7"><span id="rodape-s">*Dados do fabricante</span></div>
  <!-- CTA -->
  <div id="t3" class="clip titulo" data-start="%%T30%%" data-duration="%%T3D%%" data-track-index="6">
    <div id="t3-g" class="tg">
      <div id="t3-l0" class="tt">TOCA NO</div>
      <div id="t3-l1" class="tt am">PRODUTO</div>
    </div>
    <i id="t3-r" class="road"><i id="t3-d" class="dash"></i></i>
    <div class="subw"><div id="t3-s" class="pl esc">e confere a sua</div></div>
  </div>
  <div id="toque" class="clip" data-start="%%T30%%" data-duration="%%T3D%%" data-track-index="8">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 120 120"><path d="M80 40 L42 78 M40 50 L40 80 L70 80" fill="none" stroke="#14161A" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.9" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="13.6" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="1.5" data-duration="0.3" data-track-index="14" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="4.5" data-duration="0.3" data-track-index="14" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%SPOP%%" data-duration="0.09" data-track-index="14" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-brilho-1" data-start="8.42" data-duration="0.9" data-track-index="14" data-volume="0.25" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ%%" data-duration="0.03" data-track-index="14" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="12.91" data-duration="0.39" data-media-start="1.0" data-track-index="14" data-volume="0.36" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%T30%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO, abertura (clipe D): garrafa inteira no quadro 0, punch-in curto, título batendo ----
tl.fromTo("#camD", {scale:1.08}, {scale:1, duration:0.42, ease:"power3.out"}, 0);
tl.to("#camD", {scale:1.03, duration:1.17, ease:"none"}, 0.43);
tl.fromTo("#t1-g", {scale:1.25, transformOrigin:"50% 50%"}, {scale:1, duration:0.32, ease:"back.out(1.8)"}, 0);
tl.fromTo("#t1-r", {scaleX:0, transformOrigin:"50% 50%"}, {scaleX:1, duration:0.3, ease:"power3.out"}, 0.26);
tl.fromTo("#t1-d", {backgroundPosition:"0px 0px"}, {backgroundPosition:"-384px 0px", duration:2.2, ease:"none"}, 0);
tl.fromTo("#t1-l1", {scale:1, transformOrigin:"50% 60%"}, {scale:1.07, duration:0.13, yoyo:true, repeat:1, ease:"power2.out"}, %%TESTRADA%%);
tl.to("#t1-g", {y:-70, opacity:0, duration:0.2, ease:"power2.in"}, 1.98);
tl.to("#t1-r", {scaleX:0, duration:0.18, ease:"power2.in"}, 1.98);

// ---- INTRO, painel (clipe A): corte seco, placas sobre o céu, calor subindo em "esquenta" ----
tl.fromTo("#camA", {scale:1.13, x:0}, {scale:1.06, x:0, duration:0.36, ease:"power3.out"}, 1.6);
tl.to("#camA", {scale:1.09, x:-10, duration:%%DA1%%, ease:"none"}, 1.97);
tl.to("#camA", {scale:1.14, duration:0.28, ease:"power2.out"}, %%TESQ0%%);
tl.to("#camA", {scale:1.17, x:-22, duration:%%DA2%%, ease:"none"}, %%TESQ1%%);
tl.fromTo("#pa-a", {x:-700}, {x:0, duration:0.3, ease:"power3.out"}, 2.22);
tl.fromTo("#pa-b", {opacity:0, scale:1.45, transformOrigin:"0% 50%"}, {opacity:1, scale:1, duration:0.22, ease:"back.out(1.6)"}, %%TESQ0%%);
tl.fromTo("#calor-b", {opacity:0}, {opacity:1, duration:0.7, ease:"power1.out"}, %%TESQ0%%);
tl.to("#pa-a", {x:-760, duration:0.17, ease:"power2.in"}, 4.42);
tl.to("#pa-b", {x:-860, duration:0.17, ease:"power2.in"}, 4.43);

// ---- APRESENTAÇÃO (clipe E em 0,7x): zoom máximo 1,10; nada aponta para a linha pequena da etiqueta ----
tl.fromTo("#camE", {scale:1.06, x:0}, {scale:1, x:0, duration:0.4, ease:"power3.out"}, 4.6);
tl.to("#camE", {scale:1.015, duration:%%DE1%%, ease:"none"}, 5.01);
// "alça": a câmera vai para o lado da alça enquanto a mão chega
tl.to("#camE", {scale:1.085, x:-46, duration:0.4, ease:"power2.out"}, %%TALCA0%%);
tl.to("#camE", {scale:1.095, duration:0.2, ease:"none"}, %%TALCA1%%);
tl.to("#camE", {scale:1.02, x:0, duration:0.42, ease:"power2.inOut"}, %%TALCA2%%);
tl.to("#camE", {scale:1.03, duration:%%DE2%%, ease:"none"}, %%TALCA3%%);
// produto herói: a garrafa sobe, uma luz varre a tela e a câmera fecha um pouco (vídeo rodando)
tl.to("#camE", {scale:1.045, duration:0.5, ease:"power2.out"}, 8.4);
tl.to("#camE", {scale:1.06, duration:4.39, ease:"none"}, 8.91);
tl.fromTo("#luz-b", {x:-760, rotation:17}, {x:1420, rotation:17, duration:0.85, ease:"power1.inOut"}, 8.42);
// placas ao lado da tampa
tl.fromTo("#pm-a", {x:-420}, {x:0, duration:0.3, ease:"power3.out"}, %%PM1%%);
tl.fromTo("#pm-m", {scale:1, transformOrigin:"50% 55%"}, {scale:1.12, duration:0.14, yoyo:true, repeat:1, ease:"power2.out"}, %%TMODUS%%);
tl.fromTo("#pm-b", {x:-420}, {x:0, duration:0.28, ease:"power3.out"}, %%TPAREDE%%);
tl.to("#pm-b", {x:-420, duration:0.16, ease:"power2.in"}, %%TSAI%%);
tl.fromTo("#pm-c", {opacity:0, scale:0.55, transformOrigin:"50% 0%"}, {opacity:1, scale:1, duration:0.26, ease:"back.out(1.9)"}, %%TDOIS%%);
tl.fromTo("#pm-n", {scale:1, transformOrigin:"50% 60%"}, {scale:1.14, duration:0.15, yoyo:true, repeat:1, ease:"power2.out"}, %%TQUATRO%%);

// ---- CTA (clipe F em 1,0x): mais calma; o título só entra em "Toca" ----
tl.fromTo("#camF", {scale:1.09}, {scale:1.045, duration:0.4, ease:"power3.out"}, 13.3);
tl.to("#camF", {scale:1.03, duration:%%DF1%%, ease:"none"}, 13.71);
tl.to("#camF", {scale:1.012, duration:0.1, ease:"power2.in"}, %%T30%%);
tl.to("#camF", {scale:1.032, duration:0.18, ease:"power2.out"}, %%T31%%);
tl.to("#camF", {scale:1, duration:%%DF2%%, ease:"none"}, %%T32%%);
tl.fromTo("#t3-g", {opacity:0, scale:1.25, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:0.28, ease:"back.out(1.8)"}, %%T30%%);
tl.fromTo("#t3-r", {scaleX:0, transformOrigin:"50% 50%"}, {scaleX:1, duration:0.3, ease:"power3.out"}, %%T3R%%);
tl.fromTo("#t3-d", {backgroundPosition:"0px 0px"}, {backgroundPosition:"-384px 0px", duration:%%T3D%%, ease:"none"}, %%T30%%);
tl.fromTo("#t3-l1", {scale:1, transformOrigin:"50% 60%"}, {scale:1.07, duration:0.13, yoyo:true, repeat:1, ease:"power2.out"}, %%TPRODUTO%%);
tl.fromTo("#t3-s", {opacity:0, scale:0.7}, {opacity:1, scale:1, duration:0.22, ease:"back.out(2)"}, %%TCONF%%);
tl.fromTo("#tq-b", {scale:0.5, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%T30%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.8, opacity:0, duration:0.6, ease:"power2.out"}, %%T30%%);
tl.fromTo("#tq-s", {x:0, y:0}, {x:-7, y:7, duration:0.22, yoyo:true, repeat:7, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.8, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);
tl.fromTo("#tq-o", {scale:0.6, opacity:0.95}, {scale:1.8, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA3%%);

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

T30 = round(T_TOCA - 0.02, 3)
PM0 = round(T_GARRAFA - 0.03, 3)  # no silêncio entre "alça" e "Garrafa"
subs = {
    "TOTAL": str(TOTAL),
    "DV1": str(DUR_MP3["intro"]), "DV2": str(DUR_MP3["apresentacao"]), "DV3": str(DUR_MP3["cta"]),
    "TESTRADA": R(T_ESTRADA),
    "TESQ0": R(T_ESQ - 0.03), "TESQ1": R(T_ESQ + 0.26), "DA1": R(T_ESQ - 0.03 - 1.97), "DA2": R(4.6 - (T_ESQ + 0.26)),
    "TALCA0": R(T_ALCA - 0.07), "TALCA1": R(T_ALCA + 0.34), "TALCA2": R(T_ALCA + 0.55), "TALCA3": R(T_ALCA + 0.98),
    "DE1": R(T_ALCA - 0.07 - 5.01), "DE2": R(8.39 - (T_ALCA + 0.98)),
    "PM0": R(PM0), "PMD": R(13.3 - PM0), "PM1": R(PM0 + 0.02), "SPOP": R(PM0 - 0.04),
    "TMODUS": R(T_MODUS + 0.02), "TPAREDE": R(T_PAREDE - 0.04),
    "TSAI": R(T_DOIS - 0.16), "TDOIS": R(T_DOIS), "STIQ": R(T_DOIS - 0.07), "TQUATRO": R(T_QUATRO + 0.1),
    "T30": R(T30), "T3D": R(TOTAL - T30), "T31": R(T30 + 0.11), "T32": R(T30 + 0.3),
    "DF1": R(T30 - 13.72), "DF2": R(TOTAL - (T30 + 0.3)),
    "T3R": R(T30 + 0.2), "TPRODUTO": R(T_PRODUTO + 0.02), "TCONF": R(T_CONF - 0.03),
    "TPULSO": R(T30 + 0.3), "TONDA2": R(T30 + 0.9), "TONDA3": R(T30 + 1.7),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
open(OUT, "w").write(html)
print("ok", OUT, "| alça", T_ALCA, "| placa MODUS", PM0, "| toca", T30)
