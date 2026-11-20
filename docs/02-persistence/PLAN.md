# Plano: persistence

Status: implementado e verificado em 2026-11-20
## Decisões

- Usar um banco operacional SQLite e SQLAlchemy assíncrona.
- Modelos separados por tabela; `id` de sessão gerado pelo sistema.
- Eventos com chave composta `session_id`, sequência monotônica.
- Reservas possuem estado `active/cancelled`; a unicidade usa índice parcial
  exclusivo para linhas ativas `(area, data)`.
- Uma tabela independente registra todos os códigos já usados.
- Confirmações guardam payload canônico serializado, estado e identificador de
  retomada.
- Migração simples e versionada é executada no startup; a restauração é um
  comando explícito, não efeito colateral do servidor.

## Componentes

```text
src/aurora/persistence/
  database.py
  models.py
  repositories.py
  bootstrap.py
  exceptions.py
```

## Sequência de commits

1. `feat: add persistent domain schema`
   - cria engine, tabelas, migração e testes de schema;
   - confirma que o projeto inicia e fecha sem perdas.
2. `feat: bootstrap immutable condominium data`
   - importa apartamentos, áreas, reservas e visitantes para banco;
   - não altera ou copia dados sensivelmente no evento.
3. `feat: add transactional repositories`
   - CRUD tipado de sessão, evento, reservas, visitantes e confirmações;
   - exceções de domínio para `not found`, `conflict` e `invalid transition`.
4. `feat: add data restoration command`
   - restaura estado derivado de JSON e pode preservar sessões por padrão;
   - verifica idempotência e hashes de origem.
5. `test: verify persistence across restarts`
   - recria engine/serviço contra o mesmo arquivo e valida sessão/eventos/dados.

## Verificação por checkpoint

- criação e migração em banco temporário;
- inspeção das constraints no SQLite real;
- restauração executada duas vezes;
- comparação dos JSON de origem antes/depois;
- recriação do processo/engine preservando linhas;
- corrida direta de duas inserções na mesma área/data.

## Riscos

- Índice parcial incorreto no SQLite. Mitigação: teste do esquema e corrida real.
- Colisão entre tabelas próprias e tabelas ADK. Mitigação: prefixos próprios e
  revisão do `DatabaseSessionService`.
- Migração no startup mascara dados. Mitigação: migração explícita, transação e
  falha visível.

## Critério de saída

Banco versionado, restaurável, persistente e com restrições físicas comprovadas.
