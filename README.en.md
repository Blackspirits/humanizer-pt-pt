# Humanizer pt-PT

A portable Agent Skill for auditing, editing and rewriting European Portuguese (`pt-PT`, AO90). It removes common AI-writing patterns, Brazilian Portuguese leakage, English translationese and unnecessary corporate formality while preserving facts, intent, literal content and the author's voice.

Inspired by [`blader/humanizer`](https://github.com/blader/humanizer), this is an independent language-specific editorial adaptation, not a literal translation.

## Modes

- `AUTO`: selects the least destructive suitable rewrite mode.
- `AUDITAR`: reports observable patterns without rewriting or claiming AI authorship.
- `HUMANIZAR`: deep rewrite for artificial, promotional or translated prose.
- `QA HUMANO`: restrained editing for human-written text.
- `CLONAR VOZ`: calibrates against authentic writing samples.

## Install

```bash
npx skills add Blackspirits/humanizer-pt-pt --global
```

Manual installation must copy the complete `humanizer-pt-pt` directory. Claude Code 2.1.143 or later supports a root `SKILL.md` as a single-skill plugin when no `skills/` directory is declared.

## Quality gates

```bash
python scripts/validate-package.py
python -m unittest discover -s tests -v
python evals/score-results.py --template > responses.json
python scripts/package-release.py
```

- `references/patterns.md`: 36 language and style patterns;
- `references/composition.md`: safe composition principles with a strict no-fabrication rule;
- `references/formats.md`: format-specific guidance;
- `evals/`: model-response evaluation corpus;
- `tests/`: unit tests for repository tooling.

## Non-goals

The project does not promise detector bypass, assign AI-authorship percentages, inject deliberate errors, randomly replace synonyms, or send user text to external services.

## License

MIT. See `LICENSE`, `NOTICE` and `CITATION.cff` for attribution.
