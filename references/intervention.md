# Política de intervenção e precedência

Este ficheiro define **como o Humanizer decide se deve alterar texto e até que ponto**. Não define verdade linguística genérica; essa autoridade pertence ao PT-PT Language Intelligence.

## Regra central

> A melhor alteração é a menor alteração que resolve um problema real sem perder significado, voz ou contexto.

Humanizar não significa maximizar a diferença entre input e output.

## Precedência

Quando duas instruções entram em conflito, usa esta ordem dentro da tarefa de humanização:

1. **Exatidão semântica e não invenção** — factos, negação, modalidade, quantidades, relações temporais e causalidade não podem mudar só para melhorar estilo.
2. **Pedido explícito do utilizador** — mudanças de conteúdo só são permitidas quando foram realmente pedidas; um pedido estilístico não autoriza alterar factos.
3. **Conteúdo literal/protegido** — código, comandos, URLs, identificadores, citações, nomes próprios, títulos oficiais e outros elementos marcados para preservação.
4. **Constraints e terminologia do projeto/formato** — UI, limites de caracteres, glossário aplicado, convenções técnicas e requisitos do meio.
5. **Amostra autêntica de voz** — quando existe, governa ritmo e escolhas estilísticas dentro dos limites acima.
6. **Política do modo** — QA HUMANO intervém menos; HUMANIZAR pode reorganizar mais; AUTO escolhe a menor intervenção adequada.
7. **Conhecimento linguístico pt-PT** — corrige problemas reais de naturalidade, variedade, sintaxe ou translationese quando aplicável ao contexto.
8. **Heurísticas estilísticas do Humanizer** — padrões, ritmo, concisão e composição. Nunca vencem uma camada superior.

## Orçamento de intervenção

### AUDITAR

- reescrita: nenhuma;
- só diagnóstico observável;
- não altera o texto.

### QA HUMANO

- orçamento: mínimo;
- corrige erro, ambiguidade real, pt-BR inadequado, tradução literal, repetição involuntária ou fricção clara;
- se a frase já é natural, preserva-a.

### AUTO

- escolhe QA HUMANO por defeito quando a evidência de intervenção profunda não é clara;
- HUMANIZAR só quando existem sinais suficientes e combinados;
- não usa “quantidade de diferenças” como prova de melhoria.

### HUMANIZAR

- permite intervenção moderada/profunda na forma;
- mantém significado, factos, modalidade, nomes, números e elementos protegidos;
- não introduz personalidade artificial que não esteja no original ou no pedido.

### CLONAR VOZ

- orçamento condicionado pela amostra;
- a voz pode sobrepor-se a preferências estilísticas genéricas;
- nunca se sobrepõe a exatidão, conteúdo protegido ou não invenção.

## Âncoras semânticas

O tooling consegue verificar automaticamente alguns elementos de alto risco:

- números e percentagens;
- datas;
- moedas;
- versões;
- URLs;
- e-mails;
- código inline;
- paths;
- texto explicitamente citado.

Esta verificação é **necessária mas não suficiente**. Não deteta, por si só, mudanças subtis como:

- “pode” → “vai”;
- “não é obrigatório” → “é obrigatório”;
- “antes de” → “depois de”;
- mudança de agente;
- causalidade inventada.

Esses casos precisam de evals dedicados e/ou revisão semântica.

## Over-editing

Casos negativos fazem parte da qualidade do produto.

Um output pode falhar mesmo estando gramaticalmente correto se:

- reescreve texto já natural sem necessidade;
- uniformiza uma voz legítima;
- troca terminologia correta por sinónimos;
- formaliza oralidade adequada;
- remove hesitação ou humor intencional;
- transforma uma frase simples numa versão mais longa apenas para “parecer diferente”.

Alguns evals definem `max_change_ratio`. É um guard de regressão para esses casos, não uma métrica universal de qualidade.

## Relação com PT-PT Language Intelligence

Language Intelligence pode dizer:

> esta construção é comum, contextual, rara ou inadequada em determinado contexto pt-PT.

O Humanizer decide:

> neste modo, neste formato e neste texto concreto, devo alterá-la?

A primeira decisão é linguística. A segunda é de produto.
