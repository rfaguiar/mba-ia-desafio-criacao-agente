# Tarefas: regulation-retrieval

Pré-requisito: `foundation`; pode evoluir em paralelo com `04`-`06`.

- [ ] **G01 — Parsear capítulos e artigos**
  - Commit: `feat: parse regulation into focused articles`
  - Arquivos: `regulation/parser.py`, testes.
  - Aceitação: todos os artigos mantêm número/título/conteúdo e não alteram o
    arquivo fonte.
  - Verificar: contagem dos blocos e hash do Markdown.

- [ ] **G02 — Recuperar passagem correta**
  - Commit: `feat: retrieve relevant regulation passages`
  - Arquivos: `retriever.py`, corpus de queries.
  - Aceitação: piscina/domingo retorna Art. 22; limite de caracteres aplicado.
  - Verificar: `pytest` com exclusão de artigos não relacionados.

- [ ] **G03 — Expor tool focada**
  - Commit: `feat: expose regulation retrieval tool`
  - Arquivos: `tools/regulation.py`, testes.
  - Aceitação: DTO tem somente consulta, referências e trechos necessários.
  - Verificar: busca vazia retorna resultado explícito.

- [ ] **G04 — Auditar eventos**
  - Commit: `test: audit regulation event context`
  - Aceitação: chamada aparece no evento; capítulos alheios não aparecem.
  - Verificar: serialização do evento da pergunta da piscina.

## Saída do módulo

- [ ] O regulamento integral não está em prompt ou estado.
- [ ] A resposta pode citar somente conteúdo recuperado.
