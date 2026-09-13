# Changelog

## 1.1.0 - 2026-09-13

### Segurança de intervenção

- Adicionada política normativa de precedência e orçamento de intervenção em `references/intervention.md`.
- O fluxo da skill passa a identificar âncoras semânticas antes da reescrita e a rever negação, modalidade, quantidades, datas, causalidade e relações temporais.
- Adicionados guards determinísticos para números, percentagens, datas, moedas, versões, URLs, e-mails, paths, código inline e citações.
- O runner de evals suporta `preserve_semantic_anchors`, exceções explícitas e `max_change_ratio`.
- Adicionados casos negativos de over-editing e regressões de preservação semântica.
- Mantida a fronteira: estes guards testam o comportamento do Humanizer; verdade linguística genérica continua no PT-PT Language Intelligence.

## 1.0.1 - 2026-09-13

### Arquitetura e tooling

- Documentada a arquitetura própria do Humanizer: modelo/agente como runtime, `SKILL.md` como contrato de comportamento, Language Intelligence como autoridade linguística genérica e Python apenas como tooling de suporte.
- Adicionados contratos JSON para respostas de reescrita, AUDITAR e corpus de evals.
- Versão da release passou a ser derivada da própria skill; removido o hardcode `EXPECTED_VERSION = 1.0.0`.
- IDs válidos de padrões passam a ser derivados de `references/patterns.md`; o tooling deixou de congelar o limite 36.
- Empacotamento de release passou de inclusão implícita de todo o repo para allowlist explícita.
- Criado `humanizer_support/` para lógica partilhada entre validação, evals e release.
- Mantido o comportamento editorial da 1.0.0; esta patch melhora a fundação de engenharia e a capacidade de evolução segura.

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
- Mapeamentos polissémicos de opção única, como `salvar`, `senha`, `controle`, `equipe` e `registro`, também exigem notas contextuais.
- Exemplos revistos para não inventarem nem perderem métricas, fontes, funcionalidades, experiências ou consequências.
- AUDITAR descreve padrões observáveis sem atribuir autoria ou percentagens de IA.

### Avaliação e ferramentas

- Corpus com 46 avaliações, incluindo AUTO, auditoria, falsos positivos, nomes próprios, citações, UI, oralidade, *Title Case*, notoriedade mediática, ganchos dramáticos e desambiguação de `roteiro` (guião vs itinerário).
- Runner de evals com relatórios JSON, seleção por caso, validação de excertos e controlo de afirmações de origem IA. A comparação preserva diacríticos para não confundir formas como `a` e `à`; riscos de invenção são apresentados explicitamente para revisão manual.
- Dezasseis testes unitários para o runner, validador, empacotamento e ausência de brasileirismos na documentação.
- `roteiro` corrigido para `guião` em toda a documentação e no validador; mapeamento contextual `roteiro` → guião/plano/itinerário no mapa terminológico.
- Validador sem dependências para estrutura, versões, referências, manifests, vocabulário, documentação e CI.
- Empacotamento determinístico em ZIP e TAR.GZ, verificação de paridade e checksums SHA-256.

### Integração

- Compatibilidade com Agent Skills e com o esquema de plugin de skill única do Claude Code.
- Manifests para plugin e marketplace do Claude Code.
- CI com Python 3.12, testes unitários, empacotamento, Skills CLI e validação do plugin.
- Documentação em pt-PT e inglês, guia de contribuição, instruções para agentes e metadados de citação.
