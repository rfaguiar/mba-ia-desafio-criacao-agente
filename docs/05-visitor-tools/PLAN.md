# Plano: visitor-tools

## Decisões

- Especialista usa service/tool e nunca toca visitante diretamente.
- Lista somente DTO próprio.
- Solicitar autorização sempre produz intenção pendente; não há atalho de taxa
  ou confirmação por texto.
- Nome é normalizado para exibição, preservando dados de domínio e impedindo
  seu uso como instrução ou consulta.

## Componentes

```text
src/aurora/domain/visitors.py
src/aurora/tools/visitors.py
tests/visitors/
```

## Sequência de commits

1. `feat: list session visitors safely`
   - lista própria com DTO fechado e testes de privacidade.
2. `feat: create pending visitor authorization`
   - registra nome/data em intenção sem efeito.
3. `test: reject prompt-based visitor approval`
   - texto de confirmação continua sem registro.

## Verificação por checkpoint

- `Joana Ribeiro` pendente não aparece na rota de verificação;
- nomes maliciosos permanecem texto e usam bind parameters;
- visitante de 302 não aparece em sessão 101.

## Riscos

- Especialista tentar aprovar diretamente. Mitigação: nenhuma tool de
  autorização efetiva exposta ao modelo; somente callback de confirmação.

## Critério de saída

Autorizar visitante sempre requer confirmação persistente, e leitura é isolada.
