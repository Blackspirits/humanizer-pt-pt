# Avaliações editoriais

`cases.json` é um corpus de regressão para respostas de modelos. Não é um conjunto de testes unitários da skill nem prova que um texto foi escrito por uma pessoa.

## O que é automático

`score-results.py` consegue verificar:

- palavras ou expressões proibidas;
- literais que devem permanecer;
- alternativas válidas;
- limites de extensão;
- modo escolhido em casos AUTO;
- estrutura, IDs, excertos e nível geral no modo AUDITAR;
- ausência de afirmações ou percentagens de autoria IA.

## O que continua manual

Voz, cadência, fidelidade semântica profunda e invenções subtis. O runner apresenta estes critérios e os itens de `must_not_invent` como revisão manual explícita; não tenta fingir que os prova automaticamente.

## Gerar um ficheiro de respostas

```bash
python evals/score-results.py --template > responses.json
```

Preenche:

- `output` e `selected_mode` nos casos AUTO;
- o relatório estruturado nos casos AUDITAR;
- uma string com a saída final nos restantes casos.

## Avaliar

```bash
python evals/score-results.py responses.json
```

Avaliar apenas alguns casos:

```bash
python evals/score-results.py responses.json \
  --case audit-problematic-001 \
  --case audit-clean-001 \
  --allow-partial
```

Guardar relatório JSON:

```bash
python evals/score-results.py responses.json --report-json report.json
```

O comando falha quando uma resposta obrigatória está em falta ou quando um critério verificável falha.
