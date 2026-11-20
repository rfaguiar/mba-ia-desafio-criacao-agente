# Tarefas: reservation-tools

Status: implementado e verificado em 2026-11-20
Pré-requisito: `session-policy`.

- [x] **R01 — Implementar consultas**
  - Commit: `feat: add reservation queries and availability`
  - Arquivos: `domain/reservations.py`, `tools/reservations.py`, testes.
  - Aceitação: validação área/data, listagem própria e disponibilidade mascarada.
  - Verificar: testes com salão ocupado pelo 302 na sessão 101.

- [x] **R02 — Cancelar reserva própria**
  - Commit: `feat: cancel resident reservation without confirmation`
  - Aceitação: `RSV-1377` do 101 pode ser cancelada; `RSV-4821` do 302 nunca.
  - Verificar: consulta posterior à reserva, sem pendência criada.

- [x] **R03 — Reservar área sem taxa**
  - Commit: `feat: reserve free areas without confirmation`
  - Implementar: geração de código e inserção transacional.
  - Aceitação: quadra livre grava imediatamente e sem confirmação.
  - Verificar: taxa 0 + código novo não repetido.

- [x] **R04 — Preparar área com taxa**
  - Commit: `feat: prepare paid reservation intent`
  - Aceitação: salão/churrasqueira criam intenção para `confirmation`, sem
    inserir reserva.
  - Verificar: contagem de reservas não muda.

- [x] **R05 — Provar exclusividade**
  - Commit: `test: enforce atomic reservation conflict`
  - Aceitação: corrida concorrente de inserção deixa exatamente uma ativa.
  - Verificar: `asyncio.gather` ou threads reais com SQLite.

## Saída do módulo

- [x] Códigos não se repetem após cancelamento/reinício.
- [x] Data ocupada por terceiro não vaza identidade.
- [x] Taxa decide deterministicamente a exigência de confirmação.
