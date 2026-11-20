# Plano: acceptance

## Decisões

- Um cenário automatizado usa subprocesso real da API e banco temporário.
- O roteiro segue os 15 passos na ordem, com as mensagens do avaliador ou
  equivalentes parametrizadas.
- Auditorias de segredo, integridade e dependência são scripts executáveis, não
  checklist manual isolado.
- O README final substitui o enunciado somente depois que links e trechos reais
  puderem ser verificados.

## Componentes

```text
tests/acceptance/test_evaluation_flow.py
tests/acceptance/test_restart.py
tests/acceptance/test_concurrency.py
scripts/verify_delivery.py
README.md
```

## Sequência de commits

1. `test: cover core acceptance conversations`
   - passos 1 a 11 no mesmo cenário da API.
2. `test: cover regulation events and restart`
   - passos 12 e 13, contagem e estado persistente.
3. `test: cover simultaneous paid reservation approvals`
   - passo 14 com duas requisições concorrentes.
4. `chore: audit delivery integrity and secrets`
   - hashes de `dados/`, ADK exato, ignore de `.env` e interfaces proibidas.
5. `docs: replace challenge statement with delivery readme`
   - arquitetura, cinco garantias com trechos e como rodar.
6. `chore: verify clean clone delivery commands`
   - executa instalação/restauração/subida/testes no fluxo documentado.

## Verificação por checkpoint

- suíte de aceitação completa;
- duas respostas concorrentes em `200` e uma reserva;
- processo parado/subido novamente;
- `git grep` e verificador de arquivos para credenciais;
- links do README resolvem para código real;
- comandos copiados do README funcionam.

## Riscos

- Testes dependerem de resposta textual do Gemini. Mitigação: avaliar dados,
  confirmações, status e eventos; texto apenas onde o README exige.
- Chave externa torna CI instável. Mitigação: suite unitária não exige rede; o
  fluxo real de aceite exige chave e fica claramente marcado/documentado.

## Critério de saída

Todos os critérios de aceite possuem evidência executável e persistente.
