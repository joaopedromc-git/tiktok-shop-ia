import React from 'react';
import {Easing, interpolate, interpolateColors, useCurrentFrame} from 'remotion';
import {C, CL, Cena, F, Visto, lerp, mola, rampa, saida} from '../comum';

export const DURACAO_03 = 267;

// Quadros das palavras-gatilho: round((0,25 + início) × 30)
const W = {
  claude: 11,
  coordena: 29,
  tudo: 44,
  opera: 61,
  google: 73,
  flow: 83,
  tres: 104,
  escrevem: 126,
  editam: 150,
  revisam: 171,
  pessoa: 204,
  aprova: 219,
  posta: 239,
};

const Y1 = 220; // linha de cima
const Y2 = 760; // linha de baixo
const XR = 1740; // descida pela direita
const HUB = {x: 960, y: 490, w: 440, h: 124};

type No = {id: string; x0: number; x1: number; y: number; h: number; nome: string; sub: string; tipo: 'ferr' | 'agente' | 'pessoa'};

const NOS: Record<string, No> = {
  anuncio: {id: 'anuncio', x0: 96, x1: 286, y: Y1, h: 96, nome: 'anúncio', sub: 'do vendedor', tipo: 'ferr'},
  roteiro: {id: 'roteiro', x0: 352, x1: 642, y: Y1, h: 96, nome: 'roteiro', sub: '9 partes que se combinam', tipo: 'agente'},
  conf: {id: 'conf', x0: 1382, x1: 1640, y: Y1, h: 96, nome: 'conferência', sub: 'quadro a quadro', tipo: 'ferr'},
  editor: {id: 'editor', x0: 1370, x1: 1640, y: Y2, h: 96, nome: 'editor', sub: 'HyperFrames', tipo: 'agente'},
  revisor: {id: 'revisor', x0: 1030, x1: 1300, y: Y2, h: 96, nome: 'revisor', sub: 'texto e vídeo', tipo: 'agente'},
  postagem: {id: 'postagem', x0: 556, x1: 960, y: Y2, h: 96, nome: 'postagem manual', sub: '“Conteúdo gerado por IA”', tipo: 'pessoa'},
};
const FLOW = {x0: 812, x1: 1312, y: Y1, h: 172};
const PORTAO1 = {x: 712, y: Y1};
const PORTAO2 = {x: XR, y: HUB.y};

// Espinha do fluxo (do centro do anúncio ao centro da postagem)
const ESPINHA: [number, number][] = [
  [191, Y1],
  [XR, Y1],
  [XR, Y2],
  [758, Y2],
];
const segs = ESPINHA.slice(1).map((p, i) => Math.hypot(p[0] - ESPINHA[i][0], p[1] - ESPINHA[i][1]));
const TOTAL = segs.reduce((a, b) => a + b, 0);
const pontoEm = (t: number): [number, number] => {
  let d = Math.max(0, Math.min(1, t)) * TOTAL;
  for (let i = 0; i < segs.length; i++) {
    if (d <= segs[i] || i === segs.length - 1) {
      const k = segs[i] === 0 ? 0 : d / segs[i];
      const a = ESPINHA[i];
      const b = ESPINHA[i + 1];
      return [lerp(a[0], b[0], k), lerp(a[1], b[1], k)];
    }
    d -= segs[i];
  }
  return ESPINHA[ESPINHA.length - 1];
};
const fracaoDe = (x: number, y: number) => {
  // posição (0..1) de um ponto que está sobre a espinha
  let acc = 0;
  for (let i = 0; i < segs.length; i++) {
    const a = ESPINHA[i];
    const b = ESPINHA[i + 1];
    const naReta = (a[1] === b[1] && Math.abs(y - a[1]) < 1) || (a[0] === b[0] && Math.abs(x - a[0]) < 1);
    const dentro = x >= Math.min(a[0], b[0]) - 1 && x <= Math.max(a[0], b[0]) + 1 && y >= Math.min(a[1], b[1]) - 1 && y <= Math.max(a[1], b[1]) + 1;
    if (naReta && dentro) return (acc + Math.hypot(x - a[0], y - a[1])) / TOTAL;
    acc += segs[i];
  }
  return 0;
};
const ESPINHA_D = 'M' + ESPINHA.map((p) => p.join(',')).join(' L');

// Raios do Claude Code para os nós que ele opera
type Raio = {alvo: string; d: string; p: [number, number, number, number, number, number, number, number]; atraso: number};
const bez = (x0: number, y0: number, x1: number, y1: number, x2: number, y2: number, x3: number, y3: number) =>
  ({d: `M${x0},${y0} C${x1},${y1} ${x2},${y2} ${x3},${y3}`, p: [x0, y0, x1, y1, x2, y2, x3, y3] as Raio['p']});
const RAIOS: Raio[] = [
  {alvo: 'roteiro', ...bez(850, HUB.y - HUB.h / 2, 850, 360, 497, 360, 497, Y1 + 48), atraso: 2},
  {alvo: 'flow', ...bez(1000, HUB.y - HUB.h / 2, 1000, 380, 1062, 380, 1062, Y1 + FLOW.h / 2), atraso: 0},
  {alvo: 'conf', ...bez(1090, HUB.y - HUB.h / 2, 1090, 360, 1511, 360, 1511, Y1 + 48), atraso: 4},
  {alvo: 'editor', ...bez(1100, HUB.y + HUB.h / 2, 1100, 640, 1505, 640, 1505, Y2 - 48), atraso: 6},
  {alvo: 'revisor', ...bez(1010, HUB.y + HUB.h / 2, 1010, 640, 1165, 640, 1165, Y2 - 48), atraso: 3},
];
const ptBez = (p: Raio['p'], t: number): [number, number] => {
  const u = 1 - t;
  const x = u * u * u * p[0] + 3 * u * u * t * p[2] + 3 * u * t * t * p[4] + t * t * t * p[6];
  const y = u * u * u * p[1] + 3 * u * u * t * p[3] + 3 * u * t * t * p[5] + t * t * t * p[7];
  return [x, y];
};

// Pontas de seta onde a linha entra em cada etapa
const SETAS: {x: number; y: number; dir: 'd' | 'e' | 'b'}[] = [
  {x: 350, y: Y1, dir: 'd'},
  {x: 680, y: Y1, dir: 'd'},
  {x: 810, y: Y1, dir: 'd'},
  {x: 1380, y: Y1, dir: 'd'},
  {x: XR, y: PORTAO2.y - 32, dir: 'b'},
  {x: 1642, y: Y2, dir: 'e'},
  {x: 1302, y: Y2, dir: 'e'},
  {x: 962, y: Y2, dir: 'e'},
];
const setaPath = (s: (typeof SETAS)[number]) => {
  const k = 9;
  if (s.dir === 'd') return `M${s.x - k},${s.y - k * 0.75} L${s.x},${s.y} L${s.x - k},${s.y + k * 0.75}`;
  if (s.dir === 'e') return `M${s.x + k},${s.y - k * 0.75} L${s.x},${s.y} L${s.x + k},${s.y + k * 0.75}`;
  return `M${s.x - k * 0.75},${s.y - k} L${s.x},${s.y} L${s.x + k * 0.75},${s.y - k}`;
};

const COR_TIPO = {ferr: 'rgba(245,244,240,.42)', agente: C.azul, pessoa: C.laranja};
const RGB_TIPO = {ferr: '245,244,240', agente: '61,139,255', pessoa: '255,138,61'};

const Chip: React.FC<{no: No; aceso: number; surge?: number; flash: number; style?: React.CSSProperties}> = ({no, aceso, surge = 1, flash, style}) => {
  const w = no.x1 - no.x0;
  const cor = COR_TIPO[no.tipo];
  const borda = interpolateColors(aceso, [0, 1], ['rgba(255,255,255,.09)', cor]);
  return (
    <div
      style={{
        position: 'absolute',
        left: no.x0,
        top: no.y - no.h / 2,
        width: w,
        height: no.h,
        borderRadius: 16,
        background: '#151518',
        border: `${no.tipo === 'ferr' ? 1.5 : 2}px solid ${borda}`,
        boxShadow: `0 0 ${36 + flash * 30}px rgba(${RGB_TIPO[no.tipo]},${(no.tipo === 'ferr' ? 0.14 * flash : 0.28 * aceso + 0.4 * flash).toFixed(3)})`,
        boxSizing: 'border-box',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 4,
        transform: `scale(${surge})`,
        ...style,
      }}
    >
      <div style={{display: 'flex', alignItems: 'center', gap: 10, opacity: 0.32 + 0.68 * aceso}}>
        {no.tipo !== 'ferr' ? (
          <div style={{width: 10, height: 10, borderRadius: 99, background: cor, opacity: aceso}} />
        ) : null}
        <div style={{fontWeight: 600, fontSize: 27, letterSpacing: '-0.01em', color: C.texto}}>{no.nome}</div>
      </div>
      <div style={{fontWeight: 500, fontSize: 19, color: C.texto2, opacity: aceso}}>{no.sub}</div>
    </div>
  );
};

const Portao: React.FC<{x: number; y: number; surge: number; visto: number; flash: number; rotulo: string; lado: 'cima' | 'esq'}> = ({
  x,
  y,
  surge,
  visto,
  flash,
  rotulo,
  lado,
}) => (
  <>
    <div
      style={{
        position: 'absolute',
        left: x - 31,
        top: y - 31,
        width: 62,
        height: 62,
        borderRadius: 99,
        background: interpolateColors(visto, [0, 1], ['#151518', C.laranja]),
        border: `2.5px solid ${C.laranja}`,
        boxSizing: 'border-box',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transform: `scale(${surge})`,
        boxShadow: `0 0 ${30 + 30 * flash}px rgba(255,138,61,${(0.35 * surge + 0.4 * flash).toFixed(3)})`,
      }}
    >
      <Visto p={visto} tamanho={34} cor={C.fundo} espessura={3.6} />
    </div>
    <div
      style={{
        position: 'absolute',
        ...(lado === 'cima'
          ? {left: x - 150, width: 300, top: y - 108, textAlign: 'center' as const}
          : {left: x - 360, width: 300, top: y - 15, textAlign: 'right' as const}),
        fontSize: 21,
        fontWeight: 500,
        color: C.laranja,
        opacity: Math.min(1, surge),
        transform: `translateY(${(1 - Math.min(1, surge)) * 10}px)`,
      }}
    >
      {rotulo}
    </div>
  </>
);

export const Fluxo03: React.FC = () => {
  const frame = useCurrentFrame();

  // Entrada da direita (casa com o whoosh para a esquerda da cena 02)
  const entra = interpolate(frame, [0, 16], [0, 1], {...CL, easing: Easing.out(Easing.cubic)});
  const dx = (1 - entra) * 220;

  // Saída: tudo apaga e a postagem vira a moldura de celular
  const SAI = 254;
  const apaga = 1 - saida(frame, SAI, 7);
  const morf = rampa(frame, 253, 264, Easing.inOut(Easing.cubic));

  // Claude Code
  const hub = mola(frame, W.claude);
  const raioDesenho = (atraso: number) => rampa(frame, W.claude + 3 + atraso, W.claude + 25 + atraso, Easing.out(Easing.cubic));

  // Espinha acesa, esquerda → direita
  const espinha = rampa(frame, W.coordena - 4, W.opera + 8, Easing.inOut(Easing.quad));

  // Flow
  const flowAceso = rampa(frame, W.google - 6, W.google + 4);
  const passo1 = mola(frame, W.flow);
  const setaFlow = rampa(frame, W.flow + 8, W.flow + 15);
  const passo2 = mola(frame, W.flow + 13);

  // Agentes
  const agRoteiro = mola(frame, W.escrevem);
  const agEditor = mola(frame, W.editam);
  const agRevisor = mola(frame, W.revisam);

  // Pessoa
  const p1 = mola(frame, W.pessoa);
  const p2 = mola(frame, W.pessoa + 6);
  const vistos = rampa(frame, W.aprova, W.aprova + 10, Easing.out(Easing.cubic));
  const posta = mola(frame, W.posta, {damping: 12});

  // Pulso do anúncio à postagem (0,8 s)
  const pulsoT = rampa(frame, W.posta - 8, W.posta + 14, Easing.inOut(Easing.quad));
  const pulsoVivo = frame >= W.posta - 8 && frame <= W.posta + 20;
  const flashEm = (f: number) => (pulsoVivo ? Math.exp(-Math.pow((pulsoT - f) / 0.045, 2)) : 0);

  const aceso = {
    anuncio: 1,
    conf: rampa(frame, W.tudo + 4, W.tudo + 12),
  };

  const ativo = (k: string) => {
    if (k === 'flow') return interpolate(frame, [W.opera, W.google, W.flow + 26, W.flow + 40], [0.35, 1, 1, 0.35], CL);
    if (k === 'roteiro') return interpolate(frame, [W.escrevem, W.escrevem + 6, W.escrevem + 24, W.escrevem + 36], [0.35, 1, 1, 0.35], CL);
    if (k === 'editor') return interpolate(frame, [W.editam, W.editam + 6, W.editam + 20, W.editam + 30], [0.35, 1, 1, 0.35], CL);
    if (k === 'revisor') return interpolate(frame, [W.revisam, W.revisam + 6, W.revisam + 20, W.revisam + 30], [0.35, 1, 1, 0.35], CL);
    return 0.35;
  };

  // Palavra-chave embaixo
  const kw1 = mola(frame, W.tres) * (1 - saida(frame, W.revisam + 22, 8));
  const kw2 = mola(frame, W.pessoa) * (1 - saida(frame, W.posta - 4, 8));

  // Moldura final (postagem → celular 420×747 no centro)
  const P = NOS.postagem;
  const fim = {x0: 960 - 210, y0: 540 - 373.5, w: 420, h: 747};
  const mx0 = lerp(P.x0, fim.x0, morf);
  const my0 = lerp(P.y - P.h / 2, fim.y0, morf);
  const mw = lerp(P.x1 - P.x0, fim.w, morf);
  const mh = lerp(P.h, fim.h, morf);

  return (
    <Cena
      id="03_fluxo"
      duracao={DURACAO_03}
      respiroAte={[236, 262]}
      sfx={[
        {som: 'clique', quadro: W.claude},
        {som: 'tique', quadro: W.flow},
        {som: 'pop', quadro: W.escrevem},
        {som: 'pop', quadro: W.editam},
        {som: 'pop', quadro: W.revisam},
        {som: 'brilho', quadro: W.aprova},
        {som: 'whoosh', quadro: W.posta},
      ]}
    >
      <div style={{position: 'absolute', inset: 0, transform: `translateX(${dx}px)`, opacity: 0.6 + 0.4 * entra}}>
        <div style={{position: 'absolute', inset: 0, opacity: apaga}}>
          <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
            {/* espinha apagada */}
            <path d={ESPINHA_D} fill="none" stroke="rgba(255,255,255,.10)" strokeWidth={2} />
            {/* espinha acesa */}
            <path
              d={ESPINHA_D}
              fill="none"
              stroke="rgba(245,244,240,.55)"
              strokeWidth={2}
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - espinha}
            />
            {SETAS.map((s, i) => {
              const t = fracaoDe(s.x, s.y);
              const vis = espinha >= t ? 1 : 0.25;
              return (
                <path
                  key={i}
                  d={setaPath(s)}
                  fill="none"
                  stroke="rgba(245,244,240,.7)"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  opacity={vis}
                />
              );
            })}
            {/* raios do Claude Code */}
            {RAIOS.map((r) => {
              const dd = raioDesenho(r.atraso);
              const a = ativo(r.alvo);
              return (
                <g key={r.alvo}>
                  <path
                    d={r.d}
                    fill="none"
                    stroke={C.azul}
                    strokeOpacity={0.25 + 0.6 * a}
                    strokeWidth={1.5 + a}
                    strokeLinecap="round"
                    pathLength={1}
                    strokeDasharray={1}
                    strokeDashoffset={1 - dd}
                  />
                  {/* pacotes de dados indo do Claude Code para cada etapa */}
                  {dd >= 1
                    ? [0, 0.5].map((off) => {
                        const per = 46;
                        const t = (((frame - W.claude + off * per + r.atraso * 5) % per) + per) % per / per;
                        const [x, y] = ptBez(r.p, t);
                        const al = Math.sin(t * Math.PI) * (0.45 + 0.55 * a);
                        return <circle key={off} cx={x} cy={y} r={3.5 + a} fill={C.azul} opacity={al} />;
                      })
                    : null}
                </g>
              );
            })}
          </svg>

          {/* nós */}
          <Chip no={NOS.anuncio} aceso={aceso.anuncio} flash={flashEm(0)} />
          {[NOS.roteiro, NOS.editor, NOS.revisor].map((n) => (
            <div
              key={n.id}
              style={{position: 'absolute', left: n.x0, top: n.y - n.h / 2, width: n.x1 - n.x0, height: n.h, borderRadius: 16, border: '1.5px solid rgba(255,255,255,.09)', background: '#131316', boxSizing: 'border-box'}}
            />
          ))}
          <Chip no={NOS.roteiro} aceso={Math.min(1, agRoteiro)} surge={0.7 + 0.3 * agRoteiro} flash={flashEm(fracaoDe(497, Y1))} style={{opacity: Math.min(1, agRoteiro * 2)}} />
          <Chip no={NOS.conf} aceso={aceso.conf} flash={flashEm(fracaoDe(1511, Y1))} />
          <Chip no={NOS.editor} aceso={Math.min(1, agEditor)} surge={0.7 + 0.3 * agEditor} flash={flashEm(fracaoDe(1505, Y2))} style={{opacity: Math.min(1, agEditor * 2)}} />
          <Chip no={NOS.revisor} aceso={Math.min(1, agRevisor)} surge={0.7 + 0.3 * agRevisor} flash={flashEm(fracaoDe(1165, Y2))} style={{opacity: Math.min(1, agRevisor * 2)}} />

          {/* Google Flow · navegador */}
          {(() => {
            const fl = flashEm(fracaoDe(1062, Y1));
            return (
              <div
                style={{
                  position: 'absolute',
                  left: FLOW.x0,
                  top: FLOW.y - FLOW.h / 2,
                  width: FLOW.x1 - FLOW.x0,
                  height: FLOW.h,
                  borderRadius: 18,
                  background: '#151518',
                  border: `1.5px solid ${interpolateColors(flowAceso, [0, 1], ['rgba(255,255,255,.09)', 'rgba(245,244,240,.42)'])}`,
                  boxShadow: `0 0 ${30 + fl * 30}px rgba(245,244,240,${(0.1 * fl).toFixed(3)})`,
                  boxSizing: 'border-box',
                  padding: '16px 20px',
                }}
              >
                <div style={{display: 'flex', alignItems: 'baseline', gap: 10, opacity: 0.25 + 0.75 * flowAceso}}>
                  <span style={{fontWeight: 600, fontSize: 27, color: C.texto}}>Google Flow</span>
                  <span style={{fontWeight: 500, fontSize: 19, color: C.texto2}}>· navegador · Veo</span>
                </div>
                <div style={{display: 'flex', alignItems: 'center', marginTop: 14, gap: 0}}>
                  {[
                    {nome: '1º quadro', sub: 'editor de imagem', p: passo1},
                    {nome: 'clipe de 8 s', sub: 'Veo', p: passo2},
                  ].map((s, i) => (
                    <React.Fragment key={i}>
                      {i === 1 ? (
                        <svg width={20} height={20} style={{opacity: 0.3 + 0.7 * setaFlow}}>
                          <path d="M3,10 L17,10 M11,5 L17,10 L11,15" fill="none" stroke={C.texto} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                      ) : null}
                      <div
                        style={{
                          width: 220,
                          height: 82,
                          borderRadius: 12,
                          boxSizing: 'border-box',
                          border: `1.5px solid ${interpolateColors(Math.min(1, s.p), [0, 1], ['rgba(255,255,255,.07)', 'rgba(245,244,240,.55)'])}`,
                          background: `rgba(255,255,255,${(0.02 + 0.07 * Math.min(1, s.p)).toFixed(3)})`,
                          display: 'flex',
                          flexDirection: 'column',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: 2,
                          transform: `scale(${0.94 + 0.06 * s.p})`,
                        }}
                      >
                        <div style={{fontWeight: 600, fontSize: 24, color: C.texto, opacity: 0.25 + 0.75 * Math.min(1, s.p)}}>{s.nome}</div>
                        <div style={{fontWeight: 500, fontSize: 18, color: C.texto2, opacity: Math.min(1, s.p)}}>{s.sub}</div>
                      </div>
                    </React.Fragment>
                  ))}
                </div>
              </div>
            );
          })()}

          {/* portões de aprovação humana */}
          <Portao x={PORTAO1.x} y={PORTAO1.y} surge={p1} visto={vistos} flash={flashEm(fracaoDe(PORTAO1.x, PORTAO1.y))} rotulo="aprova o roteiro" lado="cima" />
          <Portao x={PORTAO2.x} y={PORTAO2.y} surge={p2} visto={vistos} flash={flashEm(fracaoDe(PORTAO2.x, PORTAO2.y))} rotulo="aprova os clipes" lado="esq" />

          {/* Claude Code */}
          <div
            style={{
              position: 'absolute',
              left: HUB.x - HUB.w / 2,
              top: HUB.y - HUB.h / 2,
              width: HUB.w,
              height: HUB.h,
              borderRadius: 22,
              background: '#121a2a',
              border: `2px solid ${C.azul}`,
              boxSizing: 'border-box',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              transform: `scale(${0.92 + 0.08 * hub})`,
              opacity: Math.min(1, hub * 1.4),
              boxShadow: `0 0 ${50 + 30 * Math.max(0, 1 - Math.abs(frame - W.claude - 6) / 14)}px rgba(61,139,255,${(0.3 + 0.25 * Math.max(0, 1 - Math.abs(frame - W.claude - 6) / 14)).toFixed(3)})`,
            }}
          >
            <div style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 60, lineHeight: 0.95, letterSpacing: '-0.02em', color: C.texto}}>
              Claude Code
            </div>
            <div
              style={{
                marginTop: 10,
                fontWeight: 500,
                fontSize: 21,
                color: C.texto2,
                opacity: rampa(frame, W.coordena, W.coordena + 8),
              }}
            >
              coordena tudo e opera o navegador
            </div>
          </div>

          {/* palavra-chave */}
          <div style={{position: 'absolute', left: 0, right: 0, top: 880, display: 'flex', justifyContent: 'center'}}>
            <div
              style={{
                position: 'absolute',
                display: 'flex',
                alignItems: 'center',
                gap: 18,
                opacity: Math.min(1, kw1),
                transform: `translateY(${(1 - kw1) * 40}px)`,
              }}
            >
              <span style={{fontFamily: F.titulo, fontWeight: 800, fontSize: 84, lineHeight: 0.95, letterSpacing: '-0.02em', color: C.lima}}>
                3 agentes
              </span>
              <div style={{display: 'flex', gap: 8}}>
                {[agRoteiro, agEditor, agRevisor].map((a, i) => (
                  <div key={i} style={{width: 16, height: 16, borderRadius: 99, background: C.azul, opacity: 0.2 + 0.8 * Math.min(1, a), transform: `scale(${0.6 + 0.4 * a})`}} />
                ))}
              </div>
            </div>
            <div
              style={{
                position: 'absolute',
                opacity: Math.min(1, kw2),
                transform: `translateY(${(1 - kw2) * 40}px)`,
                fontFamily: F.titulo,
                fontWeight: 800,
                fontSize: 84,
                lineHeight: 0.95,
                letterSpacing: '-0.02em',
                color: C.laranja,
              }}
            >
              aprovação humana
            </div>
          </div>
        </div>

        {/* pulso */}
        {pulsoVivo
          ? (() => {
              const pts = Array.from({length: 60}, (_, i) => pontoEm(pulsoT - i * 0.0022));
              const somePulso = pulsoT >= 1 ? Math.max(0, 1 - (frame - W.posta - 14) / 5) : 1;
              return (
                <svg width={1920} height={1080} style={{position: 'absolute', inset: 0}}>
                  {pts.map(([x, y], i) => (
                    <circle key={i} cx={x} cy={y} r={8 - i * 0.1} fill={C.lima} opacity={Math.pow(1 - i / 60, 2) * 0.7 * somePulso} />
                  ))}
                  <circle cx={pts[0][0]} cy={pts[0][1]} r={22} fill={C.lima} opacity={0.2 * somePulso} />
                </svg>
              );
            })()
          : null}

        {/* postagem → moldura de celular */}
        <div
          style={{
            position: 'absolute',
            left: mx0,
            top: my0,
            width: mw,
            height: mh,
            borderRadius: lerp(16, 36, morf),
            background: interpolateColors(morf, [0, 1], ['#151518', '#050506']),
            border: `${lerp(2, 6, morf)}px solid ${interpolateColors(morf, [0, 0.6, 1], [interpolateColors(Math.min(1, posta), [0, 1], ['rgba(255,255,255,.09)', C.laranja]), '#5a3a26', C.moldura])}`,
            boxShadow:
              morf > 0
                ? `0 ${30 * morf}px ${80 * morf}px rgba(0,0,0,${(0.55 * morf).toFixed(3)}), 0 0 ${40 * (1 - morf)}px rgba(255,138,61,${(0.3 * (1 - morf)).toFixed(3)})`
                : `0 0 ${36 + 40 * flashEm(1)}px rgba(255,138,61,${(0.3 * Math.min(1, posta) + 0.4 * flashEm(1)).toFixed(3)})`,
            boxSizing: 'border-box',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 4,
            transform: `scale(${morf > 0 ? 1 : 0.94 + 0.06 * posta})`,
            overflow: 'hidden',
          }}
        >
          <div style={{opacity: 1 - rampa(frame, 253, 257), display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 4}}>
            <div style={{display: 'flex', alignItems: 'center', gap: 10, opacity: 0.25 + 0.75 * Math.min(1, posta)}}>
              <div style={{width: 10, height: 10, borderRadius: 99, background: C.laranja, opacity: Math.min(1, posta)}} />
              <div style={{fontWeight: 600, fontSize: 27, color: C.texto, whiteSpace: 'nowrap'}}>{P.nome}</div>
            </div>
            <div style={{fontWeight: 500, fontSize: 19, color: C.texto2, opacity: Math.min(1, posta), whiteSpace: 'nowrap'}}>{P.sub}</div>
          </div>
        </div>
      </div>
    </Cena>
  );
};
