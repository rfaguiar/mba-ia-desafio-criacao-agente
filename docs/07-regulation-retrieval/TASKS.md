# Tarefas: regulation-retrieval

Status: implementado e verificado em 2026-11-20
Pré-requisito: `foundation`; pode evoluir em paralelo com `04`-`06`.

- [x] **G01 — Parsear capítulos e artigos**
  - Commit: `feat: parse regulation into focused articles`
  - Arquivos: `regulation/parser.py`, testes.
  - Aceitação: todos os artigos mantêm número/título/conteúdo e não alteram o
    arquivo fonte.
  - Verificar: contagem dos blocos e hash do Markdown.

- [x] **G02 — Recuperar passagem correta**
  - Commit: `feat: retrieve relevant regulation passages`
  - Arquivos: `retriever.py`, corpus de queries.
  - Aceitação: piscina/domingo retorna Art. 22; limite de caracteres aplicado.
  - Verificar: `pytest` com exclusão de artigos não relacionados.

- [x] **G03 — Expor tool focada**
  - Commit: `feat: expose regulation retrieval tool`
  - Arquivos: `tools/regulation.py`, testes.
  - Aceitação: DTO tem somente consulta, referências e trechos necessários.
  - Verificar: busca vazia retorna resultado explícito.

- [x] **G04 — Auditar eventos**
  - Commit: `test: audit regulation event context`
  - Aceitação: chamada aparece no evento; capítulos alheios não aparecem.
  - Verificar: serialização do evento da pergunta da piscina.

## Saída do módulo

- [x] O regulamento integral não está em prompt ou estado.
- [x] A resposta pode citar somente conteúdo recuperado.
