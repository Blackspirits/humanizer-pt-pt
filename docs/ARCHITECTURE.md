# Arquitetura do Humanizer pt-PT

## Princípio

O Humanizer não é um programa clássico em que Python transforma texto diretamente.

O runtime principal é o **modelo que executa a skill**. O repositório fornece o contrato de comportamento, referências, conhecimento aplicado, evals e tooling que tornam essa execução reproduzível e auditável.

```text
MODELO / AGENTE
      ↓ executa
SKILL.md
      ↓ consulta
COMPORTAMENTO + REFERÊNCIAS DO HUMANIZER
      ↓ consome
CONHECIMENTO LINGUÍSTICO VERSIONADO
      ↓ validado por
EVALS / REGRESSÕES
```

## Camadas

### 1. Behavior contract — owned pelo Humanizer

`SKILL.md` possui:

- modos;
- política de intervenção;
- preservação de factos/voz;
- escolha AUTO;
- política de saída;
- UX da skill.

Esta camada não deve ser absorvida pelo PT-PT Language Intelligence.

### 2. Editorial behavior — owned pelo Humanizer

`references/composition.md`, partes de `references/formats.md` e os padrões específicos de humanização definem como intervir no texto.

Um padrão pode usar conhecimento linguístico externo, mas a decisão de **quando e quanto reescrever** continua local.

### 3. Generic language knowledge — externo

A autoridade é `Blackspirits/ptpt-language-intelligence`.

Inclui:

- naturalidade genérica pt-PT;
- contraste pt-PT/pt-BR;
- léxico e preferências semânticas;
- sintaxe, regência e colocação pronominal;
- translationese;
- evidência e confiança.

Enquanto não existe snapshot consumível, `vocabulary-map.json` e regras linguísticas locais são fallback compatível com a release. Devem migrar progressivamente para consumo versionado, sem copiar a source of truth de volta para o Humanizer.

### 4. Contracts

`contracts/` descreve as interfaces de eval/output.

Isto permite que runners, agentes e integrações validem estruturas sem depender de detalhes internos do Python.

### 5. Evals

`evals/` mede comportamento observável do produto:

- preservação;
- falsos positivos;
- escolha de modo;
- padrões AUDITAR;
- regressões contextuais;
- constraints verificáveis.

Evals não são a autoridade linguística. São testes do comportamento do consumidor.

### 6. Support tooling

Python em `scripts/`, `evals/` e `humanizer_support/` existe para:

- validar o pacote;
- pontuar evals;
- verificar contracts;
- construir releases determinísticas.

Não deve tornar-se um segundo “motor linguístico” com listas privadas de regras.

## Evolução

A evolução segura deve seguir:

```text
evidência linguística
      ↓
PT-PT Language Intelligence
      ↓ snapshot versionado
Humanizer consumer adapter
      ↓
behavior/eval impact
      ↓
release Humanizer
```

Mudanças puramente de comportamento podem evoluir diretamente no Humanizer, desde que sejam cobertas por evals.

## Relação com blader/humanizer

`blader/humanizer` foi uma inspiração inicial para padrões de escrita artificial e formato de skill.

Não é upstream arquitetural obrigatório.

A partir da linha 1.x, este repo evolui segundo:

- necessidades reais de pt-PT;
- conhecimento validado do PT-PT Language Intelligence;
- evals próprios;
- regressões próprias;
- requisitos dos runtimes de skills suportados.

Portanto, melhorias futuras não devem ser avaliadas pela proximidade ao Humanizer inglês, mas pela qualidade e segurança do comportamento pt-PT.
