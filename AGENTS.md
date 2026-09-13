# Instruções para agentes

## Fonte de verdade

- `SKILL.md`: comportamento, modos e política de saída.
- `references/patterns.md`: catálogo dos 36 padrões.
- `references/composition.md`: princípios para construir a versão final sem inventar.
- `references/formats.md`: regras específicas por género textual.
- `vocabulary-map.json`: apoio terminológico contextual.
- `evals/cases.json`: corpus editorial de regressão.
- `contracts/`: contratos de outputs/evals.
- `docs/ARCHITECTURE.md`: fronteira entre runtime, comportamento, conhecimento e tooling.


## Autoridade linguística externa

Este repositório é um **consumidor/aplicação editorial**, não a autoridade BlackSpirits para conhecimento linguístico genérico pt-PT.

A autoridade canónica é:

`Blackspirits/ptpt-language-intelligence`

Regra:

`Language Intelligence owns generic language truth; humanizer owns humanization behavior.`

Enquanto não existir um snapshot versionado aplicável do PT-PT Language Intelligence, as regras e mapas deste repositório continuam a definir o comportamento da versão publicada da skill. No entanto, novas claims linguísticas genéricas devem ser validadas e, quando apropriado, promovidas no Language Intelligence em vez de criarem uma segunda fonte de verdade aqui.

Preferências específicas do Humanizer, modos, política de saída, proteção da voz, critérios de intervenção e UX da skill permanecem neste repositório.

## Regras de manutenção

- Preservar pt-PT e AO90.
- Não converter preferências contextuais em substituições cegas.
- Não alterar nomes próprios, citações, código ou títulos oficiais nos exemplos.
- Não substituir uma atribuição vaga por uma fonte inventada.
- Manter as versões sincronizadas sem hardcodes redundantes no tooling.
- Derivar IDs de padrões do catálogo canónico em vez de congelar limites no código.
- Manter release packaging por allowlist explícita.
- Atualizar evals quando uma regra muda.
- Adicionar testes unitários quando o comportamento dos scripts muda.
- Executar antes de publicar:

```bash
python scripts/validate-package.py
python -m unittest discover -s tests -v
python scripts/package-release.py
```

## Modo AUDITAR

A auditoria identifica características observáveis e cita apenas excertos presentes no original. Nunca apresenta percentagens de IA, não determina a identidade do autor e não reescreve o texto.

## Âmbito

Este repositório contém instruções, referências e ferramentas locais. Não deve incluir serviços para contornar deteção académica, recolher textos de utilizadores ou enviar conteúdo para terceiros.
