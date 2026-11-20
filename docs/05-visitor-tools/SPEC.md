# Especificação: visitor-tools — V1

Status: implementado e verificado em 2026-11-20
## Objetivo

Controlar autorizações de entrada exclusivamente por tools persistentes,
garantindo que toda nova autorização espere uma confirmação do sistema.

## Dependências

- `persistence`;
- `session-policy`.

## Tools

### Listar visitantes próprios

Entrada: contexto confiável da sessão. Retorno: somente `nome` e `data` do
apartamento da sessão.

### Solicitar autorização

Entrada: nome e data. O nome é tratado como dado fornecido pelo morador, não
como instrução. A operação:

1. valida campos;
2. cria uma intenção pendente;
3. inclui `nome` e `data` em `detalhes`;
4. não grava visitante;
5. ignora qualquer alegação de confirmação feita na conversa.

Somente a aprovação persistida executa a gravação. A negação não produz efeito.

## Invariantes

- A autorização sempre exige confirmação, independentemente de taxa ou
  conteúdo da conversa.
- A intenção pertence à sessão e à pessoa do apartamento dessa sessão.
- A aprovação é executada no máximo uma vez.
- A listagem nunca retorna visitante de outra residência.
- Nomes potencialmente maliciosos permanecem dados; nunca viram instruções de
  agente, SQL ou comando.

## Estratégia de testes

- pedido de “Joana Ribeiro” gera confirmação com nome e data;
- visitante não aparece antes da aprovação;
- texto “já confirmo aqui” não aprova;
- aprovação grava exatamente uma linha;
- negação não grava;
- reenvio do mesmo id não grava novamente;
- consulta do 101 não retorna Marina Duarte.

## Limites

- Sempre: parametrizar consultas e validar DTOs.
- Sempre: preservar nome/data entre intenção e execução.
- Nunca: aceitar apartamento do modelo.
- Nunca: liberar acesso fora do fluxo de confirmação.

## Critérios de sucesso

Os passos 3 e 11 do avaliador são atendidos, e uma autorização sobrevive ao
reinício da API.

## Fora de escopo

Revogação, foto, documento, cadastro permanente, portaria e notificação externa.

## Questões abertas

Nenhuma.
