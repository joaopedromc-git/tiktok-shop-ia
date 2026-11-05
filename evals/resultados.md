# Resultados do revisor

Gerado por `python evals/rodar.py`. Gabarito em `evals/casos.json`.

## Placar (só vídeos postados, com resultado conhecido)

| Camada | Vídeos que levaram a violação | Outros vídeos postados (sem essa violação) |
|---|---|---|
| Texto, regras originais (alegação exagerada) | 0 de 1 reprovados (0 de 1 sinalizados) | 0 reprovados, 0 em atenção (de 25) |
| Texto, todas as regras (alegação exagerada) | 1 de 1 reprovados (1 de 1 sinalizados) | 0 reprovados, 0 em atenção (de 25) |
| Texto, agente de IA (alegação exagerada) | 1 de 1 reprovados (1 de 1 sinalizados) | 5 reprovados, 13 em atenção (de 25) |
| Vídeo, movimento real (quadro estático) | 1 de 2 reprovados (1 de 2 sinalizados) | 2 reprovados, 3 em atenção (de 25) |
| Texto, agente de IA (produto inconsistente; fora do escopo, é visual) | 0 de 2 reprovados (1 de 2 sinalizados) | 6 reprovados, 12 em atenção (de 24) |

## Por vídeo

| Vídeo | Postado | Violação real | Regras originais | Todas as regras | Agente IA | Sem movimento | Movimento |
|---|---|---|---|---|---|---|---|
| bodysplash A | sim | — | — | — | — | 45% | ⚠️ atenção |
| bodysplash B | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 47% | ⚠️ atenção |
| bodysplash C | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 63% | ❌ reprova |
| bodysplash D | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 32% | ✅ aprova |
| bodysplash E | sim | — | ✅ aprova | ✅ aprova | ✅ aprova | 33% | ✅ aprova |
| bodysplash F | sim | — | ✅ aprova | ✅ aprova | ✅ aprova | 34% | ✅ aprova |
| bodysplash G | sim | — | ✅ aprova | ✅ aprova | ✅ aprova | 22% | ✅ aprova |
| bodysplash H | sim | — | ✅ aprova | ✅ aprova | ✅ aprova | 2% | ✅ aprova |
| extensao A | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 73% | ❌ reprova |
| extensao B | sim | — | ✅ aprova | ✅ aprova | ❌ reprova | 51% | ⚠️ atenção |
| extensao C | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 28% | ✅ aprova |
| extensao D | sim | — | ✅ aprova | ✅ aprova | ❌ reprova | 41% | ✅ aprova |
| extensao E | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 21% | ✅ aprova |
| extensao F | não confirmado | — | ✅ aprova | ✅ aprova | ✅ aprova | 3% | ✅ aprova |
| facas A | sim | quadro_estatico | ✅ aprova | ✅ aprova | ❌ reprova | 74% | ❌ reprova |
| facas B | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 11% | ✅ aprova |
| facas C | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 16% | ✅ aprova |
| facas D | sim | — | ✅ aprova | ✅ aprova | ❌ reprova | 44% | ✅ aprova |
| facas E | sim | alegacao_exagerada | ✅ aprova | ❌ reprova | ❌ reprova | 27% | ✅ aprova |
| garrafa B | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 27% | ✅ aprova |
| garrafa C | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 18% | ✅ aprova |
| garrafa D | sim | — | ✅ aprova | ✅ aprova | ❌ reprova | 6% | ✅ aprova |
| garrafa E | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 30% | ✅ aprova |
| garrafa F | sim | — | ✅ aprova | ✅ aprova | ✅ aprova | 4% | ✅ aprova |
| hilee A | sim | — | ✅ aprova | ✅ aprova | ⚠️ atenção | 10% | ✅ aprova |
| hilee B | sim | quadro_estatico | ✅ aprova | ✅ aprova | ✅ aprova | 40% | ✅ aprova |
| hilee C | sim | produto_inconsistente | ✅ aprova | ✅ aprova | ✅ aprova | 6% | ✅ aprova |
| piseira A | sim | produto_inconsistente | ✅ aprova | ✅ aprova | ⚠️ atenção | 22% | ✅ aprova |

## O que as regras fixas acharam

- **facas E** · apresentacao.fala: "do primeiro ao último" (promessa_no_tempo)
- **facas E** · cta.tela: "adeus" (promessa_no_tempo)
