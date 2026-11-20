# Tarefas: session-policy

Status: implementado e verificado em 2026-11-20
Pré-requisito: `persistence`.

- [x] **S01 — Vincular apartamento imutável**
  - Commit: `feat: bind immutable apartment to session`
  - Arquivos: `session_identity.py`, testes.
  - Implementar: resolver `session_id`, rejeitar sessão inexistente e criar
    contexto imutável.
  - Aceitação: mensagens não alteram apartamento.
  - Verificar: `uv run pytest tests/security/test_session_identity.py`.

- [x] **S02 — Delimitar repositórios à sessão**
  - Commit: `feat: scope domain repositories by session`
  - Arquivos: interfaces/repositórios, testes de cancelamento fictício.
  - Implementar: consultas recebem `SessionIdentity`.
  - Aceitação: zero linhas afetadas em apartamento alheio.
  - Verificar: testes parametrizados 101/302.

- [x] **S03 — Fechar saídas de tools**
  - Commit: `feat: filter privacy-sensitive tool outputs`
  - Arquivos: `output_policy.py`, DTOs, auditoria.
  - Aceitação: disponibilidade retorna apenas livre/ocupado; erro não revela
    proprietário; DTO não contém campo interno indevido.
  - Verificar: testes adversariais buscam `RSV-4821`, `Marina Duarte` e `302`.

## Saída do módulo

- [x] Nenhuma interface futura de tool exige apartamento do modelo.
- [x] Dados de terceiro não entram em resultado ou evento.
