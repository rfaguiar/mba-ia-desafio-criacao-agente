# Tarefas: reservation-tools

Pré-requisito: `session-policy`.

- [ ] **R01 — Implementar consultas**
  - Commit: `feat: add reservation queries and availability`
  - Arquivos: `domain/reservations.py`, `tools/reservations.py`, testes.
  - Aceitação: validação área/data, listagem própria e disponibilidade mascarada.
  - Verificar: testes com salão ocupado pelo 302 na sessão 101.

- [ ] **R02 — Cancelar reserva própria**
  - Commit: `feat: cancel resident reservation without confirmation`
  - Aceitação: `RSV-1377` do 101 pode ser cancelada; `RSV-4821` do 302 nunca.
  - Verificar: consulta posterior à reserva, sem pendência criada.

- [ ] **R03 — Reservar área sem taxa**
  - Commit: `feat: reserve free areas without confirmation`
  - Implementar: geração de código e inserção transacional.
  - Aceitação: quadra livre grava imediatamente e sem confirmação.
  - Verificar: taxa 0 + código novo não repetido.

- [ ] **R04 — Preparar área com taxa**
  - Commit: `feat: prepare paid reservation intent`
  - Aceitação: salão/churrasqueira criam intenção para `confirmation`, sem
    inserir reserva.
  - Verificar: contagem de reservas não muda.

- [ ] **R05 — Provar exclusividade**
  - Commit: `test: enforce atomic reservation conflict`
  - Aceitação: corrida concorrente de inserção deixa exatamente uma ativa.
  - Verificar: `asyncio.gather` ou threads reais com SQLite.

## Saída do módulo

- [ ] Códigos não se repetem após cancelamento/reinício.
- [ ] Data ocupada por terceiro não vaza identidade.
- [ ] Taxa decide deterministicamente a exigência de confirmação.
