-- Esquema do projeto TikTok Shop. Rodar uma vez no PostgreSQL da VPS.
CREATE SCHEMA IF NOT EXISTS tiktok;
SET search_path = tiktok;

CREATE TABLE IF NOT EXISTS produto (
    id              serial PRIMARY KEY,
    codigo          text NOT NULL UNIQUE,          -- ex.: modus2400 (vai no nome dos arquivos)
    nome            text NOT NULL,
    link            text,
    caracteristicas text,                          -- so o que esta no anuncio do vendedor
    comissao        numeric(10,2),
    ativo           boolean NOT NULL DEFAULT true,
    criado_em       timestamptz NOT NULL DEFAULT now()
);

-- 9 linhas por produto: 3 partes x 3 variantes
CREATE TABLE IF NOT EXISTS clipe (
    id          serial PRIMARY KEY,
    produto_id  int  NOT NULL REFERENCES produto(id) ON DELETE CASCADE,
    parte       text NOT NULL CHECK (parte IN ('intro','descricao','cta')),
    variante    int  NOT NULL CHECK (variante BETWEEN 1 AND 9),
    fala        text NOT NULL,
    texto_tela  text NOT NULL DEFAULT '',
    rodape      text NOT NULL DEFAULT '',          -- *Dados do fabricante, quando a fala cita dado
    prompt      text,
    arq_clipe   text,
    arq_audio   text,
    -- roteiro -> roteiro_ok (parada 1) -> gerado -> aprovado (parada 2) | rejeitado
    status      text NOT NULL DEFAULT 'roteiro'
                CHECK (status IN ('roteiro','roteiro_ok','gerado','aprovado','rejeitado')),
    UNIQUE (produto_id, parte, variante)
);

CREATE TABLE IF NOT EXISTS video (
    id            serial PRIMARY KEY,
    produto_id    int NOT NULL REFERENCES produto(id) ON DELETE CASCADE,
    intro_id      int NOT NULL REFERENCES clipe(id),
    descricao_id  int NOT NULL REFERENCES clipe(id),
    cta_id        int NOT NULL REFERENCES clipe(id),
    arquivo       text,
    capa          text,
    legenda       text,
    status        text NOT NULL DEFAULT 'montado'
                  CHECK (status IN ('montado','enviado','postado','descartado')),
    criado_em     timestamptz NOT NULL DEFAULT now(),
    dia           date NOT NULL DEFAULT (now() AT TIME ZONE 'America/Sao_Paulo')::date,
    UNIQUE (intro_id, descricao_id, cta_id)
);

-- Proxima combinacao a montar hoje. Regras:
--   1. nunca repete combinacao;
--   2. nunca duas com a mesma introducao no mesmo dia;
--   3. alterna produtos (primeiro quem tem menos video hoje);
--   4. prefere a combinacao que menos se parece com as ja feitas do produto.
CREATE OR REPLACE VIEW proximo_video AS
WITH hoje AS (SELECT (now() AT TIME ZONE 'America/Sao_Paulo')::date AS d),
feitos AS (SELECT * FROM video WHERE status <> 'descartado'),
cand AS (
    SELECT p.id AS produto_id, p.codigo,
           i.id AS intro_id, d.id AS descricao_id, c.id AS cta_id
    FROM produto p
    JOIN clipe i ON i.produto_id = p.id AND i.parte = 'intro'     AND i.status = 'aprovado'
    JOIN clipe d ON d.produto_id = p.id AND d.parte = 'descricao' AND d.status = 'aprovado'
    JOIN clipe c ON c.produto_id = p.id AND c.parte = 'cta'       AND c.status = 'aprovado'
    WHERE p.ativo
      AND NOT EXISTS (SELECT 1 FROM feitos v WHERE v.intro_id = i.id
                        AND v.descricao_id = d.id AND v.cta_id = c.id)
      AND NOT EXISTS (SELECT 1 FROM feitos v, hoje WHERE v.intro_id = i.id AND v.dia = hoje.d)
)
SELECT cand.*,
       (SELECT count(*) FROM feitos v, hoje
         WHERE v.produto_id = cand.produto_id AND v.dia = hoje.d) AS do_produto_hoje,
       -- maior numero de partes em comum com um video ja feito (0 a 2)
       COALESCE((SELECT max((v.intro_id = cand.intro_id)::int
                          + (v.descricao_id = cand.descricao_id)::int
                          + (v.cta_id = cand.cta_id)::int)
                   FROM feitos v WHERE v.produto_id = cand.produto_id), 0) AS repeticao,
       -- quantas vezes essas partes ja foram usadas
       (SELECT count(*) FROM feitos v
         WHERE v.intro_id = cand.intro_id OR v.descricao_id = cand.descricao_id
            OR v.cta_id = cand.cta_id) AS uso
FROM cand
ORDER BY do_produto_hoje, repeticao, uso, random();
