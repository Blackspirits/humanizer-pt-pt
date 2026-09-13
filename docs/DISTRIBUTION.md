# Modelo de Distribuição Pública

## Papel deste repositório

`Blackspirits/humanizer-pt-pt` é a distribuição pública do Humanizer pt-PT.

Uma release pública deve ser:
- autocontida;
- instalável sem acesso a infraestrutura privada;
- reproduzível e validável com os ficheiros publicados;
- construída por allowlist explícita;
- livre de segredos, corpus privado, fixtures sensíveis e material experimental.

## Desenvolvimento e publicação

O desenvolvimento canónico pode ocorrer num upstream privado. Esse upstream não é uma dependência do utilizador e não deve ser necessário para instalar, executar ou validar a release pública.

Fluxo esperado:

```text
upstream privado
    ↓ seleção explícita
    ↓ validação + evals + testes
    ↓ revisão do diff público
humanizer-pt-pt público
    ↓ tag/release
utilizadores
```

## Contrato de publicação

Cada publicação privado → público deve:

1. selecionar ficheiros por allowlist;
2. rejeitar ficheiros desconhecidos por predefinição;
3. excluir segredos, corpus, dados pessoais, logs, caches e experiências não aprovadas;
4. atualizar versões e `CHANGELOG.md` quando aplicável;
5. executar `scripts/validate-package.py`;
6. executar a suite de testes;
7. construir os arquivos determinísticos;
8. confirmar que o repositório público não introduz dependências privadas;
9. registar a versão/commit upstream no processo privado de release;
10. permitir rollback para a última release pública válida.

## Contribuições públicas

Issues e pull requests públicos podem servir como propostas, correções ou evidência. A aceitação conceptual não obriga a desenvolver diretamente neste repositório: mantenedores podem reproduzir e validar a alteração no upstream canónico e publicá-la posteriormente como parte de uma release revista.

O estado publicado neste repositório continua, contudo, a ser a fonte de verdade para o comportamento que os utilizadores efetivamente instalam.

## Não fazer

- não importar automaticamente todo o upstream privado;
- não sincronizar ficheiros desconhecidos;
- não incluir links necessários para repositórios privados;
- não exigir autenticação privada em CI ou runtime público;
- não editar independentemente as mesmas regras em dois repositórios sem um fluxo explícito de publicação.
