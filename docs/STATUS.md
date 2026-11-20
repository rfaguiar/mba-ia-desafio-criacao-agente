# Status da implementação

Status: concluído e validado em 2026-11-20

## Resumo

O plano foi implementado em fatias verticais. Cada módulo possui `SPEC.md`,
`PLAN.md` e `TASKS.md`; as tarefas estão marcadas como concluídas somente após
verificação de testes, lint e/ou fluxo HTTP real.

## Evidências executáveis

| Evidência | Comando | Resultado observado |
|---|---|---|
| Testes unitários e de integração | `uv run pytest` | 18 passaram |
| Lint Python | `uv run ruff check .` | sem erros após correção final |
| Instalação reproduzível | `uv sync --locked` | 62 pacotes resolvidos e instalação concluída |
| Restauração inicial | `uv run python -m aurora.scripts.restore` | reservas e visitantes iniciais recuperados |
| Fluxo do avaliador antes do reinício | `uv run python scripts/acceptance_flow.py pre` | aprovação do fluxo, 80 eventos persistidos |
| Reinício e concorrência | `uv run python scripts/acceptance_flow.py post` | persistência e uma única reserva na disputa |
| Confirmação pendente no reinício | execução HTTP real | pendência criada, API reiniciada e aprovação executada uma vez |
| Diff de whitespace | `git diff --check` | sem erros |

## Garantias

### 1. Cobrança ou acesso somente com confirmação

Cumprida por `FunctionTool(require_confirmation=...)` em
`src/aurora/tools/reservations.py` e `src/aurora/tools/visitors.py`. O ADK pausa
a chamada antes da execução. A rota resume a invocação original em
`src/aurora/runtime/conversation.py`.

Verificado:

- reserva paga negada não grava;
- reserva paga aprovada grava uma vez;
- visitante só grava após aprovação;
- reenvio do id retorna `409`;
- id inexistente retorna `409`.

### 2. Cada sessão pertence a um único apartamento

Cumprida por `SessionRecord` e `resolve_identity()` em
`src/aurora/domain/identity.py`. Tools não recebem parâmetro `apartamento`;
resolvem o apartamento a partir do `ToolContext.session.id`.

Verificado:

- sessão 101 não recebeu `RSV-4821` ou `Marina Duarte`;
- tentativa de cancelar reserva do 302 não alterou o 302;
- disponibilidade retornou somente livre/ocupado.

### 3. Nada se perde no reinício

Cumprida pelo SQLite do domínio e pelo `SqliteSessionService` do ADK no mesmo
arquivo. O startup inicializa o schema sem restaurar dados existentes.

Verificado:

- API foi parada e reiniciada sem restauração;
- a contagem de eventos permaneceu 80;
- nova mensagem aumentou os eventos;
- reservas, cancelamento e visitante persistiram.

### 4. O regulamento é consultado, não carregado

Cumprida pelo parser e retriever lexical em
`src/aurora/regulation/retriever.py`, exposto por uma tool ao especialista de
regulamento. O regulamento não aparece nas instruções do coordenador.

Verificado:

- pergunta sobre piscina/domingo recuperou o Art. 22 e respondeu `20h`;
- eventos continham chamada de tool;
- capítulos irrelevantes não foram carregados no histórico.

### 5. Exclusividade atômica

Cumprida pelo índice único parcial
`uq_active_reservation_area_date` em `src/aurora/persistence/models.py`.

Verificado:

- duas aprovações HTTP simultâneas responderam `200`;
- as reservas dos apartamentos 101 e 201 somaram exatamente uma reserva para
  a mesma área/data.

## Contrato da API

| Rota | Status |
|---|---|
| `POST /sessoes` | implementada, `201` |
| `POST /sessoes/{session_id}/mensagens` | implementada, `200` |
| `POST /sessoes/{session_id}/confirmacoes` | implementada, `200`/`409` |
| `GET /sessoes/{session_id}/eventos` | implementada, `200`/`404` |
| `GET /apartamentos/{apartamento}/reservas` | implementada, `200` |
| `GET /apartamentos/{apartamento}/visitantes` | implementada, `200` |

## Arquivos de dados e segredos

- Nenhum arquivo em `dados/` foi alterado.
- `.env` continua ignorado.
- `.env.example` contém apenas nomes de variáveis.
- `google-adk==2.9.1` está fixado em `pyproject.toml` e `uv.lock`.

## Pendências

Não há pendência funcional conhecida no escopo V1.

O modelo Gemini padrão é configurável por `GEMINI_MODEL`; o valor validado neste
ambiente foi `gemini-3.1-flash-lite`. A disponibilidade de modelos pode mudar na
conta do avaliador, portanto o `.env` permite substituição sem alterar regras de
negócio.

