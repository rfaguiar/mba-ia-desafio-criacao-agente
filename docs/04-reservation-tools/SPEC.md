# Especificação: reservation-tools — V1

## Objetivo

Fornecer as únicas operações de leitura e escrita de reservas, com regras
determinísticas e sem permitir que o modelo crie, memorize ou atribua dados.

## Dependências

- `persistence`;
- `session-policy`.

## Tools

### Consultar disponibilidade

Entrada: área e data. Comportamento: validar área/data, consultar agenda
completa e retornar somente `livre` ou `ocupado`.

### Listar reservas próprias

Entrada: contexto confiável da sessão. Retorno: DTOs fechados `codigo`, `area`,
`data` pertencentes ao apartamento da sessão.

### Cancelar reserva própria

Entrada: área e data, resolvidas no apartamento da sessão. Não pede
confirmação. Pode ser idempotente quando nada estiver ativo, desde que nunca
afete outro apartamento nem vaze a existência desse registro.

### Solicitar nova reserva

Entrada: área e data no contexto da sessão. A tool avalia a taxa:

- taxa zero: executa imediatamente a reserva;
- taxa positiva: cria somente uma intenção pendente, sem gravar reserva;
- data ocupada: retorna indisponibilidade normal, sem confirmação necessária.

O passo de aprovação final revalida todas as condições e executa a inserção
transacional.

## Códigos de reserva

- gerados pelo sistema e nunca pelo modelo;
- únicos entre reservas ativas e canceladas;
- verificados e reservados sob transação;
- não reutilizados após rollback lógico, cancelamento ou reinício.

## Regras de data e área

- formato `AAAA-MM-DD`;
- a data deve pertencer ao calendário real;
- área deve existir em `dados/areas.json`;
- regras de antecedência, capacidade e horários não são aplicadas.

## Resultado de conflito

Um conflito na restrição única retorna um resultado de domínio como
`data_indisponivel`. A camada HTTP/Runner não deve transformar esse cenário em
erro 500, ainda que a aprovação receba resposta `200`.

## Estratégia de testes

- quadra sem taxa grava sem confirmação;
- salão/churrasqueira só viram intenção pendente;
- cancelamento afeta somente registro próprio;
- código único após cancelamento e reinício;
- duas inserções simultâneas deixam uma reserva;
- tool de disponibilidade mascara o proprietário.

## Limites

- Sempre: acesso a reservas exclusivamente por repositórios.
- Nunca: aceitar apartamento do modelo.
- Nunca: usar `get + set` em memória para exclusividade.
- Nunca: logar objeto bruto de reserva de terceiro em evento da sessão.

## Critérios de sucesso

Os passos 5, 6, 7, 8, 10, 13 e 14 do fluxo do avaliador funcionam pelas tools,
sem gravação prematura e com no máximo uma reserva ativa por área/data.

## Fora de escopo

Pagamento, estorno, espera em fila e alteração de reserva existente.

## Questões abertas

Nenhuma.
