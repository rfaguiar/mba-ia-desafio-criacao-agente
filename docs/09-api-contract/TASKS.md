# Tarefas: api-contract

Pré-requisito: `agent-runtime`.

- [ ] **I01 — Expor sessão e verificação**
  - Commit: `feat: expose session creation and verification routes`
  - Arquivos: `api/main.py`, `schemas.py`, `routes/apartments.py`,
    `routes/sessions.py`.
  - Aceitação: `POST /sessoes` retorna 201; verificação retorna DTOs exatos.
  - Verificar: testes dos status/campos.

- [ ] **I02 — Integrar mensagens**
  - Commit: `feat: expose persisted session messages`
  - Aceitação: texto chama Runner e saída sempre contém os dois campos.
  - Verificar: caso de resposta vazia com pendência.

- [ ] **I03 — Integrar confirmações**
  - Commit: `feat: expose confirmation response route`
  - Aceitação: true/false seguem fluxo; 409 para inválida sem efeito.
  - Verificar: repetir id e id de outra sessão.

- [ ] **I04 — Expor eventos**
  - Commit: `feat: expose complete ordered session events`
  - Aceitação: lista completa, ordenada e JSON; sessão inexistente 404.
  - Verificar: serialização do conteúdo real do ADK.

- [ ] **I05 — Congelar contrato**
  - Commit: `test: verify full API contract`
  - Aceitação: todas rotas, status, campos e conflitos passam.
  - Verificar: testes HTTP + duas aprovações simultâneas.

## Saída do módulo

- [ ] Nenhuma rota de negócio transforma conflito esperado em 500.
- [ ] Rotas de verificação não passam pelo modelo.
