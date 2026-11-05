# Faqueiro 6 peças — roteiro do lote B (13/10/2026)

Escrito pela sessão (regras do `especialista-promocao`). Ideia do operador: a caixa abre, sai uma faca e o kit se forma ao redor dela. Feito para atender a regra da 3ª violação: há movimento real na cena nos 3 clipes e o clipe F muda de cenário.

| Parte | Clipe | Modelo | Quadros | Fala | Texto de tela | Rodapé |
|---|---|---|---|---|---|---|
| intro | D | Veo 3.1 Fast | início `fotos/quadro_caixa.jpg` | Olha o que vem dentro dessa caixa: um faqueiro completo, de seis peças. | OLHA O QUE VEM / Faqueiro de 6 peças |  |
| apresentacao | E | Veo 3.1 Fast | início `fotos/quadro_faca_sozinha.jpg`, fim `fotos/quadro_kit_reto.jpg` | Faca do chefe, faca de carne, cutelo, faca de descascar, tesoura e descascador. | 6 PEÇAS NO KIT / 4 facas, tesoura e descascador |  |
| cta | F | Veo 3.1 Lite | início `fotos/quadro_tomate.jpg` | Segundo o fabricante, as ondulações da lâmina prolongam a durabilidade. Toca no produto e confere o seu. | LÂMINA ONDULADA / mais durabilidade* → TOCA NO PRODUTO / e confere o seu | *Dados do fabricante |

Os prompts completos estão em `roteiro_B.json`. O clipe E foi pedido ao agente do Flow com dois anexos: "B_faca_inicio.jpg as the FIRST FRAME and B_kit_fim.jpg as the LAST FRAME" (o agente aceita, 20 créditos no Fast).

## Alertas
- A tampa da caixa aparece lisa, sem letreiro (a tampa real é impressa e só existe minúscula na foto do anúncio).
- "Ondulações que prolongam a durabilidade" é dado do vendedor: fala com "segundo o fabricante" e rodapé.
- O anúncio diz "cabo madeira" e "Material: Aço + Plástico": a fala não afirma madeira.
- Nenhum clipe mostra marca (INVICTUS / LIEXY).
