# Plano: reservation-tools

Status: implementado e verificado em 2026-11-20
## Decisões

- Service de reservas orquestra repositórios; as funções expostas ao ADK apenas
  validam args e convertem resultados.
- Área/taxa vem do catálogo persistido, não do modelo.
- Reserva de taxa zero executa imediatamente; taxa positiva retorna intenção e
  delega execução ao módulo `confirmation`.
- Conflitos de índice único são mapeados para `DATA_INDISPONIVEL`.
- Código UUID opaco com prefixo `RSV-` é gerado no serviço e gravado/checado em
  transação junto da tabela de códigos.

## Componentes

```text
src/aurora/domain/reservations.py
src/aurora/tools/reservations.py
tests/reservations/
```

## Sequência de commits

1. `feat: add reservation queries and availability`
   - valida área/data, lista próprias e mascara disponibilidade.
2. `feat: cancel resident reservation without confirmation`
   - cancelamento próprio, sem efeito em outro apartamento.
3. `feat: reserve free areas without confirmation`
   - código único e gravação transacional de taxa zero.
4. `feat: prepare paid reservation intent`
   - produz payload pendente, sem gravar reserva.
5. `test: enforce atomic reservation conflict`
   - duas inserções simultâneas e reinício provam uma vencedora.

## Verificação por checkpoint

- chamadas de serviço/tool em banco temporário;
- índices/constraints reais em conflito concorrente;
- testes de taxa `0`, `80` e `150`;
- histórico de códigos depois de cancelamento.

## Riscos

- `consulta + inserção` não garante atomicidade. Mitigação: o teste de corrida
  precisa falhar se depender apenas da consulta.
- Geração aleatória colidir. Mitigação: unique constraint e retry limitado
  explícito sem reutilizar código conhecido.

## Critério de saída

Reservas próprias, cancelamento e disputa passam sem confirmação precoce.
