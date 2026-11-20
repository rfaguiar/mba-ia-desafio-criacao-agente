# Especificação: regulation-retrieval — V1

## Objetivo

Responder dúvidas sobre o regulamento consultando somente as passagens
pertinentes a cada pergunta, sem colocar o documento completo nas instruções
do agente principal ou no estado/eventos da sessão.

## Dependências

- `foundation`.

## Fonte oficial

`dados/regulamento.md` é a única fonte de verdade. O arquivo não é alterado nem
resumido globalmente por modelo durante a inicialização.

## Pipeline mínimo

1. ler o arquivo na inicialização do componente ou índice de consulta;
2. dividir por capítulos/artigos, preservando títulos e números;
3. classificar uma consulta de forma estreita;
4. recuperar poucos blocos compatíveis com a pergunta;
5. devolver somente esses blocos e metadados necessários;
6. registrar a chamada e o resultado focado como tool/evento;
7. não persistir capítulos irrelevantes.

Pode-se usar busca lexical determinística, embeddings locais ou serviço
compatível. A solução V1 não pode depender de um serviço externo sem comando de
subida único e documentação.

## Política de contexto

- o agente principal não recebe o regulamento em suas instruções;
- o regulamento integral não entra em state, histórico ou memória do ADK;
- um especialista de regulamento recebe apenas a consulta e os blocos da tool;
- a pergunta sobre piscina aos domingos deve recuperar Art. 22 e, se
  necessário, contexto imediatamente adjacente;
- capítulos sobre piscina não são misturados com silêncio, garagem ou visitas;
- chamadas de tool continuam visíveis em eventos.

## Estratégia de testes

- consultar horário da piscina retorna domingo 9h às 20h;
- evento da consulta não contém capítulos claramente irrelevantes;
- pergunta não regulatória não chama a recuperação;
- agente principal não contém texto de `dados/regulamento.md`;
- alteração do arquivo fonte refletida na próxima inicialização/índice;
- resultados de busca vazios são informados como tal, sem resposta inventada.

## Limites

- Sempre: citar apenas conteúdo recuperado.
- Sempre: limitar tamanho dos blocos.
- Consultar antes: adicionar banco vetorial ou serviço externo.
- Nunca: inserir o Markdown integral no prompt ou session state.

## Critérios de sucesso

Passo 12 do avaliador é atendido, a tool aparece nos eventos e nenhum trecho de
capítulos irrelevantes é persistido.

## Fora de escopo

Atualização online, OCR, suporte a outros formatos e memória global do
regulamento.

## Questões abertas

A escolha entre busca lexical por artigos e embeddings locais será tomada no
plano com base na precisão observável sobre perguntas representativas.
