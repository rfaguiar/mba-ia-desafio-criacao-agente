# Especificação: foundation — V1

Status: implementado e verificado em 2026-11-20
## Objetivo

Criar uma base Python reproduzível, segura e executável em ambiente limpo. Esta
capacidade não implementa regras do condomínio; ela permite que todas as etapas
seguintes sejam instaladas, configuradas, restauradas e verificadas da mesma
forma.

## Entregáveis

- `pyproject.toml` compatível com Python 3.12+ e gerenciado por `uv`;
- `uv.lock` versionado e reproduzível;
- `google-adk` na série 2, igual ou superior a 2.2.0 e fixado exatamente;
- FastAPI e dependências estritamente necessárias ao runtime e aos testes;
- configuração por variáveis de ambiente, sem valores secretos versionados;
- `.env.example` apenas com nomes e placeholders não sensíveis;
- `.gitignore` cobrindo `.env`, `.venv`, caches e banco local;
- comando único para restaurar reservas e visitantes;
- comando único para subir a API em `http://localhost:8000`.

## Comandos obrigatórios planejados

```text
uv sync
uv run pytest
uv run ruff check .
uv run python -m aurora.scripts.restore
uv run uvicorn aurora.api.main:app --host 0.0.0.0 --port 8000
```

Os nomes dos módulos poderão ser ajustados na fase de plano, mas os efeitos e a
reprodutibilidade desses comandos não poderão mudar.

## Estrutura planejada

```text
src/aurora/            código da aplicação
tests/                 testes unitários, integração e aceitação
scripts/ ou módulo CLI  restauração e verificações operacionais
docs/                  especificações, planos e tarefas por módulo
.env.example           nomes das variáveis
```

## Requisitos funcionais

- `uv sync` instala a aplicação em um clone limpo.
- O processo falha de forma explícita quando `GOOGLE_API_KEY` está ausente no
  fluxo que precisa do modelo; nenhum segredo é embutido no código.
- A restauração lê exclusivamente os arquivos imutáveis em `dados/`.
- A restauração recria o estado operacional inicial de reservas e visitantes.
- A restauração pode remover sessões apenas se isso for documentado de forma
  explícita e não for usado para corrigir erros comuns de desenvolvimento.
- O caminho do banco operacional é configurável, com valor local seguro padrão.
- O processo não modifica arquivos em `dados/`.

## Estratégia de testes

- Instalação reproduzível em ambiente limpo ou ambiente temporário.
- Teste da configuração ausente e inválida.
- Teste que compara hashes de `dados/` antes e depois da restauração.
- Teste que garante estado inicial após executar a restauração duas vezes.
- Varredura do conteúdo versionado em busca de formato de chave ou segredo.

## Limites

- Sempre: fixar versões exatas das dependências críticas e preservar `dados/`.
- Sempre: manter `.env` fora do Git.
- Consultar antes: adicionar serviço externo ou ferramenta de migração.
- Nunca: carregar valores reais de chave em exemplos, testes ou commits.

## Critérios de sucesso

- `uv sync` termina sem erro.
- `pyproject.toml` contém ADK 2.x fixado exatamente em versão `>= 2.2.0`.
- `.env.example` e `.gitignore` obedecem ao contrato do repositório.
- Os hashes de `dados/` não mudam após restauração.
- Os comandos documentados sobem a API e recuperam os dados iniciais.

## Fora de escopo

- Conteinerização, deploy, observabilidade de produção e autenticação externa.

## Questões abertas

Nenhuma. A escolha de comandos concretos será consolidada no plano técnico sem
alterar seus efeitos exigidos.
