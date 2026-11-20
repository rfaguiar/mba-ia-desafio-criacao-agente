# Plano: session-policy

Status: implementado e verificado em 2026-11-20
## Decisões

- O `ToolContext` é preenchido pelo runtime com `session_id`.
- `SessionIdentity` é um contexto imutável contendo somente
  `session_id/apartamento`.
- Um `SessionPolicyService` resolve a sessão no repositório e bloqueia ausência.
- Repositórios de negócio não recebem apartamento cru; recebem `SessionIdentity`
  validada.
- DTOs de saída fechados e sanitarização antes de retornar resultado ao modelo.

## Componentes

```text
src/aurora/security/session_identity.py
src/aurora/security/output_policy.py
tests/security/
```

## Sequência de commits

1. `feat: bind immutable apartment to session`
   - cria resolução `session_id -> apartamento` e rejeita alteração;
   - testa identidade própria/inexistente.
2. `feat: scope domain repositories by session`
   - adiciona interfaces que recebem `SessionIdentity`;
   - testes mostram zero registros afetados fora do apartamento.
3. `feat: filter privacy-sensitive tool outputs`
   - DTOs fechados e auditoria de disponibilidade/conflitos;
   - testes adversariais rejeitam `RSV-4821`, `Marina Duarte` e `302`.

## Verificação por checkpoint

- assinatura das tools não contém apartamento fornecível pelo modelo;
- casos adversariais em banco de fixture;
- diff de eventos serializados não contém dados de terceiro;
- mensagens e retries não conseguem alterar a identidade.

## Riscos

- Fuga por exceção, representação `repr` ou log. Mitigação: erros de domínio
  genéricos e testes de serialização de evento.
- Atalho de rota administrativa reutilizado por tools. Mitigação: separar
  interfaces de verificação e sessão.

## Critério de saída

Toda tool futura recebe identidade confiável e só consegue produzir DTO seguro.
