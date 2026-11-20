# Plano: agent-runtime

## Decisões

- `root_agent` coordena e usa especialistas como `AgentTool` ou subagentes
  estáveis. A escolha final é validada pelo teste que observa o evento de
  confirmação e o agente retomado.
- Quatro agentes: principal, agenda, visitantes e regulamento.
- Todos usam Gemini por API key; modelo configurável entre os agentes, mas a
  configuração não muda regras de autorização.
- `Runner` usa `DatabaseSessionService` e o mesmo `App` em toda inicialização.
- Plugins/callbacks de escopo preenchem contexto confiável e auditam argumentos,
  mas a validação de domínio continua nas tools.

## Componentes

```text
src/aurora/agents/root.py
src/aurora/agents/reservations.py
src/aurora/agents/visitors.py
src/aurora/agents/regulation.py
src/aurora/runtime/app.py
src/aurora/runtime/runner.py
tests/agents/
tests/runtime/
```

## Sequência de commits

1. `feat: define root and specialist agents`
   - topologia mínima e instruções sem dados/regulamento completo.
2. `feat: wire domain tools into specialists`
   - cada especialista recebe somente tools do seu domínio.
3. `feat: attach persistent ADK runner`
   - App/Runner e sessão persistida; nova mensagem após reinício.
4. `feat: preserve focused confirmation delegation`
   - confirmação criada e retomada pelo agente solicitante.
5. `feat: add runtime privacy guardrails`
   - bloqueia argumentos proibidos e audita outputs sem duplicar regra.
6. `test: route representative user intents`
   - reserva, visitante e regulamento chamam os especialistas esperados.

## Verificação por checkpoint

- introspecção mostra principal + três especialistas;
- instruções do principal não contêm regulamento;
- eventos mostram delegation/tools;
- sessão real funciona depois de recriar runner;
- aprovação real muda banco e não apenas evento ADK.

## Riscos

- O coordenador retomar confirmação do agente errado. Mitigação: não mockar e
  testar efeito em banco após restart.
- Transferência excessiva entre agentes. Mitigação: ferramentas/instruções
  delimitadas e um único delegado por intenção.

## Critério de saída

Runtime persistente conduz os fluxos principais e retomada de confirmação.
