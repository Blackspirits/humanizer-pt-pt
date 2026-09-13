# Instruções para agentes

## Fonte de verdade

- `SKILL.md`: comportamento, modos e política de saída.
- `references/patterns.md`: catálogo dos 36 padrões.
- `references/composition.md`: princípios para construir a versão final sem inventar.
- `references/formats.md`: regras específicas por género textual.
- `vocabulary-map.json`: apoio terminológico contextual.
- `evals/cases.json`: corpus editorial de regressão.
- `contracts/`: contratos de outputs/evals.
- `references/intervention.md`: precedência, orçamento de intervenção e segurança semântica.
- `humanizer_support/semantic.py`: guards determinísticos de eval; não é um motor linguístico.
- `docs/ARCHITECTURE.md`: fronteira entre runtime, comportamento, conhecimento e tooling.


## Autonomia da distribuição

Este repositório define a release pública do Humanizer e deve permanecer autocontido. Nenhum agente pode exigir acesso a repositórios, corpus ou serviços privados para executar, validar ou empacotar a skill.

Modos, política de saída, proteção da voz, critérios de intervenção, UX, evals e comportamento publicado pertencem ao Humanizer. Afirmações linguísticas incluídas na release são conhecimento aplicado e contextual: não devem ser promovidas automaticamente a regras universais da língua.

A manutenção pode validar conhecimento em fontes upstream privadas, mas apenas artefactos explicitamente importados, versionados e testados neste repositório fazem parte da release pública.

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
