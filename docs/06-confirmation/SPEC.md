# Especificação: confirmation — V1

Status: implementado e verificado em 2026-11-20
## Objetivo

Implementar aprovação humana fora do diálogo, durável e idempotente, retomando
o agente/runner correto no ADK. Nenhuma confirmação é inferida da linguagem do
morador.

## Dependências

- `reservation-tools`;
- `visitor-tools`.

## Máquina de estados

```text
pendente -> executada
pendente -> negada
```

Não existem outras transições a partir de `executada` ou `negada`.

## Criação

Toda intenção crítica cria:

- id opaco;
- `session_id`;
- agente/runner ou token persistível de retomada;
- tipo de ação;
- detalhes não sensíveis exigidos pela API;
- argumentos estruturados e canônicos;
- estado e timestamps;
- correlação com eventos ADK.

`confirmacoes_pendentes` lista todas as pendências atuais da sessão. Negadas e
executadas não aparecem.

## Aprovar

1. Abrir transação apropriada.
2. Validar sessão existente.
3. Validar id pendente e pertencente à sessão.
4. Reservar a transição de estado de modo concorrente.
5. Resolver/retomar a chamada no agente que solicitou a confirmação.
6. Executar exatamente a ação registrada, sem recalcular o apartamento a
   partir do texto ou da resposta.
7. Gravar resultado e evento.

No conflito de reserva concorrente, a aprovação retorna `200` com uma resposta
normal de indisponibilidade; o erro de restrição não escapa como `500`.

## Negar

Marca a confirmação como negada, não chama a tool de efeito e retorna o formato
de resposta padrão.

## Id inválido

Id inexistente, de outra sessão ou já respondido produz `409`, sem efeito. A
rota deve distinguir esse resultado antes de executar a intenção.

## Retomada ADK

- o serviço de sessão precisa ser compatível com persistência;
- a resposta da rota precisa carregar a invocação/evento suspenso correto;
- a retomada deve chegar ao agente solicitante, não ao coordenador errado;
- um teste real deve aprovar em sessão persistida, reiniciar o processo e
  continuar a sessão;
- se possível sem alterar o contrato, a confirmação também deve sobreviver a
  reinício antes de ser respondida.

## Estratégia de testes

- negar reserva e visitante;
- aprovar reserva e visitante;
- repetir id já respondido;
- usar id inexistente;
- usar id de outra sessão;
- reiniciar entre criação e aprovação;
- duas confirmações concorrentes na mesma área/data;
- aprovação não duplica após retry.

## Limites

- Sempre: estado persistente e execução única.
- Sempre: validar contexto de sessão antes da ação.
- Consultar antes: abstrair a confirmação para fora das primitivas ADK.
- Nunca: considerar mensagem comum como consentimento.

## Critérios de sucesso

Passos 7, 8, 9, 11, 13 e 14 do avaliador são atendidos. A armadilha de uma rota
`200` sem retomar a ação é explicitamente coberta.

## Fora de escopo

Duas respostas simultâneas exatamente no mesmo id; o comportamento sequencial
permanece obrigatório.

## Questões abertas

- A versão exata de ADK será inspecionada na fase de plano para escolher a API
  concreta de confirmação e retomada suportada por SQLite.
