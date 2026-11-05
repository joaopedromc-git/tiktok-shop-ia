# Revisor de conformidade

Confere um vídeo antes de postar, para não tomar violação automática do TikTok Shop. A conta levou 5 violações; o revisor transforma o que elas ensinaram em uma verificação que roda sozinha.

```
python revisor/revisar.py facas E              # texto (regras + agente) e vídeo
python revisor/revisar.py facas E --sem-video  # só o texto, antes de gastar crédito do Flow
python revisor/revisar.py facas E --sem-ia     # sem chamar o agente
```

Sai com código 1 quando reprova, então dá para usar como trava num script.

## As três verificações

| Verificação | O que olha | Como |
|---|---|---|
| Regras fixas (`regras.py`) | fala, texto de tela, rodapé e legenda | Expressões proibidas (preço, urgência, superioridade, saúde, promessa no tempo) e dado numérico sem "segundo o fabricante" ou sem o rodapé. Cada regra registra se é original ou se nasceu de uma violação. |
| Agente de IA (`ia.py` + `.claude/agents/revisor-conformidade.md`) | as mesmas frases, comparadas com o anúncio | Claude Code sem ferramentas (`claude -p --tools ""`), saída presa a um JSON Schema, numa pasta vazia para não ler as anotações do projeto sobre as violações. Usa a assinatura, sem API paga. |
| Movimento (`movimento.py`) | o vídeo final | Fluxo óptico entre quadros, com o movimento de câmera (zoom, deslocamento) ajustado e descontado. O que sobra é movimento real na cena. Mede a fração do tempo sem movimento real e lista os trechos parados. |

O movimento de câmera é descontado porque o TikTok não aceita "imagem de produto parada com aproximação" como movimento. Esse foi o motivo da 3ª violação.

## Resultado nos vídeos já postados

`python evals/rodar.py` roda as três verificações nos 24 vídeos postados com resultado conhecido (gabarito em `evals/casos.json`, tabela completa em `evals/resultados.md`).

| Verificação | Pegou a violação | Alarmes nos outros 22 vídeos (sem essa violação) |
|---|---|---|
| Regras fixas originais | 0 de 1 (alegação exagerada) | 0 |
| Regras fixas + regra criada após a 4ª violação | 1 de 1 | 0 |
| Agente de IA | 1 de 1 | 5 reprovados, 13 em atenção |
| Movimento | 1 de 2 (quadro estático) | 2 reprovados, 3 em atenção |

### Como ler

- **As regras fixas originais não pegariam a alegação exagerada (facas E).** A regra que pega ("do primeiro ao último", "adeus") foi escrita depois da violação, então acertar esse caso não prova nada. Ela fica porque evita a repetição.
- **O agente pegou a facas E sem ter visto a análise dela.** Ele reprovou "Pegada firme do primeiro ao último corte" e pôs o gancho "faca dançando na mão?" em atenção, com o motivo certo (o anúncio não promete resolver isso). O prompt do agente traz as categorias gerais da política, mas foi escrito depois das 5 violações, então não é um teste cego.
- **O agente é mais rígido que o TikTok.** Dos 5 vídeos que ele reprovou e que não levaram violação de alegação:
  - garrafa D: o anúncio diz que o design "pode deixar a garrafa livre de suor", e o vídeo diz "SEM SUOR POR FORA". É risco real;
  - extensão B ("carrega tudo junto") e extensão D ("ao alcance da mão"): inferências que o anúncio não faz. Risco real, porém pequeno;
  - facas A: o gancho "faca que amassa em vez de cortar?" tem o mesmo padrão da facas E (esse vídeo levou violação, mas por quadro estático);
  - facas D ("pra cada tarefa da cozinha"): exagero do revisor.

  Muitos vídeos em "atenção" querem dizer mais trabalho para quem revisa. Por isso a atenção não trava o vídeo: ela mostra o trecho e o operador decide.
- **O movimento pegou a facas A (74% do tempo sem movimento real) e não pegou a Hilee B (40%).** A Hilee B levou violação por clipes lentos e uma moldura fixa sobre o vídeo, um padrão que essa medida não separa dos vídeos aprovados. Os limites (60% reprova, 45% atenção) são números redondos e não foram ajustados para incluir a Hilee B.
- **Os 2 alarmes de movimento são vídeos que as regras de hoje já proíbem:** o body splash C (63%) usa uma arte parada na apresentação, e a extensão A (73%) congela um quadro com textos por cima. Passaram no TikTok, mas eram o mesmo risco da facas A.

### Limites

- São só 4 vídeos com violação, e as regras e o prompt foram escritos depois deles. O teste que vale são os próximos vídeos: cada um que levar ou não levar violação entra em `evals/casos.json`.
- A inconsistência visual do produto (cor, formato, padrão diferentes do anúncio, como na peseira A) não é verificada aqui. Continua na conferência humana dos clipes.
- O agente pode responder diferente a cada execução. As respostas usadas na tabela estão guardadas em `evals/saida_ia/`.

## Instalação

```
pip install -r revisor/requirements.txt   # numpy, opencv-python-headless e imageio-ffmpeg
```

O `ffmpeg` vem do PATH, de `$FFMPEG` ou do pacote `imageio-ffmpeg`. Para o agente, precisa do Claude Code logado. Os testes das regras rodam com `python revisor/test_regras.py`.
