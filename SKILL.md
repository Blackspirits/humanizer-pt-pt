---
name: humanizer-pt-pt
description: |
  Revê e reescreve texto em português europeu (pt-PT, AO90) para remover
  padrões típicos de escrita gerada por IA, tradução literal, português do
  Brasil e formalismo artificial. Preserva factos, intenção, voz, termos
  técnicos, formatação e nomes próprios. Inclui modos de humanização profunda,
  revisão mínima de texto humano, auditoria sem reescrita e clonagem de voz a partir de amostras.
license: MIT
compatibility: Agent Skills clients; Claude Code 2.1.143+ (root single-skill plugin layout).
metadata:
  version: "1.0.0"
  locale: "pt-PT"
---

# Humanizer pt-PT

Edita texto em português europeu para que pareça escrito por uma pessoa competente, com uma voz adequada ao contexto. O objetivo é melhorar a escrita, não enganar classificadores de IA.

## Princípios obrigatórios

1. **Preserva a informação, não a forma.** Mantém todas as afirmações relevantes, mas podes comprimir repetições, juntar ou separar parágrafos e alterar a ordem quando isso melhorar o texto.
2. **Nunca inventes.** Não acrescentes factos, nomes, datas, números, citações, fontes, experiências pessoais ou detalhes concretos que não estejam no original ou nas instruções do utilizador.
3. **Mantém a intenção.** Não transformes uma nota informal num comunicado, uma opinião numa resposta neutra ou uma sinopse num texto promocional.
4. **Preserva elementos literais.** Não alteres código, comandos, caminhos, URLs, chaves, identificadores, nomes de produtos, nomes próprios, títulos oficiais ou texto citado, salvo pedido explícito.
5. **Usa pt-PT e AO90.** Evita pt-BR, mas não faças substituições cegas. O contexto decide.
6. **A voz do autor tem prioridade.** Quando existirem amostras autênticas do autor, imita os hábitos observados em vez de impor uma cadência genérica.
7. **Não introduzas erros deliberados.** Naturalidade não significa escrever mal, inserir gralhas ou forçar gíria.

## Modos

### MODO: AUTO

Determina o nível de intervenção:

- texto claramente gerado por IA, promocional ou traduzido literalmente: aplica **HUMANIZAR**;
- texto humano com problemas pontuais: aplica **QA HUMANO**;
- amostras de voz fornecidas: combina o modo adequado com **CLONAR VOZ**.

Em caso de dúvida, prefere **QA HUMANO**. É mais fácil deixar uma frase um pouco rígida do que apagar a voz de uma pessoa. O modo **AUDITAR** só é ativado quando o utilizador pedir análise, diagnóstico, pontuação ou revisão sem alterações.

### MODO: AUDITAR

Analisa o texto sem o reescrever. Identifica apenas padrões observáveis e apresenta, para cada ocorrência relevante:

- ID e nome do padrão;
- excerto exato do texto;
- gravidade: **ligeira**, **clara** ou **grave**;
- motivo e direção de correção.

Termina com a contagem de padrões, categorias afetadas e nível geral: **limpo**, **ligeiro**, **moderado** ou **pesado**. Não atribuas percentagens de IA, não afirmes que o texto foi gerado por IA e não uses classificadores externos como prova.

### MODO: HUMANIZAR

Reescrita profunda. Remove padrões de IA, tradução literal, enchimento e estrutura mecânica. Podes reorganizar livremente, desde que preserves a informação e o objetivo.

### MODO: QA HUMANO

Revisão contida. Corrige apenas problemas reais: gramática, ambiguidade, repetição involuntária, pt-BR, tradução literal, tom inadequado ou frase pouco natural. Não substituas frases simples apenas para parecerem mais elegantes.

### MODO: CLONAR VOZ

Analisa primeiro as amostras do autor:

- extensão e ritmo das frases;
- vocabulário e nível de formalidade;
- pontuação e uso de parênteses ou travessões;
- forma de iniciar parágrafos;
- transições frequentes ou ausência delas;
- repetições deliberadas, humor, secura ou hesitação;
- tratamento usado: tu, você, construção impessoal ou terceira pessoa.

Replica esses hábitos sem copiar frases completas. A amostra sobrepõe-se às preferências genéricas desta skill, exceto às regras de exatidão, segurança e não invenção.

## Fluxo de trabalho

1. Identifica o formato, o público, o objetivo e o registo.
2. Escolhe o modo.
3. Deteta problemas com `references/patterns.md`. Procura combinações; uma palavra isolada raramente prova alguma coisa.
4. Consulta `references/composition.md` antes de reescrever. Aplica os princípios apenas quando melhorarem clareza, precisão ou ritmo sem acrescentar conteúdo.
5. Se o modo for **AUDITAR**, produz o relatório e não alteres o texto. Nos restantes modos, reescreve apenas o necessário.
6. Faz uma auditoria silenciosa:
   - introduzi algum facto novo?
   - alterei a posição ou a intenção do autor?
   - deixei clichés, pt-BR ou tradução literal?
   - regularizei demasiado a voz?
   - mexi em texto literal ou nomes próprios?
7. Entrega a versão final. Só mostra a auditoria quando o utilizador a pedir ou quando o modo ativo for **AUDITAR**.

## Ficheiros de apoio

Esta skill inclui ficheiros de referência que deves consultar conforme o contexto, em vez de os carregar sempre:

- **`references/patterns.md`** — os 36 padrões de deteção com exemplos e correções. Consulta sempre que estiveres a detetar ou corrigir problemas no texto.
- **`references/composition.md`** — princípios de composição em pt-PT: clareza, concisão, voz ativa contextual, ritmo e estrutura de parágrafos, sempre com proteção contra invenções. Consulta antes de uma reescrita.
- **`references/formats.md`** — regras específicas por formato (e-mail, documentação técnica, UI, sinopse, texto jurídico, guião e texto falado). Consulta quando souberes o formato.
- **`references/regional-variation.md`** — consulta quando o texto tiver regionalismos, oralidade, fala transcrita ou público regional identificado. Define como preservar variedades portuguesas legítimas em vez de as uniformizar.
- **`vocabulary-map.json`** — consulta quando o texto envolver localização, infiltração de pt-BR, terminologia de interface (UI), anglicismos ou linguagem burocrática. Contém mapeamentos pt-BR→pt-PT, termos de UI, marcadores de IA e notas contextuais que evitam substituições cegas. As notas em `context_notes` têm prioridade sobre qualquer mapeamento direto.
- **`profiles/blackspirits.md`** — consulta apenas quando o autor ou o projeto indicar explicitamente que segue as preferências de BlackSpirits. Define terminologia e tom próprios que se sobrepõem às predefinições genéricas, mas nunca às regras de exatidão e não invenção.
- **`examples/terminology-overrides.json`** — consulta quando um projeto declarar terminologia própria que deva prevalecer sobre o mapa geral.

Se os ficheiros especializados não se aplicarem, segue apenas o núcleo desta `SKILL.md` e consulta `references/patterns.md` para a deteção.

# Padrões a detetar e corrigir

Os 36 padrões — sinais, exemplos antes/depois e correções — estão em **`references/patterns.md`**. Consulta esse ficheiro sempre que estiveres a detetar ou corrigir problemas no texto.

Resumo das categorias:

- **Conteúdo** (1-6): importância inflacionada, linguagem promocional, atribuições vagas, análise por gerúndio, secções formulaicas, contextualização genérica.
- **Vocabulário e sintaxe** (7-21): vocabulário de IA, verbos vagos, paralelismos negativos, regra de três, sinónimos artificiais, intervalos falsos, voz passiva, conectores em excesso, tradução literal, pt-BR, gerúndio progressivo, pronomes, tratamento, artigos/possessivos, nominalizações.
- **Estilo e formatação** (22-29): travessões, negrito mecânico, listas com cabeçalhos, títulos genéricos, emojis, parágrafos regulares, frases curtas dramáticas, aforismos fabricados.
- **Comunicação** (30-33): artefactos de chatbot, tom servil, falsas experiências, anúncios do que vem a seguir.
- **Enchimento e conclusão** (34-36): expressões longas sem função, hesitação/falsa certeza, conclusões genéricas.

Procura combinações de sinais, não palavras isoladas.

# Falsos positivos

Não classifiques automaticamente como escrita de IA:

- gramática correta;
- texto formal ou académico;
- uma palavra como “além disso” usada uma vez;
- um travessão isolado;
- uma lista bem organizada;
- uma frase curta para ênfase;
- aspas tipográficas;
- vocabulário técnico;
- repetição necessária para consistência terminológica;
- texto neutro num contexto jurídico, técnico ou enciclopédico.

Procura grupos de sinais. A combinação de introdução genérica, regra de três, importância inflacionada, conectores repetidos e conclusão otimista é mais relevante do que qualquer elemento isolado.

# Sinais de voz humana a preservar

- detalhes específicos fornecidos pelo autor;
- dúvidas ou sentimentos contraditórios;
- humor seco, apartes e autocorreções;
- repetições com intenção emocional;
- ritmo irregular mas legível;
- opiniões que o autor consegue justificar;
- regionalismos adequados ao autor e ao público;
- escolhas terminológicas consistentes com o projeto.

# Princípios de composição e regras por formato

Os princípios de clareza, concisão, ritmo e organização estão em **`references/composition.md`**. As regras específicas por formato (e-mail, documentação técnica, UI e microcopy, sinopses, texto jurídico, guião e texto falado) estão em **`references/formats.md`**. Consulta os ficheiros aplicáveis antes de reescrever.

# Política de saída

- Pedido de auditoria: entrega apenas o relatório estruturado; não reescrevas o texto nem atribuas origem humana/IA.
- Pedido de reescrita: entrega apenas o texto final, salvo pedido de auditoria.
- Pedido de revisão: podes indicar brevemente problemas reais e depois apresentar a versão final.
- Ficheiro: altera apenas prosa; preserva frontmatter, código, dados, links e estrutura técnica.
- Uso integrado por outro agente: devolve apenas a versão final, sem rascunho, perguntas retóricas ou relatório de processo.

# Checklist final

Antes de responder, confirma silenciosamente:

- [ ] Mantive todos os factos e não acrescentei nenhum?
- [ ] Preservei nomes próprios, números, citações e termos literais?
- [ ] O texto está em pt-PT e segue AO90 de forma coerente?
- [ ] Evitei substituições cegas entre pt-BR e pt-PT?
- [ ] Mantive a voz e o nível de formalidade adequados?
- [ ] Removi clichés, enchimento e estrutura mecânica?
- [ ] A pontuação e o ritmo parecem naturais, não fabricados?
- [ ] O final termina numa ideia útil, sem conclusão automática?
- [ ] Se auditei, citei excertos reais e evitei afirmar que o texto foi escrito por IA?

## Atribuição

Adaptação para português europeu inspirada em `blader/humanizer`, de Siqi Chen, distribuído sob licença MIT, e no guia “Signs of AI writing” do WikiProject AI Cleanup. Esta versão é uma adaptação linguística e editorial, não uma tradução literal.
