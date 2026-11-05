import React from 'react';
import {Easing, Sequence, interpolate, interpolateColors, useCurrentFrame} from 'remotion';
import {C, CL, Celular, Cena, F, Visto, contar, lerp, mola, qp, rampa, saida} from '../comum';

export const DURACAO_09 = 359;

// public/audio/09_revisor.json → quadro da cena = round((0,25 + início) × 30)
const W = {
  erros: qp(0.166),
  memoria: qp(0.991),
  revisor: qp(1.829),
  testes: qp(2.914),
  alegacao: qp(3.928),
  exagerada: qp(4.424),
  dois: qp(5.485),
  estaticos: qp(6.192),
  seguinte: qp(7.725),
  passou: qp(8.137),
  em: qp(8.444),
  tudo: qp(8.574),
  punido: qp(9.211),
  inconsistente: qp(10.26),
};

// ---------- Fase 0: o prompt que vem da cena 08 (mesma posição do último quadro dela, já com a escala 1,03) ----------
const PROMPT = {x: 672, y: 561, w: 577, h: 107};

// ---------- Fase 1: memória (produtos/aprendizados.md, resumido das linhas reais) ----------
const REGISTROS = [
  '12/10 · facas A · quadro estático: os 3 clipes só com câmera',
  '21/10 · facas E · alegação: “do primeiro ao último”, “adeus”',
  '08/10 · peseira A · produto inconsistente: o quarto da foto no quadro',
  '08/10 · extensão B · o clipe começou com outra extensão',
  '09/10 · body splash E · o Veo escreveu texto no canto',
  '10/10 · extensão D · o Veo não respeita a contagem de tomadas',
  '12/10 · facas · o Veo ignora “very slow push-in”',
  '14/10 · extensão I · luz e sombra não substituem a mão',
  '15/10 · garrafa D · a mão levanta rápido e alto demais',
  '19/10 · facas D · Lite só com mão parada',
  '09/10 · body splash D · a luz estourou um rótulo',
  '04/11 · Hilee C · produto inconsistente: comparar com as fotos',
];

// ---------- Fase 2: terminal com a saída real de revisor/revisar.py ----------
type Seg = {t: string; cor?: string; peso?: number; marca?: boolean; pilula?: boolean; antes?: number};
type Linha = {f: number; segs: Seg[]; digita?: [number, number]; bloco: 'E' | 'A'};
const TERM = {x: 160, y: 182, w: 1600, h: 776, barra: 58, pad: 30};
const LH = 46;
const VIEW = TERM.h - TERM.barra - TERM.pad * 2;

const T2 = C.texto2;
const RE = W.alegacao;
const LINHAS: Linha[] = [
  {bloco: 'E', f: W.revisor + 1, digita: [W.revisor + 3, W.revisor + 20], segs: [{t: '$ ', cor: C.lima, peso: 700}, {t: 'python revisor/revisar.py facas E'}]},
  {bloco: 'E', f: W.revisor + 24, segs: [{t: '== Regras fixas do texto: ', cor: T2}, {t: 'REPROVA', cor: C.vermelho, peso: 700, antes: RE}]},
  {bloco: 'E', f: RE + 2, segs: [{t: '   - ', cor: T2}, {t: '“do primeiro ao último”', marca: true}, {t: ': promessa absoluta ou de desempenho no tempo', cor: T2}]},
  {bloco: 'E', f: RE + 5, segs: [{t: '   - ', cor: T2}, {t: '“adeus”', marca: true}, {t: ': promessa absoluta ou de desempenho no tempo', cor: T2}]},
  {bloco: 'E', f: W.revisor + 30, segs: [{t: '== Agente revisor-conformidade: ', cor: T2}, {t: 'REPROVA', cor: C.vermelho, peso: 700, antes: RE + 8}]},
  {bloco: 'E', f: W.revisor + 36, segs: [{t: '== Movimento real no vídeo: ', cor: T2}, {t: 'APROVA', cor: C.lima, peso: 700, antes: RE + 10}]},
  {bloco: 'E', f: RE + 11, segs: [{t: '   27% do tempo sem movimento além da câmera ', cor: T2}, {t: '(reprova a partir de 60%)', cor: 'rgba(169,167,159,.6)'}]},
  {bloco: 'E', f: W.exagerada, segs: [{t: 'VEREDITO: ', peso: 700}, {t: 'REPROVA', pilula: true}]},
  {bloco: 'A', f: W.dois - 1, segs: [{t: ' '}]},
  {bloco: 'A', f: W.dois, digita: [W.dois + 1, W.dois + 8], segs: [{t: '$ ', cor: C.lima, peso: 700}, {t: 'python revisor/revisar.py facas A'}]},
  {bloco: 'A', f: W.dois + 10, segs: [{t: '== Regras fixas do texto: ', cor: T2}, {t: 'APROVA', cor: C.lima, peso: 700}]},
  {bloco: 'A', f: W.dois + 12, segs: [{t: '== Agente revisor-conformidade: ', cor: T2}, {t: 'REPROVA', cor: C.vermelho, peso: 700}]},
  {bloco: 'A', f: W.dois + 14, segs: [{t: '== Movimento real no vídeo: ', cor: T2}, {t: 'REPROVA', cor: C.vermelho, peso: 700}]},
  {bloco: 'A', f: W.dois + 16, segs: [{t: '   ', cor: T2}, {t: '74%', marca: true}, {t: ' do tempo sem movimento real além da câmera', cor: T2}]},
  {bloco: 'A', f: W.dois + 18, segs: [{t: '   - parado de ', cor: T2}, {t: '2,3 s a 4,7 s', cor: C.texto}, {t: '  e de ', cor: T2}, {t: '18,3 s a 20,5 s', cor: C.texto}, {t: '  (+3 trechos)', cor: 'rgba(169,167,159,.6)'}]},
  {bloco: 'A', f: W.dois + 20, segs: [{t: 'VEREDITO: ', peso: 700}, {t: 'REPROVA', pilula: true}]},
];

const SegView: React.FC<{s: Seg; frame: number; fLinha: number}> = ({s, frame, fLinha}) => {
  if (s.antes !== undefined && frame < s.antes) {
    const n = 1 + (Math.floor((frame - fLinha) / 4) % 3);
    return <span style={{color: 'rgba(169,167,159,.6)'}}>{'.'.repeat(n)}</span>;
  }
  const inicio = s.antes ?? fLinha;
  if (s.pilula) {
    const m = mola(frame, inicio, {damping: 11});
    return (
      <span
        style={{
          display: 'inline-block',
          padding: '0 16px',
          borderRadius: 10,
          background: C.vermelho,
          color: C.fundo,
          fontFamily: F.titulo,
          fontWeight: 800,
          letterSpacing: '0.01em',
          transform: `scale(${lerp(1.6, 1, Math.min(1, m))})`,
          transformOrigin: '0% 50%',
          boxShadow: `0 0 ${30 * Math.max(0, 1 - (frame - inicio) / 14)}px rgba(255,77,77,.8)`,
        }}
      >
        {s.t}
      </span>
    );
  }
  if (s.marca) {
    const p = rampa(frame, inicio, inicio + 6, Easing.out(Easing.cubic));
    return (
      <span style={{position: 'relative', color: interpolateColors(p, [0, 1], [C.texto, C.vermelho]), fontWeight: 600}}>
        <span
          style={{
            position: 'absolute',
            left: -4,
            right: -4,
            top: 4,
            bottom: 2,
            borderRadius: 6,
            background: 'rgba(255,77,77,.16)',
            transform: `scaleX(${p})`,
            transformOrigin: '0% 50%',
          }}
        />
        <span
          style={{position: 'absolute', left: 0, bottom: 2, height: 3, width: `${p * 100}%`, background: C.vermelho, borderRadius: 2}}
        />
        <span style={{position: 'relative'}}>{s.t}</span>
      </span>
    );
  }
  const novo = s.antes !== undefined ? mola(frame, s.antes, {damping: 12}) : 1;
  return (
    <span
      style={{
        color: s.cor ?? C.texto,
        fontWeight: s.peso ?? 500,
        display: s.antes !== undefined ? 'inline-block' : undefined,
        transform: s.antes !== undefined ? `scale(${lerp(1.35, 1, Math.min(1, novo))})` : undefined,
        transformOrigin: '0% 60%',
      }}
    >
      {s.t}
    </span>
  );
};

const Terminal: React.FC<{frame: number}> = ({frame}) => {
  // altura de cada linha cresce ao aparecer: as linhas novas empurram as de baixo
  const alturas = LINHAS.map((l) => rampa(frame, l.f, l.f + 5, Easing.out(Easing.cubic)));
  const ys: number[] = [];
  let acc = 0;
  alturas.forEach((h) => {
    ys.push(acc);
    acc += h * LH;
  });
  const rolagem = Math.max(0, acc - VIEW);
  const apagaE = rampa(frame, W.dois - 2, W.dois + 8);
  const ultima = LINHAS.reduce((u, l, i) => (frame >= l.f ? i : u), 0);

  return (
    <div style={{position: 'absolute', left: TERM.pad + 10, right: TERM.pad, top: TERM.barra + TERM.pad, height: VIEW, overflow: 'hidden'}}>
      {LINHAS.map((l, i) => {
        if (frame < l.f) return null;
        const vis = rampa(frame, l.f + 3, l.f + 7);
        let segs = l.segs;
        let digitando = false;
        if (l.digita) {
          const total = segs.reduce((a, s) => a + s.t.length, 0);
          const n = Math.round(interpolate(frame, l.digita, [2, total], CL));
          digitando = n < total;
          let resta = n;
          segs = segs.map((s) => {
            const t = s.t.slice(0, Math.max(0, resta));
            resta -= s.t.length;
            return {...s, t};
          });
        }
        const cursor = l.digita && (digitando || (i === ultima && Math.floor(frame / 8) % 2 === 0));
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 0,
              top: ys[i] - rolagem,
              height: LH,
              lineHeight: `${LH}px`,
              whiteSpace: 'pre',
              fontSize: 30,
              fontWeight: 500,
              fontVariantNumeric: 'tabular-nums',
              opacity: vis * (l.bloco === 'E' ? lerp(1, 0.38, apagaE) : 1),
              transform: `translateY(${(1 - vis) * 8}px)`,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            {segs.map((s, k) => (
              <SegView key={k} s={s} frame={frame} fLinha={l.f} />
            ))}
            {cursor ? <span style={{display: 'inline-block', width: 16, height: 34, marginLeft: 4, background: C.lima}} /> : null}
          </div>
        );
      })}
    </div>
  );
};

// ---------- Fase 3: placar (evals/resultados.md) ----------
const PLACAR = {w: 1000, h: 600};

const Quadrado: React.FC<{pegou: boolean; p: number}> = ({pegou, p}) => (
  <div
    style={{
      width: 30,
      height: 30,
      borderRadius: 7,
      boxSizing: 'border-box',
      background: pegou ? C.lima : 'transparent',
      border: pegou ? `2px solid #9DC21E` : '2.5px solid #B9B8B2',
      transform: `scale(${0.4 + 0.6 * p})`,
      opacity: Math.min(1, p * 1.5),
    }}
  />
);

const Placar: React.FC<{frame: number}> = ({frame}) => {
  const linhas = [
    {rot: 'alegação exagerada', q: [true], val: '1 de 1', tipo: 'lima' as const, f: W.estaticos + 3},
    {rot: 'quadro estático', q: [true, false], val: '1 de 2', tipo: 'meio' as const, f: W.estaticos + 9},
    {rot: 'produto inconsistente', q: [] as boolean[], val: 'fora do escopo', tipo: 'cinza' as const, f: W.estaticos + 15},
  ];
  // "fora do escopo" pisca em vermelho no "punido"
  const pisca = frame >= W.punido && frame < W.punido + 30 ? (Math.floor((frame - W.punido) / 5) % 2 === 0 ? 1 : 0.35) : frame >= W.punido + 30 ? 1 : 0;
  const vermelho = frame >= W.punido ? pisca : 0;
  return (
    <div
      style={{
        width: PLACAR.w,
        height: PLACAR.h,
        borderRadius: 24,
        background: C.cartao,
        boxShadow: '0 30px 80px rgba(0,0,0,.45)',
        boxSizing: 'border-box',
        padding: '44px 56px',
        color: C.cartaoTexto,
        position: 'relative',
      }}
    >
      <div style={{display: 'flex', alignItems: 'baseline', justifyContent: 'space-between'}}>
        <div style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 56, lineHeight: 0.95, letterSpacing: '-0.02em'}}>Placar do revisor</div>
        <div style={{display: 'flex', alignItems: 'center', gap: 10, fontSize: 21, fontWeight: 500, color: C.cartaoTexto2}}>
          <Quadrado pegou p={1} /> pegou
          <span style={{width: 6}} />
          <Quadrado pegou={false} p={1} /> passou
        </div>
      </div>
      <div style={{marginTop: 10, fontSize: 24, fontWeight: 500, color: C.cartaoTexto2}}>vídeos punidos pelo TikTok, por tipo de violação</div>
      <div style={{marginTop: 34, display: 'flex', flexDirection: 'column'}}>
        {linhas.map((l, i) => {
          const m = mola(frame, l.f);
          const ultimo = i === 2;
          const corPilula =
            l.tipo === 'lima'
              ? {background: C.lima, color: C.fundo}
              : l.tipo === 'meio'
                ? {background: `linear-gradient(90deg, ${C.lima} 0%, ${C.lima} 50%, #DAD9D3 50%, #DAD9D3 100%)`, color: C.fundo}
                : {
                    background: interpolateColors(vermelho, [0, 1], ['#E6E5E0', C.vermelho]),
                    color: interpolateColors(vermelho, [0, 1], [C.cartaoTexto2, C.fundo]),
                  };
          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                height: 104,
                borderTop: `1px solid ${C.cartaoLinha}`,
                opacity: Math.min(1, m * 1.5),
                transform: `translateY(${(1 - Math.min(1, m)) * 24}px)`,
                background: ultimo && vermelho > 0 ? `rgba(255,77,77,${(0.08 * vermelho).toFixed(3)})` : undefined,
              }}
            >
              <div style={{width: 430, fontSize: 36, fontWeight: 600, color: ultimo ? C.cartaoTexto2 : C.cartaoTexto}}>{l.rot}</div>
              <div style={{width: 130, display: 'flex', gap: 10}}>
                {l.q.map((pg, k) => (
                  <Quadrado key={k} pegou={pg} p={mola(frame, l.f + 4 + k * 4)} />
                ))}
              </div>
              <div
                style={{
                  marginLeft: 'auto',
                  padding: '8px 22px',
                  borderRadius: 999,
                  fontFamily: l.tipo === 'cinza' ? F.corpo : F.titulo,
                  fontWeight: l.tipo === 'cinza' ? 600 : 800,
                  fontSize: l.tipo === 'cinza' ? 30 : 40,
                  fontVariantNumeric: 'tabular-nums',
                  whiteSpace: 'nowrap',
                  ...corPilula,
                }}
              >
                {l.val}
              </div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: 56, bottom: 36, fontSize: 26, fontWeight: 500, color: C.cartaoTexto2}}>testado nos 27 vídeos postados</div>
    </div>
  );
};

// ---------- Fase 4: Hilee C ----------
const CEL = {w: 420, h: 747, y: 200, xDir: 1310, xFim: 750}; // xFim/y = posição de abertura da cena 10

export const Revisor09: React.FC = () => {
  const frame = useCurrentFrame();

  // Fase 0 → 1: o prompt da 08 vira registro na memória
  const promptSai = saida(frame, W.erros + 6, 10);
  const nomeVermelho = rampa(frame, W.erros, W.erros + 6);
  const voa = rampa(frame, W.erros + 8, W.memoria + 2, Easing.inOut(Easing.cubic));
  const cursorPisca = Math.floor(frame / 8) % 2 === 0 ? 1 : 0;

  // Memória
  const doc = mola(frame, W.memoria - 5);
  const n58 = contar(frame, W.memoria, W.revisor - 4, 58);
  const canto = rampa(frame, W.revisor - 2, W.revisor + 12, Easing.inOut(Easing.cubic));
  const somePapel = saida(frame, W.seguinte, 8);
  const fundoReg = rampa(frame, W.memoria - 6, W.memoria + 4) * (1 - rampa(frame, W.revisor, W.revisor + 14));

  // Terminal
  const term = mola(frame, W.revisor);
  const camadas = mola(frame, W.revisor + 4);
  const recua = rampa(frame, W.estaticos + 2, W.estaticos + 14, Easing.inOut(Easing.cubic));
  const someTerm = rampa(frame, W.seguinte - 2, W.seguinte + 8);

  // Placar
  const placar = mola(frame, W.estaticos);
  const placarLado = rampa(frame, W.seguinte - 2, W.seguinte + 12, Easing.inOut(Easing.cubic));

  // Hilee C
  const cel = mola(frame, W.seguinte);
  const titHilee = mola(frame, W.passou);
  const vistos = [W.passou, W.em, W.tudo].map((f) => mola(frame, f));
  const carimbo = mola(frame, W.punido, {damping: 12, stiffness: 160});
  const tremor = frame >= W.punido && frame < W.punido + 8 ? Math.sin((frame - W.punido) * 2.4) * (8 - (frame - W.punido)) * 1.2 : 0;

  // Saída: tudo sai, a moldura desliza para o centro (posição da cena 10)
  const SAI = 322;
  const fora = 1 - saida(frame, SAI, 9);
  const carimboFora = 1 - saida(frame, SAI - 2, 7);
  const desliza = rampa(frame, SAI + 2, 350, Easing.inOut(Easing.cubic));
  const celX = lerp(CEL.xDir + (1 - Math.min(1, cel)) * 260, CEL.xFim, desliza);

  // geometria do arquivo (centro → canto)
  const docX = lerp(560, 96, canto);
  const docY = lerp(250, 72, canto);
  const docS = lerp(1, 0.34, canto);

  return (
    <Cena
      id="09_revisor"
      duracao={DURACAO_09}
      respiroAte={[318, 350]}
      sfx={[
        {som: 'tique', quadro: W.memoria},
        {som: 'clique', quadro: W.revisor},
        {som: 'batida', quadro: W.alegacao},
        {som: 'clique', quadro: W.dois},
        {som: 'pop', quadro: W.estaticos},
        {som: 'brilho', quadro: W.passou, volume: 0.26},
        {som: 'batida', quadro: W.punido},
      ]}
    >
      {/* registros reais passando ao fundo */}
      {fundoReg > 0 ? (
        <div style={{position: 'absolute', inset: 0, opacity: fundoReg, overflow: 'hidden'}}>
          {REGISTROS.concat(REGISTROS).map((r, i) => {
            const y = 1100 + i * 64 - (frame - W.memoria + 40) * 9;
            const mascara = interpolate(y, [700, 820, 1000, 1080], [0, 1, 1, 0], CL);
            if (mascara <= 0) return null;
            return (
              <div
                key={i}
                style={{
                  position: 'absolute',
                  left: i % 2 === 0 ? 560 : 640,
                  top: y,
                  fontSize: 26,
                  fontWeight: 500,
                  color: C.texto2,
                  opacity: (0.14 + (i % 3) * 0.04) * mascara,
                  whiteSpace: 'nowrap',
                }}
              >
                {r}
              </div>
            );
          })}
        </div>
      ) : null}

      {/* prompt herdado da cena 08 */}
      {promptSai < 1 ? (
        <div
          style={{
            position: 'absolute',
            left: PROMPT.x,
            top: PROMPT.y,
            width: PROMPT.w,
            height: PROMPT.h,
            borderRadius: 20,
            background: '#141417',
            border: `1px solid ${C.moldura}`,
            boxSizing: 'border-box',
            opacity: 1 - promptSai,
            transform: `scale(${1 - 0.06 * promptSai})`,
          }}
        >
          <div style={{position: 'absolute', left: 35, top: 0, lineHeight: `${PROMPT.h - 2}px`, fontFamily: F.titulo, fontWeight: 800, fontSize: 62, color: C.lima}}>›</div>
          <div style={{position: 'absolute', left: 362, top: 26, width: 23, height: 54, background: C.lima, opacity: cursorPisca * (1 - nomeVermelho)}} />
        </div>
      ) : null}
      {/* "facas_A.mp4" voa para dentro do arquivo de memória */}
      {voa < 1 ? (
        <div
          style={{
            position: 'absolute',
            left: lerp(883, 560 + 130, voa),
            top: lerp(614, 250 + 210, voa),
            transform: `translate(-50%, -50%) scale(${lerp(1, 0.4, voa)})`,
            fontWeight: 600,
            fontSize: 41,
            color: interpolateColors(nomeVermelho, [0, 1], [C.texto, C.vermelho]),
            whiteSpace: 'nowrap',
            opacity: 1 - rampa(frame, W.memoria - 2, W.memoria + 2),
          }}
        >
          facas_A.mp4
        </div>
      ) : null}

      {/* arquivo de memória: aprendizados.md */}
      <div
        style={{
          position: 'absolute',
          left: docX,
          top: docY,
          transform: `scale(${docS * (0.9 + 0.1 * doc)})`,
          transformOrigin: '0% 0%',
          opacity: Math.min(1, doc * 1.6) * (1 - somePapel),
          display: 'flex',
          alignItems: 'center',
          gap: 56,
        }}
      >
        <svg width={260} height={330} viewBox="0 0 260 330" style={{display: 'block', overflow: 'visible'}}>
          <path d="M18,0 H196 L260,64 V312 Q260,330 242,330 H18 Q0,330 0,312 V18 Q0,0 18,0 Z" fill="#151a24" stroke={C.azul} strokeWidth={3} />
          <path d="M196,0 V48 Q196,64 212,64 H260" fill="none" stroke={C.azul} strokeWidth={3} />
          {Array.from({length: 9}, (_, i) => {
            const p = rampa(frame, W.memoria - 4 + i * 2.2, W.memoria + i * 2.2);
            const larg = [170, 130, 186, 112, 160, 140, 176, 120, 150][i];
            const ehNovo = i === 8;
            return (
              <rect
                key={i}
                x={30}
                y={92 + i * 24}
                width={larg * p}
                height={9}
                rx={4.5}
                fill={ehNovo ? C.vermelho : i % 3 === 0 ? 'rgba(61,139,255,.75)' : 'rgba(245,244,240,.28)'}
              />
            );
          })}
          <text x={30} y={50} fontFamily="Inter" fontWeight={700} fontSize={26} fill={C.azul}>
            .md
          </text>
        </svg>
        <div style={{display: 'flex', flexDirection: 'column', opacity: 1}}>
          <div style={{fontSize: 52, fontWeight: 600, color: C.texto}}>aprendizados.md</div>
          <div style={{display: 'flex', alignItems: 'baseline', gap: 22, marginTop: 6}}>
            <div style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 230, lineHeight: 0.95, letterSpacing: '-0.02em', color: C.azul, fontVariantNumeric: 'tabular-nums', minWidth: 270}}>
              {n58}
            </div>
            <div style={{fontSize: 48, fontWeight: 500, color: C.texto}}>registros</div>
          </div>
          <div style={{marginTop: 14, fontSize: 30, fontWeight: 500, color: C.texto2, opacity: 1 - canto}}>cada falha e cada violação · lido antes de cada roteiro</div>
        </div>
      </div>

      {/* 3 camadas */}
      <div
        style={{
          position: 'absolute',
          right: 96,
          top: 96,
          display: 'flex',
          gap: 12,
          alignItems: 'center',
          opacity: Math.min(1, camadas * 1.5) * (1 - recua),
          transform: `translateY(${(1 - Math.min(1, camadas)) * 20}px)`,
        }}
      >
        <span style={{fontSize: 26, fontWeight: 600, color: C.texto2, marginRight: 6}}>3 camadas</span>
        {['regras fixas', 'agente de IA', 'movimento real'].map((t, i) => (
          <div
            key={t}
            style={{
              opacity: Math.min(1, mola(frame, W.revisor + 6 + i * 4) * 1.5),
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              fontSize: 22,
              fontWeight: 600,
              padding: '8px 16px',
              borderRadius: 999,
              background: 'rgba(61,139,255,.12)',
              border: '1px solid rgba(61,139,255,.45)',
              color: C.texto,
            }}
          >
            <div style={{width: 9, height: 9, borderRadius: 99, background: C.azul}} />
            {t}
          </div>
        ))}
      </div>

      {/* terminal */}
      {frame >= W.revisor - 1 && someTerm < 1 ? (
        <div
          style={{
            position: 'absolute',
            left: TERM.x,
            top: TERM.y,
            width: TERM.w,
            height: TERM.h,
            borderRadius: 22,
            background: '#0A0A0C',
            border: `1px solid ${C.moldura}`,
            boxShadow: '0 30px 80px rgba(0,0,0,.55)',
            overflow: 'hidden',
            opacity: Math.min(1, term * 1.6) * lerp(1, 0.22, recua) * (1 - someTerm),
            transform: `translateY(${(1 - Math.min(1, term)) * 50}px) scale(${(0.94 + 0.06 * term) * lerp(1, 0.9, recua)})`,
            filter: recua > 0 ? `blur(${(recua * 2).toFixed(2)}px)` : undefined,
          }}
        >
          <div style={{height: TERM.barra, background: '#141417', borderBottom: `1px solid ${C.moldura}`, display: 'flex', alignItems: 'center', padding: '0 24px', gap: 10}}>
            {['#3a3a40', '#3a3a40', '#3a3a40'].map((c, i) => (
              <div key={i} style={{width: 14, height: 14, borderRadius: 99, background: c}} />
            ))}
            <div style={{marginLeft: 18, fontSize: 21, fontWeight: 500, color: C.texto2}}>revisor de conformidade · ~/tiktok-shop-ia</div>
          </div>
          <Terminal frame={frame} />
        </div>
      ) : null}

      {/* placar */}
      {frame >= W.estaticos - 1 ? (
        <div
          style={{
            position: 'absolute',
            left: lerp(460, 96, placarLado),
            top: lerp(250 + (1 - Math.min(1, placar)) * 70, 236, placarLado),
            transform: `scale(${(0.92 + 0.08 * placar) * lerp(1, 0.82, placarLado)})`,
            transformOrigin: placarLado > 0 ? '0% 0%' : '50% 50%',
            opacity: Math.min(1, placar * 1.6) * fora,
          }}
        >
          <Placar frame={frame} />
        </div>
      ) : null}

      {/* Hilee C: passou nas 3 */}
      <div
        style={{
          position: 'absolute',
          left: 960,
          top: 372,
          opacity: Math.min(1, titHilee * 1.5) * fora,
          transform: `translateX(${(1 - Math.min(1, titHilee)) * -30}px)`,
        }}
      >
        <div style={{fontSize: 30, fontWeight: 600, color: C.texto, whiteSpace: 'nowrap'}}>
          Hilee C: <span style={{color: C.lima}}>passou nas 3</span>
        </div>
        <div style={{fontSize: 22, fontWeight: 500, color: C.texto2, marginTop: 4}}>1º vídeo depois do revisor</div>
      </div>
      {['regras fixas', 'agente de IA', 'movimento real'].map((t, i) => {
        const v = vistos[i];
        return (
          <div
            key={t}
            style={{
              position: 'absolute',
              left: 960,
              top: 470 + i * 72,
              display: 'flex',
              alignItems: 'center',
              gap: 12,
              padding: '8px 18px 8px 8px',
              borderRadius: 999,
              background: 'rgba(255,255,255,.08)',
              border: '1px solid rgba(255,255,255,.14)',
              fontSize: 24,
              fontWeight: 600,
              color: C.texto,
              opacity: Math.min(1, v * 1.6) * fora,
              transform: `translateX(${(1 - Math.min(1, v)) * -24}px) scale(${0.9 + 0.1 * v})`,
              transformOrigin: '0% 50%',
            }}
          >
            <div style={{width: 38, height: 38, borderRadius: 99, background: C.lima, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
              <Visto p={rampa(frame, [W.passou, W.em, W.tudo][i] + 2, [W.passou, W.em, W.tudo][i] + 9)} tamanho={26} cor={C.fundo} espessura={3.6} />
            </div>
            {t}
          </div>
        );
      })}

      {/* moldura do Hilee C, sempre rodando */}
      {frame >= W.seguinte - 1 ? (
        <Sequence from={W.seguinte - 1} layout="none">
          <div
            style={{
              position: 'absolute',
              left: celX,
              top: CEL.y,
              opacity: Math.min(1, cel * 1.8),
              transform: `scale(${0.92 + 0.08 * Math.min(1.05, cel)}) translateX(${tremor}px)`,
            }}
          >
            <Celular src="midia/hilee_C.mp4" largura={CEL.w} inicioVideo={0} />
          </div>
        </Sequence>
      ) : null}

      {/* carimbo: produto inconsistente */}
      {frame >= W.punido ? (
        <div
          style={{
            position: 'absolute',
            left: celX + CEL.w / 2,
            top: CEL.y + 500,
            transform: `translate(-50%, -50%) rotate(-7deg) scale(${lerp(1.7, 1, Math.min(1, carimbo)) * (0.85 + 0.15 * carimboFora)})`,
            opacity: Math.min(1, carimbo * 2.2) * carimboFora,
            padding: '14px 30px',
            borderRadius: 18,
            background: C.vermelho,
            outline: `6px solid ${C.vermelho}`,
            outlineOffset: 6,
            boxShadow: '0 20px 50px rgba(0,0,0,.5)',
            fontFamily: F.titulo,
            fontWeight: 800,
            fontSize: 46,
            lineHeight: 1,
            letterSpacing: '-0.01em',
            color: C.fundo,
            whiteSpace: 'nowrap',
          }}
        >
          produto inconsistente
        </div>
      ) : null}
    </Cena>
  );
};
