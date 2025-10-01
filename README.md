# IA para Apita Cidadão

Este módulo integra recursos de Inteligência Artificial ao Apita Cidadão, oferecendo funcionalidades para processamento automático de denúncias, classificação inicial (filtro de spam / irrelevante), suporte a busca e respostas fundamentadas (RAG) e clusterização de denúncias.

> Objetivo principal: prover uma **camada inteligente** que limpa, organiza, prioriza e contextualiza denúncias, permitindo que os administradores atuem de forma mais rápida e estratégica na identificação de padrões de manipulação no esporte.

---

## Visão geral (o que temos até o momento)

Principais componentes em planejamento:

- **Filtra o ruído** (spam, conteúdo irrelevante).

- **Agrupa denúncias similares** para identificar tendências e focos de atividade (macro e micro áreas).

- **Contextualiza as denúncias**, permitindo buscas em linguagem natural contra uma base de conhecimento (leis, normas, relatórios).

---

## Diagramas da Arquitetura (visualizações)

Toda a modelagem visual e os fluxos de dados da arquitetura de IA estão centralizados em `docs/diagramas/`.  
Lá você encontra diagramas prontos para apresentação e para revisão técnica com a PF, incluindo:

- **Fluxo de Dados Geral** — visão de ponta a ponta do processamento de denúncias.  

- **Pipeline de Pré-processamento** — validação, detecção/anonimização de PII, tradução e preparação.

- **Fluxo de Classificação** — gate por palavras-chave, classificador e fallback humano.

- **RAG Flow** — retrieval → prompt → LLM → resposta fundamentada.

- **Pipeline de Clusterização** — descoberta de macro e micro temas e geração de alertas.

- **Privacidade & Retenção** — regras de anonimização e ciclo de vida dos dados.

Veja a documentação visual em: [`docs/diagramas/README.md`](docs/diagramas/README.md).

> **Nota:** os fontes (Mermaid `.mmd` / `.mermaid`) e as imagens exportadas (PNG) estão em `docs/diagramas/`. Ao alterar qualquer diagrama, mantenha tanto a fonte quanto a imagem atualizadas.

---

## Funcionalidades Principais

**1. Classificação e Filtragem**

- **O que faz?** Atua como um "portão de entrada", separando denúncias legítimas de spam ou conteúdo irrelevante.

- **Como?** Utiliza uma abordagem em duas etapas: um filtro rápido por palavras-chave, seguido por um modelo de classificação treinado com embeddings.

Dessa forma, **reduz a carga de trabalho manual**, garantindo que **apenas informações pertinentes avancem** para análises mais complexas.

**2. Busca e Geração de Respostas (RAG)**

- **O que faz?** Permite que um analista "converse" com os documentos, fazendo perguntas em linguagem natural e recebendo respostas fundamentadas.

- **Como?** Integra o RAG Flow com o Google Gemini Pro. As denúncias relevantes e os documentos de apoio (leis, notícias) são vetorizados e armazenados, permitindo uma busca semântica para gerar respostas contextuais.

Assim, ajudando ao acelerar a investigação, contextualizando denúncias e ajudando a conectar eventos que, de outra forma, pareceriam isolados.

**3. Clusterização e Descoberta de Padrões**

- **O que faz?** Agrupa denúncias textualmente similares de forma não supervisionada para descobrir "macro" e "micro" áreas de atividade suspeita.

- **Como?**
    1. As denúncias relevantes são transformadas em vetores (embeddings).

    2. Algoritmos de clusterização são aplicados para agrupar esses vetores.

    3. Os clusters resultantes são analisados para extrair temas comuns (ex: um tipo específico de manipulação, uma região, um grupo de pessoas).

Portanto, em vez de analisar caso a caso, este módulo deverá permitir identificar surtos de denúncias sobre um mesmo tema, indicando uma operação coordenada ou um problema sistêmico.

Onde um cluster (agrupamento de denúncias similares) que cresce rapidamente ou que tem alta densidade geográfica pode ser priorizado para o direcionamento do planejamento de operações e identificação de novas frentes de investigação.

## Boas Práticas de Contribuição

Siga o nosso [GUIA DE CONTRIBUIÇÃO](CONTRIBUTING.md). Ele define nosso fluxo de trabalho, padrão de commits semânticos e template de Pull Request.
