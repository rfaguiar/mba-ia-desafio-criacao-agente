# Validação individual do checklist

Data: 2026-11-20

Resultado: 28 de 28 critérios atendidos.

| # | Critério | Verificação executada | Resultado |
|---:|---|---|---|
| 1 | Instalação `uv` e ADK exato | `uv sync --locked`; inspeção de `pyproject.toml` e `uv.lock` | ✅ `google-adk==2.9.1` |
| 2 | Restaurar, subir e dados iniciais | restauração + Uvicorn em `0.0.0.0:8000`; GETs das rotas de verificação | ✅ 200 com `RSV-1377` e Marina Duarte |
| 3 | Integridade de `dados/` | `git diff --exit-code -- dados` | ✅ sem diferenças |
| 4 | Segredos e `.env.example` | `scripts/verify_delivery.py`, `git ls-files`, `.gitignore` | ✅ sem chave; nomes exigidos |
| 5 | Principal e especialistas | introspecção de `factory.py` e teste de topologia | ✅ 1 principal + 3 especialistas |
| 6 | Dados somente por tools e efeito observável | fluxo real + rotas 5, 6, 8 e 11 | ✅ efeitos iguais às rotas |
| 7 | Reserva paga pendente | mensagem do salão; contagem antes e depois | ✅ pendência com área/data; sem gravação |
| 8 | Negação sem efeito | confirmação `false`; rota de reservas | ✅ nenhuma reserva criada |
| 9 | Aprovação grava uma vez | confirmação `true`; rota de reservas | ✅ exatamente uma reserva |
| 10 | Replay retorna 409 | mesmo id após aprovação | ✅ 409; contagem inalterada |
| 11 | Id inválido retorna 409 | `id-inexistente` | ✅ 409; sem alteração |
| 12 | Área gratuita sem confirmação | reserva da quadra 2030-04-06 | ✅ sem pendência e gravada |
| 13 | Visitante sempre confirmado | nome/data na pendência; tentativa textual de confirmação | ✅ sem efeito até a aprovação |
| 14 | Privacidade de consulta 302 | S1 do 101 solicita dados do 302; auditoria de resposta/eventos | ✅ sem `RSV-4821`/Marina |
| 15 | Cancelamento cruzado bloqueado | S1 solicita cancelamento do salão do 302 | ✅ reserva 302 mantida; sem vazamento |
| 16 | Cancelamento próprio | quadra 2030-03-09 do 101 | ✅ cancelada sem confirmação |
| 17 | Conflito com outro apartamento | tentativa de salão 2030-03-16 na S2 | ✅ sem reserva, sem `RSV-4821`/302 |
| 18 | Apartamento originado da sessão | AST das tools + testes de injeção | ✅ nenhuma tool recebe `apartamento` |
| 19 | Eventos e sessão após restart | 82 eventos antes do restart; GET depois; nova mensagem | ✅ mesma contagem inicial e crescimento |
| 20 | Dados e códigos após restart | rotas do 101/302 e unicidade dos códigos | ✅ estado persistido e códigos distintos |
| 21 | Horário da piscina | pergunta real e Art. 22 do regulamento | ✅ resposta contém `20h` |
| 22 | Tools nos eventos e recuperação focada | serialização dos eventos + teste do retriever | ✅ tool registrada; capítulos alheios ausentes |
| 23 | Regulamento fora do agente principal | inspeção das instruções do coordenador | ✅ texto do regulamento não está presente |
| 24 | Aprovações concorrentes retornam 200 | duas requisições HTTP simultâneas | ✅ `200` e `200` |
| 25 | Exatamente uma reserva na disputa | soma das reservas 101 + 201 em 2030-05-11 | ✅ exatamente uma |
| 26 | Unicidade na gravação | índice SQLite parcial exclusivo inspecionado e corrida real | ✅ restrição no banco, conflito normal |
| 27 | Contrato das rotas | testes de API + fluxo HTTP completo, incluindo 404/409 | ✅ caminhos, JSON e status atendidos |
| 28 | README de entrega | títulos Arquitetura/Garantias/Como rodar; links e snippets validados | ✅ seções, arquivos e trechos existentes |

## Cenários corrigidos durante a auditoria

### Pergunta redundante para visitante

- Cenário: nome e data estavam completos, mas o especialista perguntou se
  deveria prosseguir e não criou a confirmação.
- Causa: a instrução permitia uma confirmação conversacional adicional.
- Correção: `especialista_visitantes` agora chama `authorize_visitor`
  imediatamente quando nome e data estão presentes.
- Verificação posterior: o fluxo do visitante gerou pendência, não gravou antes
  da aprovação e gravou depois.

### Limite de requisições do Gemini

- Cenário: execução automatizada rápida recebeu `429 RESOURCE_EXHAUSTED`.
- Causa: o plano gratuito permitia 15 requisições/minuto.
- Correção do roteiro: pausas curtas entre chamadas externas no script de
  aceitação.
- Sugestão operacional: usar cota adequada ou configurar outro modelo Gemini
  disponível em `GEMINI_MODEL`; isso não altera as regras de negócio.

## Verificações complementares

```text
uv sync --locked              PASS
uv run pytest                 18 passed
uv run ruff check .           PASS
scripts/acceptance_flow.py pre   PASS (82 eventos)
scripts/acceptance_flow.py post  PASS
scripts/verify_delivery.py    PASS
git diff --check              PASS
git diff --exit-code -- dados PASS
```
