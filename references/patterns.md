# Padrões a detetar e corrigir

Referência dos 36 padrões da skill humanizer-pt-pt. Consulta este ficheiro quando estiveres a rever ou reescrever texto e precisares dos sinais concretos, exemplos antes/depois e correções de cada padrão.

Procura **combinações** de sinais, não palavras isoladas. Uma única ocorrência raramente prova alguma coisa (ver "Falsos positivos" na SKILL.md).

---


## Conteúdo

### 1. Importância inflacionada

**Sinais:** “momento crucial”, “papel fundamental”, “marco incontornável”, “mudança de paradigma”, “deixou uma marca indelével”, “reflete uma tendência mais ampla”.

**Problema:** acrescenta importância sem explicar o efeito concreto.

**Antes:**
> Esta atualização reduz o tempo de carregamento e acrescenta pesquisa por filtros, representando um marco crucial na evolução da plataforma.

**Depois:**
> A atualização reduz o tempo de carregamento e acrescenta pesquisa por filtros.

Se o original não indicar efeitos concretos, corta a afirmação inflacionada em vez de inventar resultados.

### 2. Linguagem promocional sem base

**Sinais:** “experiência inesquecível”, “solução revolucionária”, “destino imperdível”, “qualidade excecional”, “interface deslumbrante”, “tecnologia de ponta”.

**Problema:** apresenta opinião publicitária como descrição factual.

**Antes:**
> Situada no centro da região e servida por comboio, esta vila vibrante oferece uma experiência inesquecível.

**Depois:**
> A vila fica no centro da região e é servida por comboio.

### 3. Atribuições vagas e notoriedade por associação

**Sinais:** “os especialistas afirmam”, “segundo vários estudos”, “observadores consideram”, “há quem defenda”, sem fonte ou contexto; listas de órgãos de comunicação, prémios, seguidores ou menções usadas como prova automática de importância.

**Problema:** usa uma autoridade indistinta ou uma associação mediática para sustentar uma afirmação sem explicar o que a fonte demonstrou.

**Antes:**
> O projeto foi mencionado no Jornal A e no Jornal B, demonstrando a sua relevância incontornável no setor.

**Depois:**
> O projeto foi mencionado no Jornal A e no Jornal B.

**Correção:** identifica a fonte real e o conteúdo relevante quando tiverem sido fornecidos. Caso contrário, preserva apenas o facto verificável, apresenta a afirmação como opinião do autor ou remove-a. Não inventes uma citação concreta para substituir uma atribuição vaga.

### 4. Análise superficial acrescentada por gerúndio

**Sinais:** finais com “demonstrando”, “reforçando”, “evidenciando”, “garantindo”, “promovendo”, “contribuindo”, “simbolizando”.

**Antes:**
> O serviço passou a aceitar pagamentos móveis, demonstrando o seu compromisso com a modernização e promovendo uma experiência mais fluida.

**Depois:**
> O serviço passou a aceitar pagamentos móveis.

Mantém a consequência apenas quando estiver sustentada pelo texto.

### 5. Secções formulaicas de desafios e futuro

**Sinais:** “Apesar dos desafios”, “Perspetivas futuras”, “Caminho a seguir”, seguidos de generalidades otimistas.

**Antes:**
> Apesar dos atrasos frequentes nas entregas, a empresa continua bem posicionada para prosperar num futuro cada vez mais digital.

**Depois:**
> A empresa tem atrasos frequentes nas entregas.

Remove a projeção otimista quando não estiver sustentada, mas preserva todos os factos concretos presentes no original.

### 6. Contextualização genérica

**Sinais:** “No mundo atual”, “Numa era marcada por”, “No panorama digital”, “À medida que a tecnologia continua a evoluir”.

**Correção:** começa no facto, problema ou decisão que interessa ao leitor.

## Vocabulário e sintaxe

### 7. Vocabulário típico de IA

Vigia sobretudo acumulações de palavras como:

- crucial, fundamental, essencial, robusto, inovador, transformador;
- panorama, cenário, ecossistema, jornada, sinergia, paradigma;
- potenciar, alavancar, impulsionar, otimizar, maximizar;
- destacar, sublinhar, evidenciar, demonstrar, proporcionar;
- abrangente, holístico, multifacetado, intrincado, dinâmico;
- mergulhar, desvendar, desbloquear, navegar.

Não são palavras proibidas. Mantém-nas quando forem a escolha mais exata. Corrige o uso repetido, abstrato ou ornamental.

**Manter quando:** «Este requisito é fundamental para o cálculo» usa *fundamental* com sentido técnico preciso; «O método é robusto a valores extremos» descreve uma propriedade verificável, não um elogio.

### 8. Evitar verbos simples

**Sinais:** “serve como”, “apresenta-se como”, “assume-se como”, “constitui-se como”, “posiciona-se como”, “oferece a possibilidade de”, quando “é”, “tem”, “permite” ou um verbo concreto resolvem.

**Antes:**
> A aplicação apresenta-se como uma solução que oferece a possibilidade de gerir ficheiros.

**Depois:**
> A aplicação permite gerir ficheiros.

### 9. Paralelismos negativos

**Sinais:** “não é apenas X, é Y”, “não se trata só de X”, “não só X, mas também Y”, repetidos como recurso dramático.

**Antes:**
> Não é apenas uma atualização. É uma nova forma de trabalhar.

**Depois:**
> A atualização muda a forma de trabalhar.

### 10. Regra de três forçada

**Sinais:** grupos constantes de três adjetivos, benefícios ou conceitos sem necessidade real.

**Antes:**
> A solução reduz o número de passos necessários, tornando o processo simples, intuitivo e eficiente.

**Depois:**
> A solução reduz o número de passos necessários para concluir a tarefa.

Usa dois, três ou mais elementos quando o conteúdo o exigir. Não forces simetria.

### 11. Rotação artificial de sinónimos

**Problema:** muda de termo apenas para evitar repetição, prejudicando consistência.

**Antes:**
> O utilizador abre a aplicação. A pessoa escolhe um ficheiro. O indivíduo confirma a operação.

**Depois:**
> O utilizador abre a aplicação, escolhe um ficheiro e confirma a operação.

Em texto técnico, repetir o termo correto é melhor do que variar.

### 12. Intervalos falsos

**Sinais:** “desde X até Y”, “de X a Y”, quando os elementos não formam uma escala ou percurso coerente.

**Antes:**
> O guia aborda tudo, desde autenticação até design e produtividade.

**Depois:**
> O guia aborda autenticação, design e produtividade.

### 13. Voz passiva ou sujeito escondido

**Antes:**
> Os dados são guardados automaticamente e os erros são apresentados no ecrã.

**Depois:**
> Os dados ficam guardados automaticamente e os erros aparecem no ecrã.

Não elimines a passiva quando o agente for desconhecido, irrelevante ou deliberadamente omitido em texto formal.

### 14. Conectores em excesso

**Sinais:** “além disso”, “por outro lado”, “nesse sentido”, “deste modo”, “por conseguinte”, “por fim” em quase todos os parágrafos.

**Correção:** remove o conector quando a relação já for evidente. Usa-o apenas quando orientar realmente a leitura.

**Manter quando:** «Além disso» pode ficar uma vez quando introduzir informação verdadeiramente adicional e a ligação não for evidente sem o conector.

### 15. Tradução literal do inglês

Vigia construções como:

- “endereçar um problema” → resolver, tratar ou abordar;
- “suportar um formato” → ser compatível com, aceitar;
- “aplicar para uma vaga” → candidatar-se;
- “fazer sentido para” → ser adequado a, compensar para;
- “experienciar um erro” → encontrar, ter, ocorrer;
- “eventualmente” com sentido de *eventually* → por fim, mais tarde;
- “assumir” com sentido de presumir, quando ambíguo;
- “realizar que” → perceber que;
- “baseado em” quando “com base em” for mais natural;
- ordem de palavras e possessivos copiados do inglês.

Não traduzas termos técnicos estabelecidos só para evitar anglicismos.

### 16. Infiltração de pt-BR

Corrige conforme o contexto:

- usuário → utilizador;
- aplicativo → aplicação;
- arquivo informático → ficheiro;
- salvar → guardar;
- baixar → transferir ou descarregar;
- tela → ecrã;
- celular → telemóvel;
- equipe → equipa;
- senha → palavra-passe;
- banco de dados → base de dados;
- gerenciar → gerir;
- compartilhar → partilhar;
- excluir → eliminar ou apagar;
- cadastro → registo, inscrição ou criação de conta, conforme o fluxo;
- acessar o sistema → aceder ao sistema (ajusta também a regência);
- trem → comboio;
- ônibus → autocarro;
- pedágio → portagem;
- café da manhã → pequeno-almoço.

Não alteres palavras válidas nas duas variantes quando o contexto não o justificar. Nunca mudes nomes próprios por causa da ortografia.

### 17. Gerúndio progressivo brasileiro

**Antes:**
> Estamos analisando o problema e vamos enviando atualizações.

**Depois:**
> Estamos a analisar o problema e enviaremos atualizações.

Em descrições de comportamento, prefere muitas vezes o presente simples:

> O painel está a mostrar os resultados. → O painel mostra os resultados.

### 18. Colocação dos pronomes

Corrige pt-BR como:

- “me avise” → avise-me;
- “se registre” → registe-se;
- “me envie” → envie-me;
- “te mando depois” → mando-te depois.

Mantém próclise quando existe um elemento que a exige ou favorece:

- não se esqueça;
- quando me disser;
- quem se registou;
- já lhe enviei.

Evita aplicar regras mecânicas sem considerar a frase completa.

### 19. Tratamento e sujeito repetidos

O uso insistente de “você” tende a soar brasileiro ou distante em pt-PT.

- documentação: usa imperativo, infinitivo ou construção impessoal;
- mensagens informais: usa “tu” apenas quando a relação já o permitir;
- texto público: mantém tratamento consistente;
- plural: “vocês” é válido, mas não precisa de aparecer em todas as frases.

### 20. Artigos, contrações e possessivos

Vigia:

- “acesse sua conta” → aceda à sua conta;
- “verifique seus ficheiros” → verifique os seus ficheiros;
- “em um” → num, quando natural;
- “de este” → deste;
- “em este” → neste;
- “para mim fazer” → para eu fazer.

Não forces artigos quando a expressão idiomática ou o estilo os dispensa.

### 21. Nominalizações e linguagem burocrática

**Antes → depois:**

- proceder à implementação → implementar;
- efetuar a configuração → configurar;
- realizar a validação → validar;
- dar início ao processo → começar;
- proceder à análise → analisar;
- efetuar o envio → enviar;
- com vista a / no sentido de → para.

Mantém a formulação formal em contratos, legislação ou documentos onde a precisão institucional a exija.

## Estilo e formatação

### 22. Travessões usados como assinatura de estilo

O travessão é válido em português. Não o proíbas. Corrige apenas quando aparece repetidamente para fabricar ritmo, interromper todas as frases ou substituir pontuação mais clara.

A amostra do autor decide a frequência aceitável.

### 23. Negrito mecânico

Evita destacar palavras em todas as linhas ou transformar cada conceito num rótulo visual. Usa negrito para orientar leitura, não para simular importância.

### 24. Listas com cabeçalhos em todas as linhas

**Antes:**
> - **Desempenho:** O tempo de carregamento passou de quatro para dois segundos.
> - **Segurança:** Foi acrescentada autenticação de dois fatores.

**Depois:**
> O tempo de carregamento passou de quatro para dois segundos e foi acrescentada autenticação de dois fatores.

Mantém listas quando houver passos, opções ou itens que o leitor precise de consultar rapidamente.

### 25. Títulos genéricos ou capitalização importada

Vigia:

- secções como “Introdução”, “Principais benefícios”, “Desafios” e “Conclusão” quando apenas reproduzem um molde;
- *Title Case* importado do inglês, com maiúscula em quase todas as palavras: “Estratégia De Crescimento E Parcerias Globais”.

**Correção:** usa títulos informativos e capitalização portuguesa: “Estratégia de crescimento e parcerias globais”. Preserva títulos oficiais, marcas e o guia editorial do projeto.

### 26. Emojis decorativos

Não acrescentes emojis automaticamente em títulos, listas ou chamadas à ação. Mantém os fornecidos pelo autor quando forem adequados ao canal.

### 27. Parágrafos com estrutura demasiado regular

Sinais:

- todos têm extensão semelhante;
- começam com o mesmo tipo de frase;
- terminam sempre numa conclusão limpa;
- cada secção tem exatamente três pontos.

Varia apenas quando o conteúdo pedir. Não introduzas caos artificial.

### 28. Frases curtas e ganchos encadeados para criar drama

**Sinais:** sequências de frases mínimas e anúncios como “É aqui que tudo muda”, “E isso muda tudo”, “Mas eis o que ninguém conta”, “Foi aí que percebi” ou “Porque é que isto importa?”, quando apenas encenam uma revelação.

**Antes:**
> A mudança chegou. Sem aviso. Sem preparação. E é aqui que tudo muda.

**Depois:**
> A mudança foi aplicada sem aviso nem preparação.

Uma frase curta ou uma pergunta pode dar ênfase. Corrige apenas a acumulação ou o suspense sem conteúdo; preserva ganchos que tenham função narrativa real.

### 29. Aforismos fabricados

**Sinais:** “X é a linguagem de Y”, “X é a moeda de Y”, “não é uma ferramenta, é um espelho”, “a simplicidade torna-se uma armadilha”.

**Correção:** substitui a frase memorável pela afirmação concreta que ela tenta disfarçar.

## Comunicação

### 30. Artefactos de chatbot

Remove do texto final expressões como:

- “Claro!”;
- “Excelente pergunta!”;
- “Espero que isto ajude”;
- “Diga se quiser que continue”;
- “Aqui está uma versão melhorada”;
- “Como modelo de linguagem”.

Mantém cortesias reais em e-mails e mensagens quando fizerem parte do género textual.

### 31. Tom servil ou elogio automático

**Antes:**
> Tem toda a razão: a sua observação sobre os custos altera a recomendação e é muito importante.

**Depois:**
> A observação sobre os custos altera a recomendação.

Discorda com clareza quando os factos o justificarem.

### 32. Falsas experiências pessoais

Nunca escrevas “na minha experiência”, “já reparei”, “quando visitei” ou “lembro-me” sem uma experiência fornecida pelo autor.

Para dar perspetiva sem fingir vivências, usa observações explícitas:

> Na prática, este fluxo obriga o utilizador a repetir o mesmo passo.

### 33. Anúncios do que vem a seguir

**Sinais:** “Vamos explorar”, “Vejamos agora”, “Eis o que precisa de saber”, “Sem mais demoras”, “Vamos analisar ponto por ponto”, “E é exatamente aí que entra X”.

Começa pela análise ou pelo conteúdo. Mantém orientação explícita quando o leitor precisar de saber a sequência, como num tutorial, apresentação ou guião.

## Enchimento e conclusão

### 34. Expressões longas sem função

**Antes → depois:**

- tendo em consideração o facto de que → porque;
- com o objetivo de → para;
- no momento atual → agora;
- no caso de ser necessário → se for necessário;
- tem a capacidade de → consegue;
- importa salientar que → [começar diretamente pela afirmação].

### 35. Hesitação excessiva ou falsa certeza

Reduz combinações como “poderá eventualmente talvez”. Usa uma modalidade proporcional às provas:

- facto confirmado: afirma diretamente;
- inferência razoável: “sugere”, “parece”, “provavelmente”;
- informação insuficiente: declara o que não se sabe;
- opinião: identifica-a como tal.

Não uses hesitação apenas para parecer humano.

### 36. Conclusões genéricas

Corta finais como:

- “O futuro parece promissor”;
- “Só o tempo dirá”;
- “Esta é uma jornada que está apenas a começar”;
- “Em última análise, tudo dependerá da capacidade de adaptação”.

Termina no último facto útil, decisão, consequência ou próximo passo concreto.

