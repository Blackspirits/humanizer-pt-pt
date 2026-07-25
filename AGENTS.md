# Instruções para agentes

## Fonte de verdade

- `SKILL.md`: comportamento, modos e política de saída.
- `references/patterns.md`: catálogo dos 36 padrões.
- `references/composition.md`: princípios para construir a versão final sem inventar.
- `references/formats.md`: regras específicas por género textual.
- `vocabulary-map.json`: apoio terminológico contextual.
- `evals/cases.json`: corpus editorial de regressão.

## Regras de manutenção

- Preservar pt-PT e AO90.
- Não converter preferências contextuais em substituições cegas.
- Não alterar nomes próprios, citações, código ou títulos oficiais nos exemplos.
- Não substituir uma atribuição vaga por uma fonte inventada.
- Manter as versões sincronizadas.
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
