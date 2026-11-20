# Tarefas: agent-runtime

Status: implementado e verificado em 2026-11-20
Pré-requisitos: `confirmation` e `regulation-retrieval`.

- [x] **A01 — Criar agentes**
  - Commit: `feat: define root and specialist agents`
  - Arquivos: `agents/root.py`, três especialistas, testes de topologia.
  - Aceitação: principal + três especialistas; instrução raiz sem regulamento
    completo.
  - Verificar: introspecção da árvore e busca no texto de instruções.

- [x] **A02 — Conectar tools**
  - Commit: `feat: wire domain tools into specialists`
  - Aceitação: agenda/visitante/regulamento recebem apenas tools autorizadas.
  - Verificar: catálogo de tools por agente.

- [x] **A03 — Persistir Runner**
  - Commit: `feat: attach persistent ADK runner`
  - Arquivos: `runtime/app.py`, `runner.py`, testes.
  - Aceitação: App/Runner estável abre sessão após reinício.
  - Verificar: contar evento, recriar Runner, enviar nova mensagem.

- [x] **A04 — Preservar delegação de confirmação**
  - Commit: `feat: preserve focused confirmation delegation`
  - Aceitação: confirmação paga e de visitante retoma no agente criador.
  - Verificar: cenário real com persistência e efeito no banco.

- [x] **A05 — Adicionar guardrails**
  - Commit: `feat: add runtime privacy guardrails`
  - Aceitação: argumentos proibidos, incluindo apartamento livre, são
    bloqueados; tools continuam sendo a autoridade.
  - Verificar: testes de prompt injection e DTO.

- [x] **A06 — Testar roteamento**
  - Commit: `test: route representative user intents`
  - Aceitação: pedidos de reserva, visitante e regulamento geram eventos de
    tools/especialistas corretos.
  - Verificar: suíte de integração com Runner.

## Saída do módulo

- [x] Agentes e tools estão persistidos na configuração real.
- [x] Reinício e confirmação não dependem de memória do processo.
