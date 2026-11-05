# Primeira versão (desligada em 08/10/2026)

`bot.ts` é o fluxo do n8n da primeira arquitetura: o operador mandava o anúncio para um bot do Telegram, o Gemini escrevia o roteiro em JSON e o bot gravava no PostgreSQL, com botões de aprovar e refazer.

Ele foi desligado quando a sessão do Claude Code passou a coordenar o ciclo inteiro, inclusive operar o Google Flow pelo navegador, conferir os clipes e mandar editar, coisa que o bot não fazia. O arquivo fica como registro da evolução; o esquema do banco (`db/schema.sql`) continua em uso.
