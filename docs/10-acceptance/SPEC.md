# Especificação: acceptance — V1

## Objetivo

Comprovar de ponta a ponta os critérios do README, consolidar a documentação de
entrega e impedir regressões nas cinco garantias.

## Dependências

- `api-contract`.

## Níveis de verificação

### Ambiente limpo

- copiar `.env.example` para `.env`;
- preencher chave do avaliador;
- `uv sync`;
- restaurar dados;
- subir API;
- conferir dados iniciais das rotas de verificação.

### Fluxos funcionais

Cobrir todos os 15 passos do avaliador, incluindo:

- isolamento do apartamento;
- cancelamento próprio;
- reserva gratuita sem confirmação;
- reserva paga negada e aprovada;
- execução única;
- confirmação inválida;
- visitante;
- regulamento focado;
- reinício;
- disputa simultânea.

### Auditoria do repositório

- hashes idênticos aos de `dados/` do repositório base;
- `.env` ignorado e nenhuma credencial versionada;
- versão exata do ADK na série 2 e `>= 2.2.0`;
- principal + pelo menos dois especialistas;
- acesso a reservas/visitantes somente por tools;
- ausência de argumento livre de apartamento nas tools;
- principal sem regulamento completo;
- restrição de banco demonstrada no código/migração.

### Documentação final

Substituir o enunciado por README com:

1. Arquitetura e acionamento de cada agente;
2. Garantias, com links de arquivo, trecho real e explicação da garantia
   determinística;
3. Como rodar, variáveis, subida e restauração.

## Testes planejados

- testes de integração para APIs com banco temporário;
- testes ADK reais com Runner persistente;
- roteiro HTTP para o fluxo avaliador;
- teste concorrente com chamadas paralelas;
- teste de reinício de processo;
- testes de auditoria de eventos;
- script/check de integridade de dados e segredos.

Nenhuma garantia deve ser considerada passada apenas por criação de estado
pendente. O caminho de aprovação real é obrigatório.

## Evidências

Cada etapa registra:

- comando executado;
- saída relevante;
- cenário coberto;
- arquivo/teste que comprova;
- estado observável via rota;
- ausência ou presença de efeitos esperados.

## Limites

- Sempre: executar a verificação antes de declarar sucesso.
- Sempre: limpar apenas bancos temporários e artefatos de teste conhecidos.
- Consultar antes: alterar o comportamento livre permitido pelo enunciado.
- Nunca: mascarar teste concorrente com lock somente em processo.

## Critérios de sucesso

- todas as caixas de “Critérios de aceite” do README são reproduzíveis;
- o fluxo completo passa em clone limpo;
- reinício e concorrência são observados, não inferidos;
- README final referencia trechos existentes;
- `dados/` permanece intacto e credenciais não aparecem no Git.

## Fora de escopo

Deploy, benchmark de custo, evals qualitativos de tom e cobertura além dos
fluxos do avaliador.

## Questões abertas

Nenhuma.
