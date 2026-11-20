# Plano de implementação do Assistente do Residencial Aurora

## Fonte e controle de decisões

- O contrato e os critérios de aceite são definidos pelo `README.md` raiz.
- A decomposição aprovada está em [capability-map.md](./capability-map.md).
- Cada módulo tem uma especificação, um plano técnico e tarefas atômicas.
- A ordem numérica das pastas é a ordem padrão de execução.
- A implementação só avança quando a verificação do módulo anterior está verde.

## Decisões arquiteturais

- Python 3.12+, `uv`, FastAPI assíncrono.
- Google ADK `2.9.1`, fixado exatamente: versão indicada nos próprios casos de
  referência do desafio e mais recente entre as duas versões testadas citadas
  no enunciado. O primeiro slice confirma a instalação real.
- SQLite local com SQLAlchemy/driver assíncrono e restrições físicas de unicidade.
- Banco operacional separado dos JSON originais em `dados/`.
- `DatabaseSessionService` do ADK ou integração compatível com o mesmo SQLite.
- Tools de negócio recebem `ToolContext`; resolvem o apartamento pelo
  `session_id`, nunca por argumento fornecido pelo modelo.
- Confirmações ADK são persistidas junto com a intenção de negócio e retomadas
  no agente/Runner que as criou.
- Regulamento dividido por capítulos/artigos e recuperado por busca lexical
  focada V1, sem serviço ou modelo de embeddings externo.
- Um principal, especialista de agenda, especialista de visitantes e
  especialista de regulamento.

## Estratégia de integração

Os slices devem ser verticais. Uma etapa não termina com “estrutura criada”:
ela termina com um comportamento observável, testes e comandos documentados.
Após cada commit:

1. `uv sync --locked`;
2. testes unitários e de integração do módulo;
3. lint/type-check aplicáveis;
4. auditoria de segredos;
5. verificação manual curta indicada no `TASKS.md`.

## Sequência

```text
01 foundation -> 02 persistence -> 03 session-policy
                                      ├── 04 reservation-tools
                                      └── 05 visitor-tools
                                             └── 06 confirmation
07 regulation-retrieval (começa após foundation)
06 + 07 -> 08 agent-runtime -> 09 api-contract -> 10 acceptance
```

`04` e `05` podem evoluir em paralelo após `03`; eles convergem em `06`.
`07` também pode evoluir em paralelo, desde que não bloqueie a trilha principal.

## Política de commits

Cada task marcada como commit:

- é autocontida e deixa testes/verificações existentes verdes;
- altera aproximadamente cinco arquivos ou menos, salvo migração/documentação
  coesa;
- usa `feat:`, `fix:`, `test:`, `docs:` ou `chore:`;
- inclui no corpo do commit, quando necessário, o requisito coberto;
- não contém `.env`, banco local, cache ou saída gerada;
- não altera arquivos em `dados/`.

## Definição de pronto do projeto

O projeto só está pronto quando o fluxo completo dos 15 passos é executado contra
a API real, incluindo reinício e aprovações concorrentes, e quando os checks de
dados, dependências, credenciais e documentação também passam.
