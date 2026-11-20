# Especificação: api-contract — V1

## Objetivo

Expor o contrato HTTP JSON exatamente como descrito no `README.md`, mantendo
erros esperados e serialização fora do modelo.

## Dependências

- `agent-runtime`.

## Rotas

### `POST /sessoes`

Entrada: `{"apartamento": "<numero>"}`. Cria sessão imutável. Sucesso `201` com
`{"session_id": "..."}`. Apartamento inexistente tem comportamento livre, mas a
implementação deve escolhê-lo de forma explícita e documentá-lo.

### `POST /sessoes/{session_id}/mensagens`

Entrada: `{"texto": "..."}`. Sessão inexistente: `404`. Sucesso `200`:

```json
{
  "resposta": "string, possivelmente vazia",
  "confirmacoes_pendentes": []
}
```

### `POST /sessoes/{session_id}/confirmacoes`

Entrada: `{"id": "...", "confirmado": true}`. Sessão inexistente: `404`.
Confirmação inválida, de outra sessão ou não pendente: `409`, sem efeito. Sucesso
`200` no mesmo formato da rota de mensagens.

### `GET /sessoes/{session_id}/eventos`

Sessão inexistente: `404`. Sucesso `200` com lista completa e ordenada dos
eventos. O conteúdo é JSON serializável e não é reduzido a um resumo.

### `GET /apartamentos/{apartamento}/reservas`

`200` com objetos exatamente `codigo`, `area`, `data`.

### `GET /apartamentos/{apartamento}/visitantes`

`200` com objetos exatamente `nome`, `data`.

## Validação

- todos os corpos são JSON;
- campos obrigatórios seguem os nomes do contrato;
- datas nas rotas de verificação seguem `AAAA-MM-DD`;
- erros esperados usam schemas explícitos da API;
- conflitos de reserva e confirmação não viram resposta 500.

## Comportamento concorrente

As aprovações em sessões diferentes podem ser processadas em paralelo. Cada
requisição retorna um resultado normal. A regra de uma reserva por área/data
fica no armazenamento, não no lock da API.

## Estratégia de testes

- contrato OpenAPI/requests para cada rota;
- `404` de todas as rotas com sessão inexistente;
- `409` sem efeito para confirmação inválida;
- paralelismo real com duas aprovações;
- schema exato das rotas de verificação;
- `resposta` vazia aceita durante espera;
- serialização integral e ordenada dos eventos.

## Limites

- Sempre: preservar caminhos, campos e status do enunciado.
- Nunca: transformar erro esperado em 500.
- Nunca: passar payload cru do modelo para verificação sem DTO.

## Critérios de sucesso

Todos os passos 2 a 14 do avaliador cumprem o contrato externo, e os modelos
Pydantic/OpenAPI não adicionam requisitos incompatíveis.

## Fora de escopo

CORS, frontend, rate limiting, autenticação HTTP e documentação visual de API.

## Questões abertas

Nenhuma para o contrato; detalhes de serialização de eventos ADK ficam para o
plano depois da inspeção da versão fixada.
