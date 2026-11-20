# Instruções para agentes de desenvolvimento

Este arquivo define as regras obrigatórias do projeto. A fonte de verdade dos
requisitos e do fluxo de avaliação é o documento `README.md` atualmente
versionado. Em caso de dúvida, preserve o contrato de API e as garantias abaixo
sem depender de instruções do modelo.

## Princípio central

O modelo decide o caminho da conversa; o código decide o que é permitido.
Validação de identidade, autorização, cobrança, exclusividade, persistência e
acesso a dados devem ser garantidos por implementações determinísticas e não
apenas por prompts.

## Stack obrigatória

- Implementar a API em Python 3.12 ou superior.
- Gerenciar o projeto com `uv`; versionar `pyproject.toml` e `uv.lock`.
- Usar Google ADK na série 2, versão 2.2.0 ou mais nova, fixada exatamente.
- Usar modelos Gemini por chave do Google AI Studio.
- Expor a API em `http://localhost:8000`.
- Não versionar segredos. Manter `.env` ignorado e versionar `.env.example`
  apenas com os nomes das variáveis, sem valores.
- Se houver dependência externa, documentar e fornecer um único comando para
  iniciá-la.

## Dados e regras de negócio

- Não alterar os arquivos originais em `dados/`.
- Restaurar reservas e visitantes ao estado inicial por um comando documentado.
- Dados persistidos e sessões podem ficar em armazenamento separado.
- Uma área aceita no máximo uma reserva ativa por data.
- Área com taxa positiva requer confirmação por gerar cobrança; taxa zero não
  requer confirmação.
- Autorizar visitante sempre requer confirmação.
- Cancelamento só pode afetar reserva do apartamento autenticado na sessão e
  não requer confirmação.
- Códigos de novas reservas devem ser únicos, inclusive em relação a reservas
  canceladas anteriormente.

## Arquitetura do agente

- Deve existir um agente principal e pelo menos dois especialistas.
- O principal coordena a conversa e delega aos especialistas.
- Reservas e visitantes devem ser lidos e gravados exclusivamente por tools que
  acessam o armazenamento; o modelo nunca pode inventar ou memorizar esses
  dados.
- O apartamento nunca pode ser escolhido livremente pelo modelo. O contexto
  confiável vem da sessão e deve ser obtido pelo runtime das tools.
- Nenhuma tool pode aceitar apartamento para operar em nome de outro morador
  sem validá-lo contra o apartamento registrado na sessão.
- O regulamento deve ser consultado por recuperação focada, sem ser incluído nas
  instruções do agente principal nem inserido integralmente no histórico.
- Eventos da sessão não podem expor capítulos ou trechos do regulamento que não
  sejam necessários à pergunta atual.
- Eventos também não podem expor código, nome, data ou apartamento pertencente
  à consulta não autorizada de outro morador.

## Garantias obrigatórias

### 1. Cobrança e acesso só por confirmação do sistema

- Toda reserva de área com taxa ou autorização de visitante deve ficar pendente
  antes de produzir efeito.
- Não basta o usuário declarar que confirmou na conversa.
- `confirmacoes_pendentes` deve listar as ações ainda pendentes e incluir
  detalhes relevantes, como área e data ou visitante e data.
- Aprovar executa exatamente uma vez. Negar não produz efeito.
- A retomada deve chegar ao agente/runner que solicitou a confirmação.
- Um `id` inexistente, de outra sessão ou já respondido retorna `409` e não pode
  executar a ação.
- A confirmação persistida deve ser testada com sessão real, inclusive após
  reinício da API.

### 2. Cada sessão pertence a um único apartamento

- Definir o apartamento uma única vez ao criar a sessão.
- Mensagens posteriores não podem alterá-lo.
- Tools operam somente sobre o apartamento da sessão.
- Consultas de disponibilidade podem ler a agenda da área, mas somente
  devolvem livre/ocupado, sem identificar reserva, código ou morador de outro
  apartamento.

### 3. Nada se perde no reinício

- Persistir eventos e estado da sessão.
- Persistir reservas, cancelamentos, códigos já usados e visitantes.
- Reiniciar a API deve manter histórico existente e permitir continuar a
  sessão.
- Não implementar concorrência ou persistência apenas em memória.

### 4. O regulamento é consultado, não carregado

- Recuperar apenas a passagem pertinente à pergunta.
- Não colocar o texto completo do regulamento no prompt ou no estado da sessão.
- Preservar chamadas de tool nos eventos quando o regulamento for consultado.
- A resposta deve ser baseada no conteúdo oficial em
  `dados/regulamento.md`.

### 5. Exclusividade atômica da reserva

- A garantia de uma única reserva por área e data deve existir no instante da
  gravação, não apenas em uma conferência prévia.
- Usar restrição única, transação ou mecanismo equivalente do armazenamento.
- Conflito concorrente deve ser tratado como resposta normal, sem `500`.
- Em disputas simultâneas, somente uma reserva pode ser persistida, embora ambas
  as aprovações possam responder com sucesso conforme o contrato.

## Contrato obrigatório da API

Todas as rotas recebem e devolvem JSON.

- `POST /sessoes`
  - entrada: `{"apartamento": "<numero>"}`
  - sucesso: `201`, `{"session_id": "..."}`
- `POST /sessoes/{session_id}/mensagens`
  - entrada: `{"texto": "..."}`
  - sucesso: `200`, objeto com `resposta` e `confirmacoes_pendentes`
- `POST /sessoes/{session_id}/confirmacoes`
  - entrada: `{"id": "...", "confirmado": true|false}`
  - sucesso: `200`, no mesmo formato da rota de mensagens
  - confirmação inválida: `409`, sem efeitos
- `GET /sessoes/{session_id}/eventos`
  - sucesso: `200`, lista completa e ordenada dos eventos
- `GET /apartamentos/{apartamento}/reservas`
  - sucesso: `200`, objetos com `codigo`, `area` e `data`
- `GET /apartamentos/{apartamento}/visitantes`
  - sucesso: `200`, objetos com `nome` e `data`

Rotas com `{session_id}` devem retornar `404` quando a sessão não existir.
Datas devem usar o formato `AAAA-MM-DD`. Não alterar nomes de campos, caminhos
ou códigos de status definidos no `README.md`.

## Requisitos de desenvolvimento

- Fazer mudanças pequenas, atômicas e diretamente ligadas ao requisito tratado.
- Separar claramente API, runtime dos agentes, tools, persistência e recuperação
  do regulamento.
- Não introduzir atalhos que controlem regras críticas somente por prompt.
- Tratar explicitamente erros esperados, sobretudo conflitos de reserva e
  confirmações inválidas.
- Preservar comportamento assíncrono e concorrência segura.
- Ao adicionar lógica, cobrir os fluxos de cobrança, visitante, autorização por
  apartamento, reinício e conflito concorrente nos testes ou verificações
  executáveis.
- Antes de concluir, validar o caminho de aprovação real, não apenas a criação
  da confirmação.
- Não afirmar que requisitos passaram sem executar a verificação correspondente
  e observar seu resultado.

## Documentação de entrega

O `README.md` final deve substituir o enunciado e conter:

1. **Arquitetura**: responsabilidade de cada agente, como é acionado e por quê.
2. **Garantias**: para cada uma das cinco garantias, arquivos e trechos reais do
   código que a implementam e por que não dependem do modelo.
3. **Como rodar**: pré-requisitos, variáveis de ambiente, comando de subida e
   comando de restauração.

Antes da entrega, verificar a integridade dos arquivos de `dados/`, a ausência
de credenciais versionadas, a versão exata do ADK e a execução dos comandos do
README em um ambiente limpo.
