# Contratos

Estes contratos tornam explícitas as estruturas usadas pelo Humanizer sem transformar a skill numa aplicação pesada.

- `rewrite-response.schema.json` — saída de modos de reescrita/revisão.
- `audit-response.schema.json` — saída estruturada de AUDITAR.
- `eval-corpus.schema.json` — corpus de regressão, incluindo guards de âncoras semânticas e orçamento de alteração.

Os contratos descrevem **interfaces do Humanizer**, não uma autoridade universal sobre conhecimento linguístico. Regras de português europeu incluídas na release são conhecimento aplicado e versionado do produto.

Os IDs de padrões não têm um limite máximo congelado no schema. A lista válida é derivada de `references/patterns.md`, o catálogo da release instalada.
