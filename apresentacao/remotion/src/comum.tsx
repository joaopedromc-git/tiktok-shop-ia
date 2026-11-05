import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
} from 'remotion';

// Identidade visual (briefing.md / public/tokens.css)
export const C = {
  fundo: '#0E0E10',
  texto: '#F5F4F0',
  texto2: '#A9A79F',
  lima: '#C6F432',
  azul: '#3D8BFF',
  vermelho: '#FF4D4D',
  laranja: '#FF8A3D',
  cartao: '#FCFCFB',
  cartaoTexto: '#0B0B0B',
  cartaoTexto2: '#5E5D58',
  cartaoLinha: '#E7E6E1',
  moldura: '#2A2A2E',
};

export const F = {
  titulo: '"Bricolage Grotesque", sans-serif',
  corpo: '"Inter", sans-serif',
};

export const FPS = 30;
/** Quadro da cena em que a palavra começa (a fala entra em 0,25 s). */
export const qp = (inicio: number) => Math.round((0.25 + inicio) * FPS);

const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
export const CL = clamp;

/** Entrada com mola leve (overshoot), 0 → 1 a partir de `inicio`. */
export const mola = (frame: number, inicio: number, cfg?: {damping?: number; mass?: number; stiffness?: number}) =>
  spring({
    frame: frame - inicio,
    fps: FPS,
    config: {damping: 14, mass: 0.8, stiffness: 100, ...cfg},
  });

/** Saída com aceleração (power2.in), 0 → 1 em `dur` quadros. */
export const saida = (frame: number, inicio: number, dur = 9) =>
  interpolate(frame, [inicio, inicio + dur], [0, 1], {...clamp, easing: Easing.in(Easing.cubic)});

/** Rampa suave 0 → 1. */
export const rampa = (frame: number, a: number, b: number, easing = Easing.inOut(Easing.cubic)) =>
  interpolate(frame, [a, b], [0, 1], {...clamp, easing});

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

/** Número no formato brasileiro (16.522 / 23,13). */
export const fmt = (n: number, casas = 0) =>
  n.toLocaleString('pt-BR', {minimumFractionDigits: casas, maximumFractionDigits: casas});

/** Contador que sobe com desaceleração e trava no valor exato em `fim`. */
export const contar = (frame: number, ini: number, fim: number, valor: number, casas = 0) => {
  const t = interpolate(frame, [ini, fim], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const p = Math.pow(10, casas);
  return frame >= fim ? valor : Math.floor(valor * t * p) / p;
};

export const Fontes: React.FC = () => (
  <style>{`
@font-face { font-family: "Bricolage Grotesque"; font-weight: 200 800; src: local("Bricolage Grotesque"); }
@font-face { font-family: "Inter"; font-weight: 100 900; src: local("Inter"); }
`}</style>
);

const Granulado: React.FC = () => {
  const frame = useCurrentFrame();
  const seed = frame % 12;
  return (
    <svg width={1920} height={1080} style={{position: 'absolute', inset: 0, opacity: 0.04, pointerEvents: 'none'}}>
      <filter id={`grao${seed}`} x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed={seed} stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
        <feComponentTransfer>
          <feFuncA type="linear" slope="0" intercept="1" />
        </feComponentTransfer>
      </filter>
      <rect width="100%" height="100%" filter={`url(#grao${seed})`} />
    </svg>
  );
};

const Vinheta: React.FC = () => (
  <AbsoluteFill
    style={{
      background: 'radial-gradient(ellipse farthest-corner at 50% 50%, rgba(0,0,0,0) 0%, rgba(0,0,0,0.35) 100%)',
      pointerEvents: 'none',
    }}
  />
);

export type Sfx = {som: string; quadro: number; volume?: number};

/**
 * Cena padrão: fundo, respiro de câmera (1,00 → 1,03; volta a 1,00 na saída
 * quando `respiroAte` é dado, para o corte casar com a próxima cena),
 * vinheta, granulado, narração em 0,25 s e efeitos.
 */
export const Cena: React.FC<{
  id: string;
  duracao: number;
  sfx: Sfx[];
  respiroAte?: [number, number];
  children: React.ReactNode;
  sobre?: React.ReactNode;
}> = ({id, duracao, sfx, respiroAte, children, sobre}) => {
  const frame = useCurrentFrame();
  const fimSubida = respiroAte ? respiroAte[0] : duracao;
  let escala = interpolate(frame, [0, fimSubida], [1, 1.03], clamp);
  if (respiroAte) {
    const volta = rampa(frame, respiroAte[0], respiroAte[1]);
    escala = lerp(escala, 1, volta);
  }
  return (
    <AbsoluteFill style={{background: C.fundo, fontFamily: F.corpo, color: C.texto, overflow: 'hidden'}}>
      <Fontes />
      <AbsoluteFill style={{transform: `scale(${escala})`, transformOrigin: '50% 50%'}}>{children}</AbsoluteFill>
      {sobre}
      <Vinheta />
      <Granulado />
      <Sequence from={8} layout="none">
        <Audio src={staticFile(`audio/${id}.mp3`)} />
      </Sequence>
      {sfx.map((s, i) => (
        <Sequence key={i} from={s.quadro} layout="none">
          <Audio src={staticFile(`sfx/${s.som}.wav`)} volume={s.volume ?? 0.3} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

/** Moldura de celular padrão: 9:16, cantos 36, borda 6 #2A2A2E, vídeo sempre rodando e mudo. */
export const Celular: React.FC<{
  src?: string;
  largura?: number;
  inicioVideo?: number;
  style?: React.CSSProperties;
  children?: React.ReactNode;
  corBorda?: string;
}> = ({src, largura = 300, inicioVideo = 0, style, children, corBorda = C.moldura}) => {
  const altura = Math.round((largura * 16) / 9);
  return (
    <div
      style={{
        width: largura,
        height: altura,
        borderRadius: 36,
        border: `6px solid ${corBorda}`,
        boxShadow: '0 30px 80px rgba(0,0,0,.55)',
        overflow: 'hidden',
        background: '#050506',
        boxSizing: 'border-box',
        position: 'relative',
        ...style,
      }}
    >
      {src ? (
        <OffthreadVideo
          src={staticFile(src)}
          muted
          startFrom={inicioVideo}
          style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}}
        />
      ) : null}
      {children}
    </div>
  );
};

/** Etiqueta (pílula). Sem `cor`: neutra; com `cor`: versão de status. */
export const Pilula: React.FC<{
  cor?: string;
  corTexto?: string;
  tamanho?: number;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({cor, corTexto, tamanho = 22, style, children}) => (
  <div
    style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 10,
      fontFamily: F.corpo,
      fontWeight: 600,
      fontSize: tamanho,
      lineHeight: 1.2,
      padding: '8px 16px',
      borderRadius: 999,
      whiteSpace: 'nowrap',
      background: cor ?? 'rgba(255,255,255,.08)',
      border: cor ? `1px solid ${cor}` : '1px solid rgba(255,255,255,.14)',
      color: corTexto ?? (cor ? C.fundo : C.texto),
      ...style,
    }}
  >
    {children}
  </div>
);

/** Visto desenhado (traço animado por `p` 0 → 1). */
export const Visto: React.FC<{p: number; tamanho?: number; cor?: string; espessura?: number}> = ({
  p,
  tamanho = 28,
  cor = C.fundo,
  espessura = 3.5,
}) => (
  <svg width={tamanho} height={tamanho} viewBox="0 0 24 24" style={{display: 'block'}}>
    <path
      d="M5 12.5 L10 17.5 L19 7"
      fill="none"
      stroke={cor}
      strokeWidth={espessura}
      strokeLinecap="round"
      strokeLinejoin="round"
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - p}
    />
  </svg>
);
