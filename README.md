# Humanizer pt-PT

Skill portátil para rever, auditar e reescrever texto em português europeu (`pt-PT`, AO90). Remove padrões artificiais, infiltração de pt-BR, tradução literal e formalismo desnecessário sem alterar factos, intenção, nomes próprios ou voz do autor.

É inspirada em [`blader/humanizer`](https://github.com/blader/humanizer), mas constitui uma adaptação editorial própria para pt-PT, não uma tradução literal.

## O que resolve

- introduções genéricas e conclusões previsíveis;
- importância inflacionada, notoriedade por associação e linguagem promocional;
- conectores, enumerações e estruturas demasiado simétricas;
- pt-BR em texto destinado a Portugal;
- gerúndios progressivos e colocação pronominal pouco natural;
- traduções literais do inglês;
- tom empresarial, académico ou burocrático sem necessidade;
- ganchos dramáticos, títulos em *Title Case* e artefactos de chatbot;
- falsa experiência pessoal e pormenores inventados;
- perda da voz original durante a revisão.

## Princípio central

A qualidade é medida por exatidão, preservação, adequação e naturalidade. A skill não promete contornar GPTZero, Turnitin ou qualquer classificador de IA, nem usa percentagens de “origem IA” como prova.
A CI valida contratos estruturais e critérios objetivos; não prova, por si só, que um modelo nunca inventará informação. A preservação factual completa continua a exigir avaliações com respostas reais e revisão editorial.

## Modos

### AUTO

Escolhe a intervenção menos destrutiva. Usa HUMANIZAR para texto claramente artificial ou traduzido; QA HUMANO para problemas pontuais. AUDITAR só é ativado por pedido explícito.

### AUDITAR

Analisa sem reescrever. Indica padrão, excerto, gravidade, motivo e direção de correção. Não afirma que o texto foi escrito por IA.

### HUMANIZAR

Faz uma reescrita profunda, removendo enchimento, tradução literal, publicidade e estrutura mecânica.

### QA HUMANO

Corrige apenas problemas reais num texto humano, sem apagar a voz do autor nem reescrever por gosto.

### CLONAR VOZ

Usa amostras autênticas para reproduzir ritmo, vocabulário, pontuação e formalidade sem copiar frases nem inventar experiências.

## Instalação

### Skills CLI

```bash
npx skills add Blackspirits/humanizer-pt-pt --global
```

Para todos os agentes suportados:

```bash
npx skills add Blackspirits/humanizer-pt-pt --global --agent '*'
```

Retira `--global` para instalar apenas no projeto atual.

### Claude Code

O Claude Code 2.1.143 ou posterior reconhece uma única `SKILL.md` na raiz quando o plugin não declara uma pasta `skills/`:

```text
/plugin marketplace add Blackspirits/humanizer-pt-pt
/plugin install humanizer-pt-pt@humanizer-pt-pt
```

Invocação prevista:

```text
/humanizer-pt-pt:humanizer-pt-pt
```

### Instalação manual

Copia a pasta completa `humanizer-pt-pt` para a pasta de skills do agente. Não copies apenas `SKILL.md`: os padrões, princípios de composição, regras por formato e mapas terminológicos vivem em ficheiros de apoio.

## Utilização

### Automático

```text
Revê este texto com a skill humanizer-pt-pt:

[texto]
```

### Auditoria sem alterações

```text
MODO: AUDITAR

Analisa este texto, identifica padrões problemáticos e não o reescrevas:

[texto]
```

### Humanização profunda

```text
MODO: HUMANIZAR

Reescreve em pt-PT, preservando todos os factos:

[texto]
```

### Revisão mínima

```text
MODO: QA HUMANO

Corrige apenas problemas reais. Mantém a minha voz:

[texto]
```

### Clonagem de voz

```text
MODO: CLONAR VOZ

Amostras minhas:
[duas ou três amostras]

Texto a rever:
[texto]
```

## Arquitetura editorial

A skill usa divulgação progressiva:

- `SKILL.md`: princípios, modos, fluxo e política de saída;
- `references/patterns.md`: catálogo dos 36 padrões;
- `references/composition.md`: construção da versão final sem invenções;
- `references/formats.md`: regras para e-mail, documentação, UI, localização, sinopses, guiões e texto formal;
- `references/regional-variation.md`: preservação de variedades portuguesas legítimas;
- `vocabulary-map.json`: pt-BR, UI, tradução literal e notas contextuais;
- `profiles/blackspirits.md`: preferências opcionais do autor;
- `evals/`: corpus editorial e runner de respostas reais;
- `tests/`: testes unitários dos scripts do repositório.

## Decisões linguísticas

A skill usa pt-PT nacional neutro por defeito, sem impor uma variedade lisboeta. Quando o autor ou público estiver identificado, preserva regionalismos e oralidade legítimos.

Não aplica substituições cegas como:

- `fato` → `facto` sem analisar o sentido: em pt-PT, `facto` designa algo real ou ocorrido, enquanto `fato` designa vestuário;
- nomes próprios → grafia portuguesa: `Antônio Fato` permanece exatamente como foi escrito;
- `você` → `tu`, sem conhecer a relação entre interlocutores;
- `arquivo` → `ficheiro` quando designa um acervo, uma instituição ou documentação histórica; nesses sentidos, mantém-se `arquivo`;
- substituir `software livre` por `código aberto`: preserva `software livre` quando o original designa *free software*, o movimento, a FSF, o GNU ou as quatro liberdades; usa `código aberto` para *open source*;
- `release` → `versão` em nomes de releases, Scene/P2P, torrents, grupos de lançamento ou metadados multimédia;
- `boleto` → `referência Multibanco`, porque não são mecanismos equivalentes;
- substituir `acessar o sistema` por `aceder o sistema`: a adaptação correta é `aceder ao sistema`, com ajuste da regência.

## Auditoria

O modo AUDITAR descreve sinais observáveis. Cada ocorrência usa:

- ID e nome do padrão;
- excerto literal;
- gravidade `ligeira`, `clara` ou `grave`;
- motivo e direção de correção.

O nível geral é `limpo`, `ligeiro`, `moderado` ou `pesado`. Consulta [`examples/audit-report.md`](examples/audit-report.md).

## Avaliações e testes

Validar o pacote:

```bash
python scripts/validate-package.py
```

Executar os testes unitários:

```bash
python -m unittest discover -s tests -v
```

Gerar um modelo de respostas e avaliar um modelo:

```bash
python evals/score-results.py --template > responses.json
python evals/score-results.py responses.json
```

O runner verifica critérios objetivos, incluindo preservação literal, expressões proibidas, escolha AUTO e estrutura do modo AUDITAR. Voz, cadência e ausência de invenção subtil continuam sob revisão humana.

## Criar uma versão de lançamento

```bash
python scripts/package-release.py
```

O script valida o repositório, cria ZIP e TAR.GZ determinísticos com o mesmo conteúdo e gera `SHA256SUMS` em `dist/`.

## Estrutura

```text
humanizer-pt-pt/
├── SKILL.md
├── README.md
├── README.en.md
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE
├── NOTICE
├── vocabulary-map.json
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .github/workflows/validate.yml
├── references/
│   ├── patterns.md
│   ├── composition.md
│   ├── formats.md
│   └── regional-variation.md
├── profiles/
│   └── blackspirits.md
├── examples/
│   ├── audit-report.md
│   ├── before-after.md
│   └── terminology-overrides.json
├── evals/
│   ├── README.md
│   ├── cases.json
│   └── score-results.py
├── tests/
│   ├── test_package.py
│   └── test_score_results.py
└── scripts/
    ├── validate-package.py
    └── package-release.py
```

## Limites

- Não atribui autoria IA.
- Não garante resultados em classificadores.
- Não acrescenta gralhas deliberadas.
- Não substitui fact-checking.
- Não envia texto para serviços externos.
- Não transforma linguagem formal, técnica ou regional em “erro” apenas por não ser coloquial.

## Licença e atribuição

MIT. Consulta `LICENSE`, `NOTICE` e `CITATION.cff`.

## Contribuir

Consulta [`CONTRIBUTING.md`](CONTRIBUTING.md). Ao alterar uma regra, acrescenta pelo menos um caso de regressão relevante e confirma os falsos positivos.
