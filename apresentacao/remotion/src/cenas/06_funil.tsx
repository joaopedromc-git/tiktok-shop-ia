import React from 'react';
import {Easing, interpolate, interpolateColors, useCurrentFrame} from 'remotion';
import {C, CL, Cena, F, Pilula, contar, fmt, lerp, mola, rampa, saida} from '../comum';

export const DURACAO_06 = 338;

// Geometria compartilhada com a saída da cena 05 (a barra girada vira a faixa de cima)
export const FUNIL = {
  card: {x: 96, y: 72, w: 1728, h: 936},
  cx: 1240,
  larg: 1000,
  r1: 330,
  r2: 560,
  r3: 790,
  h: 72,
};

const W = {
  dezessete: 9,
  impressoes: 55,
  cento: 81,
  cliques: 107,
  duas: 125,
  vendas: 136,
  vinte: 161,
  comissao: 225,
  retorno: 248,
  gargalo: 291,
  clique: 312,
};

// metricas/vendas_2026-10.md
const IMPRESSOES = 17800;
const CLIQUES = 135;
const VENDAS = 2;

const larg = (v: number) => Math.max(4, (FUNIL.larg * v) / IMPRESSOES);
const L1 = larg(IMPRESSOES);
const L2 = larg(CLIQUES); // 7,6 px: o salto é real
const L3 = larg(VENDAS);

export const Funil06: React.FC = () => {
  const frame = useCurrentFrame();
  const {cx, r1, r2, r3, h} = FUNIL;

  const titulo = mola(frame, 2);
  const n1 = contar(frame, W.dezessete, W.impressoes - 6, IMPRESSOES);
  const rot1 = mola(frame, W.dezessete);

  // queda para os cliques
  const cai = rampa(frame, W.cento, W.cento + 12, Easing.in(Easing.quad));
  const rot2 = mola(frame, W.cento + 2);
  const n2 = contar(frame, W.cento + 2, W.cliques - 4, CLIQUES);
  const pct = mola(frame, W.cliques);

  // vendas: dois pontos caem
  const cai2 = rampa(frame, W.duas - 6, W.duas + 4, Easing.in(Easing.quad));
  const ponto = (ini: number) => {
    const t = interpolate(frame, [ini, ini + 9], [0, 1], {...CL, easing: Easing.in(Easing.quad)});
    const quique = frame > ini + 9 ? Math.abs(Math.sin(((frame - ini - 9) / 7) * Math.PI)) * Math.max(0, 1 - (frame - ini - 9) / 10) * 14 : 0;
    return {y: lerp(r2 + h / 2, r3, t) - quique, vis: frame >= ini ? 1 : 0, chegou: frame >= ini + 9};
  };
  const p1 = ponto(W.duas);
  const p2 = ponto(W.vendas);
  const n3 = (p1.chegou ? 1 : 0) + (p2.chegou ? 1 : 0);
  const rot3 = mola(frame, W.duas);
  const gmv = mola(frame, W.vendas + 12);

  // comissão: tudo encolhe para a esquerda
  const esq = rampa(frame, W.vinte - 7, W.vinte + 5, Easing.inOut(Easing.cubic));
  const volta = rampa(frame, W.gargalo - 2, W.gargalo + 12, Easing.inOut(Easing.cubic));
  const encolhe = esq * (1 - volta);
  const escala = lerp(1, 0.55, encolhe);
  const com = mola(frame, W.vinte + 3) * (1 - saida(frame, W.gargalo - 4, 8));
  const valorCom = contar(frame, W.vinte + 3, W.comissao - 6, 23.13, 2);
  const travaCom = frame >= W.comissao - 6 ? mola(frame, W.comissao - 6, {damping: 10}) : 0;
  const retorno = rampa(frame, W.retorno, W.retorno + 9, Easing.out(Easing.quad));

  // gargalo
  const garg = rampa(frame, W.gargalo + 6, W.gargalo + 14);
  const pulso = 0.55 + 0.45 * Math.cos(((frame - W.gargalo) / 15) * Math.PI * 2);
  const vermelho = rampa(frame, 322, 328);
  const corGarg = interpolateColors(vermelho, [0, 1], [C.lima, C.vermelho]);
  const callout = mola(frame, W.gargalo + 8);

  // corte em preto nos 2 últimos quadros
  const corte = frame >= DURACAO_06 - 2;

  // conector 1 (impressões → cliques)
  const y1b = r1 + h / 2;
  const y2t = r2 - h / 2;
  const yQueda = lerp(y1b, y2t, cai);
  const wQueda = lerp(L1, L2, cai);
  const con1 = `M${cx - L1 / 2},${y1b} L${cx + L1 / 2},${y1b} L${cx + wQueda / 2},${yQueda} L${cx - wQueda / 2},${yQueda} Z`;
  const y2b = r2 + h / 2;
  const y3t = r3 - h / 2;
  const yQ2 = lerp(y2b, y3t, cai2);
  const con2 = `M${cx - L2 / 2},${y2b} L${cx + L2 / 2},${y2b} L${cx + lerp(L2, L3, cai2) / 2},${yQ2} L${cx - lerp(L2, L3, cai2) / 2},${yQ2} Z`;

  const Linha: React.FC<{y: number; num: string; unidade: string; o: number; extra?: React.ReactNode}> = ({y, num, unidade, o, extra}) => (
    <div style={{position: 'absolute', left: 168, top: y - 66, opacity: Math.min(1, o * 1.5), transform: `translateX(${(1 - o) * -40}px)`}}>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 18}}>
        <div style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 96, lineHeight: 0.95, letterSpacing: '-0.02em', color: C.cartaoTexto, fontVariantNumeric: 'tabular-nums'}}>
          {num}
        </div>
        {extra}
      </div>
      <div style={{marginTop: 6, fontSize: 30, fontWeight: 500, color: C.cartaoTexto2}}>{unidade}</div>
    </div>
  );

  if (corte) return <Cena id="06_funil" duracao={DURACAO_06} sfx={[]}>{null}</Cena>;

  return (
    <Cena
      id="06_funil"
      duracao={DURACAO_06}
      sfx={[
        {som: 'subida', quadro: W.dezessete},
        {som: 'whoosh_curto', quadro: W.cento},
        {som: 'pop', quadro: W.duas},
        {som: 'pop', quadro: W.vendas, volume: 0.22},
        {som: 'tique', quadro: W.vinte},
        {som: 'batida', quadro: W.gargalo},
      ]}
    >
      {/* cartão + funil (encolhe para a esquerda na comissão) */}
      <div
        style={{
          position: 'absolute',
          inset: 0,
          transform: `scale(${escala})`,
          transformOrigin: `${FUNIL.card.x}px 540px`,
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: FUNIL.card.x,
            top: FUNIL.card.y,
            width: FUNIL.card.w,
            height: FUNIL.card.h,
            borderRadius: 24,
            background: C.cartao,
            boxShadow: '0 30px 80px rgba(0,0,0,.35)',
          }}
        />
        <div style={{position: 'absolute', left: 168, top: 120, opacity: Math.min(1, titulo * 1.5), transform: `translateY(${(1 - titulo) * 20}px)`}}>
          <div style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 60, lineHeight: 0.95, letterSpacing: '-0.02em', color: C.cartaoTexto}}>Funil de outubro</div>
          <div style={{marginTop: 10, fontSize: 22, fontWeight: 500, color: C.cartaoTexto2}}>painel de afiliado do TikTok Shop · 1 a 31/10/2026</div>
        </div>

        <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
          {/* lavagem dos conectores */}
          {frame >= W.cento ? <path d={con1} fill={C.azul} opacity={0.12} /> : null}
          {frame >= W.duas - 6 ? <path d={con2} fill={C.azul} opacity={0.12} /> : null}
          {/* destaque do gargalo */}
          {garg > 0 ? (
            <path
              d={con1}
              fill={corGarg}
              fillOpacity={0.42 * garg}
              stroke={corGarg}
              strokeWidth={4}
              strokeOpacity={garg * (vermelho > 0 ? 1 : pulso)}
              strokeLinejoin="round"
            />
          ) : null}
          {/* faixas */}
          <rect x={cx - L1 / 2} y={r1 - h / 2} width={L1} height={h} rx={4} fill={C.azul} />
          {cai >= 1 ? <rect x={cx - L2 / 2} y={r2 - h / 2} width={L2} height={h} rx={2} fill={C.azul} /> : null}
          {cai2 >= 1 ? <rect x={cx - L3 / 2} y={r3 - h / 2} width={L3} height={h} rx={2} fill={C.azul} /> : null}
          {/* vendas */}
          {[
            {p: p1, dx: -26},
            {p: p2, dx: 26},
          ].map(({p, dx}, i) =>
            p.vis ? <circle key={i} cx={cx + dx} cy={p.y} r={15} fill={C.lima} stroke={C.cartaoTexto} strokeWidth={2.5} /> : null,
          )}
        </svg>

        <Linha y={r1} num={fmt(n1)} unidade="impressões do produto" o={rot1} />
        <Linha
          y={r2}
          num={fmt(n2)}
          unidade="cliques no produto"
          o={rot2}
          extra={
            <div
              style={{
                opacity: Math.min(1, pct * 1.5),
                transform: `scale(${0.9 + 0.1 * pct})`,
                fontSize: 26,
                fontWeight: 600,
                color: C.cartaoTexto,
                background: '#EFEEE9',
                borderRadius: 999,
                padding: '6px 14px',
                whiteSpace: 'nowrap',
              }}
            >
              0,76% das impressões
            </div>
          }
        />
        <Linha
          y={r3}
          num={fmt(n3)}
          unidade={n3 === 1 ? 'venda' : 'vendas'}
          o={rot3}
          extra={
            <div style={{opacity: Math.min(1, gmv * 1.5), transform: `translateY(${(1 - gmv) * 10}px)`, fontSize: 26, fontWeight: 500, color: C.cartaoTexto2, whiteSpace: 'nowrap'}}>
              R$ 290,06 em vendas
            </div>
          }
        />

        {/* chamada do gargalo */}
        <div style={{position: 'absolute', left: 1352, top: 474, opacity: Math.min(1, callout * 1.5), transform: `translateX(${(1 - callout) * 30}px)`}}>
          <svg width={70} height={40} style={{position: 'absolute', left: -76, top: 10}}>
            <path d="M64,20 L8,20 M18,11 L8,20 L18,29" fill="none" stroke={C.cartaoTexto} strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <div style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 48, lineHeight: 0.95, letterSpacing: '-0.02em', color: C.cartaoTexto, whiteSpace: 'nowrap'}}>
            gargalo: o clique
          </div>
          <div style={{marginTop: 12, fontSize: 26, fontWeight: 500, color: C.cartaoTexto2, whiteSpace: 'nowrap'}}>menos de 1% toca no produto</div>
        </div>
      </div>

      {/* comissão */}
      <div
        style={{
          position: 'absolute',
          left: 1120,
          width: 704,
          top: 330,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          opacity: Math.min(1, com * 1.5),
          transform: `translateX(${(1 - Math.min(1, com)) * 60}px)`,
        }}
      >
        <div
          style={{
            fontFamily: F.titulo,
            fontWeight: 800,
            fontSize: 168,
            lineHeight: 0.95,
            letterSpacing: '-0.02em',
            color: C.lima,
            fontVariantNumeric: 'tabular-nums',
            whiteSpace: 'nowrap',
            transform: `scale(${1 + 0.05 * Math.sin(Math.min(1, travaCom) * Math.PI)})`,
            transformOrigin: '0% 50%',
          }}
        >
          R$ {fmt(valorCom, 2)}
        </div>
        <div style={{marginTop: 18, fontSize: 46, fontWeight: 500, color: C.texto}}>de comissão</div>
        <div style={{marginTop: 34, opacity: retorno}}>
          <Pilula corTexto={C.texto2} tamanho={26}>
            retorno pequeno
          </Pilula>
        </div>
      </div>
    </Cena>
  );
};
