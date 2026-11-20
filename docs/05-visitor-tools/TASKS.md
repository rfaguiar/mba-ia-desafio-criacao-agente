# Tarefas: visitor-tools

Status: implementado e verificado em 2026-11-20
Pré-requisito: `session-policy`; converge em `confirmation`.

- [x] **V01 — Listar visitantes próprios**
  - Commit: `feat: list session visitors safely`
  - Arquivos: `domain/visitors.py`, `tools/visitors.py`, testes.
  - Aceitação: sessão 101 não recebe Marina Duarte.
  - Verificar: testes de DTO e evento serializado.

- [x] **V02 — Criar intenção de autorização**
  - Commit: `feat: create pending visitor authorization`
  - Implementar: validar nome/data, registrar ação pendente e detalhes.
  - Aceitação: nenhum visitante é gravado antes da aprovação.
  - Verificar: consulta de rota/repositório após solicitação.

- [x] **V03 — Bloquear aprovação conversacional**
  - Commit: `test: reject prompt-based visitor approval`
  - Implementar: cenário “já estou confirmando”.
  - Aceitação: continua pendente e sem registro.
  - Verificar: teste de integração com intenção.

## Saída do módulo

- [x] Toda nova autorização produz pendência.
- [x] Nome permanece dado parametrizado.
