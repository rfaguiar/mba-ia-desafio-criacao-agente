# Especificação: persistence — V1

Status: implementado e verificado em 2026-11-20
## Objetivo

Persistir todo estado mutável em SQLite, com transações e restrições no banco,
para que reinícios, concorrência e aprovações não dependam de memória ou do
modelo.

## Dependências

- `foundation`.

## Estado persistido

O esquema deve representar, no mínimo:

- sessões, com `session_id`, apartamento imutável e metadados de criação;
- eventos ordenados e completos da sessão;
- estado ADK necessário para retomar a execução;
- áreas, apartamentos e dados de referência carregados de `dados/`;
- reservas ativas e cancelamentos com marca de estado;
- histórico de códigos de reserva já emitidos;
- visitantes autorizados;
- confirmações pendentes, executadas ou negadas;
- intenção estruturada vinculada a cada confirmação.

## Invariantes

1. Uma linha de reserva ativa não pode coexistir com outra para a mesma área e
   data. A garantia nasce de uma restrição única no instante da inserção.
2. Cancelar preserva o histórico necessário e não recicla códigos.
3. Cada código usado, inclusive de reserva cancelada, permanece reservado.
4. Uma confirmação pertence a uma única sessão e a uma única intenção.
5. A ordem dos eventos é total, estável e reproduzível por sessão.
6. Todos os commits de uma intenção crítica são transacionais.
7. O SQLite usa configuração segura para múltiplas conexões e concorrência.

## Interfaces planejadas

- `transaction()` para unidade de trabalho;
- repositórios de sessão, evento, reserva, visitante e confirmação;
- exceções de domínio específicas para conflito, não encontrado e estado
  inválido;
- serviço de restauração que substitui somente o estado operacional derivado de
  `dados/`, preservando ou limpando sessões conforme a decisão documentada.

Nenhuma interface aceita um apartamento livre para contexto de uma tool
mutável. O apartamento vem do repositório de sessão por meio de `session_id`.

## Tratamento de concorrência

- `UNIQUE(area, data)` se aplica somente ao estado ativo; se isso for modelado por
  coluna/índice parcial, o índice deve existir no banco real.
- Um conflito de unicidade é convertido em erro de domínio normal, nunca em
  `500`.
- A aprovação da reserva não faz `consulta + inserção` como garantia isolada;
  a inserção trata a corrida.

## Estratégia de testes

- migração/restauração em banco novo;
- persistência antes e depois de fechar conexões ou recriar o serviço;
- unicidade para reservas simultâneas;
- recusa de duplicidade de código;
- histórico de cancelamento;
- ordenação dos eventos;
- transição de confirmação apenas uma vez.

## Limites

- Sempre: usar chaves e restrições explícitas.
- Sempre: manter transações curtas.
- Consultar antes: trocar SQLite por serviço externo.
- Nunca: depender de lista ou dicionário em memória como fonte de verdade.

## Critérios de sucesso

- O banco pode ser criado e restaurado com um comando.
- Reiniciar o processo não perde sessões, eventos, confirmações, reservas,
  cancelamentos ou códigos.
- A tentativa concorrente gera no máximo uma reserva ativa.
- Conflitos são erros de domínio serializáveis.

## Fora de escopo

- PostgreSQL, replicação, backup remoto e alta disponibilidade.

## Questões abertas

Nenhuma para V1. A definição física de tabelas será especificada no plano após
validar as APIs exatas da versão ADK fixada.
