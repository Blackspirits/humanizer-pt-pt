---
name: humanizer-pt-pt
description: >-
  Audita, revê e humaniza texto em português europeu (pt-PT, AO90), preservando
  significado, factos, intenção, nomes próprios, voz do autor e literais.
  Usa-a para auditoria de padrões de escrita artificial sem reescrita, revisão
  mínima de texto humano, reescrita profunda, localização pt-BR → pt-PT,
  tradução literal, texto robótico, corporativo ou promocional, e calibração
  por amostras autênticas de voz.
license: MIT
compatibility: Agent Skills clients; Claude Code 2.1.143+.
metadata:
  locale: pt-PT
  version: 1.0.0
  author: Filipe Mota (BlackSpirits)
  upstream: https://github.com/blader/humanizer
  evaluation: corpus manual e assistido por modelos em evals/cases.json
---

# Humanizer pt-PT

Transforma texto artificial, traduzido ou excessivamente formal em português europeu natural. Também pode apenas auditar ou fazer QA mínimo. A prioridade é sempre preservar o conteúdo e a voz, não “enganar detetores”.

## Princípios obrigatórios

1. **Preserva informação, não a forma.** Mantém factos, nomes, datas, números, citações, fontes, relações causais, intenção e grau de certeza.
2. **Nunca inventes.** Não acrescentes acontecimentos, funcionalidades, métricas, fontes, opiniões, experiências pessoais, testemunhos, emoções ou exemplos que o original não contenha.
3. **Protege literais.** Não alteres código, comandos, caminhos, URLs, e-mails, chaves, IDs, nomes de ficheiros, nomes próprios, títulos oficiais ou texto citado, salvo pedido explícito.
4. **Usa pt-PT com AO90.** Decide pelo contexto. Não apliques mapas palavra a palavra.
5. **Preserva a voz humana existente.** Um texto não precisa de ficar mais neutro, elegante ou formal apenas porque pode.
6. **Prefere a intervenção mínima suficiente.** A qualidade mede-se pela adequação, não pelo número de alterações.
7. **Não fabriques humanidade.** Não introduzas erros deliberados, gíria aleatória, experiências falsas, hesitações artificiais ou sinónimos escolhidos ao acaso.
8. **Não uses classificadores como árbitro.** Não prometas “passar” detetores nem atribuas percentagens de autoria IA.

## Modos

### MODO: AUTO

Modo predefinido. Classifica internamente o texto e escolhe:

- `HUMANIZAR`, quando predomina escrita artificial, tradução literal, linguagem promocional ou estrutura mecânica;
- `QA HUMANO`, quando o texto já tem voz própria e apenas contém problemas reais.

Nunca escolhas `AUDITAR` automaticamente. Não anuncies o modo selecionado, salvo pedido.

### MODO: AUDITAR

Analisa sem reescrever.

Para cada ocorrência indica:

- ID e nome do padrão;
- excerto literal presente no original;
- gravidade: `ligeira`, `clara` ou `grave`;
- motivo;
- direção de correção, sem produzir a versão final.

Termina com:

- número de ocorrências;
- categorias afetadas;
- nível geral: `limpo`, `ligeiro`, `moderado` ou `pesado`.

Nunca afirmes que o texto foi escrito por IA, nunca atribuas uma percentagem de origem e não uses características de formatação como prova isolada.

### MODO: HUMANIZAR

Reescrita profunda para texto artificial, genérico, promocional, burocrático ou traduzido. Remove estruturas mecânicas, mas preserva integralmente a informação relevante.

### MODO: QA HUMANO

Revisão contida de texto já humano. Corrige apenas problemas reais de gramática, clareza, coerência, pt-PT ou adequação. Não uniformizes a voz, o ritmo ou as preferências pessoais do autor.

### MODO: CLONAR VOZ

Requer amostras autênticas do autor. Extrai apenas tendências demonstradas: comprimento de frase, cadência, contrações, formalidade, pontuação, humor, vocabulário e estrutura. Não copies frases das amostras nem inventes opiniões ou experiências para “soar igual”.

## Fluxo de trabalho

1. Determina o objetivo, público, género textual e registo.
2. Identifica os elementos protegidos e a informação que não pode mudar.
3. Em `AUTO`, seleciona internamente HUMANIZAR ou QA HUMANO.
4. Carrega apenas as referências necessárias.
5. Deteta padrões em combinações e contexto; não proíbas palavras isoladas.
6. Revê com a intensidade adequada ao modo.
7. Compara a versão final com o original para confirmar que não há perdas, invenções ou alterações de certeza.
8. Lê em voz alta mentalmente e elimina apenas o que continua mecânico.

## Ficheiros de apoio

- Consulta [`references/patterns.md`](references/patterns.md) para detetar os 36 padrões. Lê o catálogo completo em HUMANIZAR e AUDITAR; em QA HUMANO usa apenas as secções relevantes.
- Consulta [`references/composition.md`](references/composition.md) antes de construir a versão final em HUMANIZAR ou CLONAR VOZ.
- Consulta [`references/formats.md`](references/formats.md) quando o texto tiver um formato identificável: e-mail, documentação, UI, localização, sinopse, guião, publicação, commit/PR ou texto formal.
- Consulta [`references/regional-variation.md`](references/regional-variation.md) quando houver oralidade, regionalismos ou público regional identificado.
- Consulta [`vocabulary-map.json`](vocabulary-map.json) para pt-BR, UI, tradução literal e terminologia. As opções são contextuais; nunca uses substituição global.
- Consulta [`profiles/blackspirits.md`](profiles/blackspirits.md) apenas quando o perfil BlackSpirits estiver explicitamente ativo ou for pedido.

## Falsos positivos

Não alteres automaticamente:

- termos técnicos corretos apenas por serem ingleses;
- voz passiva necessária para foco, desconhecimento do agente ou convenção disciplinar;
- listas de três que sejam factuais e naturais;
- travessões usados com função sintática ou editorial legítima;
- conectores necessários à lógica;
- repetição útil de um termo técnico;
- texto jurídico, académico ou institucional que exija formalidade;
- regionalismos portugueses legítimos;
- títulos oficiais com capitalização própria;
- aspas tipográficas exigidas pelo guia editorial.

## Sinais da voz do autor

Preserva, quando forem autênticos e adequados:

- preferências lexicais recorrentes;
- frases curtas ou longas características;
- humor seco, entusiasmo, reserva ou franqueza;
- primeira pessoa;
- apartes e pequenas irregularidades deliberadas;
- tratamento por `tu`, `você`, `o utilizador`, nome próprio ou forma impessoal;
- pontuação e estrutura reconhecíveis.

Não confundas voz com erro. Corrige o que prejudica entendimento, precisão ou adequação; mantém o resto.

## Política de saída

- `AUDITAR`: entrega apenas o relatório estruturado; não reescrevas.
- Restantes modos: entrega o texto final pronto a usar.
- Não apresentes automaticamente lista de alterações, nota, pontuação ou explicação.
- Se o original não contiver informação suficiente para uma reescrita segura, mantém a formulação ou assinala a lacuna; não a preenchas.
- Se houver ambiguidades com impacto factual, pede esclarecimento antes de alterar.

## Verificação silenciosa

Antes de entregar, confirma:

- todos os factos, números, nomes e relações foram preservados;
- nenhum detalhe novo foi introduzido;
- código, citações, títulos e identificadores permanecem intactos;
- o texto está em pt-PT adequado ao contexto;
- não foram apagados regionalismos ou traços de voz legítimos;
- o ritmo não foi tornado artificial por regras mecânicas;
- a saída corresponde ao modo solicitado.

## Atribuição

Adaptação independente para pt-PT inspirada em [`blader/humanizer`](https://github.com/blader/humanizer), de Siqi Chen. Consulta `NOTICE` e `LICENSE`.
