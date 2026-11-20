# Plano: foundation

Status: aprovado para implementação após review do conjunto

## Decisões

- Fixar `requires-python = ">=3.12"` e ADK `2.9.1` sem range.
- Usar FastAPI, Uvicorn, Pydantic, SQLAlchemy assíncrona, `aiosqlite`, pytest,
  pytest-asyncio e Ruff; adicionar somente dependências necessárias ao slice.
- Empacotar em `src/aurora/`.
- Configurar variáveis com validação tipada e leitura de ambiente.
- Usar `.data/aurora.db` como padrão, ignorado pelo Git e substituível por
  variável.

## Arquivos-alvo

- `pyproject.toml`, `uv.lock`;
- `.env.example`, `.gitignore`;
- `src/aurora/config.py`;
- `src/aurora/__init__.py`;
- `tests/test_config.py`;
- scripts de restauração em etapa posterior, quando houver schema.

## Sequência de commits

1. `chore: initialize reproducible python project`
   - cria projeto, dependências, lock e diretório de pacote;
   - verifica importação, versão do ADK e `uv sync --locked`.
2. `chore: enforce environment configuration`
   - cria configuração tipada, ajusta `.env.example` e `.gitignore`;
   - testa chave ausente/caminho de banco/configuração.
3. `chore: add quality gates and smoke entrypoint`
   - define pytest/Ruff e um entrypoint de health/smoke não definitivo;
   - garante base verde antes da persistência.

## Verificação por checkpoint

- `uv sync --locked`;
- `uv run python -c "import importlib.metadata; print(importlib.metadata.version('google-adk'))"`
  imprimindo a versão resolvida;
- `uv run pytest tests/test_config.py`;
- `uv run ruff check .`;
- busca por segredo nas mudanças staged.

## Riscos

- A versão 2.9.1 pode exigir metadados ou extras específicos. Mitigação: instalar
  e travar no primeiro commit; não prosseguir se `uv sync --locked` falhar.
- Dependência do ADK pode puxar versões transitivas amplas. Mitigação: lock é
  parte do contrato e os imports usados são testados.

## Critério de saída

Clone limpo instala, configura ambiente sem segredo e executa os gates da base.
