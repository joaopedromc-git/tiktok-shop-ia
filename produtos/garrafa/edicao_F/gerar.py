#!/usr/bin/env python3
"""Gera produtos/garrafa/edicao_F/index.html — "Pulseira de rolê" (receita do body splash D, sistema visual próprio).
Tinta #120F1C / ultravioleta #9061FF / papel #FFF8EE; Bricolage Grotesque 800 condensada (wdth 75) + Poppins 800;
legenda "carimbo" (palavra carimba no tempo da voz; palavra-chave em bloco violeta inclinado; na intro as 3 opções
viram pulseiras numeradas 1-2-3 sobre o seu cenário). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Regras (analise_F.md + violações 3 e 5): clipe em tela cheia (sem moldura/janela), vídeo sempre rodando, nada abaixo
de 0,9x na apresentação/CTA, zoom máx. 1,10x, nada de brilho/realce sobre a garrafa, nada sobre a etiqueta MODUS
(y ~580-1265) nem sobre a mão (x > 730, y 380-1210): títulos em y 190-380, legenda em y 1300, rodapé em 1468.
PROIBIDO: G 1,9-2,4 s e H 3,2-4,3 s.
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

VOZ = {"intro": 0.15, "apresentacao": 3.83, "cta": 11.11}
FIM_VOZ = {p: round(VOZ[p] + falas[p]["palavras"][-1]["fim"], 3) for p in VOZ}
P1 = round(FIM_VOZ["intro"] + 0.30, 3)          # 3,682
P2 = round(FIM_VOZ["apresentacao"] + 0.30, 3)   # 10,959
TOTAL = round(FIM_VOZ["cta"] + 0.326, 2)        # 14,62
FIM_PARTE = {"intro": P1, "apresentacao": P2, "cta": TOTAL}
DV = {"intro": 3.55, "apresentacao": 7.15, "cta": round(TOTAL - VOZ["cta"] - 0.005, 3)}  # mp3 3,576 / 7,152 / 3,528
TOPO_LEG = 1300


def t_pal(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


# ---- cortes: (id, clipe, início no vídeo, fim no vídeo, início na mídia, velocidade) ----
C1 = round(t_pal("intro", 1) - 0.03, 3)          # "acampamento": G -> H
C2 = round(t_pal("intro", 3) - 0.03, 3)          # "trilha": H -> E
C3 = round(t_pal("intro", 8) - 0.02, 3)          # "rolê": E -> H (garrafa no alto)
C4 = round(t_pal("apresentacao", 1) - 0.03, 3)   # "Térmica": H -> G
C5 = round(t_pal("apresentacao", 8) - 0.03, 3)   # "corrosão": G -> H
C6 = 7.59                                        # entre "corrosão" e "segundo": H -> G
C7 = round(t_pal("apresentacao", 15) - 0.02, 3)  # "lavar": G -> H
C8 = FIM_VOZ["apresentacao"]                      # fim de "rápido": H -> E (CTA)
SEG = [
    ("G1", "G", 0.0, C1, 0.55, 1.0),    # mão entra e fecha na alça (para antes de 1,85)
    ("H1", "H", C1, C2, 0.95, 1.0),     # mão chega e pega a alça, fogueira atrás
    ("E1", "E", C2, C3, 3.20, 0.95),    # mão chega e pega a alça, mirante
    ("H2", "H", C3, C4, None, 0.9),     # garrafa levantada (continua do H1)
    ("G2", "G", C4, C5, 2.50, 0.9),     # garrafa no alto, inclina e volta (MODUS grande)
    ("H3", "H", C5, C6, 4.40, 0.9),     # volta à mesa
    ("G3", "G", C6, C7, None, 0.9),     # desce à mesa (continua do G2)
    ("H4", "H", C7, C8, None, 0.9),     # mão solta, fumaça da fogueira (continua do H3)
    ("E2", "E", C8, TOTAL, None, None), # CTA: mão levanta a garrafa e segura (continua do E1)
]
PROIBIDO = {"G": [(1.85, 2.45)], "H": [(3.15, 4.35)], "E": [(0, 3.15)]}
LIMITE = {"G": 6.7, "H": 6.0, "E": 7.98}
fim_midia = {}
segs = []
for sid, cl, a, b, ms, rate in SEG:
    if ms is None:
        ms = fim_midia[cl]
    if rate is None:
        rate = round((LIMITE[cl] - 0.005 - ms) / (b - a), 4)
    me = round(ms + (b - a) * rate, 3)
    assert rate >= 0.9 and me <= LIMITE[cl], (sid, rate, me)
    for p0, p1 in PROIBIDO[cl]:
        assert me <= p0 or ms >= p1, (sid, ms, me)
    fim_midia[cl] = me
    segs.append((sid, cl, round(a, 3), round(b, 3), round(ms, 3), rate, me))
assert segs[-1][3] == TOTAL
S = {s[0]: s for s in segs}

R = lambda v: str(round(v, 3))

# ---- legenda "carimbo" ----
GRUPOS = {
    "intro": [[0], [1], [2, 3], [4, 5], [6, 7, 8]],
    "apresentacao": [[0], [1], [2], [3, 4], [5, 6], [7, 8], [9, 10, 11], [12, 13], [14, 15], [16]],
    "cta": [[0], [1, 2], [3], [4, 5], [6, 7], [8, 9]],
}
CHAVE = {"intro": {0, 1, 3, 8}, "apresentacao": {2, 4, 8, 13}, "cta": {0, 3, 5, 7}}
PULSEIRA = {("intro", 0): "1", ("intro", 1): "2", ("intro", 3): "3"}   # opções numeradas (pulseira com canhoto)
EXIBE = {("intro", 0): "TRABALHO", ("intro", 1): "ACAMPAMENTO", ("intro", 3): "TRILHA", ("intro", 8): "rolê?",
         ("apresentacao", 2): "MODUS:", ("apresentacao", 8): "corrosão,", ("apresentacao", 11): "fabricante.",
         ("apresentacao", 16): "rápido.", ("cta", 9): "conferir."}

def topo_leg(t):
    """No G levantado (G2) o MODUS em relevo sobe para y ~1400: a legenda vai para 1235 (etiqueta termina em ~1040)."""
    a, b = S["G2"][2], S["G2"][3]
    if a - 0.05 <= t < a + 0.3:
        return 1160   # início do G2: garrafa no ponto mais alto, relevo em ~1310
    return 1235 if a - 0.05 <= t < b - 0.1 else TOPO_LEG


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
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = s if k == 0 else round(voz + pal[wi]["inicio"] - 0.03, 3)
            chave = wi in CHAVE[parte]
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            n = PULSEIRA.get((parte, wi))
            if n:
                inner = f'<em class="tx k pu"><b class="nr">{n}</b><i class="fu"></i>{txt}</em>'
            elif chave:
                inner = f'<em class="tx k">{txt}</em>'
            else:
                inner = f'<em class="tx">{txt}</em>'
            spans += f'<span id="{gid}-{k}" class="pal">{inner}</span>'
            rot = -7 if chave else -4
            leg_js.append(
                f'tl.fromTo("#{gid}-{k}",{{opacity:0,scale:1.38,rotation:{rot}}},'
                f'{{opacity:1,scale:1,rotation:0,duration:0.13,ease:"power3.out"}},{t});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div id="{gid}-c" class="cap" style="top:{topo_leg(s)}px">{spans}</div></div>')

T_GARRAFA = t_pal("apresentacao", 0)
T_MODUS = t_pal("apresentacao", 2)
T_ACO = t_pal("apresentacao", 3)
T_RESISTE = t_pal("apresentacao", 6)
T_SEGUNDO = t_pal("apresentacao", 9)
T_BOCA = t_pal("apresentacao", 12)
T_USARIA = t_pal("cta", 3)
T_TOCA0 = round(t_pal("cta", 5) - 0.03, 3)

videos = []
for i, (sid, cl, a, b, ms, rate, me) in enumerate(segs):
    videos.append(
        f'  <div id="cam{sid}" class="cam"><video id="v{sid}" class="clip full" data-start="{R(a)}" '
        f'data-duration="{R(b - a)}" data-media-start="{R(ms)}" data-playback-rate="{rate}" data-track-index="{i % 2}" '
        f'src="assets/clipe_{cl}.mp4" muted playsinline></video></div>')

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
/* nomes completos das fontes do container (Bricolage é variável: opsz, wdth, wght) */
@font-face{font-family:"Bric Role";font-weight:200 800;font-stretch:75% 100%;src:local("Bricolage Grotesque 96pt ExtraBold"),local("Bricolage Grotesque")}
@font-face{font-family:"Pop Role";font-weight:800;src:local("Poppins ExtraBold"),local("Poppins-ExtraBold")}
@font-face{font-family:"Pop Role";font-weight:600;src:local("Poppins SemiBold"),local("Poppins-SemiBold")}
:root{--tinta:#120F1C;--violeta:#9061FF;--papel:#FFF8EE}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#120F1C}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#120F1C;font-family:"Pop Role";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1;transform-origin:50% 45%}
#camG2{transform-origin:47% 40%}
.full{width:100%;height:100%;object-fit:cover}
.vinheta{z-index:3;background:radial-gradient(ellipse 96% 72% at 50% 50%,rgba(0,0,0,0) 62%,rgba(18,15,28,.45) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(18,15,28,.62) 0,rgba(18,15,28,.34) 14%,rgba(18,15,28,0) 25%)}
.flash{z-index:9;background:#FFF8EE;opacity:0}
/* títulos: Bricolage 800 condensada, papel; destaque em bloco violeta "carimbado" */
.titulo{z-index:6}
.bric{font-family:"Bric Role";font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75,"opsz" 96}
.tw{position:absolute;left:50px;width:860px;display:flex;justify-content:flex-start;align-items:center}
.tt{display:flex;align-items:center;gap:22px;line-height:1;white-space:nowrap;color:var(--papel);
  text-shadow:0 6px 22px rgba(0,0,0,.5)}
.blk{display:block;background:var(--violeta);color:var(--papel);padding:4px 22px 12px;border-radius:14px;
  box-shadow:0 0 0 5px var(--tinta),0 12px 26px rgba(0,0,0,.45);text-shadow:none}
.kick{display:block;font-family:"Pop Role";font-weight:800;font-size:42px;line-height:1;color:var(--papel);letter-spacing:1px;
  -webkit-text-stroke:7px var(--tinta);paint-order:stroke fill}
/* letreiro: pulseira violeta com canhoto picotado; cada item entra carimbado no tempo da voz */
.lt{position:absolute;left:50px;top:258px;display:flex;align-items:center;height:118px;background:var(--violeta);border-radius:16px;
  box-shadow:0 0 0 5px var(--tinta),0 14px 30px rgba(0,0,0,.45);opacity:0}
.lt .cn{display:block;width:30px;height:118px;border-right:4px dashed rgba(18,15,28,.55);margin-right:22px;
  background:radial-gradient(circle at 15px 22px,var(--tinta) 0 6px,transparent 7px),radial-gradient(circle at 15px 96px,var(--tinta) 0 6px,transparent 7px)}
.lt b{display:block;font-family:"Bric Role";font-weight:800;font-stretch:75%;font-variation-settings:"wdth" 75,"opsz" 96;
  line-height:118px;color:var(--papel);white-space:nowrap;padding-right:30px}
.lt sup{font-size:.55em;vertical-align:.7em;line-height:0}
/* rodapé */
#rod{z-index:6}
#rod span{position:absolute;left:40px;top:1468px;display:block;font-family:"Pop Role";font-weight:600;font-size:30px;line-height:1;
  color:rgba(255,248,238,.86);background:rgba(18,15,28,.5);padding:8px 14px 9px;border-radius:10px}
/* balão de comentário da CTA */
#bolha{position:absolute;left:56px;top:190px;display:block;background:var(--violeta);border-radius:34px;padding:20px 38px 24px;
  box-shadow:0 0 0 5px var(--tinta),0 14px 30px rgba(0,0,0,.45)}
#bolha em{display:block;font-style:normal;font-family:"Pop Role";font-weight:800;font-size:36px;line-height:1;color:var(--tinta);margin-bottom:8px}
#bolha b{display:block;font-size:96px;line-height:1;white-space:nowrap;color:var(--papel)}
#bolha i{position:absolute;left:64px;bottom:-36px;width:62px;height:42px;display:block;background:var(--violeta);clip-path:polygon(0 0,100% 0,0 100%)}
/* legenda carimbo */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:878px;display:flex;justify-content:center;align-items:center;gap:20px;flex-wrap:nowrap}
.pal{position:relative;display:block;white-space:nowrap}
.tx{display:block;font-style:normal;font-family:"Pop Role";font-weight:800;font-size:76px;line-height:1.1;color:var(--papel);
  -webkit-text-stroke:10px var(--tinta);paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.5)}
.tx.k{background:var(--violeta);-webkit-text-stroke:0;padding:2px 20px 8px;border-radius:14px;transform:rotate(-3deg);
  box-shadow:0 0 0 5px var(--tinta),0 10px 22px rgba(0,0,0,.45);text-shadow:none}
.tx.pu{display:flex;align-items:center;padding-left:0}
.tx.pu .nr{display:block;width:74px;text-align:center;font-size:52px;color:var(--tinta);font-weight:800}
.tx.pu .fu{display:block;width:0;height:74px;border-right:4px dashed rgba(18,15,28,.55);margin-right:20px}
/* CTA: botão violeta com seta para baixo/esquerda + "toca no produto" */
#toque{z-index:8}
#tq-b{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border-radius:50%;background:var(--violeta);
  box-shadow:0 0 0 6px var(--tinta),0 12px 26px rgba(0,0,0,.5)}
#tq-b svg{display:block;width:116px;height:116px}
#tq-o{position:absolute;left:56px;top:1404px;width:116px;height:116px;display:block;border:7px solid var(--violeta);border-radius:50%;opacity:0}
#tq-l{position:absolute;left:192px;top:1428px;display:block;white-space:nowrap;background:var(--tinta);color:var(--papel);
  font-family:"Pop Role";font-weight:800;font-size:38px;line-height:1;padding:16px 26px 18px;border-radius:40px;box-shadow:inset 0 0 0 3px var(--violeta)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- clipes em tela cheia: G escritório / H fogueira / E mirante; nada de G 1,9-2,4 nem H 3,2-4,3 -->
%%VIDEOS%%

  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="5"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="11"></div>

  <!-- intro: "QUAL SEU ROLÊ?" já no quadro 0 -->
  <div id="t1" class="clip titulo" data-start="0" data-duration="%%D_T1%%" data-track-index="6">
    <div class="tw" style="top:196px"><div id="t1-l" class="tt bric" style="font-size:128px"><span>QUAL SEU</span><span id="t1-b" class="blk">ROLÊ?</span></div></div>
  </div>

  <!-- apresentação: "garrafa térmica" + pulseira que troca MODUS / AÇO INOX 304* / RESISTE À CORROSÃO* / BOCA LARGA -->
  <div id="t2" class="clip titulo" data-start="%%T2S%%" data-duration="%%D_T2%%" data-track-index="7">
    <div class="tw" style="top:200px"><span id="t2-k" class="kick">garrafa térmica</span></div>
    <span id="lt1" class="lt"><i class="cn"></i><b style="font-size:104px">MODUS</b></span>
    <span id="lt2" class="lt"><i class="cn"></i><b style="font-size:100px">AÇO INOX 304<sup>*</sup></b></span>
    <span id="lt3" class="lt"><i class="cn"></i><b style="font-size:84px">RESISTE À CORROSÃO<sup>*</sup></b></span>
    <span id="lt4" class="lt"><i class="cn"></i><b style="font-size:104px">BOCA LARGA</b></span>
  </div>
  <div id="rod" class="clip" data-start="%%P1%%" data-duration="%%D_ROD%%" data-track-index="8"><span id="rod-t">*Dados do fabricante</span></div>

  <!-- CTA: balão "ONDE VOCÊ USARIA?" antes do toque; botão com seta para baixo/esquerda em "toca" -->
  <div id="t3" class="clip titulo" data-start="%%T_BOLHA%%" data-duration="%%D_BOLHA%%" data-track-index="6">
    <span id="bolha"><em>comenta:</em><b class="bric">ONDE VOCÊ USARIA?</b><i></i></span>
  </div>
  <div id="toque" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="10">
    <i id="tq-o"></i>
    <span id="tq-b"><svg id="tq-s" viewBox="0 0 116 116"><path d="M78 38 L40 76 M38 48 L38 78 L68 78" fill="none" stroke="#FFF8EE" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
    <span id="tq-l">toca no produto</span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="9"></div>
  <div id="fl2" class="clip flash" data-start="%%T_FL2%%" data-duration="0.14" data-track-index="9"></div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="%%V1%%" data-duration="%%DV1%%" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="%%V2%%" data-duration="%%DV2%%" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="%%V3%%" data-duration="%%DV3%%" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-curto-1" data-start="%%SW1%%" data-duration="0.35" data-track-index="15" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="%%SW2%%" data-duration="0.55" data-track-index="14" data-volume="0.34" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%SPOP1%%" data-duration="0.2" data-track-index="15" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.32" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="15" data-volume="0.32" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whoosh-curto-2" data-start="%%SW3%%" data-duration="0.35" data-track-index="14" data-volume="0.28" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-2" data-start="%%SPOP2%%" data-duration="0.2" data-track-index="15" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-subida-1" data-start="%%SSUB%%" data-duration="0.5" data-media-start="0.9" data-track-index="14" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="15" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO: G (trabalho) -> H (acampamento) -> E (trilha); cada opção carimba sobre o seu cenário ----
tl.fromTo("#fl1", {opacity:0.18}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camG1", {scale:1.1}, {scale:1.03, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camG1", {scale:1.05, duration:%%DG1%%, ease:"none"}, 0.4);
tl.fromTo("#camG1", {x:0, y:0}, {keyframes:[{x:14, y:-8, duration:0.05}, {x:-11, y:6, duration:0.06}, {x:7, y:-4, duration:0.06}, {x:0, y:0, duration:0.08}], ease:"none", immediateRender:false}, 0.02);
tl.fromTo("#t1-l", {scale:1.22, transformOrigin:"0% 50%"}, {scale:1, duration:0.3, ease:"back.out(1.8)"}, 0);
tl.fromTo("#t1-b", {rotation:-10, scale:1.15, transformOrigin:"0% 50%"}, {rotation:-3, scale:1, duration:0.34, ease:"back.out(2)"}, 0.02);
tl.fromTo("#camH1", {scale:1.08}, {scale:1.02, duration:0.25, ease:"power3.out"}, %%C1%%);
tl.to("#camH1", {scale:1.04, duration:%%DH1%%, ease:"none"}, %%C1B%%);
tl.fromTo("#camE1", {scale:1.08, x:40}, {scale:1.02, x:0, duration:0.25, ease:"power3.out"}, %%C2%%);
tl.to("#camE1", {scale:1.045, duration:%%DE1%%, ease:"none"}, %%C2B%%);
// "QUAL SEU ROLÊ?" dá um soco em "qual" e o bloco treme em "rolê"
tl.fromTo("#t1-l", {scale:1}, {scale:1.06, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TQUAL%%);
tl.fromTo("#t1-b", {rotation:-3}, {keyframes:[{rotation:-8, duration:0.06}, {rotation:2, duration:0.08}, {rotation:-3, duration:0.08}], ease:"none", immediateRender:false}, %%TROLE%%);
// passagem E -> H em "rolê": zoom com desfoque + flash curto
tl.to("#camE1", {scale:1.1, filter:"blur(16px)", duration:0.16, ease:"power2.in"}, %%C3OUT%%);
tl.fromTo("#fl2", {opacity:0}, {keyframes:[{opacity:0.5, duration:0.04}, {opacity:0, duration:0.1}], ease:"none"}, %%T_FL2%%);
tl.fromTo("#camH2", {scale:1.1, filter:"blur(16px)"}, {scale:1.02, filter:"blur(0px)", duration:0.28, ease:"power3.out"}, %%C3%%);
tl.to("#camH2", {scale:1.05, duration:%%DH2%%, ease:"none"}, %%C3B%%);
tl.to("#t1-l", {x:-140, opacity:0, duration:0.18, ease:"power2.in"}, %%T1OUT%%);

// ---- APRESENTAÇÃO: pulseira troca no tempo da voz; produto herói em "MODUS" (zoom 1,10x na garrafa no alto) ----
tl.fromTo("#t2-k", {y:24, opacity:0}, {y:0, opacity:1, duration:0.22, ease:"power3.out"}, %%TGARRAFA%%);
tl.fromTo("#camG2", {scale:1.07}, {scale:1.02, duration:0.24, ease:"power3.out"}, %%C4%%);
tl.to("#camG2", {scale:1.1, duration:0.55, ease:"power2.inOut"}, %%THERO%%);
tl.to("#camG2", {x:-14, duration:%%DG2A%%, ease:"none"}, %%THERO2%%);
tl.to("#camG2", {scale:1.05, x:0, duration:0.3, ease:"power2.inOut"}, %%TRES0%%);
tl.to("#camG2", {scale:1.06, duration:%%DG2B%%, ease:"none"}, %%TRES1%%);
%%LETREIRO%%
tl.fromTo("#camH3", {scale:1.08, x:-60}, {scale:1.02, x:0, duration:0.26, ease:"power3.out"}, %%C5%%);
tl.to("#camH3", {scale:1.045, duration:%%DH3%%, ease:"none"}, %%C5B%%);
tl.fromTo("#rod-t", {opacity:0, y:12}, {opacity:1, y:0, duration:0.24, ease:"power2.out"}, %%P1%%);
tl.fromTo("#rod-t", {scale:1}, {scale:1.12, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false, transformOrigin:"0% 50%"}, %%TSEGUNDO%%);
tl.fromTo("#camG3", {scale:1.07}, {scale:1.02, duration:0.24, ease:"power3.out"}, %%C6%%);
tl.to("#camG3", {scale:1.05, duration:%%DG3A%%, ease:"none"}, %%C6B%%);
tl.to("#camG3", {scale:1.09, duration:0.12, ease:"power2.out"}, %%TBOCA%%);
tl.to("#camG3", {scale:1.07, duration:0.45, ease:"power2.inOut"}, %%TBOCA2%%);
tl.to("#camG3", {scale:1.075, duration:%%DG3B%%, ease:"none"}, %%TBOCA3%%);
tl.fromTo("#camH4", {scale:1.07}, {scale:1.03, duration:0.24, ease:"power3.out"}, %%C7%%);
tl.to("#camH4", {scale:1.05, duration:%%DH4A%%, ease:"none"}, %%C7B%%);
// saída da apresentação: chicote lateral com desfoque
tl.to("#camH4", {scale:1.1, x:-90, filter:"blur(14px)", duration:0.15, ease:"power2.in"}, %%C8OUT%%);
tl.to(["#t2-k", "#lt4"], {x:-140, opacity:0, duration:0.16, ease:"power2.in"}, %%T2OUT%%);

// ---- CTA: E entra em chicote; balão no respiro; botão com seta em "toca" ----
tl.fromTo("#camE2", {scale:1.09, x:110, filter:"blur(14px)"}, {scale:1.02, x:0, filter:"blur(0px)", duration:0.3, ease:"power3.out"}, %%C8%%);
tl.to("#camE2", {scale:1.04, duration:%%DE2A%%, ease:"none"}, %%C8B%%);
tl.to("#camE2", {scale:1.06, duration:0.24, ease:"power2.out"}, %%TTOCA%%);
tl.to("#camE2", {scale:1.075, duration:%%DE2B%%, ease:"none"}, %%TTOCA2%%);
tl.fromTo("#bolha", {scale:0.3, opacity:0, transformOrigin:"12% 100%"}, {scale:1, opacity:1, duration:0.6, ease:"elastic.out(1,0.55)"}, %%T_BOLHA%%);
tl.fromTo("#bolha", {rotation:0}, {keyframes:[{rotation:-3, duration:0.08}, {rotation:3, duration:0.12}, {rotation:0, duration:0.1}], ease:"none", immediateRender:false}, %%TUSARIA%%);
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

# letreiro: entra carimbado; o anterior sai para cima
LT = [("lt1", T_MODUS), ("lt2", T_ACO), ("lt3", T_RESISTE), ("lt4", T_BOCA)]
lt_js = []
for i, (lid, t) in enumerate(LT):
    t0 = round(t - 0.05, 3)
    if i:
        lt_js.append(f'tl.to("#{LT[i-1][0]}", {{y:-50, opacity:0, duration:0.12, ease:"power2.in"}}, {R(t0 - 0.06)});')
    lt_js.append(f'tl.fromTo("#{lid}", {{opacity:0, scale:1.35, rotation:-8, transformOrigin:"10% 50%"}}, '
                 f'{{opacity:1, scale:1, rotation:-2, duration:0.2, ease:"back.out(2)"}}, {R(t0)});')

T1OUT = round(P1 - 0.3, 3)
THERO = round(T_MODUS - 0.06, 3)
TRES0 = round(T_RESISTE - 0.05, 3)
T_BOLHA = round(P2 - 0.1, 3)
TPULSO = round(T_TOCA0 + 0.3, 3)
REP = int(((TOTAL - 0.05) - TPULSO) / 0.22) - 1
REP -= (REP + 1) % 2 == 1
C1, C2, C3, C4, C5, C6, C7, C8 = (S[k][2] for k in ("H1", "E1", "H2", "G2", "H3", "G3", "H4", "E2"))
TBOCA = round(T_BOCA - 0.05, 3)
TTOCA = T_TOCA0
subs = {
    "TOTAL": R(TOTAL), "VIDEOS": "\n".join(videos), "LETREIRO": "\n".join(lt_js),
    "D_T1": R(T1OUT + 0.2), "T1OUT": R(T1OUT),
    "C1": R(C1), "C1B": R(C1 + 0.25), "DH1": R(C2 - C1 - 0.25 - 0.003),
    "C2": R(C2), "C2B": R(C2 + 0.25), "DE1": R(C3 - 0.16 - C2 - 0.25 - 0.003),
    "DG1": R(C1 - 0.4 - 0.003),
    "TQUAL": R(t_pal("intro", 4) - 0.03), "TROLE": R(t_pal("intro", 8)),
    "C3OUT": R(C3 - 0.16), "T_FL2": R(C3 - 0.04), "C3": R(C3), "C3B": R(C3 + 0.28), "DH2": R(C4 - C3 - 0.28 - 0.003),
    "T2S": R(T_GARRAFA - 0.05), "D_T2": R(P2 - (T_GARRAFA - 0.05)), "TGARRAFA": R(T_GARRAFA - 0.03),
    "C4": R(C4), "THERO": R(THERO), "THERO2": R(THERO + 0.55), "DG2A": R(TRES0 - THERO - 0.55 - 0.003),
    "TRES0": R(TRES0), "TRES1": R(TRES0 + 0.3), "DG2B": R(C5 - TRES0 - 0.3 - 0.003),
    "C5": R(C5), "C5B": R(C5 + 0.26), "DH3": R(C6 - C5 - 0.26 - 0.003),
    "P1": R(P1), "D_ROD": R(P2 - P1), "TSEGUNDO": R(T_SEGUNDO),
    "C6": R(C6), "C6B": R(C6 + 0.24), "DG3A": R(TBOCA - C6 - 0.24 - 0.003),
    "TBOCA": R(TBOCA), "TBOCA2": R(TBOCA + 0.12), "TBOCA3": R(TBOCA + 0.57), "DG3B": R(C7 - TBOCA - 0.57 - 0.003),
    "C7": R(C7), "C7B": R(C7 + 0.24), "DH4A": R(C8 - 0.15 - C7 - 0.24 - 0.003), "C8OUT": R(C8 - 0.15),
    "T2OUT": R(C8 - 0.12),
    "C8": R(C8), "C8B": R(C8 + 0.3), "DE2A": R(TTOCA - C8 - 0.3 - 0.003),
    "T_BOLHA": R(T_BOLHA), "D_BOLHA": R(TOTAL - T_BOLHA), "TUSARIA": R(T_USARIA),
    "TTOCA": R(TTOCA), "TTOCA1": R(TTOCA + 0.08), "TTOCA2": R(TTOCA + 0.24), "DE2B": R(TOTAL - TTOCA - 0.24),
    "DTOCA": R(TOTAL - TTOCA), "TPULSO": R(TPULSO), "REP": str(REP), "TONDA2": R(TTOCA + 0.95),
    "V1": R(VOZ["intro"]), "V2": R(VOZ["apresentacao"]), "V3": R(VOZ["cta"]),
    "DV1": R(DV["intro"]), "DV2": R(DV["apresentacao"]), "DV3": R(DV["cta"]),
    "SW1": R(C2 - 0.06), "SW2": R(C3 - 0.08), "SPOP1": R(T_MODUS - 0.07), "STIQ1": R(T_ACO - 0.06),
    "STIQ2": R(T_RESISTE - 0.06), "SW3": R(C6 - 0.05), "SPOP2": R(TBOCA - 0.03), "SSUB": R(P2 - 0.5),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
assert VOZ["intro"] + DV["intro"] <= VOZ["apresentacao"] and VOZ["apresentacao"] + DV["apresentacao"] <= VOZ["cta"]
assert VOZ["cta"] + DV["cta"] <= TOTAL
assert THERO + 0.55 < TRES0 and TBOCA + 0.57 < C7 and C6 + 0.24 < TBOCA
open(OUT, "w").write(html)
print("ok", OUT, "| total", TOTAL, "| P1", P1, "P2", P2)
for s in segs:
    print("  %-3s %s  vídeo %6.3f-%6.3f  mídia %5.3f-%5.3f  %.4fx" % (s[0], s[1], s[2], s[3], s[4], s[6], s[5]))
print("  MODUS", T_MODUS, "aço", T_ACO, "resiste", T_RESISTE, "segundo", T_SEGUNDO, "boca", T_BOCA, "| bolha", T_BOLHA, "toca", TTOCA)
