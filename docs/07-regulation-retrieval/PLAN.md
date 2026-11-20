# Plano: regulation-retrieval

Status: implementado e verificado em 2026-11-20
## Decisões

- Parser estrutural por `## Capítulo`, artigos e parágrafos.
- Índice léxico local com título, número do artigo e termos normalizados.
- Rankeamento por tokens/nomes de domínio; para “piscina domingo” a passagem
  retornada inclui Art. 22.
- Limite rígido por quantidade de blocos e caracteres.
- Ferramenta devolve apenas passagens selecionadas; o texto integral existe
  somente no componente de indexação, não em state/evento.

## Componentes

```text
src/aurora/regulation/parser.py
src/aurora/regulation/retriever.py
src/aurora/tools/regulation.py
tests/regulation/
```

## Sequência de commits

1. `feat: parse regulation into focused articles`
   - lê capítulos/artigos sem alterar fonte;
   - testes do parser e isolamento de capítulo.
2. `feat: retrieve relevant regulation passages`
   - busca lexical, ranking e limite de saída;
   - cenário piscina/domingo.
3. `feat: expose regulation retrieval tool`
   - DTO focado e testes de resultado ausente.
4. `test: audit regulation event context`
   - garante tool registrada e ausência de capítulos irrelevantes.

## Verificação por checkpoint

- corpus de perguntas esperadas com passagem correta;
- evento serializado contém somente blocos selecionados;
- agente principal não referencia conteúdo do arquivo;
- hash do regulamento permanece estável.

## Riscos

- Busca lexical não resolve linguagem muito variada. Mitigação: sinônimos
  locais, segmentação por artigo e corpus de consultas; sem resposta inventada.
- Bloco adjacente trazer assunto não solicitado. Mitigação: limite por artigo
  e teste explícito de exclusão.

## Critério de saída

Art. 22 é recuperado para piscina aos domingos sem inserir outros capítulos.
