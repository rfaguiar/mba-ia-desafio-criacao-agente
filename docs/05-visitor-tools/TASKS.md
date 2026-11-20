# Tarefas: visitor-tools

Pré-requisito: `session-policy`; converge em `confirmation`.

- [ ] **V01 — Listar visitantes próprios**
  - Commit: `feat: list session visitors safely`
  - Arquivos: `domain/visitors.py`, `tools/visitors.py`, testes.
  - Aceitação: sessão 101 não recebe Marina Duarte.
  - Verificar: testes de DTO e evento serializado.

- [ ] **V02 — Criar intenção de autorização**
  - Commit: `feat: create pending visitor authorization`
  - Implementar: validar nome/data, registrar ação pendente e detalhes.
  - Aceitação: nenhum visitante é gravado antes da aprovação.
  - Verificar: consulta de rota/repositório após solicitação.

- [ ] **V03 — Bloquear aprovação conversacional**
  - Commit: `test: reject prompt-based visitor approval`
  - Implementar: cenário “já estou confirmando”.
  - Aceitação: continua pendente e sem registro.
  - Verificar: teste de integração com intenção.

## Saída do módulo

- [ ] Toda nova autorização produz pendência.
- [ ] Nome permanece dado parametrizado.
