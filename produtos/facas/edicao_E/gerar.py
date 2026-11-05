#!/usr/bin/env python3
"""Gera produtos/facas/edicao_E/index.html ("Pegada firme": nanquim #0D0E10 / osso #F2EDE3 / turquesa-ferramenta #19E0C4,
Bebas Neue + Poppins 800, legenda karaokê "empunhadura"). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida>

Lote E (rotação, sem clipe novo). Regra da 3ª violação: o vídeo roda do primeiro ao último quadro; não há <img>,
quadro congelado, cartão nem Ken Burns. Trechos permitidos: I 0-2,4 · H 0-6,25 · G 0-5,0 · E 0-4,5 (parado depois de 4,3).
  intro   I  0,00-2,40 a 0,80x  ( 0,00- 3,00)  cutelo entrando na carne, fogo e fumaça
  apres.  H  0,20-5,30 a 1,00x  ( 3,00- 8,10)  kit inteiro + tesoura no cheiro-verde ("seis peças", "aço inoxidável")
          G  0,55-4,90 a 0,95x  ( 8,10-12,68)  faca do chefe partindo a cebola ("o cabo encaixa na mão", "Pegada firme")
  CTA     E  0,10-4,49 a 0,858x (12,68-17,80)  peças deslizando até formar o kit
Transições "seis lâminas": 6 faixas opacas nanquim de borda dura (filete turquesa) que se cruzam e cobrem a tela no corte.
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

P1, CUT, P2, TOTAL = 3.0, 8.1, 12.68, 17.8
VOZ = {"intro": 0.2, "apresentacao": 3.2, "cta": 12.98}
FIM = {"intro": P1, "apresentacao": P2, "cta": TOTAL}
DUR_MP3 = {"intro": 2.736, "apresentacao": 9.432, "cta": 4.68}

# vídeos: (id, clipe, início, fim, media-start, velocidade, limite de media permitido)
VIDS = [("I", "I", 0.0, P1, 0.0, 0.8, 2.4), ("H", "H", P1, CUT, 0.2, 1.0, 6.25),
        ("G", "G", CUT, P2, 0.55, 0.95, 5.0), ("E", "E", P2, TOTAL, 0.1, 0.858, 4.5)]
for _, _, a, b, m, r, lim in VIDS:
    assert m + (b - a) * r <= lim + 1e-6, (a, b, m, r, m + (b - a) * r)
for p in VOZ:
    assert VOZ[p] + DUR_MP3[p] <= FIM[p], p

CAP_W = 78  # px da legenda
GRUPOS = {
    "intro": [[0, 1], [2], [3, 4, 5], [6], [7, 8]],
    "apresentacao": [[0], [1, 2, 3], [4], [5, 6], [7, 8, 9], [10], [11, 12, 13], [14], [15, 16], [17], [18],
                     [19, 20], [21, 22], [23]],
    "cta": [[0, 1], [2, 3, 4], [5, 6], [7], [8, 9], [10, 11], [12, 13]],
}
CHAVE = {"intro": {2, 5, 6}, "apresentacao": {2, 9, 10, 13, 16, 18, 23}, "cta": {6, 7, 9, 13}}
EXIBE = {("intro", 8): "mão?", ("apresentacao", 3): "peças.", ("apresentacao", 6): "fabricante,",
         ("apresentacao", 10): "inoxidável,", ("apresentacao", 16): "mão.", ("apresentacao", 23): "corte.",
         ("cta", 6): "gaveta?", ("cta", 13): "confira."}


def T(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


def cap_top(parte, s):
    if parte == "intro":
        return 604
    if parte == "cta":
        return 288
    return 1020 if s < CUT else 604   # H: sobre as ervas, acima da tesoura; G: logo abaixo do título


R = lambda v: str(round(v, 3))

# ---------------- legenda karaokê "empunhadura" ----------------
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz, pal = VOZ[parte], falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.06, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.06, 3), fim_voz) if gi + 1 < len(grupos) else min(fim_voz, FIM[parte] - 0.1)
        if parte == "apresentacao" and s < CUT:
            e = min(e, CUT)
        gid = f"lg{parte[:3]}{gi}"
        spans = ""
        for k, wi in enumerate(g):
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            ch = wi in CHAVE[parte]
            spans += (f'<span id="{gid}w{k}" class="w{" k" if ch else ""}"><span class="b">{txt}</span>'
                      f'<span id="{gid}f{k}" class="f">{txt}</span></span>')
            t0 = max(s + 0.04, round(voz + pal[wi]["inicio"] - 0.02, 3))
            dur = max(0.12, min(0.3, pal[wi]["fim"] - pal[wi]["inicio"]))
            leg_js.append(f'tl.fromTo("#{gid}f{k}",{{width:"0%"}},{{width:"100%",duration:{R(dur)},ease:"power1.out"}},{R(t0)});')
            if ch:
                leg_js.append(f'tl.fromTo("#{gid}w{k}",{{scale:1}},{{scale:1.08,duration:0.1,yoyo:true,repeat:1,ease:"power2.out",immediateRender:false}},{R(t0 + 0.04)});')
        leg_js.append(f'tl.fromTo("#{gid}p",{{scaleX:1.12,scaleY:0.84}},{{scaleX:1,scaleY:1,duration:0.16,ease:"back.out(2.2)"}},{R(s)});')
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{R(s)}" data-duration="{R(e - s)}" data-track-index="12">'
                        f'<div class="cap" style="top:{cap_top(parte, s)}px"><div id="{gid}p" class="placa">{spans}</div></div></div>')

# ---------------- tempos-chave ----------------
t_danc, t_mao_i = T("intro", 6), T("intro", 8)
t_seis, t_seg, t_aco = T("apresentacao", 2), T("apresentacao", 4), T("apresentacao", 9)
t_cabo, t_peg, t_firme, t_corte = T("apresentacao", 13), T("apresentacao", 17), T("apresentacao", 18), T("apresentacao", 23)
t_gav, t_toque, t_conf = T("cta", 6), T("cta", 7), T("cta", 13)
fim_conf = round(VOZ["cta"] + falas["cta"]["palavras"][13]["fim"], 3)

# ---------------- transições "seis lâminas" ----------------
def slats(nome, tcut):
    html = "".join(f'<i id="{nome}s{i}" class="sl {"pe" if i % 2 == 0 else "pd"}" style="top:{i * 320}px"></i>' for i in range(6))
    js = []
    for i in range(6):
        d = -1 if i % 2 == 0 else 1
        js.append(f'tl.fromTo("#{nome}s{i}",{{x:{d * 1120}}},{{x:0,duration:0.12,ease:"power2.in"}},{R(tcut - 0.18 + i * 0.012)});')
        js.append(f'tl.to("#{nome}s{i}",{{x:{-d * 1120},duration:0.12,ease:"power2.out"}},{R(tcut + i * 0.012)});')
    return html, "\n".join(js)


SL1, SL1JS = slats("a", P1)
SL2, SL2JS = slats("b", P2)

SETA = ('<svg viewBox="0 0 96 96" width="96" height="96"><path d="M74 22 L28 68 M26 34 L26 70 L62 70" fill="none" '
        'stroke="#0D0E10" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/></svg>')

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Bebas Pegada";src:local("Bebas Neue Regular"),local("BebasNeue-Regular"),local("Bebas Neue")}
@font-face{font-family:"Poppins Pegada";font-weight:800;src:local("Poppins ExtraBold"),local("Poppins-ExtraBold")}
@font-face{font-family:"Poppins Pegada";font-weight:700;src:local("Poppins Bold"),local("Poppins-Bold")}
:root{--nq:#0D0E10;--osso:#F2EDE3;--tq:#19E0C4}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#0D0E10}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#0D0E10;font-family:"Poppins Pegada";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camI{transform-origin:430px 950px}
#camH{transform-origin:540px 600px}
#camG{transform-origin:760px 950px}
#camE{transform-origin:540px 700px}
/* brilho no aço (H parado na fila, vídeo rodando) */
#sheen{z-index:3;mix-blend-mode:screen}
#shbox{position:absolute;left:70px;top:400px;width:760px;height:620px;overflow:hidden;-webkit-mask-image:linear-gradient(to bottom,transparent,#000 18%,#000 82%,transparent);mask-image:linear-gradient(to bottom,transparent,#000 18%,#000 82%,transparent)}
#shk{position:absolute;left:0;top:-120px;width:200px;height:880px;transform:skewX(-20deg)}
#sh{position:absolute;left:0;top:0;width:200px;height:880px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.62) 50%,rgba(255,255,255,0))}
.flash{z-index:20;background:#FFFFFF;opacity:0}
/* títulos: Bebas osso com sombra dura nanquim, palavra-chave turquesa */
.tt{z-index:6}
.ln{position:absolute;left:48px;font-family:"Bebas Pegada";color:var(--osso);line-height:.92;white-space:nowrap;
  text-shadow:6px 6px 0 #0D0E10,0 0 30px rgba(0,0,0,.5)}
.mk{position:absolute;left:0;overflow:hidden;padding:4px 80px 14px 48px}
.mk .ln{position:relative;left:0;display:block}
.q{color:var(--tq)}
.wd{position:relative;display:inline-block}
.br{position:absolute;top:2%;bottom:14%;width:34px;border:13px solid var(--tq);display:block;box-shadow:4px 4px 0 #0D0E10}
.br.l{left:-40px;border-right-width:0}
.br.r{right:-44px;border-left-width:0}
.chip{position:absolute;left:48px;display:block;background:var(--nq);color:var(--tq);font-family:"Poppins Pegada";font-weight:800;
  font-size:38px;line-height:1;padding:9px 18px 10px;white-space:nowrap;transform-origin:0 50%}
/* legenda karaokê "empunhadura": placa nanquim com cabo turquesa, palavra enche da esquerda (largura, sem clip-path) */
.legenda{z-index:9}
.cap{position:absolute;left:48px;display:flex;align-items:flex-start}
.placa{position:relative;display:flex;gap:20px;align-items:center;background:var(--nq);padding:11px 30px 15px 44px;transform-origin:0 50%}
.placa::before{content:"";position:absolute;left:0;top:0;bottom:0;width:14px;background:var(--tq)}
.w{position:relative;display:block;font-family:"Poppins Pegada";font-weight:800;font-size:%%CAPW%%px;line-height:1.05;white-space:nowrap;
  color:rgba(242,237,227,.3);transform-origin:50% 60%}
.w .b{display:block}
.w .f{position:absolute;left:0;top:0;display:block;color:var(--osso);width:0;overflow:hidden;white-space:nowrap}
.w.k .f{color:var(--tq)}
/* rodapé */
#rodape{z-index:8}
.rod{position:absolute;left:48px;top:1462px;display:block;font-family:"Poppins Pegada";font-weight:700;font-size:30px;line-height:1;
  color:rgba(242,237,227,.8);background:rgba(13,14,16,.6);padding:7px 14px 8px}
/* CTA: selo turquesa com seta para baixo/esquerda */
#selo{z-index:10}
#selo-d{position:absolute;left:14px;top:1430px;width:96px;height:96px;border-radius:50%;background:var(--tq);display:block;
  box-shadow:0 0 0 6px #0D0E10}
#selo-d svg{display:block}
.onda{position:absolute;left:14px;top:1430px;width:96px;height:96px;border-radius:50%;border:7px solid var(--tq);display:block;opacity:0}
/* transições: seis lâminas opacas */
.slats{z-index:18;overflow:hidden}
.sl{position:absolute;left:0;width:1080px;height:322px;display:block;background:var(--nq)}
.sl.pe{border-right:12px solid var(--tq)}
.sl.pd{border-left:12px solid var(--tq)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
%%VIDEOS%%

  <div id="sheen" class="clip" data-start="6.42" data-duration="1.0" data-track-index="3"><div id="shbox"><div id="shk"><i id="sh"></i></div></div></div>

  <!-- INTRO: FACA DANÇANDO? -->
  <div id="t0" class="clip tt" data-start="0" data-duration="2.98" data-track-index="6">
    <div class="ln" id="t0a" style="top:196px;font-size:172px">FACA</div>
    <div class="ln" id="t0b" style="top:354px;font-size:172px"><span id="t0w" class="wd q">DANÇANDO?</span></div>
    <span id="t0c" class="chip" style="top:540px">bem na hora do corte</span>
  </div>
  <!-- APRESENTAÇÃO (G): aço inox e cabo que encaixa / PEGADA FIRME* -->
  <div id="t1" class="clip tt" data-start="%%CUT%%" data-duration="%%DT1%%" data-track-index="6">
    <span id="t1c" class="chip" style="top:196px;font-size:36px">aço inox e cabo que encaixa</span>
    <div class="mk" style="top:248px"><div class="ln" id="t1a" style="font-size:172px">PEGADA</div></div>
    <div class="mk" style="top:404px"><div class="ln" id="t1b" style="font-size:172px"><span class="wd q">FIRME<i id="b1l" class="br l"></i><i id="b1r" class="br r"></i></span><span style="margin-left:54px">*</span></div></div>
  </div>
  <!-- CTA: ADEUS, FACA DA GAVETA -> TOQUE NO PRODUTO -->
  <div id="t2" class="clip tt" data-start="12.8" data-duration="%%DT2%%" data-track-index="7">
    <div class="mk" style="top:176px"><div class="ln" id="t2a" style="font-size:98px">ADEUS, FACA DA <span id="t2g" class="wd q">GAVETA</span></div></div>
  </div>
  <div id="t3" class="clip tt" data-start="%%TQ0%%" data-duration="%%DT3%%" data-track-index="7">
    <div class="ln" id="t3a" style="top:190px;font-size:104px">TOQUE NO <span class="wd q" style="margin-left:56px">PRODUTO<i id="b3l" class="br l"></i><i id="b3r" class="br r"></i></span></div>
  </div>
  <div id="selo" class="clip" data-start="%%TQ0%%" data-duration="%%DT3%%" data-track-index="11">
    <i id="onda1" class="onda"></i><i id="onda2" class="onda"></i>
    <span id="selo-d">%%SETA%%</span>
  </div>

  <div id="rodape" class="clip" data-start="%%P1%%" data-duration="%%DROD%%" data-track-index="10"><span class="rod">*Dados do fabricante</span></div>

  <div id="fl1" class="clip flash" data-start="0.034" data-duration="0.12" data-track-index="13"></div>
  <div id="sla" class="clip slats" data-start="%%SLA0%%" data-duration="0.4" data-track-index="14">%%SL1%%</div>
  <div id="slb" class="clip slats" data-start="%%SLB0%%" data-duration="0.4" data-track-index="15">%%SL2%%</div>

%%LEG%%

  <audio id="voz-intro" data-start="%%VZ1%%" data-duration="%%DV1%%" data-track-index="16" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="%%VZ2%%" data-duration="%%DV2%%" data-track-index="16" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="%%VZ3%%" data-duration="%%DV3%%" data-track-index="16" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="17" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="2.8" data-duration="0.45" data-track-index="18" data-volume="0.36" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-brilho-1" data-start="6.42" data-duration="0.9" data-track-index="17" data-volume="0.28" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-whoosh-2" data-start="8.04" data-duration="0.3" data-track-index="18" data-volume="0.34" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="9.6" data-duration="0.03" data-track-index="17" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-subida-1" data-start="12.3" data-duration="0.38" data-media-start="1.02" data-track-index="18" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TCLQ%%" data-duration="0.05" data-track-index="17" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%TPOP%%" data-duration="0.09" data-track-index="17" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (I 0-2,4 a 0,8x): flash + punch 1,2 -> 1,0 no cutelo; título bate; DANÇANDO? dança na palavra ----
tl.fromTo("#fl1", {opacity:0.75}, {opacity:0, duration:0.1, ease:"power1.out", immediateRender:false}, 0.034);
tl.fromTo("#camI", {scale:1.2}, {scale:1.0, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camI", {scale:1.07, duration:2.6, ease:"none"}, 0.4);
tl.fromTo("#t0a", {scale:1.8, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2)", transformOrigin:"0% 60%"}, 0.02);
tl.fromTo("#t0b", {scale:1.8, opacity:0}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2)", transformOrigin:"0% 60%"}, 0.12);
tl.fromTo("#t0c", {scaleX:0}, {scaleX:1, duration:0.16, ease:"power3.out"}, 0.62);
tl.fromTo("#t0w", {rotation:0}, {rotation:-5, duration:0.07, ease:"sine.out", transformOrigin:"50% 85%", immediateRender:false}, %%TDANC%%);
tl.fromTo("#t0w", {rotation:-5}, {rotation:5, duration:0.09, yoyo:true, repeat:4, ease:"sine.inOut", transformOrigin:"50% 85%", immediateRender:false}, %%TDANC07%%);
tl.to("#t0w", {rotation:0, duration:0.1, ease:"power2.out"}, %%TDANCF%%);
tl.to(["#t0a", "#t0b", "#t0c"], {x:-1100, duration:0.16, ease:"power2.in", stagger:0.02}, 2.74);
%%SL1JS%%

// ---- APRESENTAÇÃO 1 (H 0,2-5,3): kit inteiro, "seis peças", brilho no aço ----
tl.fromTo("#camH", {scale:1.06}, {scale:1.0, duration:0.3, ease:"power3.out"}, %%P1%%);
tl.to("#camH", {scale:1.015, duration:%%DH1%%, ease:"none"}, %%P1_30%%);
tl.fromTo("#camH", {scale:1.015}, {scale:1.05, duration:0.12, ease:"power2.out", immediateRender:false}, %%TSEIS%%);
tl.to("#camH", {scale:1.03, duration:0.3, ease:"power2.inOut"}, %%TSEIS12%%);
tl.set("#camH", {transformOrigin:"440px 690px"}, %%TSEG%%);
tl.to("#camH", {scale:1.1, duration:%%DH2%%, ease:"sine.inOut"}, %%TSEG%%);
tl.fromTo("#sh", {x:-280}, {x:1000, duration:0.95, ease:"power1.inOut"}, 6.44);

// ---- APRESENTAÇÃO 2 (G 0,55-4,9 a 0,95x): cabo na mão (produto herói), PEGADA FIRME* com grampo ----
tl.fromTo("#camG", {scale:1.13}, {scale:1.04, duration:0.2, ease:"power3.out"}, %%CUT%%);
tl.to("#camG", {scale:1.2, duration:%%DG1%%, ease:"sine.inOut"}, %%TCABO%%);
tl.fromTo("#t1c", {scaleX:0}, {scaleX:1, duration:0.16, ease:"power3.out"}, %%CUT12%%);
tl.to("#camG", {scale:1.08, duration:0.2, ease:"power3.out"}, %%TPEG%%);
tl.to("#camG", {scale:1.13, duration:%%DG2%%, ease:"none"}, %%TPEG20%%);
tl.fromTo("#t1a", {yPercent:110}, {yPercent:0, duration:0.2, ease:"power3.out"}, %%TPEG%%);
tl.fromTo("#t1b", {yPercent:110}, {yPercent:0, duration:0.2, ease:"power3.out"}, %%TFIRME02%%);
tl.fromTo("#b1l", {x:-90, opacity:0}, {x:0, opacity:1, duration:0.14, ease:"power4.in"}, %%TFIRME12%%);
tl.fromTo("#b1r", {x:90, opacity:0}, {x:0, opacity:1, duration:0.14, ease:"power4.in"}, %%TFIRME12%%);
tl.fromTo("#t1b", {scaleX:1}, {scaleX:0.95, duration:0.06, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 50%", immediateRender:false}, %%TFIRME26%%);
tl.fromTo("#camG", {scale:1.11}, {scale:1.15, duration:0.12, ease:"power2.out", immediateRender:false}, %%TCORTE%%);
tl.to("#camG", {scale:1.13, duration:0.4, ease:"power2.inOut"}, %%TCORTE12%%);
tl.to(["#t1c", "#t1a", "#t1b"], {x:-1100, duration:0.16, ease:"power2.in", stagger:0.02}, 12.42);
%%SL2JS%%

// ---- CTA (E 0,1-4,49 a 0,858x): mais calma; TOQUE NO PRODUTO com grampo e selo para baixo/esquerda ----
tl.fromTo("#camE", {scale:1.05}, {scale:1.0, duration:0.35, ease:"power3.out"}, %%P2%%);
tl.to("#camE", {scale:1.03, duration:%%DE1%%, ease:"none"}, %%P2_35%%);
tl.fromTo("#t2a", {yPercent:110}, {yPercent:0, duration:0.24, ease:"power3.out"}, 12.84);
tl.fromTo("#t2g", {scale:1}, {scale:1.08, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 60%", immediateRender:false}, %%TGAV%%);
tl.to("#t2a", {yPercent:-110, duration:0.14, ease:"power2.in"}, %%TQ0M%%);
tl.fromTo("#t3a", {scale:1.6, opacity:0}, {scale:1, opacity:1, duration:0.22, ease:"back.out(2)", transformOrigin:"0% 60%"}, %%TQ0%%);
tl.fromTo("#b3l", {x:-80, opacity:0}, {x:0, opacity:1, duration:0.14, ease:"power4.in"}, %%TQ12%%);
tl.fromTo("#b3r", {x:80, opacity:0}, {x:0, opacity:1, duration:0.14, ease:"power4.in"}, %%TQ12%%);
tl.fromTo("#selo-d", {scale:0, rotation:-40}, {scale:1, rotation:0, duration:0.26, ease:"back.out(2.4)"}, %%TQ0%%);
tl.fromTo("#onda1", {scale:0.7, opacity:0.95}, {scale:2.2, opacity:0, duration:0.7, ease:"power2.out"}, %%TQ10%%);
tl.fromTo("#selo-d", {x:0, y:0}, {x:-7, y:7, duration:0.26, yoyo:true, repeat:%%REPS%%, ease:"sine.inOut", immediateRender:false}, %%TQ40%%);
tl.fromTo("#onda2", {scale:0.7, opacity:0.95}, {scale:2.2, opacity:0, duration:0.7, ease:"power2.out"}, %%TCONF%%);
tl.fromTo("#onda1", {scale:0.7, opacity:0.95}, {scale:2.2, opacity:0, duration:0.7, ease:"power2.out", immediateRender:false}, %%TPOP%%);

// ---- legenda ----
%%LEGJS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

vids = []
for vid, clip, a, b, m, r, _ in VIDS:
    vids.append(f'  <div id="cam{vid}" class="cam"><video id="v{vid}" class="clip full" data-start="{R(a)}" data-duration="{R(b - a)}" '
                f'data-media-start="{m}" data-playback-rate="{r}" data-track-index="0" src="assets/clipe_{clip}.mp4" muted playsinline></video></div>')

tq0 = round(t_toque - 0.03, 3)
t_pop = round(fim_conf + 0.03, 3)
assert t_pop + 0.09 <= TOTAL
rep = {
    "TOTAL": R(TOTAL), "CAPW": str(CAP_W), "VIDEOS": "\n".join(vids), "SETA": SETA,
    "P1": R(P1), "P2": R(P2), "CUT": R(CUT), "SL1": SL1, "SL2": SL2, "SL1JS": SL1JS, "SL2JS": SL2JS,
    "SLA0": R(P1 - 0.2), "SLB0": R(P2 - 0.2),
    "VZ1": R(VOZ["intro"]), "VZ2": R(VOZ["apresentacao"]), "VZ3": R(VOZ["cta"]),
    "DV1": R(DUR_MP3["intro"]), "DV2": R(DUR_MP3["apresentacao"]), "DV3": R(DUR_MP3["cta"]),
    "DT1": R(P2 - CUT - 0.02), "DT2": R(tq0 + 0.16 - 12.8), "TQ0": R(tq0), "DT3": R(TOTAL - tq0), "DROD": R(P2 - P1),
    "TDANC": R(t_danc - 0.02), "TDANC07": R(t_danc + 0.05), "TDANCF": R(t_danc + 0.05 + 0.45),
    "P1_30": R(P1 + 0.3), "DH1": R(t_seis - P1 - 0.3), "TSEIS": R(t_seis), "TSEIS12": R(t_seis + 0.12),
    "TSEG": R(t_seg), "DH2": R(CUT - t_seg),
    "TCABO": R(t_cabo), "DG1": R(t_peg - t_cabo - 0.02), "CUT12": R(CUT + 0.12),
    "TPEG": R(t_peg), "TPEG20": R(t_peg + 0.2), "DG2": R(t_corte - t_peg - 0.2),
    "TFIRME02": R(t_firme - 0.02), "TFIRME12": R(t_firme + 0.12), "TFIRME26": R(t_firme + 0.26),
    "TCORTE": R(t_corte), "TCORTE12": R(t_corte + 0.12),
    "P2_35": R(P2 + 0.35), "DE1": R(TOTAL - P2 - 0.35), "TGAV": R(t_gav), "TQ0M": R(tq0 - 0.12),
    "TQ10": R(tq0 + 0.1), "TQ12": R(tq0 + 0.12), "TQ40": R(tq0 + 0.4),
    "REPS": str(int((TOTAL - tq0 - 0.4) / 0.26) - 1), "TCONF": R(t_conf), "TCLQ": R(t_toque - 0.02), "TPOP": R(t_pop),
    "LEG": "\n".join(leg_html), "LEGJS": "\n".join(leg_js),
}
for k, v in rep.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, [l for l in html.splitlines() if "%%" in l][:3]
open(OUT, "w").write(html)
print("ok", OUT, "TOTAL", TOTAL, "dançando", t_danc, "seis", t_seis, "aço", t_aco, "cabo", t_cabo, "pegada", t_peg,
      "firme", t_firme, "corte", t_corte, "toque", t_toque, "pop", t_pop)
