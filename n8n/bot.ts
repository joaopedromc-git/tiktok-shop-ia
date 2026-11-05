import { workflow, node, trigger, sticky, switchCase, expr } from '@n8n/workflow-sdk';

const PG = { postgres: { id: 'ID_DA_CREDENCIAL', name: 'tiktok(admin)' } };
const TG = { telegramApi: { id: 'ID_DA_CREDENCIAL', name: 'telegram tiktok' } };
const GM = { googlePalmApi: { id: 'ID_DA_CREDENCIAL', name: 'gemini tiktok' } };
const CHAT = "{{ $('Telegram').first().json.message?.chat?.id ?? $('Telegram').first().json.callback_query?.message?.chat?.id }}";

const REGRAS = 'Você escreve roteiros curtos para vídeos de afiliado do TikTok Shop Brasil, narrados por voz de IA sobre clipes gerados por IA (Google Flow/Veo). Ninguém aparece falando.\n\nFONTE ÚNICA: o texto do anúncio do vendedor enviado pelo usuário. Nunca invente número, medida, certificação, resultado, material ou função que não esteja no texto.\nTodo dado de desempenho ou especificação (potência, capacidade, duração, resultado) deve vir na fala com "segundo o fabricante" e o campo rodape deve ser "*Dados do fabricante". Se a parte não cita dado, rodape = "".\nProibido: preço, desconto, frete, "melhor do mundo", promessa de saúde ou cura, comparação com outras marcas, urgência falsa.\n\nEstrutura: 9 partes = 3 intros + 3 descricoes + 3 ctas. Cada vídeo final junta 1 intro + 1 descricao + 1 cta, então qualquer combinação precisa fazer sentido.\n- intro: gancho de até 12 palavras (até 4 s). As 3 com ângulos bem diferentes (problema, curiosidade, cena do dia a dia).\n- descricao: até 22 palavras (até 8 s). As 3 mostram aspectos diferentes do produto.\n- cta: até 12 palavras. Chamar para o carrinho/link do vídeo, sem preço.\n- texto_tela: até 5 palavras, resumo da fala, em português.\n- prompt: em inglês, para o Google Flow gerar um clipe vertical 9:16 de 8 segundos. Comece com "Use the attached product photo as the exact reference: keep shape, colors, logo and packaging identical." Descreva cena, ação, luz e câmera. Termine com "No text, no captions, no letters, no extra logos, no people talking to camera." Mãos usando o produto são permitidas.\n\ncodigo: identificador curto do produto, só letras minúsculas e números, até 16 caracteres (ex.: modus2400).\nalertas: avisos para o usuário (texto do anúncio incompleto, dado duvidoso etc.) ou "".\n\nResponda SOMENTE com JSON neste formato:\n{"codigo":"","nome":"","link":"","caracteristicas":"resumo fiel do anúncio","comissao":null,"alertas":"","partes":[{"parte":"intro","variante":1,"fala":"","texto_tela":"","rodape":"","prompt":""}]}';

const telegram = trigger({
  type: 'n8n-nodes-base.telegramTrigger',
  version: 1.5,
  config: {
    name: 'Telegram',
    parameters: { updates: ['message', 'callback_query'], additionalFields: { chatIds: 'SEU_CHAT_ID' } },
    credentials: TG,
  },
  output: [{ message: { chat: { id: 123 }, text: '/produto Fritadeira Modus 2400...' } }],
});

const rotear = switchCase({
  version: 3.4,
  config: {
    name: 'O que chegou',
    parameters: {
      mode: 'rules',
      rules: {
        values: [
          { renameOutput: true, outputKey: 'produto', conditions: { options: { caseSensitive: false, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.message?.text ?? $json.message?.caption ?? "" }}'), operator: { type: 'string', operation: 'regex' }, rightValue: '^/produto(@\\w+)?\\s+\\S' }], combinator: 'and' } },
          { renameOutput: true, outputKey: 'aprovar roteiro', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.callback_query?.data ?? "" }}'), operator: { type: 'string', operation: 'startsWith' }, rightValue: 'rok:' }], combinator: 'and' } },
          { renameOutput: true, outputKey: 'refazer roteiro', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ $json.callback_query?.data ?? "" }}'), operator: { type: 'string', operation: 'startsWith' }, rightValue: 'rref:' }], combinator: 'and' } },
          { renameOutput: true, outputKey: 'foto do álbum (ignorar)', conditions: { options: { caseSensitive: true, leftValue: '', typeValidation: 'loose' }, conditions: [{ leftValue: expr('{{ !!$json.message?.media_group_id && !$json.message?.caption }}'), operator: { type: 'boolean', operation: 'true', singleValue: true }, rightValue: '' }], combinator: 'and' } },
        ],
      },
      options: { fallbackOutput: 'extra', renameFallbackOutput: 'outro' },
    },
  },
});

const pedidoNovo = node({
  type: 'n8n-nodes-base.set',
  version: 3.4,
  config: {
    name: 'Pedido novo',
    parameters: {
      mode: 'manual',
      assignments: { assignments: [
        { id: 'instrucao', name: 'instrucao', type: 'string', value: expr('Texto do anúncio do vendedor (única fonte de informação):\n{{ ($json.message.text ?? $json.message.caption ?? \'\').replace(/^\\/produto(@\\w+)?\\s*/i, "") }}') },
      ] },
    },
  },
  output: [{ instrucao: 'Texto do anúncio...' }],
});

const avisoGerando = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Avisar gerando',
    onError: 'continueRegularOutput',
    parameters: { resource: 'message', operation: 'sendMessage', chatId: expr(CHAT), text: '✍️ Gerando roteiro...', additionalFields: { appendAttribution: false } },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const respostaRefazer = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Responder refazer',
    onError: 'continueRegularOutput',
    parameters: { resource: 'callback', operation: 'answerQuery', queryId: expr('{{ $json.callback_query.id }}'), additionalFields: { text: 'Refazendo roteiro...' } },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const lerProduto = node({
  type: 'n8n-nodes-base.postgres',
  version: 2.7,
  config: {
    name: 'Ler produto',
    parameters: {
      operation: 'executeQuery',
      query: "SELECT p.codigo, p.nome, coalesce(p.link,'') AS link, coalesce(p.caracteristicas,'') AS caracteristicas, (SELECT string_agg(fala, ' | ') FROM tiktok.clipe WHERE produto_id = p.id) AS anteriores FROM tiktok.produto p WHERE p.id = $1",
      options: { queryReplacement: expr("{{ $('Telegram').first().json.callback_query.data.split(':')[1] }}") },
    },
    credentials: PG,
  },
  output: [{ codigo: 'modus2400', nome: 'Fritadeira', link: '', caracteristicas: '...', anteriores: '...' }],
});

const pedidoRefazer = node({
  type: 'n8n-nodes-base.set',
  version: 3.4,
  config: {
    name: 'Pedido refazer',
    parameters: {
      mode: 'manual',
      assignments: { assignments: [
        { id: 'instrucao', name: 'instrucao', type: 'string', value: expr('Refaça o roteiro deste produto com abordagens diferentes das anteriores. Use exatamente o codigo "{{ $json.codigo }}".\nNome: {{ $json.nome }}\nLink: {{ $json.link }}\nCaracterísticas do anúncio (única fonte de informação): {{ $json.caracteristicas }}\nFalas anteriores (não repetir): {{ $json.anteriores }}') },
      ] },
    },
  },
  output: [{ instrucao: 'Refaça...' }],
});

const gemini = node({
  type: '@n8n/n8n-nodes-langchain.googleGemini',
  version: 1.2,
  config: {
    name: 'Gemini roteiro',
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 5000,
    onError: 'continueErrorOutput',
    parameters: {
      resource: 'text',
      operation: 'message',
      modelId: { __rl: true, mode: 'id', value: 'models/gemini-flash-latest' },
      messages: { values: [{ role: 'user', content: expr("{{ $('Pedido novo').isExecuted ? $('Pedido novo').first().json.instrucao : $('Pedido refazer').first().json.instrucao }}") }] },
      jsonOutput: true,
      options: { systemMessage: REGRAS, maxOutputTokens: 8192, temperature: 0.9 },
    },
    credentials: GM,
  },
  output: [{ content: { parts: [{ text: '{"codigo":"modus2400","partes":[]}' }] } }],
});

const geminiReserva = node({
  type: '@n8n/n8n-nodes-langchain.googleGemini',
  version: 1.2,
  config: {
    name: 'Gemini reserva',
    retryOnFail: true,
    maxTries: 2,
    waitBetweenTries: 5000,
    onError: 'continueErrorOutput',
    parameters: {
      resource: 'text',
      operation: 'message',
      modelId: { __rl: true, mode: 'id', value: 'models/gemini-2.5-flash' },
      messages: { values: [{ role: 'user', content: expr("{{ $('Pedido novo').isExecuted ? $('Pedido novo').first().json.instrucao : $('Pedido refazer').first().json.instrucao }}") }] },
      jsonOutput: true,
      options: { systemMessage: REGRAS, maxOutputTokens: 8192, temperature: 0.9 },
    },
    credentials: GM,
  },
  output: [{ content: { parts: [{ text: '{"codigo":"modus2400","partes":[]}' }] } }],
});

const lerRoteiro = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Conferir roteiro',
    onError: 'continueErrorOutput',
    parameters: {
      mode: 'runOnceForAllItems',
      jsCode: `const textos = [];
(function andar(o) {
  if (typeof o === 'string') { textos.push(o); return; }
  if (Array.isArray(o)) { o.forEach(andar); return; }
  if (o && typeof o === 'object') {
    if (Array.isArray(o.partes)) textos.push(JSON.stringify(o));
    Object.values(o).forEach(andar);
  }
})($input.first().json);

let r = null;
for (const t of textos) {
  if (!t.includes('"partes"')) continue;
  try { r = JSON.parse(t.replace(/^\\s*\`\`\`(json)?/i, '').replace(/\`\`\`\\s*$/, '')); break; } catch (e) {}
}
if (!r) throw new Error('O Gemini não devolveu o JSON do roteiro.');

const ordem = ['intro', 'descricao', 'cta'];
const partes = (r.partes || []).filter(p => ordem.includes(p.parte) && p.variante >= 1 && p.variante <= 3 && String(p.fala || '').trim());
if (partes.length !== 9) throw new Error('O roteiro veio com ' + partes.length + ' partes válidas (esperado 9).');

const alertas = r.alertas ? [String(r.alertas)] : [];
for (const p of partes) {
  p.variante = Number(p.variante);
  p.fala = String(p.fala).trim();
  p.texto_tela = String(p.texto_tela || '').trim();
  p.prompt = String(p.prompt || '').trim();
  const fabricante = /segundo o fabricante/i.test(p.fala);
  p.rodape = fabricante ? '*Dados do fabricante' : '';
  if (/\\d/.test(p.fala) && !fabricante) alertas.push(p.parte + ' ' + p.variante + ' cita número sem "segundo o fabricante".');
}

let codigo = String(r.codigo || '').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 16);
if (codigo.length < 3) codigo = 'prod' + Date.now().toString(36);
const comissao = parseFloat(String(r.comissao ?? '').replace(',', '.'));

const dados = {
  codigo,
  nome: String(r.nome || codigo).trim(),
  link: String(r.link || '').trim() || null,
  caracteristicas: String(r.caracteristicas || '').trim(),
  comissao: isNaN(comissao) ? null : comissao,
  partes,
};
const tag = '$tt' + Math.random().toString(36).slice(2, 8) + '$';
const literal = tag + JSON.stringify(dados).replace(/\\$/g, '\\\\u0024') + tag;
const sql = \`WITH j AS (SELECT \${literal}::jsonb AS d),
p AS (
  INSERT INTO tiktok.produto (codigo, nome, link, caracteristicas, comissao)
  SELECT d->>'codigo', d->>'nome', d->>'link', d->>'caracteristicas', (d->>'comissao')::numeric FROM j
  ON CONFLICT (codigo) DO UPDATE SET nome = EXCLUDED.nome,
    link = coalesce(EXCLUDED.link, tiktok.produto.link),
    caracteristicas = EXCLUDED.caracteristicas,
    comissao = coalesce(EXCLUDED.comissao, tiktok.produto.comissao)
  RETURNING id, codigo, nome
),
c AS (
  INSERT INTO tiktok.clipe AS k (produto_id, parte, variante, fala, texto_tela, rodape, prompt)
  SELECT p.id, x->>'parte', (x->>'variante')::int, x->>'fala', x->>'texto_tela', x->>'rodape', x->>'prompt'
  FROM p, j, jsonb_array_elements(j.d->'partes') x
  ON CONFLICT (produto_id, parte, variante) DO UPDATE SET fala = EXCLUDED.fala,
    texto_tela = EXCLUDED.texto_tela, rodape = EXCLUDED.rodape, prompt = EXCLUDED.prompt, status = 'roteiro'
  WHERE k.status IN ('roteiro', 'roteiro_ok')
  RETURNING parte, variante, fala, texto_tela, rodape
)
SELECT p.id AS produto_id, p.codigo, p.nome,
  (SELECT json_agg(c ORDER BY array_position(ARRAY['intro','descricao','cta'], c.parte), c.variante) FROM c) AS clipes
FROM p\`;
return [{ json: { dados, alertas: alertas.join('\\n'), sql } }];`,
    },
  },
  output: [{ dados: { codigo: 'modus2400' }, alertas: '', sql: 'WITH ...' }],
});

const gravarRoteiro = node({
  type: 'n8n-nodes-base.postgres',
  version: 2.7,
  config: {
    name: 'Gravar roteiro',
    parameters: {
      operation: 'executeQuery',
      query: expr('{{ $json.sql }}'),
    },
    credentials: PG,
  },
  output: [{ produto_id: 1, codigo: 'modus2400', nome: 'Fritadeira', clipes: [] }],
});

const formatarRoteiro = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Formatar roteiro',
    parameters: {
      mode: 'runOnceForAllItems',
      jsCode: `const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const r = $input.first().json;
const alertas = $('Conferir roteiro').first().json.alertas;
const titulos = { intro: '🎣 INTRODUÇÕES', descricao: '📦 DESCRIÇÕES', cta: '🛒 CHAMADAS (CTA)' };
const linhas = ['<b>Roteiro: ' + esc(r.nome) + '</b> (<code>' + esc(r.codigo) + '</code>)'];
if (alertas) linhas.push('', '⚠️ ' + esc(alertas));
let atual = '';
for (const c of (r.clipes || [])) {
  if (c.parte !== atual) { atual = c.parte; linhas.push('', '<b>' + titulos[c.parte] + '</b>'); }
  linhas.push(c.variante + '. ' + esc(c.fala));
  linhas.push('   🖥 <i>' + esc(c.texto_tela) + '</i>' + (c.rodape ? '  ' + esc(c.rodape) : ''));
}
if (!(r.clipes || []).length) linhas.push('', 'Nenhuma parte alterada: os clipes desse produto já foram gerados.');
linhas.push('', 'Confira se tudo bate com o anúncio do vendedor.');
return [{ json: { produto_id: r.produto_id, texto: linhas.join('\\n').slice(0, 4000) } }];`,
    },
  },
  output: [{ produto_id: 1, texto: 'Roteiro...' }],
});

const enviarRoteiro = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Enviar roteiro (parada 1)',
    parameters: {
      resource: 'message',
      operation: 'sendMessage',
      chatId: expr(CHAT),
      text: expr('{{ $json.texto }}'),
      replyMarkup: 'inlineKeyboard',
      inlineKeyboard: { rows: [{ row: { buttons: [
        { text: '✅ Aprovar roteiro', additionalFields: { callback_data: expr('rok:{{ $json.produto_id }}') } },
        { text: '🔁 Refazer', additionalFields: { callback_data: expr('rref:{{ $json.produto_id }}') } },
      ] } }] },
      additionalFields: { appendAttribution: false, parse_mode: 'HTML' },
    },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const avisarErro = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Avisar erro do roteiro',
    parameters: {
      resource: 'message',
      operation: 'sendMessage',
      chatId: expr(CHAT),
      text: expr('❌ Não consegui montar o roteiro: {{ $json.error?.message ?? $json.error ?? "erro desconhecido" }}\nTente de novo.'),
      additionalFields: { appendAttribution: false, parse_mode: 'HTML' },
    },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const respostaAprovar = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Responder aprovar',
    onError: 'continueRegularOutput',
    parameters: { resource: 'callback', operation: 'answerQuery', queryId: expr('{{ $json.callback_query.id }}'), additionalFields: { text: 'Roteiro aprovado' } },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const aprovarRoteiro = node({
  type: 'n8n-nodes-base.postgres',
  version: 2.7,
  config: {
    name: 'Aprovar roteiro',
    alwaysOutputData: true,
    parameters: {
      operation: 'executeQuery',
      query: "UPDATE tiktok.clipe c SET status = 'roteiro_ok' FROM tiktok.produto p WHERE c.produto_id = p.id AND p.id = $1 AND c.status = 'roteiro' RETURNING p.codigo, p.nome, c.parte, c.variante, c.fala, c.prompt",
      options: { queryReplacement: expr("{{ $('Telegram').first().json.callback_query.data.split(':')[1] }}") },
    },
    credentials: PG,
  },
  output: [{ codigo: 'modus2400', nome: 'Fritadeira', parte: 'intro', variante: 1, fala: '...', prompt: '...' }],
});

const montarFila = node({
  type: 'n8n-nodes-base.code',
  version: 2,
  config: {
    name: 'Montar fila de prompts',
    parameters: {
      mode: 'runOnceForAllItems',
      jsCode: `const esc = s => String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const ordem = ['intro', 'descricao', 'cta'];
const clipes = $input.all().map(i => i.json).filter(c => c.parte)
  .sort((a, b) => ordem.indexOf(a.parte) - ordem.indexOf(b.parte) || a.variante - b.variante);
if (!clipes.length) return [{ json: { texto: 'Esse roteiro já tinha sido aprovado. Nada novo na fila.' } }];
const msgs = [{ json: { texto: '✅ Roteiro de <b>' + esc(clipes[0].nome) + '</b> aprovado.\\n\\nSeguem ' + clipes.length + ' prompts para o Google Flow. Use a foto do anúncio como referência em todos e salve cada clipe com o nome indicado.' } }];
for (const c of clipes) {
  msgs.push({ json: { texto: '🎬 <b>' + esc(c.codigo + '_' + c.parte + '_' + c.variante + '.mp4') + '</b>\\nFala: <i>' + esc(c.fala) + '</i>\\n\\n<code>' + esc(c.prompt) + '</code>' } });
}
msgs.push({ json: { texto: 'Na parada 2, rejeite qualquer clipe com letreiro, cor ou formato diferente do anúncio.' } });
return msgs;`,
    },
  },
  output: [{ texto: '🎬 modus2400_intro_1.mp4 ...' }],
});

const enviarFila = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Enviar prompts',
    parameters: {
      resource: 'message',
      operation: 'sendMessage',
      chatId: expr(CHAT),
      text: expr('{{ $json.texto }}'),
      additionalFields: { appendAttribution: false, parse_mode: 'HTML', disable_notification: true },
    },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const ajuda = node({
  type: 'n8n-nodes-base.telegram',
  version: 1.2,
  config: {
    name: 'Ajuda',
    parameters: {
      resource: 'message',
      operation: 'sendMessage',
      chatId: expr(CHAT),
      text: expr('Comandos:\n/produto + texto do anúncio do vendedor (título, descrição, especificações e link)\n\nSeu chat id: <code>{{ $json.message?.chat?.id ?? $json.callback_query?.message?.chat?.id }}</code>'),
      additionalFields: { appendAttribution: false, parse_mode: 'HTML' },
    },
    credentials: TG,
  },
  output: [{ ok: true }],
});

const nota = sticky('## Bot TikTok\nUm só fluxo recebe tudo do Telegram (o bot só aceita um webhook).\n- /produto → roteiro (Gemini) → parada 1\n- botão Aprovar → fila de prompts para o Flow\n- botão Refazer → novo roteiro\nO estado fica no banco (tiktok.clipe.status), sem nó de espera.', [], { color: 4 });

export default workflow('tiktok-bot', 'TikTok – Bot')
  .add(telegram)
  .to(rotear
    .onCase(0, pedidoNovo.to(avisoGerando).to(gemini))
    .onCase(1, respostaAprovar.to(aprovarRoteiro).to(montarFila).to(enviarFila))
    .onCase(2, respostaRefazer.to(lerProduto).to(pedidoRefazer).to(gemini))
    .onCase(4, ajuda))
  .add(gemini)
  .to(lerRoteiro)
  .to(gravarRoteiro)
  .to(formatarRoteiro)
  .to(enviarRoteiro)
  .add(gemini.onError(geminiReserva))
  .add(geminiReserva)
  .to(lerRoteiro)
  .add(geminiReserva.onError(avisarErro))
  .add(lerRoteiro.onError(avisarErro))
  .add(nota);
