# Tarefas: persistence

Pré-requisito: `foundation`.

- [ ] **P01 — Criar engine e schema**
  - Commit: `feat: add persistent domain schema`
  - Arquivos: `database.py`, `models.py`, `exceptions.py`,
    `tests/persistence/test_schema.py`.
  - Implementar: tabelas de sessão, evento, confirmação, reserva, código,
    visitante e referência.
  - Aceitação: sequência de eventos e unicidade parcial ativa existem no banco
    real.
  - Verificar: testes + inspeção `PRAGMA index_list/index_info`.

- [ ] **P02 — Importar estado inicial**
  - Commit: `feat: bootstrap immutable condominium data`
  - Arquivos: `bootstrap.py` e testes de migração.
  - Implementar: leitura transacional dos cinco JSON/MD necessários; persistir
    dados operacionais sem alterar `dados/`.
  - Aceitação: 101/302 retornam seus dados iniciais após bootstrap.
  - Verificar: hash dos arquivos + consultas de fixture.

- [ ] **P03 — Adicionar repositórios**
  - Commit: `feat: add transactional repositories`
  - Arquivos: `repositories.py`, DTOs e testes.
  - Implementar: UoW/repositórios e exceções tipadas.
  - Aceitação: transações fecham, rollback funciona e domínio não recebe
    objeto SQLite cru.
  - Verificar: suíte de persistência.

- [ ] **P04 — Criar restauração**
  - Commit: `feat: add data restoration command`
  - Arquivos: módulo CLI, documentação temporária e testes.
  - Aceitação: duas restaurações produzem estado inicial idêntico; sessão pode
    ser removida somente conforme política documentada.
  - Verificar: `uv run python -m aurora.scripts.restore` duas vezes.

- [ ] **P05 — Provar reinício**
  - Commit: `test: verify persistence across restarts`
  - Implementar: recriar engine entre gravação/leitura.
  - Aceitação: sessões, eventos, reservas, cancelamentos, códigos e visitantes
    permanecem.
  - Verificar: teste com arquivo SQLite persistido.

## Saída do módulo

- [ ] Corrida direta entre duas inserções mantém uma reserva.
- [ ] Banco criado não depende de memória.
- [ ] Exceção de unicidade está mapeada para conflito de domínio.
