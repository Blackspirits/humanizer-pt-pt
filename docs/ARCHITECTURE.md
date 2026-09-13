# Arquitetura do Humanizer pt-PT

## Princípio

O runtime principal é o **modelo/agente que executa a skill**. Este repositório público contém tudo o que uma release necessita para executar, validar, testar e documentar o comportamento publicado.

```text
MODELO / AGENTE
      ↓ executa
SKILL.md
      ↓ consulta
COMPORTAMENTO + REFERÊNCIAS VERSIONADAS
      ↓ verificado por
EVALS / REGRESSÕES / CONTRATOS
```

Não existe dependência runtime de repositórios ou serviços privados.

## Camadas

### 1. Behavior contract

`SKILL.md` possui modos, política de intervenção, preservação de factos/voz, escolha AUTO, política de saída e UX.

### 2. Editorial behavior

`references/composition.md`, `references/formats.md`, `references/intervention.md` e os padrões específicos definem **quando e quanto intervir**.

### 3. Conhecimento linguístico aplicado

`vocabulary-map.json`, referências e exemplos contêm apenas o conhecimento necessário à release publicada.

Esse conteúdo:
- é versionado com a release;
- deve ser contextual e protegido contra falsos positivos;
- não transforma o Humanizer numa autoridade universal sobre português europeu;
- não pode exigir acesso a fontes privadas em runtime.

A manutenção pode investigar e validar claims noutros ambientes. Só conteúdo revisto, selecionado e explicitamente publicado passa a fazer parte desta camada.

### 4. Contracts

`contracts/` descreve interfaces de output/eval para permitir validação sem depender de detalhes internos do tooling.

### 5. Evals

`evals/` mede comportamento observável: preservação, falsos positivos, seleção de modo, AUDITAR, regressões contextuais e constraints verificáveis.

Evals provam comportamento da release dentro da cobertura existente; não demonstram correção linguística universal.

### 6. Support tooling

Python em `scripts/`, `evals/` e `humanizer_support/` serve para validar o pacote, pontuar evals, verificar contratos e criar releases determinísticas. Não é um motor linguístico separado.

## Distribuição

O repositório público é downstream de distribuição e deve continuar instalável diretamente.

```text
investigação / desenvolvimento
          ↓ revisão + testes
conteúdo aprovado para release
          ↓ publicação por allowlist
Blackspirits/humanizer-pt-pt (público)
          ↓
instalação pelos utilizadores
```

A publicação deve preservar versão, changelog, testes e proveniência suficiente da release, sem copiar corpus privado, segredos, fixtures sensíveis ou material experimental.

Ver `docs/DISTRIBUTION.md`.

## Evolução

Mudanças de comportamento exigem evals/regressões. Mudanças linguísticas aplicadas devem ser justificadas por evidência e testadas contra falsos positivos antes de entrar na release pública.

## Relação com blader/humanizer

`blader/humanizer` foi uma inspiração inicial para padrões de escrita artificial e formato de skill. Não é upstream arquitetural obrigatório.

A linha 1.x evolui segundo necessidades reais de pt-PT, evals/regressões próprios e requisitos dos runtimes suportados.