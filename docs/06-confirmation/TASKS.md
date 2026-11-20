# Tarefas: confirmation

Status: implementado e verificado em 2026-11-20
Pré-requisitos: `reservation-tools` e `visitor-tools`.

- [x] **C01 — Persistir pendências**
  - Commit: `feat: persist pending confirmations`
  - Arquivos: `domain/confirmations.py`, repositório e testes.
  - Aceitação: intenção inclui id, sessão, tipo, detalhes e retomada.
  - Verificar: recriar repositório e listar pendência.

- [x] **C02 — Implementar negação**
  - Commit: `feat: deny confirmations without side effects`
  - Aceitação: estado vira negado, efeito não executa e replay retorna inválido.
  - Verificar: contagem antes/depois permanece.

- [x] **C03 — Provar spike de retomada**
  - Commit: `feat: resume confirmed ADK invocation`
  - Arquivos: `runtime/resume.py`, teste de integração ADK.
  - Implementar: usar a API de confirmação/resume da versão 2.9.1.
  - Aceitação: agente solicitante retoma e tool produz efeito real.
  - Verificar: banco muda; resposta não pode ser apenas um `200`.

- [x] **C04 — Executar exatamente uma vez**
  - Commit: `feat: execute confirmations exactly once`
  - Aceitação: id inexistente/alheio/respondido é inválido; claim concorrente
    impede execução dupla.
  - Verificar: testes de replay e sessão diferente.

- [x] **C05 — Retomar após reinício**
  - Commit: `test: approve persisted confirmation after restart`
  - Aceitação: cria com serviço real, reinicia, aprova e persiste efeito.
  - Verificar: processo/Runner e engine são reconstruídos.

- [x] **C06 — Disputar reservas**
  - Commit: `test: race concurrent reservation approvals`
  - Aceitação: duas respostas normais, exatamente uma reserva ativa.
  - Verificar: barreira de sincronização real entre duas sessões.

## Saída do módulo

- [x] Sem confirmação por mensagem.
- [x] 409 sem efeito está coberto.
- [x] Retomada foi validada com armazenamento persistente.
