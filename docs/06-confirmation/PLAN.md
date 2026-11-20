# Plano: confirmation

## Decisões

- Uma confirmação não é apenas um registro: aponta para o evento/identificador
  ADK necessário para retomada.
- O executor usa um mapa fechado `ActionKind -> handler`; nunca avalia código ou
  nome dinâmico de função.
- Transição `pending -> completed/denied` usa atualização condicional
  (`WHERE state = 'pending'`) e comparação do número de linhas.
- Aprovação e efeito de negócio ficam na mesma transação quando o banco permitir;
  conflito de reserva mantém a confirmação como executada para impedir retry.
- O endpoint reinvoca o agente/Runner correto com `resume`/input de confirmação
  suportado pela versão 2.9.1.

## Componentes

```text
src/aurora/domain/confirmations.py
src/aurora/runtime/resume.py
tests/confirmation/
```

## Sequência de commits

1. `feat: persist pending confirmations`
   - criação, detalhes e listagem por sessão.
2. `feat: deny confirmations without side effects`
   - transição persistente e bloqueio de replay.
3. `feat: resume confirmed ADK invocation`
   - resposta chega ao agente solicitante e executa handler real.
4. `feat: execute confirmations exactly once`
   - claim transacional, id alheio/respondido/ausente retorna domínio 409.
5. `test: approve persisted confirmation after restart`
   - cria, reinicia serviços e aprova sessão real.
6. `test: race concurrent reservation approvals`
   - duas aprovações simultâneas, duas respostas, uma reserva.

## Verificação por checkpoint

- integração com Runner, não mock de rota;
- banco persiste pendência antes da aprovação;
- repetir id não executa outra vez;
- conflito concorrente termina como resposta normal.

## Riscos

- APIs de retomada variam por topologia e versão. Mitigação: o plano exige
  spike/teste de `FunctionTool`/`request_confirmation` antes de integrar a API.
- Atualizar estado antes do efeito pode perder ação. Mitigação: transação e
  teste de falha/reinício.
- Mesmo runner com outro agente faz confirmação silenciosa. Mitigação: teste
  end-to-end observa o efeito, não apenas status `200`.

## Critério de saída

Aprovação e negação reais funcionam em sessão SQLite, inclusive após reinício,
e replay não duplica efeito.
