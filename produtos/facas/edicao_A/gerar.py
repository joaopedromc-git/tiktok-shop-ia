#!/usr/bin/env python3
"""Gera produtos/facas/edicao_A/index.html ("fio de brasa": Archivo Black / Poppins 800,
legenda sublinhado em forma de lâmina, cortes diagonais, cartão do produto com contorno brasa).
Uso: python3 gerar.py <pasta_com_fala_*.json> <saida_index.html>

Assets extras (gerados no container render com ffmpeg, ver escolhas.md):
  b_quadro.jpg = clipe_B quadro 0 (as 4 facas inteiras, com folga nas bordas), para o cartão herói
  c_quadro.jpg = clipe_C quadro 0 (kit reto, lâmina do descascador branca), abertura e fundo da CTA
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

# (início da parte, fim da parte, início da voz)
P = {"intro": (0.0, 4.85, 0.25), "apresentacao": (4.85, 14.75, 5.10), "cta": (14.75, 20.6, 15.05)}
TOTAL = 20.6
HERO = (5.9, 9.95)   # cartão das 4 facas durante a lista
CARD_C = 18.0        # o kit vira cartão e abre espaço para o botão


def topo_legenda(t):
    if HERO[0] - 0.05 <= t < HERO[1]:
        return 1290
    return 1250


GRUPOS = {
    "intro": [[0, 1], [2], [3, 4, 5], [6], [7, 8], [9], [10, 11, 12]],
    "apresentacao": [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9], [10, 11], [12, 13], [14, 15], [16], [17, 18], [19, 20],
                     [21], [22, 23]],
    "cta": [[0, 1], [2, 3], [4, 5], [6], [7, 8], [9, 10], [11, 12]],
}
CHAVE = {
    "intro": {2, 6, 9, 11, 12},
    "apresentacao": {5, 8, 9, 13, 18, 20, 23},
    "cta": {0, 1, 3, 5, 6, 8, 10},
}
TEXTO = {("intro", 6): "cortar?"}
FIM_ULTIMA = {"intro": 4.72, "apresentacao": 14.6, "cta": 20.6}


def t_pal(parte, i):
    return round(P[parte][2] + falas[parte]["palavras"][i]["inicio"], 3)


leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = P[parte][2]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.03, 3)
        e = round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.03, 3) if gi + 1 < len(grupos) else FIM_ULTIMA[parte]
        gid = f"leg-{parte}-{gi}"
        top = topo_legenda(s + 0.05)
        spans = ""
        for k, wi in enumerate(g):
            txt = TEXTO.get((parte, wi), pal[wi]["palavra"])
            t = max(s, round(voz + pal[wi]["inicio"] - 0.03, 3))
            if wi in CHAVE[parte]:
                spans += f'<span id="{gid}-{k}" class="pal k">{txt}<i id="{gid}-{k}c" class="fio"></i></span>'
                leg_js.append(f'tl.fromTo("#{gid}-{k}c",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.16,ease:"power3.out"}},{round(t + 0.07, 3)});')
            else:
                spans += f'<span id="{gid}-{k}" class="pal">{txt}</span>'
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,y:20,scale:0.88}},{{opacity:1,y:0,scale:1,duration:0.12,ease:"back.out(2)"}},{t});')
        leg_html.append(
            f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" '
            f'data-track-index="12"><div class="cap" style="top:{top}px">{spans}</div></div>'
        )

# ---- cartão herói das 4 facas (b_quadro.jpg, 1080x1920) ----
S, TX, TY = 0.596, 38.1, 191.9
JAN = (30, 215, 1050, 1815)  # janela em coordenadas do quadro (x0, y0, x1, y1)
jx0, jy0 = round(TX + S * JAN[0]), round(TY + S * JAN[1])
jx1, jy1 = round(TX + S * JAN[2]), round(TY + S * JAN[3])
INSET = f"inset({JAN[1]}px {1080 - JAN[2]}px {1920 - JAN[3]}px {JAN[0]}px round 50px)"
H0 = HERO[0]
LISTA = [("CHEFE", t_pal("apresentacao", 5)), ("CARNE", t_pal("apresentacao", 8)),
         ("CUTELO", t_pal("apresentacao", 9)), ("DESCASCAR", t_pal("apresentacao", 13))]
lista_html = "".join(
    f'<div id="li{i}" class="item" style="top:{606 + i * 112}px"><svg id="li{i}-v" viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#FF6B2C"/>'
    f'<path d="M11 21 L17.5 27.5 L29.5 13.5" fill="none" stroke="#141210" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
    f'<span id="li{i}-t">{nome}</span></div>' for i, (nome, _) in enumerate(LISTA))
lista_js = "\n".join(
    f'tl.fromTo("#li{i}",{{opacity:0,x:40}},{{opacity:0.42,x:0,duration:0.08,ease:"power2.out"}},{round(H0 + 0.26 + i * 0.02, 3)});\n'
    f'tl.to("#li{i}",{{opacity:1,duration:0.12}},{round(t - 0.04, 3)});\n'
    f'tl.fromTo("#li{i}-v",{{scale:0,rotation:-40}},{{scale:1,rotation:0,duration:0.24,ease:"back.out(2.6)"}},{round(t - 0.04, 3)});\n'
    f'tl.fromTo("#li{i}-t",{{color:"#FFF6EA"}},{{color:"#FF6B2C",duration:0.1}},{round(t - 0.04, 3)});\n'
    f'tl.to("#li{i}-t",{{color:"#FFF6EA",duration:0.3}},{round(t + 0.5, 3)});'
    for i, (_, t) in enumerate(LISTA))

# ---- CTA: posições medidas no clipe C (quadros 0-4 s, câmera quase parada) ----
PECAS = [(130, 362), (415, 344), (585, 358), (765, 598), (880, 400), (872, 1040)]  # centro do número de cada peça
cont_html = "".join(f'<b id="n{i}" class="num" style="left:{x - 29}px;top:{y - 29}px">{i + 1}</b>' for i, (x, y) in enumerate(PECAS))
cont_js = "\n".join(
    f'tl.fromTo("#n{i}",{{opacity:0,scale:2.2}},{{opacity:1,scale:1,duration:0.16,ease:"back.out(2.4)"}},{round(15.2 + i * 0.13, 3)});'
    for i in range(6))
SC, TXC, TYC = 0.86, 75.6, 40
JC = (330, 350)  # recorte em cima / embaixo do quadro
INSET_C = f"inset({JC[0]}px 0px {JC[1]}px 0px round 46px)"
ecx0, ecy0 = round(TXC), round(TYC + SC * JC[0])
ecx1, ecy1 = round(TXC + SC * 1080), round(TYC + SC * (1920 - JC[1]))

T_TOCA = t_pal("cta", 6)       # "Toca"
T_TES = t_pal("cta", 3)        # "tesoura"
T_DESC = t_pal("cta", 5)       # "descascador"
T_OND = t_pal("apresentacao", 18)   # "ondulações"
T_PROL = t_pal("apresentacao", 21)  # "prolongam"
T_DUR = t_pal("apresentacao", 23)   # "durabilidade"
T_FAQ = t_pal("intro", 9)      # "faqueiro"
T_SEIS = t_pal("intro", 11)    # "seis"

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Archivo Black";src:local("Archivo Black"),local("Archivo Black Regular"),local("ArchivoBlack-Regular")}
@font-face{font-family:"Poppins";font-weight:600;src:local("Poppins SemiBold")}
@font-face{font-family:"Poppins";font-weight:800;src:local("Poppins ExtraBold")}
:root{--base:#141210;--brasa:#FF6B2C;--texto:#FFF6EA}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#141210}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#141210}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden}
.full{width:100%;height:100%;object-fit:cover}
#camA,#camB1,#camB2,#cardC{z-index:1}
#bgC{z-index:0}
#bgC-i{position:absolute;left:-65px;top:-115px;width:1210px;height:2150px;object-fit:cover;filter:blur(26px) brightness(.5)}
#cardC{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;overflow:hidden}
/* cartão herói: quadro nítido das 4 facas sobre ele mesmo desfocado */
.hero{z-index:2;overflow:hidden}
.hbg{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.htint{position:absolute;inset:0;background:radial-gradient(ellipse 90% 70% at 35% 42%,rgba(20,18,16,.25) 0,rgba(20,18,16,.8) 100%)}
.hcard{position:absolute;left:0;top:0;width:1080px;height:1920px;transform-origin:0 0;overflow:hidden}
.himg{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover}
.hsw{position:absolute;inset:0;mix-blend-mode:screen;overflow:hidden}
.hsw i{position:absolute;left:0;top:0;width:100%;height:100%;display:block;
  background:linear-gradient(105deg,rgba(255,107,44,0) 40%,rgba(255,214,170,.36) 50%,rgba(255,107,44,0) 60%)}
.edge{position:absolute;display:block;border:5px solid var(--brasa);border-radius:32px;opacity:0;
  box-shadow:0 0 26px rgba(255,107,44,.6),0 0 70px rgba(255,107,44,.22),inset 0 0 20px rgba(255,107,44,.28)}
.item{position:absolute;left:682px;width:236px;height:64px;display:flex;align-items:center;gap:10px;opacity:0}
.item svg{display:block;width:34px;height:34px;flex:none}
.item span{display:block;font-family:"Poppins";font-weight:800;font-size:29px;line-height:1;color:var(--texto);white-space:nowrap;
  letter-spacing:.3px;text-shadow:0 3px 10px rgba(0,0,0,.7)}
/* luz e moldura */
.vinheta{z-index:3;background:radial-gradient(ellipse 88% 64% at 50% 50%,rgba(0,0,0,0) 60%,rgba(0,0,0,.4) 100%)}
.topo{z-index:3;background:linear-gradient(to bottom,rgba(20,18,16,.72) 0,rgba(20,18,16,.4) 14%,rgba(20,18,16,0) 27%)}
.flash{z-index:9;background:#FFF6EA}
.flashb{z-index:9;background:radial-gradient(ellipse at 50% 50%,rgba(255,226,196,.9) 0,rgba(255,107,44,.5) 50%,rgba(255,107,44,0) 85%)}
/* corte: lâmina de luz em diagonal */
.corte{z-index:9;overflow:hidden}
.corte i{position:absolute;left:-330px;top:-300px;width:330px;height:2520px;display:block;
  background:linear-gradient(to right,rgba(255,107,44,0) 0,rgba(255,107,44,.7) 34%,#FFF6EA 50%,rgba(255,107,44,.7) 66%,rgba(255,107,44,0) 100%)}
#scan{z-index:4;overflow:hidden;mix-blend-mode:screen}
#scan i{position:absolute;left:0;top:0;width:1080px;height:300px;display:block;
  background:linear-gradient(to bottom,rgba(255,107,44,0) 0,rgba(255,150,90,.3) 45%,rgba(255,236,214,.5) 62%,rgba(255,107,44,0) 100%)}
/* títulos: Archivo Black, à esquerda, sombra dura */
.titulo{z-index:5}
.tl{position:absolute;left:56px;display:block;font-family:"Archivo Black";font-weight:400;color:var(--texto);line-height:1;white-space:nowrap;
  letter-spacing:-1px;text-shadow:0 6px 0 rgba(20,18,16,.9),0 14px 30px rgba(0,0,0,.55)}
.tl em{font-style:normal;color:var(--brasa)}
.tl.br{color:var(--brasa)}
.mask{position:absolute;left:56px;width:900px;overflow:hidden;display:block}
.mask .tl{left:0;top:0}
.risco{position:absolute;display:block;height:10px;border-radius:5px;background:linear-gradient(to right,var(--brasa),#FFD9B8);
  box-shadow:0 0 18px rgba(255,107,44,.7)}
.pilula{position:absolute;left:56px;display:block;font-family:"Poppins";font-weight:800;line-height:1;color:var(--base);
  background:var(--brasa);border-radius:14px;white-space:nowrap;box-shadow:0 10px 26px rgba(0,0,0,.5)}
.pilula b{font-weight:800;display:inline-block}
/* legenda sublinhado: branco com contorno, palavra-chave em brasa com fio de lâmina que se desenha */
.legenda{z-index:7}
.cap{position:absolute;left:40px;width:870px;display:flex;justify-content:center;align-items:flex-start;gap:20px;flex-wrap:nowrap}
.pal{position:relative;display:block;font-family:"Poppins";font-weight:800;font-size:76px;line-height:1.1;color:#FFFFFF;white-space:nowrap;
  -webkit-text-stroke:11px #141210;paint-order:stroke fill;text-shadow:0 8px 18px rgba(0,0,0,.5)}
.pal.k{color:var(--brasa)}
.fio{position:absolute;left:0;bottom:-12px;width:100%;height:13px;display:block;
  background:linear-gradient(to right,var(--brasa),#FFD9B8);clip-path:polygon(0 0,100% 38%,100% 62%,0 100%);
  filter:drop-shadow(0 3px 4px rgba(0,0,0,.6))}
.rodape{z-index:7}
.rodape span{position:absolute;left:56px;top:1468px;display:block;font-family:"Poppins";font-weight:600;font-size:30px;line-height:1;
  color:rgba(255,255,255,.8);text-shadow:0 2px 8px rgba(0,0,0,.85)}
/* CTA */
#ovC{z-index:4}
.num{position:absolute;display:block;width:58px;height:58px;border-radius:50%;background:var(--brasa);color:var(--base);
  font-family:"Archivo Black";font-weight:400;font-size:34px;line-height:58px;text-align:center;opacity:0;
  box-shadow:0 0 0 4px rgba(20,18,16,.85),0 6px 16px rgba(0,0,0,.6)}
.brk{position:absolute;display:block;border:5px solid var(--brasa);border-radius:20px;opacity:0;
  box-shadow:0 0 22px rgba(255,107,44,.7),inset 0 0 14px rgba(255,107,44,.3)}
#cta{z-index:8}
#cta-b{position:absolute;left:48px;top:1412px;display:flex;align-items:center;gap:20px;font-family:"Archivo Black";font-weight:400;
  font-size:52px;line-height:1;color:var(--base);background:var(--brasa);padding:16px 40px 16px 16px;border-radius:999px;white-space:nowrap;
  box-shadow:0 0 44px rgba(255,107,44,.5),0 12px 26px rgba(0,0,0,.5)}
#cta-b svg{display:block;width:78px;height:78px;flex:none}
#cta-o{position:absolute;left:43px;top:1406px;width:122px;height:122px;display:block;border:6px solid var(--brasa);border-radius:50%;opacity:0}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: clipe A 0-4,46 s (0,92x), kit inteiro no quadro -->
  <div id="camA" class="cam"><video id="vA" class="clip full" data-start="0" data-duration="4.85" data-media-start="0" data-playback-rate="0.92" data-track-index="0" src="assets/clipe_A.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: B 0-0,81 s (0,77x) > cartão das 4 facas (quadro 0,80 s) > B 4,0-7,7 s (0,77x), close do relevo -->
  <div id="camB1" class="cam"><video id="vB1" class="clip full" data-start="4.85" data-duration="1.05" data-media-start="0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <div id="hero" class="clip hero" data-start="%%H0%%" data-duration="%%HD%%" data-track-index="1">
    <img id="h-bg" class="hbg" src="assets/b_quadro.jpg" alt="" />
    <div id="h-tint" class="htint"></div>
    <div id="h-card" class="hcard"><img id="h-img" class="himg" src="assets/b_quadro.jpg" alt="As quatro facas do faqueiro" /><div id="h-sw" class="hsw"><i id="h-swi"></i></div></div>
    <i id="h-edge" class="edge" style="left:%%JX%%px;top:%%JY%%px;width:%%JW%%px;height:%%JH%%px"></i>
    %%LISTA%%
  </div>
  <div id="camB2" class="cam"><video id="vB2" class="clip full" data-start="9.95" data-duration="4.8" data-media-start="4.0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_B.mp4" muted playsinline></video></div>
  <!-- CTA: quadro 0 do C (0,6 s) + C 0-4,04 s em 0,77x (nunca passa de 4,5 s: defeito do descascador) -->
  <div id="bgC" class="clip" data-start="17.9" data-duration="2.7" data-track-index="2"><img id="bgC-i" src="assets/c_quadro.jpg" alt="" /></div>
  <div id="cardC"><div id="camC" class="cam">
    <img id="iC" class="clip full" data-start="14.75" data-duration="0.6" data-track-index="0" src="assets/c_quadro.jpg" alt="Faqueiro de 6 peças" />
    <video id="vC" class="clip full" data-start="15.35" data-duration="5.25" data-media-start="0" data-playback-rate="0.77" data-track-index="0" src="assets/clipe_C.mp4" muted playsinline></video>
  </div></div>

  <div id="vin" class="clip vinheta" data-start="0" data-duration="%%TOTAL%%" data-track-index="3"></div>
  <div id="topo" class="clip topo" data-start="0" data-duration="%%TOTAL%%" data-track-index="4"></div>
  <div id="flash0" class="clip flash" data-start="0" data-duration="0.12" data-track-index="5"></div>
  <div id="corte1" class="clip corte" data-start="4.68" data-duration="0.36" data-track-index="5"><i id="corte1-i"></i></div>
  <div id="flash2" class="clip flashb" data-start="9.95" data-duration="0.2" data-track-index="5"></div>
  <div id="scan" class="clip" data-start="11.4" data-duration="1.3" data-track-index="5"><i id="scan-i"></i></div>
  <div id="flash3" class="clip flash" data-start="14.75" data-duration="0.14" data-track-index="5"></div>
  <i id="edgeC" class="edge" style="z-index:2;left:%%ECX%%px;top:%%ECY%%px;width:%%ECW%%px;height:%%ECH%%px"></i>

  <!-- títulos -->
  <div id="ti" class="clip titulo" data-start="0" data-duration="2.3" data-track-index="6">
    <div id="ti-l0" class="tl" style="top:192px;font-size:116px">FACA QUE</div>
    <div id="ti-l1" class="tl br" style="top:312px;font-size:116px">NÃO CORTA?</div>
    <i id="ti-r" class="risco" style="left:30px;top:304px;width:890px"></i>
  </div>
  <div id="tp" class="clip titulo" data-start="2.85" data-duration="1.85" data-track-index="6">
    <span id="tp-p" class="pilula" style="top:196px;font-size:58px;padding:16px 28px 18px">Faqueiro de <b id="tp-6">6</b> peças</span>
  </div>
  <div id="ta" class="clip titulo" data-start="4.95" data-duration="5.0" data-track-index="6">
    <div id="ta-l0" class="tl" style="top:198px;font-size:84px"><em>4</em> FACAS NO KIT</div>
    <i id="ta-r" class="risco" style="left:56px;top:294px;width:300px"></i>
  </div>
  <div id="tb" class="clip titulo" data-start="11.4" data-duration="3.3" data-track-index="6">
    <div class="mask" style="top:192px;height:112px"><div id="tb-l0" class="tl" style="font-size:104px">LÂMINA</div></div>
    <div class="mask" style="top:300px;height:112px"><div id="tb-l1" class="tl br" style="font-size:104px">ONDULADA</div></div>
    <span id="tb-p" class="pilula" style="top:430px;font-size:46px;padding:13px 24px 15px">mais durabilidade*</span>
  </div>
  <div id="tc" class="clip titulo" data-start="14.75" data-duration="5.85" data-track-index="6">
    <div id="tc-l0" class="tl" style="top:198px;font-size:80px">KIT COM <em>6</em> PEÇAS</div>
    <span id="tc-p" class="pilula" style="top:300px;font-size:42px;padding:11px 22px 13px">tesoura e descascador inclusos</span>
  </div>
  <div id="rodape" class="clip rodape" data-start="4.85" data-duration="9.9" data-track-index="7"><span id="rodape-s">*Dados do fabricante</span></div>

  <!-- CTA: contagem das 6 peças e colchetes na tesoura e no descascador -->
  <div id="ovC" class="clip" data-start="15.1" data-duration="3.0" data-track-index="8">
    %%CONT%%
    <i id="bk-t" class="brk" style="left:812px;top:422px;width:248px;height:602px"></i>
    <i id="bk-d" class="brk" style="left:838px;top:1054px;width:216px;height:468px"></i>
  </div>
  <div id="cta" class="clip" data-start="%%TTOCA%%" data-duration="%%DTOCA%%" data-track-index="9">
    <i id="cta-o"></i>
    <span id="cta-b"><svg id="cta-s" viewBox="0 0 78 78"><circle cx="39" cy="39" r="37" fill="#141210"/><path d="M54 24 L26 52 M25 32 L25 53 L46 53" fill="none" stroke="#FF6B2C" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round"/></svg>TOQUE NO PRODUTO</span>
  </div>

%%LEG_HTML%%

  <audio id="voz-intro" data-start="0.25" data-duration="4.54" data-track-index="13" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="5.1" data-duration="9.55" data-track-index="13" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="15.05" data-duration="5.45" data-track-index="13" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-0" data-start="0" data-duration="0.8" data-track-index="14" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whooshc-1" data-start="2.0" data-duration="0.3" data-track-index="14" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1" data-start="%%SPOP1%%" data-duration="0.09" data-track-index="14" data-volume="0.35" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="4.64" data-duration="0.55" data-track-index="14" data-volume="0.4" src="assets/sfx/whoosh.wav"></audio>
  <audio id="sfx-whooshc-2" data-start="5.84" data-duration="0.3" data-track-index="14" data-volume="0.3" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%STIQ1%%" data-duration="0.03" data-track-index="14" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-tique-2" data-start="%%STIQ2%%" data-duration="0.03" data-track-index="14" data-volume="0.42" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-brilho-1" data-start="11.36" data-duration="0.9" data-track-index="14" data-volume="0.3" src="assets/sfx/brilho.wav"></audio>
  <audio id="sfx-subida-1" data-start="14.35" data-duration="0.4" data-media-start="1.0" data-track-index="14" data-volume="0.38" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-pop-2" data-start="15.2" data-duration="0.09" data-track-index="14" data-volume="0.3" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-tique-3" data-start="%%STIQ3%%" data-duration="0.03" data-track-index="14" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%TTOCA%%" data-duration="0.05" data-track-index="14" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO: kit inteiro no quadro 0, punch-in 1,12->1, título batendo; o título é "cortado" em "cortar?" ----
tl.fromTo("#flash0", {opacity:0.55}, {opacity:0, duration:0.12}, 0);
tl.fromTo("#camA", {scale:1.12}, {scale:1, duration:0.4, ease:"power3.out"}, 0);
tl.fromTo("#ti-l0", {scale:1.3, transformOrigin:"0% 50%"}, {scale:1, duration:0.3, ease:"back.out(1.8)"}, 0);
tl.fromTo("#ti-l1", {scale:1.3, transformOrigin:"0% 50%"}, {scale:1, duration:0.3, ease:"back.out(1.8)"}, 0.05);
tl.to("#ti-l1", {scale:1.05, transformOrigin:"0% 50%", duration:0.14, yoyo:true, repeat:1, ease:"sine.inOut"}, 1.1);
tl.fromTo("#ti-r", {scaleX:0, opacity:1, rotation:-4, transformOrigin:"0% 50%"}, {scaleX:1, opacity:1, rotation:-4, duration:0.12, ease:"power3.in"}, 1.98);
tl.to("#ti-l0", {x:-70, y:-34, opacity:0, duration:0.2, ease:"power2.in"}, 2.08);
tl.to("#ti-l1", {x:70, y:34, opacity:0, duration:0.2, ease:"power2.in"}, 2.08);
tl.to("#ti-r", {opacity:0, duration:0.12}, 2.14);
tl.fromTo("#tp-p", {opacity:0, x:-60, scale:0.9, transformOrigin:"0% 50%"}, {opacity:1, x:0, scale:1, duration:0.24, ease:"back.out(1.8)"}, %%TFAQ%%);
tl.fromTo("#tp-6", {scale:1}, {scale:1.5, duration:0.13, yoyo:true, repeat:1, ease:"power2.out"}, %%TSEIS%%);
tl.to("#tp-p", {opacity:0, y:-30, duration:0.16, ease:"power2.in"}, 4.52);

// passagem: lâmina de luz em diagonal + corte
tl.fromTo("#corte1-i", {x:-200, rotation:16}, {x:1800, rotation:16, duration:0.36, ease:"power2.inOut"}, 4.68);

// ---- APRESENTAÇÃO ----
tl.fromTo("#camB1", {scale:1.08}, {scale:1, duration:0.4, ease:"power3.out"}, 4.85);
tl.fromTo("#rodape-s", {opacity:0}, {opacity:1, duration:0.2}, 4.85);
tl.fromTo("#ta-l0", {scale:1.6, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.26, ease:"back.out(1.8)"}, 4.97);
tl.fromTo("#ta-r", {scaleX:0, transformOrigin:"0% 50%"}, {scaleX:1, duration:0.3, ease:"power3.out"}, 5.15);
// produto herói: as 4 facas congelam e viram cartão; a lista acende no tempo da fala (sem rotular faca)
tl.fromTo("#h-card", {x:-32, y:-58, scale:1.06, clipPath:"inset(0px 0px 0px 0px round 0px)"}, {x:%%TX%%, y:%%TY%%, scale:%%S%%, clipPath:"%%INSET%%", duration:0.42, ease:"power3.inOut"}, %%H0%%);
tl.fromTo("#h-bg", {filter:"blur(0px) brightness(1)", scale:1}, {filter:"blur(26px) brightness(0.5)", scale:1.12, duration:0.42, ease:"power2.out"}, %%H0%%);
tl.to("#h-bg", {scale:1.2, duration:3.6, ease:"none"}, %%H0B%%);
tl.fromTo("#h-tint", {opacity:0}, {opacity:1, duration:0.4}, %%H0%%);
tl.fromTo("#h-edge", {opacity:0, scale:1.04}, {opacity:1, scale:1, duration:0.22, ease:"power2.out"}, %%H0E%%);
%%LISTA_JS%%
tl.fromTo("#h-swi", {xPercent:-120}, {xPercent:120, duration:1.0, ease:"power2.inOut"}, 6.55);
tl.fromTo("#h-swi", {xPercent:-120}, {xPercent:120, duration:1.0, ease:"power2.inOut", immediateRender:false}, 8.15);
tl.to("#ta-l0", {x:-60, opacity:0, duration:0.16, ease:"power2.in"}, 9.76);
tl.to("#ta-r", {scaleX:0, transformOrigin:"100% 50%", duration:0.16, ease:"power2.in"}, 9.76);

// close do relevo: "as ondulações da lâmina prolongam a durabilidade"
tl.fromTo("#flash2", {opacity:0.6}, {opacity:0, duration:0.2}, 9.95);
tl.fromTo("#camB2", {scale:1.07}, {scale:1, duration:0.4, ease:"power3.out"}, 9.95);
tl.to("#camB2", {scale:1.02, duration:%%DPROL%%, ease:"none"}, 10.35);
tl.to("#camB2", {scale:1.08, duration:0.24, ease:"power3.out"}, %%TPROL%%);
tl.to("#camB2", {scale:1.1, duration:1.8, ease:"none"}, %%TPROL2%%);
tl.fromTo("#scan-i", {y:300}, {y:1900, duration:1.25, ease:"power1.inOut"}, 11.42);
tl.fromTo("#tb-l0", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, %%TOND0%%);
tl.fromTo("#tb-l1", {yPercent:110}, {yPercent:0, duration:0.28, ease:"power3.out"}, %%TOND%%);
tl.fromTo("#tb-p", {opacity:0, x:-50, scale:0.9, transformOrigin:"0% 50%"}, {opacity:1, x:0, scale:1, duration:0.22, ease:"back.out(1.8)"}, %%TDUR%%);
tl.to("#tb-l0", {yPercent:-110, duration:0.16, ease:"power2.in"}, 14.5);
tl.to("#tb-l1", {yPercent:-110, duration:0.16, ease:"power2.in"}, 14.52);
tl.to("#tb-p", {opacity:0, duration:0.14}, 14.5);
tl.to("#rodape-s", {opacity:0, duration:0.12}, 14.62);

// ---- CTA: kit reto, contagem das 6 peças, tesoura e descascador, depois cartão + botão ----
tl.fromTo("#flash3", {opacity:0.5}, {opacity:0, duration:0.14}, 14.75);
tl.fromTo("#camC", {scale:1.1}, {scale:1, duration:0.42, ease:"power3.out"}, 14.75);
tl.fromTo("#tc-l0", {scale:1.6, opacity:0, transformOrigin:"0% 50%"}, {scale:1, opacity:1, duration:0.26, ease:"back.out(1.8)"}, 14.8);
%%CONT_JS%%
tl.to(".num", {opacity:0, scale:0.6, duration:0.16, stagger:0.02}, 16.12);
tl.fromTo("#tc-p", {opacity:0, x:-50, scale:0.9, transformOrigin:"0% 50%"}, {opacity:1, x:0, scale:1, duration:0.22, ease:"back.out(1.8)"}, 16.14);
tl.fromTo("#bk-t", {opacity:0, scale:1.12}, {opacity:1, scale:1, duration:0.2, ease:"back.out(2)"}, %%TTES%%);
tl.fromTo("#bk-d", {opacity:0, scale:1.12}, {opacity:1, scale:1, duration:0.2, ease:"back.out(2)"}, %%TDESC%%);
tl.to(["#bk-t","#bk-d"], {opacity:0, duration:0.16}, 17.86);
tl.to("#tc-p", {x:-60, opacity:0, duration:0.16, ease:"power2.in"}, 17.93);
tl.fromTo("#cardC", {x:0, y:0, scale:1, clipPath:"inset(0px 0px 0px 0px round 0px)"}, {x:%%TXC%%, y:%%TYC%%, scale:%%SC%%, clipPath:"%%INSET_C%%", duration:0.3, ease:"power3.inOut"}, %%CARDC%%);
tl.fromTo("#edgeC", {opacity:0, scale:1.03}, {opacity:1, scale:1, duration:0.2, ease:"power2.out"}, %%CARDCE%%);
tl.fromTo("#cta-b", {scale:0.6, opacity:0, transformOrigin:"10% 50%"}, {scale:1, opacity:1, duration:0.24, ease:"back.out(2.2)"}, %%TTOCA%%);
tl.fromTo("#cta-o", {scale:0.4, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out"}, %%TTOCA%%);
tl.to("#cta-b", {scale:1.045, duration:0.4, yoyo:true, repeat:3, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#cta-s", {x:0, y:0}, {x:-5, y:5, duration:0.2, yoyo:true, repeat:7, ease:"sine.inOut"}, %%TPULSO%%);
tl.fromTo("#cta-o", {scale:0.4, opacity:0.95}, {scale:1.9, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TONDA2%%);

// ---- legenda ----
%%LEG_JS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

R = lambda v: str(round(v, 3))
subs = {
    "TOTAL": str(TOTAL), "H0": str(H0), "HD": R(HERO[1] - HERO[0]), "H0B": R(H0 + 0.42), "H0E": R(H0 + 0.36),
    "JX": str(jx0), "JY": str(jy0), "JW": str(jx1 - jx0), "JH": str(jy1 - jy0),
    "TX": str(TX), "TY": str(TY), "S": str(S), "INSET": INSET, "LISTA": lista_html, "LISTA_JS": lista_js,
    "ECX": str(ecx0), "ECY": str(ecy0), "ECW": str(ecx1 - ecx0), "ECH": str(ecy1 - ecy0),
    "TXC": str(TXC), "TYC": str(TYC), "SC": str(SC), "INSET_C": INSET_C, "CARDC": str(CARD_C), "CARDCE": R(CARD_C + 0.26),
    "CONT": cont_html, "CONT_JS": cont_js,
    "TTOCA": R(T_TOCA - 0.02), "DTOCA": R(TOTAL - (T_TOCA - 0.02)), "TPULSO": R(T_TOCA + 0.4), "TONDA2": R(T_TOCA + 1.2),
    "TTES": R(T_TES - 0.03), "TDESC": R(T_DESC - 0.03), "STIQ3": R(T_TES - 0.03),
    "TFAQ": R(T_FAQ - 0.03), "TSEIS": R(T_SEIS), "SPOP1": R(T_FAQ - 0.03),
    "STIQ1": R(LISTA[1][1] - 0.04), "STIQ2": R(LISTA[3][1] - 0.04),
    "TOND0": R(T_OND - 0.1), "TOND": R(T_OND), "TDUR": R(T_DUR - 0.03),
    "TPROL": R(T_PROL), "TPROL2": R(T_PROL + 0.24), "DPROL": R(T_PROL - 10.37),
    "LEG_HTML": "\n".join(leg_html), "LEG_JS": "\n".join(leg_js),
}
for k, v in subs.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, html[html.index("%%"):][:60]
open(OUT, "w").write(html)
print("ok", OUT)
