# Tarefas: acceptance

Pré-requisito: `api-contract`.

- [ ] **E01 — Cobrir conversas centrais**
  - Commit: `test: cover core acceptance conversations`
  - Arquivos: `tests/acceptance/test_evaluation_flow.py`.
  - Implementar: passos 1 a 11 com observação de banco/rotas/eventos.
  - Aceitação: isolamento, cancelamento, taxa, replay e visitante.
  - Verificar: API real em banco temporário.

- [ ] **E02 — Cobrir reinício e regulamento**
  - Commit: `test: cover regulation events and restart`
  - Arquivos: teste de regulamento/reinício.
  - Aceitação: passos 12 e 13; evento focado, contagem aumenta após restart.
  - Verificar: subprocesso parado e reiniciado sem restaurar.

- [ ] **E03 — Cobrir disputa**
  - Commit: `test: cover simultaneous paid reservation approvals`
  - Arquivos: `test_concurrency.py`.
  - Aceitação: ambas respostas 200; soma exatamente uma reserva.
  - Verificar: dois clientes/requests concorrentes.

- [ ] **E04 — Auditar entrega**
  - Commit: `chore: audit delivery integrity and secrets`
  - Arquivos: `scripts/verify_delivery.py`, testes auxiliares.
  - Implementar: hashes de `dados/`, `.gitignore`, ADK exato, busca de segredos,
    topologia e assinatura de tools.
  - Aceitação: verifier falha para qualquer requisito violado.
  - Verificar: script sobre o repositório real.

- [ ] **E05 — Escrever README final**
  - Commit: `docs: replace challenge statement with delivery readme`
  - Implementar: Arquitetura, Garantias com links/trechos reais, Como rodar.
  - Aceitação: comandos e caminhos resolvem.
  - Verificar: smoke a partir das instruções.

- [ ] **E06 — Validar clone limpo**
  - Commit: `chore: verify clean clone delivery commands`
  - Implementar: script/registro reproduzível do fluxo.
  - Aceitação: `uv sync`, restauração, subida, fluxo completo e checks passam.
  - Verificar: executar em worktree temporário limpo com `.env` do avaliador.

## Saída do módulo

- [ ] Todos os 15 passos têm evidência executável.
- [ ] Nenhuma garantia é inferida sem observar efeito.
- [ ] README final referencia código existente.
