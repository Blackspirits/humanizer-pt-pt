# Variação regional em pt-PT

Consulta este ficheiro quando o texto tiver regionalismos, oralidade, fala transcrita ou um público regional identificado.

## Princípio

O objetivo não é impor um português "central" nem catalogar termos por região. É **não apagar variedades portuguesas legítimas**. Um humanizer que uniformiza toda a fala para um pt-PT neutro de Lisboa comete o mesmo erro que quer corrigir: remove voz.

## Regras

1. **Sem contexto regional, usa pt-PT neutro.** É a predefinição segura para documentação, UI e texto público sem autor identificado.
2. **Preserva o regionalismo legítimo do autor.** Se o autor escreve numa variedade própria (Norte, Centro, Sul, Açores, Madeira) e essa variedade é coerente, mantém-na. Não a "corrijas" para a forma da capital.
3. **Nunca substituas uma forma portuguesa legítima por outra apenas por parecer mais central ou formal.** Preserva escolhas lexicais, sintáticas e de oralidade coerentes com o autor, salvo quando prejudicarem a compreensão do público-alvo.
4. **Adapta-te ao público regional apenas quando estiver identificado.** Se o projeto declara um público-alvo regional, alinha o registo; caso contrário, não presumas.

## O que NÃO fazer

- Não cries listas de "termos do Norte" vs "termos de Lisboa" para substituição automática. Gera estereótipos e falsos positivos.
- Não marques oralidade ou coloquialismo como "erro" em texto que é deliberadamente falado ou informal.
- Não confundas regionalismo com pt-BR. A origem regional de uma forma não a torna incorreta nem brasileira.

## Fronteira com pt-BR

A deteção de pt-BR (ver `vocabulary-map.json`) é ortogonal à variação regional portuguesa. Corrige pt-BR quando o texto se destina a Portugal; preserva a variedade portuguesa do autor seja ela qual for.
