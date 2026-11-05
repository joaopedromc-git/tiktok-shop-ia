#!/usr/bin/env python3
"""Gera produtos/facas/edicao_D/index.html ("fita de preparo": fita crepe #EEE0B8 / tinta #15130F / vermelho-marcador #E1262D,
Anton + Inter 800, legenda em fita escura). Uso: python3 gerar.py <pasta_com_fala_*.json> <saida>

Lote D ("Uma peça pra cada tarefa"), clipes G/H/I com mão. Regra da 3ª violação: o vídeo roda do primeiro ao último
quadro; não há <img>, quadro congelado nem cartão. Trechos permitidos (analise_D.md): G 0-5,0 · H 0-6,25 · I 0-2,4.
  intro   G  0,00-3,36 em 0,80x (0,00-4,20)        faca desce e parte a cebola
  apres.  H  0,00-1,44 em 0,75x (4,20-6,12)        kit inteiro, "seis peças" (números 1-6)
          G  3,40-4,96 em 0,80x (6,12-8,07)        CHEFE -> CEBOLA (2º corte)
          H  1,44-2,94 em 0,85x (8,07-9,84)        TESOURA -> CHEIRO-VERDE (zoom na tesoura)
          I  0,80-2,22 em 0,90x (9,84-11,42)       CUTELO -> CARNE
          H  2,94-4,47 em 0,72x (11,42-13,55)      A PEÇA CERTA (colchetes no kit)
  CTA     H  4,47-6,23 em 0,72x (13,55-15,99)      QUAL PEÇA PRIMEIRO?
          H  0,30-2,04 em 0,72x (15,99-18,40)      toca no produto (repete trecho do H em outra velocidade e enquadramento)
G e I em tela cheia (texto só no alto, livre). H (vista de cima, sem espaço livre) fica numa janela 0,755x a partir
de y=470, sobre o próprio H desfocado e escurecido (rodando): o texto fica acima da janela, nunca sobre peça ou mão.
Transições: fita opaca de bordas rasgadas (duras) que cobre a tela inteira no corte; nunca tinge as peças.
"""
import json, sys

falas = {p: json.load(open(f"{sys.argv[1]}/fala_{p}.json")) for p in ("intro", "apresentacao", "cta")}
OUT = sys.argv[2]

TOTAL = 18.4
VOZ = {"intro": 0.25, "apresentacao": 4.45, "cta": 13.85}
FIM = {"intro": 4.2, "apresentacao": 13.55, "cta": TOTAL}
DUR_MP3 = {"intro": 3.94, "apresentacao": 9.02, "cta": 4.44}
WIN = (132, 470, 0.755)  # janela do H: x, y, escala
CAP_TOP = {"intro": 492, "apresentacao": 372, "cta": 372}

GRUPOS = {
    "intro": [[0, 1], [2, 3, 4], [5, 6], [7], [8], [9, 10]],
    "apresentacao": [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9, 10], [11, 12], [13, 14], [15], [16, 17], [18, 19, 20],
                     [21, 22], [23, 24, 25, 26]],
    "cta": [[0, 1], [2, 3], [4], [5, 6, 7], [8, 9], [10, 11]],
}
CHAVE = {"intro": {4, 7, 8, 10}, "apresentacao": {2, 7, 10, 12, 15, 17, 20, 25, 26}, "cta": {1, 4, 5, 11}}
EXIBE = {("intro", 7): "cebola,", ("intro", 8): "carne", ("intro", 10): "cheiro-verde?",
         ("apresentacao", 3): "peças:", ("apresentacao", 10): "cebola,", ("apresentacao", 15): "cheiro-verde,",
         ("apresentacao", 20): "carne.", ("apresentacao", 26): "certa.",
         ("cta", 4): "primeiro?", ("cta", 11): "kit."}


def T(parte, i):
    return round(VOZ[parte] + falas[parte]["palavras"][i]["inicio"], 3)


def rasgo(n=7, d=9):
    """clip-path de fita rasgada: zigue-zague duro nas pontas esquerda e direita."""
    esq = [f"{d if k % 2 else 0}px {round(100 * k / n, 2)}%" for k in range(n + 1)]
    dir_ = [f"calc(100% - {d if k % 2 else 0}px) {round(100 - 100 * k / n, 2)}%" for k in range(n + 1)]
    return "polygon(" + ",".join(esq[::-1][::-1] + dir_[::-1][::-1]) + ")"


# ---------------- legenda (fita escura, palavra por palavra) ----------------
leg_html, leg_js = [], []
for parte, grupos in GRUPOS.items():
    voz = VOZ[parte]
    pal = falas[parte]["palavras"]
    for gi, g in enumerate(grupos):
        s = round(voz + pal[g[0]]["inicio"] - 0.05, 3)
        fim_voz = round(voz + pal[g[-1]]["fim"] + 0.3, 3)
        if gi + 1 < len(grupos):
            e = min(round(voz + pal[grupos[gi + 1][0]]["inicio"] - 0.05, 3), fim_voz)
        else:
            e = min(fim_voz, FIM[parte] - 0.08)
        gid = f"leg-{parte[:3]}-{gi}"
        spans = ""
        for k, wi in enumerate(g):
            t = s + 0.04 if k == 0 else round(voz + pal[wi]["inicio"] - 0.02, 3)
            txt = EXIBE.get((parte, wi), pal[wi]["palavra"])
            cls = "pal k" if wi in CHAVE[parte] else "pal"
            spans += f'<span id="{gid}-{k}" class="{cls}">{txt}</span>'
            esc = 1.25 if wi in CHAVE[parte] else 1.12
            leg_js.append(f'tl.fromTo("#{gid}-{k}",{{opacity:0,scale:{esc}}},{{opacity:1,scale:1,duration:0.1,ease:"power2.out"}},{round(t, 3)});')
        leg_js.append(f'tl.fromTo("#{gid}-f",{{scaleX:0}},{{scaleX:1,duration:0.12,ease:"power3.out"}},{s});')
        rot = -1.2 if gi % 2 == 0 else 0.9
        leg_html.append(f'  <div id="{gid}" class="clip legenda" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="12">'
                        f'<div class="cap" style="top:{CAP_TOP[parte]}px;transform:rotate({rot}deg)">'
                        f'<div id="{gid}-f" class="fita-esc">{spans}</div></div></div>')

# ---------------- tempos-chave ----------------
t_seis, t_pecas = T("apresentacao", 2), T("apresentacao", 3)
t_chefe, t_cebola = T("apresentacao", 7), T("apresentacao", 10)
t_tes, t_cv = T("apresentacao", 12), T("apresentacao", 15)
t_cut, t_carne = T("apresentacao", 17), T("apresentacao", 20)
t_peca = T("apresentacao", 25)
t_i_cebola, t_i_carne, t_i_cv = T("intro", 7), T("intro", 8), T("intro", 10)
t_prim, t_toca, t_conf, t_kit = T("cta", 4), T("cta", 5), T("cta", 9), T("cta", 11)

C1, C2, C3, C4, C5 = 4.2, 6.12, 8.07, 9.84, 11.42   # cortes
C6, C7 = 13.55, round(t_toca - 0.01, 2)             # entrada da CTA e corte em "Toca"

# números 1-6 no kit (coordenadas do vídeo H, 1080x1920), medidos em H 0,6 s
DOTS = [(217, 1040), (478, 985), (600, 963), (765, 912), (930, 872), (432, 1190)]
dots_html = "".join(f'<i id="dot{n+1}" class="dot" style="left:{x-36}px;top:{y-36}px">{n+1}</i>' for n, (x, y) in enumerate(DOTS))
dots_js = "\n".join(
    f'tl.fromTo("#dot{n+1}",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:0.18,ease:"back.out(2.4)"}},{round(t_seis + 0.12 * n, 3)});'
    for n in range(6))

R = lambda v: str(round(v, 3))
WX, WY, WS = WIN
RASGO = rasgo()
RASGO_F = rasgo(5, 7)

html = r"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head>
<meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="assets/fontes.css" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face{font-family:"Anton Fita";src:local("Anton Regular"),local("Anton-Regular"),local("Anton")}
@font-face{font-family:"Inter Fita";font-weight:100 900;src:local("Inter Thin"),local("Inter-Thin"),local("Inter")}
:root{--fita:#EEE0B8;--tinta:#15130F;--verm:#E1262D}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#15130F}
#root{width:100%;height:100%;position:relative;overflow:hidden;background:#15130F;font-family:"Inter Fita";font-weight:800}
.clip{position:absolute;inset:0}
.cam{position:absolute;inset:0;overflow:hidden;z-index:1}
.full{width:100%;height:100%;object-fit:cover}
#camG1{transform-origin:420px 1050px}
#camG2{transform-origin:420px 1000px}
#camI{transform-origin:500px 1100px}
/* H: fundo = o próprio H desfocado e escurecido (rodando); janela nítida a partir de y=470 */
#bgH{position:absolute;inset:0;overflow:hidden;z-index:1;filter:blur(34px) brightness(0.38) saturate(1.15)}
#bgHz{position:absolute;inset:-80px}
#winH{position:absolute;left:%%WX%%px;top:%%WY%%px;width:%%WW%%px;height:%%WH%%px;overflow:hidden;z-index:2}
#fitH{position:absolute;left:0;top:0;width:1080px;height:1920px;transform:scale(%%WS%%);transform-origin:0 0}
#zH{position:absolute;left:0;top:0;width:1080px;height:1920px}
.deco{z-index:3}
.canto{position:absolute;display:block;width:150px;height:46px;background:var(--fita);--c:var(--fita)}
/* pontas rasgadas (bordas duras) das fitas */
.canto,.tag,.big,.fita-esc,#ct-a,#ct-b{position:relative}
.canto::before,.tag::before,.big::before,.fita-esc::before,#ct-a::before,#ct-b::before,
.canto::after,.tag::after,.big::after,.fita-esc::after,#ct-a::after,#ct-b::after{content:"";position:absolute;top:0;bottom:0;width:10px}
.canto::before,.tag::before,.big::before,.fita-esc::before,#ct-a::before,#ct-b::before{left:-10px;
  background:linear-gradient(to top left,var(--c) 50%,transparent 50%) 0 0/10px 12px repeat-y,linear-gradient(to bottom left,var(--c) 50%,transparent 50%) 0 6px/10px 12px repeat-y}
.canto::after,.tag::after,.big::after,.fita-esc::after,#ct-a::after,#ct-b::after{right:-10px;
  background:linear-gradient(to top right,var(--c) 50%,transparent 50%) 0 0/10px 12px repeat-y,linear-gradient(to bottom right,var(--c) 50%,transparent 50%) 0 6px/10px 12px repeat-y}
/* números 1-6 (dentro do zoom do H, coordenadas do vídeo) */
.nums{z-index:1}
.dot{position:absolute;display:flex;align-items:center;justify-content:center;width:72px;height:72px;border-radius:50%;
  background:var(--verm);color:var(--fita);font-family:"Anton Fita";font-style:normal;font-size:44px;line-height:1;
  box-shadow:0 0 0 5px var(--fita),0 4px 10px rgba(0,0,0,.35)}
/* colchetes do kit (dentro do zoom do H) */
.colch{z-index:1}
.cl{position:absolute;display:block;width:110px;height:110px;border-color:var(--verm);border-style:solid;border-width:0}
.flash{z-index:20;background:#FFF8E8;opacity:0}
/* cabeçalho: etiqueta vermelha + fita creme com Anton */
.hd{z-index:6}
.row{position:absolute;left:48px;display:flex;align-items:flex-start}
.tag{display:block;background:var(--verm);color:var(--fita);font-family:"Inter Fita";font-weight:800;font-size:36px;line-height:1;
  letter-spacing:2px;padding:8px 24px 9px;transform-origin:0 50%;--c:var(--verm)}
.big{display:flex;align-items:center;gap:14px;background:var(--fita);color:var(--tinta);font-family:"Anton Fita";font-size:90px;
  line-height:1;padding:10px 30px 12px;transform-origin:0 50%;white-space:nowrap;--c:var(--fita)}
.big.g{font-size:128px;padding:12px 32px 16px}
.big .s{color:var(--verm)}
.seta{display:block;width:78px;height:56px}
/* legenda: fita escura, palavra-chave em vermelho */
.legenda{z-index:9}
.cap{position:absolute;left:48px;display:flex;align-items:flex-start}
.fita-esc{display:flex;gap:16px;align-items:center;background:var(--tinta);padding:10px 28px 13px;
  transform-origin:0 50%;--c:var(--tinta)}
.pal{display:block;font-family:"Inter Fita";font-weight:800;font-size:60px;line-height:1.05;color:var(--fita);white-space:nowrap}
.pal.k{color:#FF4048}
/* CTA: etiqueta "toca no produto" + seta para o produto marcado */
#ctaTag{z-index:8}
#ct-r{position:absolute;left:36px;top:1336px;display:flex;flex-direction:column;align-items:flex-start;gap:6px}
#ct-a,#ct-b{display:block;background:var(--fita);color:var(--tinta);font-family:"Inter Fita";font-weight:800;font-size:42px;line-height:1;
  padding:9px 22px 11px;transform-origin:0 50%;white-space:nowrap;--c:var(--fita)}
#ct-b{background:var(--verm);color:var(--fita);--c:var(--verm)}
#ct-s{position:absolute;left:28px;top:1470px;width:70px;height:70px;display:block}
#ct-o{position:absolute;left:14px;top:1480px;width:70px;height:70px;display:block;border:6px solid var(--verm);border-radius:50%;opacity:0}
/* transições: fita crepe opaca de bordas rasgadas */
.wipe{z-index:18;overflow:hidden}
#wp1{position:absolute;left:-210px;top:-340px;width:1500px;height:2600px;display:block;background:var(--fita);clip-path:%%RASGO%%}
#wp1 i{position:absolute;left:0;top:0;width:100%;height:100%;display:block;
  background:linear-gradient(90deg,transparent 0 46px,var(--verm) 46px 62px,transparent 62px calc(100% - 62px),var(--verm) calc(100% - 62px) calc(100% - 46px),transparent calc(100% - 46px))}
#wp1w{position:absolute;left:0;top:0;width:1080px;height:1920px;display:block;transform:rotate(-12deg)}
#wp2{position:absolute;left:-60px;top:0;width:1200px;height:2100px;display:block;background:var(--tinta);
  clip-path:polygon(0 18px,4% 0,8% 18px,12% 0,16% 18px,20% 0,24% 18px,28% 0,32% 18px,36% 0,40% 18px,44% 0,48% 18px,52% 0,56% 18px,60% 0,64% 18px,68% 0,72% 18px,76% 0,80% 18px,84% 0,88% 18px,92% 0,96% 18px,100% 0,100% 100%,0 100%)}
#wp2 i{position:absolute;left:0;top:40px;width:100%;height:16px;display:block;background:var(--verm)}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%%TOTAL%%" data-width="1080" data-height="1920">
  <!-- INTRO: G 0-3,36 em 0,8x (tela cheia) -->
  <div id="camG1" class="cam"><video id="vG1" class="clip full" data-start="0" data-duration="4.2" data-media-start="0" data-playback-rate="0.8" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: G 3,40-4,96 em 0,8x -->
  <div id="camG2" class="cam"><video id="vG2" class="clip full" data-start="%%C2%%" data-duration="%%DG2%%" data-media-start="3.4" data-playback-rate="0.8" data-track-index="0" src="assets/clipe_G.mp4" muted playsinline></video></div>
  <!-- APRESENTAÇÃO: I 0,60-2,36 em 0,9x (I depois de 2,4 s nunca entra) -->
  <div id="camI" class="cam"><video id="vI" class="clip full" data-start="%%C4%%" data-duration="%%DI%%" data-media-start="0.8" data-playback-rate="0.9" data-track-index="0" src="assets/clipe_I.mp4" muted playsinline></video></div>

  <!-- H: fundo desfocado (mesmos trechos, rodando) -->
  <div id="bgH"><div id="bgHz" data-layout-allow-overflow>
%%HBG%%
  </div></div>
  <!-- H: janela nítida -->
  <div id="winH"><div id="fitH"><div id="zH">
%%HWIN%%
    <div id="nums" class="clip nums" data-start="%%C1%%" data-duration="%%DH1%%" data-track-index="3">%%DOTS%%</div>
    <div id="colch" class="clip colch" data-start="%%TPECA%%" data-duration="%%DCOL%%" data-track-index="3">
      <i id="cl1" class="cl" style="left:84px;top:92px;border-left-width:12px;border-top-width:12px"></i>
      <i id="cl2" class="cl" style="left:926px;top:92px;border-right-width:12px;border-top-width:12px"></i>
      <i id="cl3" class="cl" style="left:84px;top:880px;border-left-width:12px;border-bottom-width:12px"></i>
      <i id="cl4" class="cl" style="left:926px;top:880px;border-right-width:12px;border-bottom-width:12px"></i>
    </div>
  </div></div></div>
  <div id="deco1" class="clip deco" data-start="%%C1%%" data-duration="%%DH1%%" data-track-index="4"><i class="canto" style="left:%%CNL%%px;top:%%CNT%%px;transform:rotate(-38deg)"></i><i class="canto" style="left:%%CNR%%px;top:%%CNT%%px;transform:rotate(38deg)"></i></div>
  <div id="deco2" class="clip deco" data-start="%%C3%%" data-duration="%%DH2%%" data-track-index="4"><i class="canto" style="left:%%CNL%%px;top:%%CNT%%px;transform:rotate(-38deg)"></i><i class="canto" style="left:%%CNR%%px;top:%%CNT%%px;transform:rotate(38deg)"></i></div>
  <div id="deco3" class="clip deco" data-start="%%C5%%" data-duration="%%DH3%%" data-track-index="4"><i class="canto" style="left:%%CNL%%px;top:%%CNT%%px;transform:rotate(-38deg)"></i><i class="canto" style="left:%%CNR%%px;top:%%CNT%%px;transform:rotate(38deg)"></i></div>

  <!-- cabeçalhos -->
  <div id="hd0" class="clip hd" data-start="0" data-duration="4.14" data-track-index="6">
    <div class="row" style="top:196px;transform:rotate(-2deg)"><div id="h0a" class="big g">UMA FACA</div></div>
    <div class="row" style="top:350px;transform:rotate(1.4deg)"><div id="h0b" class="big g">PRA <span id="h0t" class="s">TUDO?</span></div></div>
  </div>
  <div id="hd1" class="clip hd" data-start="%%C1%%" data-duration="%%DH1%%" data-track-index="7">
    <div class="row" style="top:196px"><div id="h1t" class="tag">FAQUEIRO</div></div>
    <div class="row" style="top:252px;transform:rotate(-1deg)"><div id="h1b" class="big"><span class="s">6</span> PEÇAS</div></div>
  </div>
  <div id="hd2" class="clip hd" data-start="%%C2%%" data-duration="%%DG2%%" data-track-index="7">
    <div class="row" style="top:196px"><div id="h2t" class="tag">FACA DO CHEFE</div></div>
    <div class="row" style="top:252px;transform:rotate(-1deg)"><div id="h2b" class="big">%%SETA%%<span class="s">CEBOLA</span></div></div>
  </div>
  <div id="hd3" class="clip hd" data-start="%%C3%%" data-duration="%%DH2%%" data-track-index="7">
    <div class="row" style="top:196px"><div id="h3t" class="tag">TESOURA</div></div>
    <div class="row" style="top:252px;transform:rotate(-1deg)"><div id="h3b" class="big">%%SETA%%<span class="s">CHEIRO-VERDE</span></div></div>
  </div>
  <div id="hd4" class="clip hd" data-start="%%C4%%" data-duration="%%DI%%" data-track-index="7">
    <div class="row" style="top:196px"><div id="h4t" class="tag">CUTELO</div></div>
    <div class="row" style="top:252px;transform:rotate(-1deg)"><div id="h4b" class="big">%%SETA%%<span class="s">CARNE</span></div></div>
  </div>
  <div id="hd5" class="clip hd" data-start="%%C5%%" data-duration="%%DH5%%" data-track-index="7">
    <div class="row" style="top:196px"><div id="h5t" class="tag">PRA CADA TAREFA DA COZINHA</div></div>
    <div class="row" style="top:252px;transform:rotate(-1deg)"><div id="h5b" class="big">A <span class="s">PEÇA CERTA</span></div></div>
  </div>
  <div id="hd6" class="clip hd" data-start="%%C6%%" data-duration="%%DCTA%%" data-track-index="8">
    <div class="row" style="top:252px;transform:rotate(-1deg)"><div id="h6b" class="big" style="font-size:82px">QUAL PEÇA <span id="h6p" class="s">PRIMEIRO?</span></div></div>
  </div>
  <div id="ctaTag" class="clip" data-start="%%C7%%" data-duration="%%DTAG%%" data-track-index="11">
    <div id="ct-r"><span id="ct-a">toca no produto</span><span id="ct-b">e confere</span></div>
    <i id="ct-o"></i>
    <span id="ct-s"><svg viewBox="0 0 70 70" width="70" height="70"><path d="M58 12 L16 54 M14 24 L14 56 L46 56" fill="none" stroke="#EEE0B8" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/><path d="M58 12 L16 54 M14 24 L14 56 L46 56" fill="none" stroke="#E1262D" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
  </div>

  <div id="fl1" class="clip flash" data-start="0" data-duration="0.12" data-track-index="13"></div>
  <div id="wipe1" class="clip wipe" data-start="4.04" data-duration="0.32" data-track-index="14"><i id="wp1w"><i id="wp1"><i></i></i></i></div>
  <div id="wipe2" class="clip wipe" data-start="13.39" data-duration="0.32" data-track-index="15"><i id="wp2"><i></i></i></div>

%%LEG%%

  <audio id="voz-intro" data-start="0.25" data-duration="%%DV1%%" data-track-index="16" src="assets/fala_intro.mp3"></audio>
  <audio id="voz-apresentacao" data-start="4.45" data-duration="%%DV2%%" data-track-index="16" src="assets/fala_apresentacao.mp3"></audio>
  <audio id="voz-cta" data-start="13.85" data-duration="%%DV3%%" data-track-index="16" src="assets/fala_cta.mp3"></audio>
  <audio id="sfx-batida-1" data-start="0" data-duration="0.8" data-track-index="17" data-volume="0.6" src="assets/sfx/batida.wav"></audio>
  <audio id="sfx-whoosh-1" data-start="4.06" data-duration="0.3" data-track-index="18" data-volume="0.36" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-tique-1" data-start="%%TTIQ%%" data-duration="0.03" data-track-index="17" data-volume="0.4" src="assets/sfx/tique.wav"></audio>
  <audio id="sfx-whoosh-2" data-start="6.02" data-duration="0.14" data-track-index="18" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-pop-1" data-start="7.98" data-duration="0.09" data-track-index="17" data-volume="0.34" src="assets/sfx/pop.wav"></audio>
  <audio id="sfx-whoosh-3" data-start="9.7" data-duration="0.22" data-track-index="18" data-volume="0.32" src="assets/sfx/whoosh_curto.wav"></audio>
  <audio id="sfx-subida-1" data-start="13.15" data-duration="0.4" data-media-start="1.0" data-track-index="18" data-volume="0.34" src="assets/sfx/subida.wav"></audio>
  <audio id="sfx-clique-1" data-start="%%C7%%" data-duration="0.05" data-track-index="17" data-volume="0.5" src="assets/sfx/clique.wav"></audio>
</div>
<script>
const tl = gsap.timeline({ paused: true });

// ---- INTRO (G): flash + punch 1,2 -> 1,0; "UMA FACA / PRA TUDO?" bate em fita ----
tl.fromTo("#fl1", {opacity:0.85}, {opacity:0, duration:0.1, ease:"power1.out"}, 0);
tl.fromTo("#camG1", {scale:1.2}, {scale:1.0, duration:0.4, ease:"power3.out"}, 0);
tl.to("#camG1", {scale:1.04, duration:%%D_G1A%%, ease:"none"}, 0.4);
tl.to("#camG1", {scale:1.09, duration:0.16, ease:"power2.out"}, %%TICEB%%);
tl.to("#camG1", {scale:1.12, duration:%%D_G1B%%, ease:"none"}, %%TICEB16%%);
tl.fromTo("#h0a", {scaleX:0}, {scaleX:1, duration:0.16, ease:"power3.out"}, 0.02);
tl.fromTo("#h0b", {scaleX:0}, {scaleX:1, duration:0.16, ease:"power3.out"}, 0.16);
tl.fromTo("#h0a", {scale:1}, {scale:1.06, duration:0.08, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, 0.18);
tl.fromTo("#h0t", {scale:1}, {scale:1.12, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 60%", immediateRender:false}, %%TICEB%%);
tl.fromTo("#h0t", {scale:1}, {scale:1.12, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 60%", immediateRender:false}, %%TICAR%%);
tl.fromTo("#h0t", {scale:1}, {scale:1.12, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", transformOrigin:"0% 60%", immediateRender:false}, %%TICV%%);
tl.to(["#h0a", "#h0b"], {x:-1100, duration:0.16, ease:"power2.in"}, 3.96);
// passagem: fita crepe atravessa e cobre a tela inteira no corte (4,20)
tl.fromTo("#wp1", {x:-1750}, {x:0, duration:0.16, ease:"power2.in"}, 4.04);
tl.to("#wp1", {x:1750, duration:0.16, ease:"power2.out"}, 4.2);

// ---- APRESENTAÇÃO 1 (H 0-1,44): kit inteiro, números 1-6 em "seis peças" ----
tl.set("#zH", {transformOrigin:"540px 700px", scale:1.07}, %%C1%%);
tl.to("#zH", {scale:1.0, duration:0.3, ease:"power3.out"}, %%C1%%);
tl.to("#zH", {scale:1.03, duration:%%D_H1%%, ease:"none"}, %%C1_30%%);
tl.fromTo("#h1t", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, 4.3);
tl.fromTo("#h1b", {scaleX:0}, {scaleX:1, duration:0.16, ease:"power3.out"}, 4.4);
%%DOTSJS%%
tl.fromTo("#h1b", {scale:1}, {scale:1.06, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TSEIS%%);

// ---- APRESENTAÇÃO 2 (G 3,40-4,96): CHEFE -> CEBOLA, close na lâmina cortando ----
tl.fromTo("#camG2", {scale:1.24}, {scale:1.14, duration:0.22, ease:"power3.out"}, %%C2%%);
tl.to("#camG2", {scale:1.22, duration:%%D_G2%%, ease:"none"}, %%C2_22%%);
tl.fromTo("#h2t", {scaleX:0}, {scaleX:1, duration:0.12, ease:"power3.out"}, %%C2_03%%);
tl.fromTo("#h2b", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, %%TCHEFE%%);
tl.fromTo("#h2b", {scale:1}, {scale:1.06, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TCEB%%);

// ---- APRESENTAÇÃO 3 (H 1,44-2,94): TESOURA -> CHEIRO-VERDE, zoom na tesoura (produto herói) ----
tl.set("#zH", {transformOrigin:"640px 1380px", scale:1.3}, %%C3%%);
tl.to("#zH", {scale:1.42, duration:%%DH2%%, ease:"none"}, %%C3%%);
tl.fromTo("#h3t", {scaleX:0}, {scaleX:1, duration:0.12, ease:"power3.out"}, %%C3_03%%);
tl.fromTo("#h3b", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, %%TTES%%);
tl.fromTo("#h3b", {scale:1}, {scale:1.05, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TCV%%);

// ---- APRESENTAÇÃO 4 (I 0,60-2,36): CUTELO -> CARNE, fogo ao fundo ----
tl.fromTo("#camI", {scale:1.14}, {scale:1.05, duration:0.22, ease:"power3.out"}, %%C4%%);
tl.to("#camI", {scale:1.12, duration:%%D_I%%, ease:"none"}, %%C4_22%%);
tl.fromTo("#h4t", {scaleX:0}, {scaleX:1, duration:0.12, ease:"power3.out"}, %%C4_03%%);
tl.fromTo("#h4b", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, %%TCUT%%);
tl.fromTo("#h4b", {scale:1}, {scale:1.06, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TCARNE%%);

// ---- APRESENTAÇÃO 5 (H 2,94-4,25): A PEÇA CERTA, colchetes no kit inteiro ----
tl.set("#zH", {transformOrigin:"540px 560px", scale:1.08}, %%C5%%);
tl.to("#zH", {scale:1.0, duration:0.25, ease:"power3.out"}, %%C5%%);
tl.to("#zH", {scale:1.03, duration:%%D_H5%%, ease:"none"}, %%C5_25%%);
tl.fromTo("#h5t", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, %%C5_03%%);
tl.fromTo("#h5b", {scaleX:0}, {scaleX:1, duration:0.16, ease:"power3.out"}, %%C5_12%%);
tl.fromTo(".cl", {scale:1.6, opacity:0}, {scale:1, opacity:1, duration:0.2, stagger:0.05, ease:"back.out(2)"}, %%TPECA%%);
tl.fromTo("#h5b", {scale:1}, {scale:1.06, duration:0.1, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TPECA%%);
tl.to(["#h5t", "#h5b"], {x:-1100, duration:0.16, ease:"power2.in"}, 13.36);
// passagem para a CTA: fita escura sobe e cobre no corte (13,55)
tl.fromTo("#wp2", {y:1960}, {y:-60, duration:0.16, ease:"power2.in"}, 13.39);
tl.to("#wp2", {y:-2200, duration:0.16, ease:"power2.out"}, 13.55);

// ---- CTA (H 4,25-6,01 e H 0,30-2,04): mais calma ----
tl.set("#zH", {transformOrigin:"540px 900px", scale:1.0}, %%C6%%);
tl.to("#zH", {scale:1.04, duration:%%D_H6%%, ease:"none"}, %%C6%%);
tl.fromTo("#h6b", {scaleX:0}, {scaleX:1, duration:0.2, ease:"power3.out"}, 13.66);
tl.fromTo("#h6p", {scale:1}, {scale:1.1, duration:0.12, yoyo:true, repeat:1, ease:"power2.out", immediateRender:false}, %%TPRIM%%);
tl.set("#zH", {transformOrigin:"540px 900px", scale:1.1}, %%C7%%);
tl.to("#zH", {scale:1.04, duration:0.3, ease:"power2.out"}, %%C7%%);
tl.to("#zH", {scale:1.06, duration:%%D_H7%%, ease:"none"}, %%C7_30%%);
tl.fromTo("#ct-a", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, %%TE%%);
tl.fromTo("#ct-b", {scaleX:0}, {scaleX:1, duration:0.14, ease:"power3.out"}, %%TCONF%%);
tl.fromTo("#ct-s", {scale:0, opacity:0}, {scale:1, opacity:1, duration:0.2, ease:"back.out(2.4)"}, %%C7_20%%);
tl.fromTo("#ct-o", {scale:0.6, opacity:0.95}, {scale:2, opacity:0, duration:0.6, ease:"power2.out"}, %%C7_20%%);
tl.fromTo("#ct-s", {x:0, y:0}, {x:-6, y:6, duration:0.24, yoyo:true, repeat:%%REPS%%, ease:"sine.inOut", immediateRender:false}, %%C7_50%%);
tl.fromTo("#ct-o", {scale:0.6, opacity:0.95}, {scale:2, opacity:0, duration:0.6, ease:"power2.out", immediateRender:false}, %%TKIT%%);

// ---- legenda ----
%%LEGJS%%
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

SETA = ('<svg class="seta" viewBox="0 0 78 56" width="78" height="56"><path d="M4 28 L62 28 M42 8 L64 28 L42 48" fill="none" '
        'stroke="#15130F" stroke-width="12" stroke-linecap="square" stroke-linejoin="miter"/></svg>')

# trechos do H: (início, fim na linha do tempo, media-start, velocidade)
HSEG = [(C1, C2, 0.0, 0.75), (C3, C4, 1.44, 0.85), (C5, C6, 2.94, 0.72), (C6, C7, 4.474, 0.72), (C7, TOTAL, 0.30, 0.72)]
for a, b, m, r in HSEG:
    fim_src = m + (b - a) * r
    assert fim_src <= 6.25, (a, b, fim_src)
hbg, hwin = [], []
for n, (a, b, m, r) in enumerate(HSEG, 1):
    attrs = f'data-start="{R(a)}" data-duration="{R(b - a)}" data-media-start="{m}" data-playback-rate="{r}"'
    hwin.append(f'    <video id="vH{n}" class="clip full" {attrs} data-track-index="0" src="assets/clipe_H.mp4" muted playsinline></video>')
    attrs_bg = f'data-start="{R(a - 0.001)}" data-duration="{R(b - a + 0.001)}" data-media-start="{m}" data-playback-rate="{r}"'
    hbg.append(f'    <video id="vHb{n}" class="clip full" {attrs_bg} data-track-index="1" src="assets/clipe_H.mp4" muted playsinline></video>')
assert 3.4 + (C3 - C2) * 0.8 <= 5.0 and 0.8 + (C5 - C4) * 0.9 <= 2.4 and 3.36 <= 5.0

WW, WH = round(1080 * WS), round(1920 * WS)
rep = {
    "TOTAL": R(TOTAL), "WX": str(WX), "WY": str(WY), "WS": str(WS), "WW": str(WW), "WH": str(WH),
    "RASGO": RASGO, "RASGOF": RASGO_F, "SETA": SETA,
    "CNL": str(WX - 60), "CNR": str(WX + WW - 90), "CNT": str(WY + 30),
    "DV1": R(DUR_MP3["intro"]), "DV2": R(DUR_MP3["apresentacao"]), "DV3": R(DUR_MP3["cta"]),
    "C1": R(C1), "C2": R(C2), "C3": R(C3), "C4": R(C4), "C5": R(C5), "C6": R(C6), "C7": R(C7),
    "DH1": R(C2 - C1), "DG2": R(C3 - C2), "DH2": R(C4 - C3), "DI": R(C5 - C4), "DH5": R(C6 - C5 - 0.03),
    "DH3": R(TOTAL - C5), "DCTA": R(TOTAL - C6), "DTAG": R(TOTAL - C7),
    "TPECA": R(t_peca), "DCOL": R(C6 - t_peca),
    "D_G1A": R(t_i_cebola - 0.4), "TICEB": R(t_i_cebola), "TICEB16": R(t_i_cebola + 0.16),
    "D_G1B": R(C1 - t_i_cebola - 0.16), "TICAR": R(t_i_carne), "TICV": R(t_i_cv),
    "C1_30": R(C1 + 0.3), "D_H1": R(C2 - C1 - 0.3), "TSEIS": R(t_seis), "TTIQ": R(t_seis - 0.07),
    "C2_22": R(C2 + 0.22), "D_G2": R(C3 - C2 - 0.22), "C2_03": R(C2 + 0.03), "TCHEFE": R(t_chefe - 0.02), "TCEB": R(t_cebola),
    "C3_03": R(C3 + 0.03), "TTES": R(t_tes - 0.02), "TCV": R(t_cv),
    "C4_22": R(C4 + 0.22), "D_I": R(C5 - C4 - 0.22), "C4_03": R(C4 + 0.03), "TCUT": R(t_cut - 0.02), "TCARNE": R(t_carne),
    "C5_25": R(C5 + 0.25), "D_H5": R(C6 - C5 - 0.25), "C5_03": R(C5 + 0.03), "C5_12": R(C5 + 0.12),
    "D_H6": R(C7 - C6), "TPRIM": R(t_prim),
    "C7_20": R(C7 + 0.2), "C7_30": R(C7 + 0.3), "C7_50": R(C7 + 0.5), "D_H7": R(TOTAL - C7 - 0.3),
    "REPS": str(int((TOTAL - C7 - 0.5) / 0.24) - 1), "TCONF": R(t_conf), "TE": R(T("cta", 8) - 0.04), "TKIT": R(t_kit),
    "DOTS": dots_html, "DOTSJS": dots_js,
    "HBG": "\n".join(hbg), "HWIN": "\n".join(hwin),
    "LEG": "\n".join(leg_html), "LEGJS": "\n".join(leg_js),
}
for k, v in rep.items():
    html = html.replace(f"%%{k}%%", v)
assert "%%" not in html, [l for l in html.splitlines() if "%%" in l][:3]
open(OUT, "w").write(html)
print("ok", OUT, "TOTAL", TOTAL, "toca", t_toca, "seis", t_seis, "peca", t_peca, "cortes", C1, C2, C3, C4, C5, C6, C7)
