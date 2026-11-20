# Tarefas: foundation

Status: implementado e verificado em 2026-11-20
Pré-requisito: mapa e especificação aprovados.

- [x] **F01 — Inicializar projeto reproduzível**
  - Commit: `chore: initialize reproducible python project`
  - Implementar: `pyproject.toml`, `src/aurora/__init__.py`, lock e metadados.
  - Aceitação: Python `>=3.12`; `google-adk==2.9.1`; install completo.
  - Verificar: `uv sync --locked` e import da versão do ADK.
  - Rastreia: critérios de execução/ADK.

- [x] **F02 — Configurar ambiente e segredos**
  - Commit: `chore: enforce environment configuration`
  - Arquivos: `src/aurora/config.py`, `.env.example`, `.gitignore`,
    `tests/test_config.py`.
  - Implementar: validação de `GOOGLE_API_KEY`, caminho do banco e host/porta.
  - Aceitação: erro explícito sem chave no fluxo que a exige; nenhum segredo em
    `.env.example`; `.env` ignorado.
  - Verificar: `uv run pytest tests/test_config.py` e `git check-ignore .env`.

- [x] **F03 — Instalar gates e smoke**
  - Commit: `chore: add quality gates and smoke entrypoint`
  - Implementar: configuração pytest/Ruff e smoke importável do pacote.
  - Aceitação: qualquer task futura pode começar de um baseline verde.
  - Verificar: `uv run pytest`, `uv run ruff check .`.

## Saída do módulo

- [x] Todos os checks acima passam.
- [x] Nenhum arquivo em `dados/` mudou.
- [x] `git diff --staged` não contém chave ou token.
