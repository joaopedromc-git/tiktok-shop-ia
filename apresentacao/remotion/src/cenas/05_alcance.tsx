import React from 'react';
import {Easing, interpolate, interpolateColors, useCurrentFrame} from 'remotion';
import {C, CL, Celular, Cena, F, contar, fmt, lerp, mola, rampa, saida} from '../comum';
import {FUNIL} from './06_funil';

export const DURACAO_05 = 207;

const W = {
  dezesseis: 9,
  visualizacoes: 78,
  dois: 118,
  quarenta: 152,
  cinco: 166,
  cento: 179,
};

// metricas/visualizacoes.csv (28 vídeos, ordem de postagem)
const VIDEOS: {produto: string; lote: string; v: number; violacao?: boolean}[] = [
  {produto: 'garrafa', lote: 'A', v: 2434, violacao: true},
  {produto: 'bodysplash', lote: 'A', v: 982},
  {produto: 'extensao', lote: 'A', v: 276},
  {produto: 'piseira', lote: 'A', v: 241, violacao: true},
  {produto: 'bodysplash', lote: 'B', v: 478},
  {produto: 'garrafa', lote: 'B', v: 1086},
  {produto: 'extensao', lote: 'B', v: 223},
  {produto: 'bodysplash', lote: 'C', v: 437},
  {produto: 'facas', lote: 'A', v: 241, violacao: true},
  {produto: 'facas', lote: 'B', v: 273},
  {produto: 'garrafa', lote: 'C', v: 442},
  {produto: 'bodysplash', lote: 'D', v: 4938},
  {produto: 'facas', lote: 'C', v: 321},
  {produto: 'extensao', lote: 'C', v: 216},
  {produto: 'garrafa', lote: 'D', v: 313},
  {produto: 'bodysplash', lote: 'E', v: 550},
  {produto: 'bodysplash', lote: 'F', v: 371},
  {produto: 'facas', lote: 'D', v: 326},
  {produto: 'extensao', lote: 'D', v: 223},
  {produto: 'garrafa', lote: 'E', v: 312},
  {produto: 'hilee', lote: 'A', v: 245},
  {produto: 'facas', lote: 'E', v: 227, violacao: true},
  {produto: 'bodysplash', lote: 'G', v: 339},
  {produto: 'hilee', lote: 'B', v: 228, violacao: true},
  {produto: 'bodysplash', lote: 'H', v: 231},
  {produto: 'extensao', lote: 'E', v: 206},
  {produto: 'garrafa', lote: 'F', v: 260},
  {produto: 'hilee', lote: 'C', v: 103, violacao: true},
];
const TOTAL = VIDEOS.reduce((a, b) => a + b.v, 0); // 16.522
const TOP = [11, 0]; // body splash D, garrafa A
const PARTE = (VIDEOS[11].v + VIDEOS[0].v) / TOTAL; // 0,446 → 45%

// Cartão e área do gráfico
const CARD = {x: 96, y: 196, w: 1272, h: 812};
const PLOT = {x0: CARD.x + 112, x1: CARD.x + CARD.w - 48, top: CARD.y + 150, base: CARD.y + CARD.h - 84};
const MAXV = 5000;
const ESC = (PLOT.base - PLOT.top) / MAXV;
const SLOT = (PLOT.x1 - PLOT.x0) / VIDEOS.length;
const BAR = 24;
const cx = (i: number) => PLOT.x0 + SLOT * (i + 0.5);

// Barra única que vira o topo do funil da cena 06
const FUSAO = {x: FUNIL.cx, y: 700, w: 72, h: 420};

export const Alcance05: React.FC = () => {
  const frame = useCurrentFrame();

  // --- Contador gigante
  const valor = contar(frame, W.dezesseis, W.visualizacoes - 4, TOTAL);
  const trava = mola(frame, W.visualizacoes - 4, {damping: 10});
  const soco = 1 + 0.05 * Math.sin(Math.min(1, (frame - (W.visualizacoes - 4)) / 8) * Math.PI) * (frame >= W.visualizacoes - 4 ? 1 : 0);
  const rotulo = mola(frame, W.visualizacoes);
  const mediana = mola(frame, W.visualizacoes + 8);
  const sobe = rampa(frame, W.dois, W.dois + 14, Easing.inOut(Easing.cubic)); // contador sobe e encolhe
  const progresso = interpolate(valor, [0, TOTAL], [0, 1], CL);

  // --- Gráfico
  const card = mola(frame, W.dois + 2);
  const quarenta = rampa(frame, W.quarenta, W.quarenta + 8);
  const anel = rampa(frame, W.quarenta, W.cinco + 6, Easing.out(Easing.cubic));
  const anelNum = contar(frame, W.quarenta, W.cinco + 6, 45);
  const celular = mola(frame, W.cento);
  const ext = rampa(frame, 181, 187);

  // --- Saída: barras se fundem, giram 90° e viram a faixa de cima do funil
  const fora = 1 - saida(frame, 192, 6);
  const funde = rampa(frame, 195, 201, Easing.inOut(Easing.cubic));
  const gira = rampa(frame, 201, 206, Easing.inOut(Easing.cubic));
  const cardFim = rampa(frame, 194, 206, Easing.inOut(Easing.cubic));
  const cardX = lerp(CARD.x, FUNIL.card.x, cardFim);
  const cardY = lerp(CARD.y + (1 - card) * 60, FUNIL.card.y, cardFim);
  const cardW = lerp(CARD.w, FUNIL.card.w, cardFim);
  const cardH = lerp(CARD.h, FUNIL.card.h, cardFim);

  const barras = VIDEOS.map((vd, i) => {
    const g = rampa(frame, W.dois + 2 + i * 0.75, W.dois + 12 + i * 0.75, Easing.out(Easing.cubic));
    const h = Math.max(2, vd.v * ESC * g);
    const topo = TOP.includes(i);
    const base = vd.violacao ? C.vermelho : '#9A9993';
    let cor = topo ? interpolateColors(quarenta, [0, 1], [base, C.lima]) : base;
    let op = topo ? 1 : lerp(1, 0.3, quarenta);
    cor = interpolateColors(funde, [0, 1], [cor, C.azul]);
    op = lerp(op, 1, funde);
    // retângulo normal
    const nx = cx(i) - BAR / 2;
    const ny = PLOT.base - h;
    // fundido
    const fx = lerp(nx, FUSAO.x - FUSAO.w / 2, funde);
    const fy = lerp(ny, FUSAO.y - FUSAO.h / 2, funde);
    const fw = lerp(BAR, FUSAO.w, funde);
    const fh = lerp(h, FUSAO.h, funde);
    return {i, vd, x: fx, y: fy, w: fw, h: fh, cor, op, g};
  });

  // giro: centro e altura do elemento único
  const giroCx = FUSAO.x;
  const giroCy = lerp(FUSAO.y, FUNIL.r1, gira);
  const giroH = lerp(FUSAO.h, FUNIL.larg, gira);

  const numScale = lerp(1, 0.3, sobe);
  const numX = lerp(960, 96, sobe);
  const numY = lerp(470, 92, sobe);

  return (
    <Cena
      id="05_alcance"
      duracao={DURACAO_05}
      respiroAte={[180, 203]}
      sfx={[
        {som: 'subida', quadro: W.dezesseis},
        {som: 'batida', quadro: W.visualizacoes - 3},
        {som: 'whoosh_curto', quadro: W.dois},
        {som: 'brilho', quadro: W.quarenta},
        {som: 'pop', quadro: W.cento},
      ]}
    >
      {/* eixo que vem da cena 04 + preenchimento do contador */}
      <div style={{position: 'absolute', left: 96, right: 96, top: 700, height: 2, background: 'rgba(255,255,255,.14)', opacity: 1 - sobe}} />
      <div
        style={{
          position: 'absolute',
          left: 96,
          width: 1728 * progresso,
          top: 699,
          height: 4,
          borderRadius: 2,
          background: C.lima,
          opacity: 1 - sobe,
        }}
      />

      {/* contador */}
      <div
        style={{
          position: 'absolute',
          left: numX,
          top: numY,
          transform: `translate(${lerp(-50, 0, sobe)}%, -50%) scale(${numScale * soco})`,
          transformOrigin: sobe > 0.5 ? '0% 50%' : '50% 50%',
          fontFamily: F.titulo,
          fontWeight: 800,
          fontSize: 300,
          lineHeight: 0.95,
          letterSpacing: '-0.02em',
          fontVariantNumeric: 'tabular-nums',
          color: C.lima,
          whiteSpace: 'nowrap',
          opacity: fora,
        }}
      >
        {fmt(valor)}
      </div>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 612,
          textAlign: 'center',
          opacity: Math.min(1, rotulo) * (1 - sobe),
          transform: `translateY(${(1 - rotulo) * 30 - sobe * 60}px)`,
          fontSize: 52,
          fontWeight: 500,
          color: C.texto,
        }}
      >
        visualizações
      </div>
      <div
        style={{
          position: 'absolute',
          left: 0,
          right: 0,
          top: 740,
          textAlign: 'center',
          opacity: Math.min(1, mediana) * (1 - sobe),
          transform: `translateY(${(1 - mediana) * 40 - sobe * 60}px)`,
          fontSize: 32,
          fontWeight: 500,
          color: C.texto2,
        }}
      >
        mediana de 294 por vídeo · 28 vídeos
      </div>
      {/* rótulo compacto no topo */}
      <div
        style={{
          position: 'absolute',
          left: 96 + 330,
          top: 66,
          display: 'flex',
          flexDirection: 'column',
          gap: 4,
          opacity: rampa(frame, W.dois + 8, W.dois + 16) * fora,
          transform: `translateX(${(1 - rampa(frame, W.dois + 8, W.dois + 18, Easing.out(Easing.cubic))) * 20}px)`,
        }}
      >
        <div style={{fontSize: 34, fontWeight: 600, color: C.texto}}>visualizações em 28 vídeos</div>
        <div style={{fontSize: 26, fontWeight: 500, color: C.texto2}}>mediana de 294 por vídeo</div>
      </div>

      {/* cartão do gráfico */}
      <div
        style={{
          position: 'absolute',
          left: cardX,
          top: cardY,
          width: cardW,
          height: cardH,
          borderRadius: 24,
          background: C.cartao,
          opacity: Math.min(1, card * 1.6),
          boxShadow: '0 30px 80px rgba(0,0,0,.35)',
        }}
      />
      {/* chrome do gráfico */}
      <div style={{position: 'absolute', inset: 0, opacity: Math.min(1, card * 1.6) * fora, transform: `translateY(${(1 - card) * 60}px)`}}>
        <div style={{position: 'absolute', left: CARD.x + 48, top: CARD.y + 40, color: C.cartaoTexto, fontSize: 28, fontWeight: 600}}>
          Visualizações por vídeo
          <span style={{color: C.cartaoTexto2, fontWeight: 500, fontSize: 22}}>{'  '}· na ordem de postagem</span>
        </div>
        <div style={{position: 'absolute', right: 1920 - (CARD.x + CARD.w - 48), top: CARD.y + 46, display: 'flex', gap: 24, fontSize: 20, fontWeight: 500, color: C.cartaoTexto2}}>
          {[
            {c: '#9A9993', t: 'vídeo'},
            {c: C.vermelho, t: 'levou violação'},
          ].map((l) => (
            <div key={l.t} style={{display: 'flex', alignItems: 'center', gap: 8}}>
              <div style={{width: 14, height: 14, borderRadius: 3, background: l.c}} />
              {l.t}
            </div>
          ))}
        </div>
        {/* grade: um eixo só */}
        {[0, 1000, 2000, 3000, 4000, 5000].map((t) => (
          <React.Fragment key={t}>
            <div style={{position: 'absolute', left: PLOT.x0, width: PLOT.x1 - PLOT.x0, top: PLOT.base - t * ESC, height: 1, background: t === 0 ? '#BDBCB6' : C.cartaoLinha}} />
            <div
              style={{
                position: 'absolute',
                right: 1920 - PLOT.x0 + 14,
                top: PLOT.base - t * ESC - 12,
                fontSize: 19,
                fontWeight: 500,
                color: C.cartaoTexto2,
                fontVariantNumeric: 'tabular-nums',
              }}
            >
              {fmt(t)}
            </div>
          </React.Fragment>
        ))}
        <div style={{position: 'absolute', left: cx(0) - 20, width: 40, textAlign: 'center', top: PLOT.base + 12, fontSize: 19, color: C.cartaoTexto2, fontWeight: 500}}>1º</div>
        <div style={{position: 'absolute', left: cx(27) - 20, width: 40, textAlign: 'center', top: PLOT.base + 12, fontSize: 19, color: C.cartaoTexto2, fontWeight: 500}}>28º</div>
        <div style={{position: 'absolute', left: PLOT.x0, width: PLOT.x1 - PLOT.x0, textAlign: 'center', top: PLOT.base + 12, fontSize: 19, color: C.cartaoTexto2, fontWeight: 500}}>
          05/10 → 04/11/2026
        </div>
      </div>

      {/* barras */}
      {frame < 201
        ? barras.map((b) => (
            <div
              key={b.i}
              style={{
                position: 'absolute',
                left: b.x,
                top: b.y,
                width: b.w,
                height: b.h,
                background: b.cor,
                opacity: b.op * Math.min(1, card * 1.6),
                borderRadius: funde > 0 ? `${4}px` : '4px 4px 0 0',
                transform: `translateY(${(1 - card) * 60}px)`,
              }}
            />
          ))
        : (
          <div
            style={{
              position: 'absolute',
              left: giroCx - FUSAO.w / 2,
              top: giroCy - giroH / 2,
              width: FUSAO.w,
              height: giroH,
              background: C.azul,
              borderRadius: 4,
              transform: `rotate(${90 * gira}deg)`,
            }}
          />
        )}

      {/* rótulos diretos das duas maiores */}
      <div style={{position: 'absolute', inset: 0, opacity: quarenta * fora}}>
        {TOP.map((i) => (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: cx(i) - 80,
              width: 160,
              textAlign: 'center',
              top: PLOT.base - VIDEOS[i].v * ESC - 40,
              fontSize: 24,
              fontWeight: 700,
              color: C.cartaoTexto,
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {fmt(VIDEOS[i].v)}
          </div>
        ))}
      </div>

      {/* extensão: ~220 com qualquer receita */}
      <div style={{position: 'absolute', inset: 0, opacity: ext * fora}}>
        {VIDEOS.map((v, i) =>
          v.produto === 'extensao' ? (
            <div
              key={i}
              style={{
                position: 'absolute',
                left: cx(i) - BAR / 2 - 5,
                top: PLOT.base - v.v * ESC - 5,
                width: BAR + 10,
                height: v.v * ESC + 5,
                border: `2px solid ${C.azul}`,
                borderBottom: 'none',
                borderRadius: '7px 7px 0 0',
                boxSizing: 'border-box',
              }}
            />
          ) : null,
        )}
        <div
          style={{
            position: 'absolute',
            right: 1920 - PLOT.x1,
            top: PLOT.base - 128,
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            padding: '6px 14px',
            borderRadius: 999,
            background: 'rgba(61,139,255,.10)',
            border: `1px solid rgba(61,139,255,.45)`,
            fontSize: 21,
            fontWeight: 600,
            color: C.cartaoTexto,
            transform: `translateY(${(1 - ext) * 10}px)`,
          }}
        >
          <div style={{width: 10, height: 10, borderRadius: 99, background: C.azul}} />
          extensão: ~220 com qualquer receita
        </div>
      </div>

      {/* anel: 2 vídeos = 45% */}
      <div
        style={{
          position: 'absolute',
          left: CARD.x + CARD.w + 40,
          width: 1824 - (CARD.x + CARD.w + 40),
          top: 300,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          opacity: Math.min(1, mola(frame, W.quarenta) * 1.5) * fora,
          transform: `scale(${0.92 + 0.08 * mola(frame, W.quarenta)})`,
        }}
      >
        <div style={{position: 'relative', width: 300, height: 300}}>
          <svg width={300} height={300} style={{position: 'absolute', inset: 0, transform: 'rotate(-90deg)'}}>
            <circle cx={150} cy={150} r={130} fill="none" stroke="rgba(255,255,255,.10)" strokeWidth={16} />
            <circle
              cx={150}
              cy={150}
              r={130}
              fill="none"
              stroke={C.lima}
              strokeWidth={16}
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={`${PARTE * anel} 1`}
            />
          </svg>
          <div
            style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontFamily: F.titulo,
              fontWeight: 800,
              fontSize: 88,
              letterSpacing: '-0.02em',
              color: C.lima,
              fontVariantNumeric: 'tabular-nums',
            }}
          >
            {anelNum}%
          </div>
        </div>
        <div style={{marginTop: 26, fontSize: 40, fontWeight: 600, color: C.texto}}>2 vídeos</div>
        <div style={{marginTop: 6, fontSize: 26, fontWeight: 500, color: C.texto2}}>de {fmt(TOTAL)} visualizações</div>
      </div>

      {/* celular do body splash D ao lado da barra */}
      {frame >= W.cento - 2 ? (
        <div
          style={{
            position: 'absolute',
            left: cx(11) - BAR / 2 - 16 - 204,
            top: 404,
            opacity: Math.min(1, celular * 1.5) * fora,
            transform: `translateY(${(1 - celular) * 80}px) scale(${0.92 + 0.08 * celular})`,
            transformOrigin: '100% 100%',
          }}
        >
          <Celular src="midia/bodysplash_D.mp4" largura={204} inicioVideo={30} />
        </div>
      ) : null}
      <div
        style={{
          position: 'absolute',
          right: 1920 - (cx(11) - BAR / 2 - 16),
          top: 350,
          opacity: Math.min(1, mola(frame, W.cento + 3) * 1.5) * fora,
          transform: `translateY(${(1 - mola(frame, W.cento + 3)) * 20}px)`,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '6px 14px',
          borderRadius: 999,
          background: C.cartaoTexto,
          color: C.texto,
          fontSize: 21,
          fontWeight: 600,
          whiteSpace: 'nowrap',
        }}
      >
        <div style={{width: 10, height: 10, borderRadius: 99, background: C.lima}} />
        body splash D · 4.938
      </div>
    </Cena>
  );
};
