# Plano: api-contract

Status: implementado e verificado em 2026-11-20
## Decisões

- FastAPI com lifespan que inicializa migração, Runner e serviços.
- Schemas Pydantic rígidos para request/response externos.
- Controllers finos chamam `ConversationService`.
- Exceções de domínio são mapeadas explicitamente para 404, 409 e 422.
- Rotas de verificação leem repositório diretamente, sem LLM.
- Eventos do ADK são convertidos para JSON completo por codec próprio.

## Componentes

```text
src/aurora/api/main.py
src/aurora/api/schemas.py
src/aurora/api/errors.py
src/aurora/api/routes/sessions.py
src/aurora/api/routes/apartments.py
tests/api/
```

## Sequência de commits

1. `feat: expose session creation and verification routes`
   - criação, reservas e visitantes; contrato básico.
2. `feat: expose persisted session messages`
   - mensagem chama Runner real e retorna `resposta`/pendências.
3. `feat: expose confirmation response route`
   - aprova/nega e converte erros para 409 sem efeito.
4. `feat: expose complete ordered session events`
   - serialização completa, ordenada e auditável.
5. `test: verify full API contract`
   - schemas, status, 404/409 e concorrência HTTP.

## Verificação por checkpoint

- testes `TestClient`/httpx em lifespan real;
- chamadas `curl` para todas as rotas;
- duas aprovações HTTP simultâneas;
- inspeção OpenAPI não altera os nomes/campos.

## Riscos

- Evento ADK contém objetos não JSON serializáveis. Mitigação: codec com
  fallback explícito apenas para tipos conhecidos, falhando em tipo inesperado.
- Resposta `200` sem efeito. Mitigação: integração testa banco após rota.

## Critério de saída

Todos os endpoints cumprem o contrato externo, incluindo erros esperados.
