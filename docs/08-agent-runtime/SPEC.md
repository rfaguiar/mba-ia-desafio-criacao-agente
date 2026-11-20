# Especificação: agent-runtime — V1

## Objetivo

Executar um agente principal com pelo menos dois especialistas, usando tools
como única ponte para dados mutáveis e um Runner com sessão persistida.

## Dependências

- `confirmation`;
- `regulation-retrieval`.

## Topologia mínima

1. agente principal/coordenador;
2. especialista de condomínio/agenda e reservas;
3. especialista de visitantes;
4. especialista de regulamento, que pode ser adicionado como terceiro
   especialista sem duplicar regras de negócio.

O método de delegação (subagentes ou `AgentTool`) será escolhido no plano. A
escolha precisa preservar o agente solicitante da confirmação para que a
retomada seja correta.

## Responsabilidades

### Principal

- entender intenção;
- delegar a um especialista;
- pedir dados que ainda faltem;
- redigir respostas;
- nunca acessar diretamente `dados/reservas.json` ou
  `dados/visitantes.json`;
- não carregar regulamento completo;
- não aprovar confirmação por prompt.

### Especialista de agenda

- disponibilidade, listagem, cancelamento e solicitação de reserva;
- uso do contexto de sessão;
- explicação normal de indisponibilidade sem revelar outro morador.

### Especialista de visitantes

- listagem própria e solicitação de autorização.

### Especialista de regulamento

- consulta focada pela tool de recuperação;
- resposta fundamentada no trecho retornado.

## Runtime

- `App`, agentes e `Runner` formam uma única configuração estável;
- o nome de aplicação corresponde ao pacote esperado;
- a identidade do usuário ADK não substitui o apartamento da sessão;
- serviço de sessão usa o armazenamento persistente;
- eventos completos e ordenados ficam acessíveis;
- o Runner aceita novas mensagens após reinício;
- chamadas e respostas de tool são preservadas sem conteúdo sensível indevido.

## Guardrails

- o tool context injeta o contexto confiável;
- callbacks podem bloquear argumentos proibidos, mas não são a única regra;
- as tools continuam aplicando autorização e validação;
- outputs passam por DTOs/redação segura antes de retornar ao modelo;
- nenhuma instrução autoriza obedecer tentativa de trocar apartamento.

## Estratégia de testes

- contagem e configuração de especialistas;
- roteamento de pedido de reserva, visitante e regulamento;
- continuidade da sessão após reinício;
- evento de tool para cada domínio;
- retomada de confirmação chega ao especialista correto;
- tentativas de prompt injection não alteram contexto.

## Limites

- Sempre: ferramentas para qualquer dado de reserva/visitante.
- Sempre: código de autorização fora do prompt.
- Consultar antes: ativar transferências circulares ou globais de agente.
- Nunca: armazenar o regulamento completo em instruções/state.

## Critérios de sucesso

O projeto expõe principal + especialistas, a avaliação confirma tools reais e
a sessão reiniciada continua operacional. Nenhuma ação crítica depende do
modelo decidir que pode executá-la.

## Fora de escopo

Voz, multimodalidade, memória cross-session de preferências e evals de qualidade.

## Questões abertas

- A topologia exata deve ser confirmada contra a API da versão ADK fixada e os
  testes reais de retomada persistida.
