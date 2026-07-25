# Changelog

## 1.0.0 - 2026-07-25

Primeira versão pública.

### Núcleo editorial

- Cinco modos: AUTO, AUDITAR, HUMANIZAR, QA HUMANO e CLONAR VOZ.
- 36 padrões adaptados ao português europeu.
- Princípios de composição próprios para pt-PT, com prioridade absoluta à exatidão e à não invenção.
- Regras específicas para e-mail, documentação, commits/PRs, UI, localização, sinopses, guiões, conteúdo editorial e texto formal.
- Preservação de variedades portuguesas legítimas sem centralização regional.

### Segurança editorial

- Proteção de factos, nomes próprios, citações, comandos, caminhos, URLs, identificadores e títulos oficiais.
- Mapa pt-BR → pt-PT dependente do contexto, sem substituições cegas.
- Tratamento explícito de casos ambíguos como `fato`, `arquivo`, `você`, `software livre`, `release`, `time` e `boleto`.
- Distinção contextual reforçada para `fato`/`facto`, nomes próprios e `release` em Scene/P2P, torrents e metadados multimédia.
- Regência protegida em adaptações como `acessar o sistema` → `aceder ao sistema`, com contrações corretas.
- Critérios explícitos para `cadastrar`/`cadastro` e para a distinção conceptual entre `open source` e `free software`.
- Todos os mapeamentos com várias alternativas exigem uma nota contextual; o validador impede opções sem critério de desempate.
- Exemplos revistos para não inventarem nem perderem métricas, fontes, funcionalidades, experiências ou consequências.
- AUDITAR descreve padrões observáveis sem atribuir autoria ou percentagens de IA.

### Avaliação e ferramentas

- Corpus com 45 avaliações, incluindo AUTO, auditoria, falsos positivos, nomes próprios, citações, UI, oralidade, *Title Case*, notoriedade mediática, ganchos dramáticos e desambiguação de `roteiro` (guião vs itinerário).
- Runner de evals com relatórios JSON, seleção por caso, validação de excertos e controlo de afirmações de origem IA. A comparação preserva diacríticos para não confundir formas como `a` e `à`; riscos de invenção são apresentados explicitamente para revisão manual.
- Quinze testes unitários para o runner, validador, empacotamento e ausência de brasileirismos na documentação.
- `roteiro` corrigido para `guião` em toda a documentação e no validador; mapeamento contextual `roteiro` → guião/plano/itinerário no mapa terminológico.
- Validador sem dependências para estrutura, versões, referências, manifests, vocabulário, documentação e CI.
- Empacotamento determinístico em ZIP e TAR.GZ, verificação de paridade e checksums SHA-256.

### Integração

- Compatibilidade com Agent Skills e com o esquema de plugin de skill única do Claude Code.
- Manifests para plugin e marketplace do Claude Code.
- CI com Python 3.12, testes unitários, empacotamento, Skills CLI e validação do plugin.
- Documentação em pt-PT e inglês, guia de contribuição, instruções para agentes e metadados de citação.
