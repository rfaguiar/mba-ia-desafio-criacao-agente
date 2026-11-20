# Mapa de capacidades: Assistente do Residencial Aurora

Status: implementado e verificado em 2026-11-20

## Premissas

1. Esta versão implementa exclusivamente a API JSON descrita no
   `README.md`; não haverá interface visual.
2. O armazenamento persistente será SQLite local, administrado pela aplicação
   e separado dos arquivos imutáveis em `dados/`.
3. A API será assíncrona com FastAPI e Python 3.12+, gerenciada por `uv`.
4. Google ADK 2 será usado com uma versão exata igual ou superior a 2.2.0.
5. A identidade é confiável no momento da criação da sessão: o apartamento
   informado representa o morador autenticado.
6. Um módulo só depende dos módulos listados em “Depende de”; a dependência é
   sempre de cima para baixo na ordem de construção.
7. Cada etapa termina em um commit atômico e um estado verificável no qual todos
   os testes e comandos documentados continuam funcionando.

## Módulos

| Módulo id | Pasta da documentação | Responsabilidade | Depende de |
|---|---|---|---|
| `foundation` | `docs/01-foundation/` | Projeto `uv`, versões exatas, configuração, carregamento inicial, restauração, higiene de segredos e comandos reproduzíveis | — |
| `persistence` | `docs/02-persistence/` | Esquema SQLite, migração dos dados iniciais, repositórios, sessões, eventos, confirmações, reservas, códigos usados e visitantes | `foundation` |
| `session-policy` | `docs/03-session-policy/` | Vínculo imutável sessão-apartamento, contexto confiável das tools, filtros de privacidade e acesso apenas aos dados autorizados | `persistence` |
| `reservation-tools` | `docs/04-reservation-tools/` | Tools determinísticas de disponibilidade, reserva, cancelamento e listagem; taxa, unicidade de código e exclusividade atômica na gravação | `session-policy` |
| `visitor-tools` | `docs/05-visitor-tools/` | Tools determinísticas de listagem e autorização de visitante, sempre mediadas pelo apartamento da sessão | `session-policy` |
| `confirmation` | `docs/06-confirmation/` | Ciclo pendente/aprovado/negado, validação de sessão e estado, execução única, persistência e retomada no ADK Runner correto | `reservation-tools`, `visitor-tools` |
| `regulation-retrieval` | `docs/07-regulation-retrieval/` | Indexação e recuperação focada de `dados/regulamento.md`, sem inserir o regulamento integral nas instruções ou no histórico | `foundation` |
| `agent-runtime` | `docs/08-agent-runtime/` | Agente principal, pelo menos dois especialistas, ferramentas, delegação, estado, eventos, Runner persistente e estratégias anti-injeção | `confirmation`, `regulation-retrieval` |
| `api-contract` | `docs/09-api-contract/` | Rotas FastAPI, schemas JSON, códigos HTTP, erros esperados, serialização de eventos e rotas de verificação | `agent-runtime` |
| `acceptance` | `docs/10-acceptance/` | Testes ponta a ponta dos 15 passos do avaliador, concorrência, reinício, auditoria de dados e revisão do README final | `api-contract` |

## Ordem de construção

```text
foundation
    ├── persistence
    │       └── session-policy
    │               ├── reservation-tools ─┐
    │               └── visitor-tools ─────┤
    │                                      └── confirmation
    └── regulation-retrieval ───────────────────┘
                                                   ↓
                                              agent-runtime
                                                   ↓
                                               api-contract
                                                   ↓
                                                acceptance
```

`foundation` produz o projeto instalável e restaurável. `persistence` e
`session-policy` estabelecem as fronteiras determinísticas. Em seguida,
`reservation-tools` e `visitor-tools` podem ser desenvolvidos em paralelo, mas
só produzem efeitos críticos após `confirmation`. A recuperação do regulamento
também é independente e converge em `agent-runtime`, ponto em que a orquestração
entre modelos e tools é integrada.

## Fronteiras entre módulos

### O modelo pode decidir

- qual especialista acionar;
- quais perguntas fazer para completar uma solicitação;
- como redigir uma resposta;
- como transformar a intenção do morador em chamadas de tools;
- qual trecho de regulamento pedir para uma dúvida delimitada.

### O código deve decidir

- a qual apartamento a sessão pertence;
- quais dados de reservas e visitantes cada sessão pode acessar;
- se uma área está livre e se já existe uma reserva ativa;
- se uma ação exige confirmação;
- se uma confirmação pertence à sessão, está pendente e pode executar;
- se uma gravação concorrente perde a disputa de exclusividade;
- qual código de reserva inédito será usado;
- se o conteúdo retornado ao modelo expõe dados de outro morador;
- se uma sessão ou confirmação inválida recebe `404` ou `409`.

## Contratos de integração planejados

| Provedor | Consumidor | Contrato |
|---|---|---|
| `foundation` | Todos | caminhos de configuração, dados iniciais e comandos de inicialização/restauração |
| `persistence` | Tools, API e Runner | unidades de trabalho transacionais e repositórios sem lógica de prompt |
| `session-policy` | Todas as tools | contexto de execução contendo o `session_id` e o apartamento resolvido pelo armazenamento |
| `reservation-tools` | `confirmation` e especialistas | intenção de reserva/cancelamento estruturada e resultado tipado |
| `visitor-tools` | `confirmation` e especialistas | intenção de autorização estruturada e resultado tipado |
| `confirmation` | API e `agent-runtime` | criação, listagem, negação e aprovação idempotente de confirmações |
| `regulation-retrieval` | especialista de regulamento | passagem curta, citável e associada apenas ao tema consultado |
| `agent-runtime` | `api-contract` | execução assíncrona de mensagem e resposta padronizada com confirmações pendentes |
| `api-contract` | `acceptance` | contrato HTTP e formatos JSON exatamente compatíveis com o avaliador |

## Estratégia de fatias e commits

Cada módulo será dividido em tarefas pequenas o bastante para serem concluídas
em um único ciclo de trabalho e, quando possível, alterar no máximo cinco
arquivos. Cada commit deve:

1. entregar uma fatia vertical testada, não apenas estrutura vazia;
2. deixar `main` em estado instalável;
3. preservar os arquivos em `dados/`;
4. incluir a verificação executada e seus critérios observáveis;
5. usar mensagens no formato `<tipo>: <intenção do incremento>`.

Os documentos posteriores registrarão para cada commit:

- nome sugerido do commit;
- dependências anteriores;
- arquivos previstos;
- implementação exata;
- critérios de aceite;
- comando de verificação;
- resultado esperado;
- risco de regressão;
- relação direta com os critérios do `README.md`.

## Matriz de rastreabilidade

| Requisito do `README.md` | Módulos responsáveis |
|---|---|
| Stack Python 3.12+, `uv`, ADK fixado, Gemini e sem segredos | `foundation`, `acceptance` |
| Agente principal e pelo menos dois especialistas | `agent-runtime`, `acceptance` |
| Garantia 1: confirmação sistêmica, execução única e `409` | `confirmation`, `api-contract`, `agent-runtime` |
| Garantia 2: sessão vinculada a um apartamento e privacidade | `session-policy`, todas as tools, `agent-runtime` |
| Garantia 3: eventos, sessões e dados sobrevivem ao reinício | `persistence`, `agent-runtime`, `acceptance` |
| Garantia 4: regulamento consultado de forma focada | `regulation-retrieval`, `agent-runtime`, `acceptance` |
| Garantia 5: exclusividade atômica e conflito sem `500` | `persistence`, `reservation-tools`, `confirmation`, `api-contract` |
| Rotas e formatos JSON obrigatórios | `api-contract`, `acceptance` |
| Restauração e integridade de `dados/` | `foundation`, `acceptance` |
| README final com arquitetura, garantias e execução | `acceptance` |

## Critérios globais de conclusão

- Os módulos são aprovados nesta ordem ou em uma ordem revisada e registrada.
- Os quinze passos do fluxo do avaliador são automatizados ou executados por
  um roteiro reproduzível.
- Toda aprovação real é exercitada contra sessão persistida.
- O teste de concorrência dispara aprovações simultâneas e comprova exatamente
  uma reserva gravada.
- Um reinício da API preserva os eventos, a confirmação pendente quando
  aplicável, os dados do condomínio e os códigos já usados.
- Os eventos passam por auditoria contra vazamento de dados de outro apartamento
  e contra capítulos irrelevantes do regulamento.
- A versão exata do ADK, a integridade de `dados/` e a ausência de credenciais
  versionadas são verificadas antes da entrega.
- O `README.md` final referencia arquivos e trechos reais de cada garantia.

## Pontos que requerem aprovação humana

1. Confirmar SQLite local como armazenamento de reservas, visitantes,
   confirmações, sessões e eventos.
2. Confirmar a divisão em dez módulos e a ordem de dependência apresentada.
3. Confirmar que a aprovação sistêmica será implementada como estado persistente
   retomado pelo mesmo runner/agente solicitante, e não apenas por uma checagem
   de prompt.
4. Confirmar que cada pasta de módulo conterá `SPEC.md`, `PLAN.md` e `TASKS.md`
   após a aprovação do mapa.

## Fora do escopo desta especificação

- UI, autenticação real, pagamentos, estornos e deploy.
- Regras extras de antecedência, passado, capacidade ou horários das áreas.
- Otimizações ou infraestrutura de produção não exigidas pelo avaliador.
- Alteração dos conteúdos originais em `dados/`.
