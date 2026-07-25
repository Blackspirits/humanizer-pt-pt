# Contribuir

## Antes de propor uma alteração

1. Confirma que o problema é específico ou relevante para pt-PT.
2. Distingue erro linguístico, preferência editorial e termo dependente do contexto.
3. Evita transformar hábitos pessoais em regras universais.
4. Procura falsos positivos antes de acrescentar um marcador.
5. Não uses classificadores de IA como única prova.

## Alterações editoriais

Uma alteração a `SKILL.md` ou `references/` deve incluir, quando aplicável:

- explicação curta do problema;
- exemplo “antes” e “depois” que não acrescente factos;
- proteção contra falsos positivos;
- caso em `evals/cases.json`;
- atualização da documentação.

Os exemplos devem preservar toda a informação relevante do original. Nunca “melhores” um exemplo inventando números, fontes, funcionalidades, causas, experiências ou testemunhos.

## Vocabulário

As entradas de `vocabulary-map.json` são sugestões contextuais, não substituições globais. Para cada termo ambíguo, acrescenta uma nota em `context_notes`.

Nunca criar regras que:

- alterem nomes próprios;
- mudem títulos oficiais;
- traduzam identificadores técnicos;
- imponham `tu` ou `você` sem contexto;
- confundam variantes ortográficas com erros;
- removam regionalismos legítimos do autor;
- equiparem mecanismos culturais diferentes, como `boleto` e referência Multibanco.

## Auditoria

Casos `AUDITAR` devem:

- usar excertos copiados literalmente do input;
- referir IDs de 1 a 36;
- distinguir gravidade da ocorrência e nível geral;
- proibir afirmações ou percentagens de origem IA;
- incluir um caso limpo para controlar falsos positivos.

## Validação

```bash
python scripts/validate-package.py
python -m unittest discover -s tests -v
```

Para testar respostas reais de um modelo:

```bash
python evals/score-results.py --template > responses.json
python evals/score-results.py responses.json
```

## Lançamento

Ao alterar comportamento:

1. atualiza as versões em `SKILL.md`, `vocabulary-map.json`, `evals/cases.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` e `CITATION.cff`;
2. acrescenta a alteração ao `CHANGELOG.md`;
3. executa `python scripts/package-release.py`;
4. confirma que ZIP e TAR.GZ contêm os mesmos ficheiros.
