# Chatbot Apita Cidadão (Grupo 28 e 13)

O projeto implementa um Assistente Jurídico utilizando arquitetura RAG (Retrieval-Augmented Generation) avançada, orquestrada via LangGraph.

**Nota:** Os códigos presentes nas pastas de `backend` e `frontend` servem como uma prova de conceito (PoC) para demonstrar o funcionamento do fluxo conversacional e da recuperação de documentos. O objetivo final é a integração da lógica deste agente (grafo e nós) à infraestrutura existente da plataforma.

## Arquitetura do Agente

O fluxo de controle é definido por um grafo de estados (StateGraph):

1.  **Router:** Classifica a entrada do usuário entre "Conversa Geral" e "Consulta Jurídica".
2.  **Retrieve:** Realiza a busca inicial de documentos no PostgreSQL (pgvector).
3.  **Rerank:** Reordena os documentos recuperados utilizando um modelo Cross-Encoder para priorizar a relevância semântica.
4.  **Decisão (Edge):** Avalia se, após o reranking, os documentos são suficientes.
    * Se insuficientes (e dentro do limite de loops), aciona **Transform Query** (Self-Correction).
    * Se suficientes, segue para **Generate**.
5.  **Generate:** Produz a resposta final utilizando o contexto validado.

## Ambientes de Validação

O sistema foi validado em dois cenários de infraestrutura distintos:

### Cenário 1: Desktop
* **Modelo Conversacional:** `gpt-oss:20b`
* **Embeddings:** `mxbai-embed-large`
* **Reranking:** `BAAI/bge-reranker-base`

### Cenário 2: Servidor de Alta Performance (GPU A100)
* **Modelo Conversacional:** `deepseek-r1:70b` (Reasoning Model)
* **Embeddings:** `Q78KG/gte-Qwen2-7B-instruct` (State-of-the-Art)
* **Reranking:** `BAAI/bge-reranker-base`

## Stack Tecnológica

* **Linguagem:** Python 3.11+.
* **Orquestração:** LangChain, LangGraph.
* **Banco de Dados:** PostgreSQL com extensão `vector`.
* **Driver:** `psycopg` (v3, AsyncIO).
* **Inferência Local:** Ollama (para LLMs e Embeddings).
* **API:** FastAPI (Exemplo de implementação).

## Pré-requisitos e Adaptação de Infraestrutura

Para executar o projeto localmente conforme configurado nos testes, é necessário:
1.  Python 3.10+.
2.  PostgreSQL com a extensão **[pgvector](https://github.com/pgvector/pgvector)** instalada no sistema operacional.
3.  Hardware suficiente para rodar os modelos citados via Ollama (Recomendado GPU com VRAM adequada ao tamanho do modelo escolhido).

### ⚠️ Uso de APIs de Terceiros
Caso não haja infraestrutura local (GPU) capaz de executar modelos de conversação pesados (como Llama 3 ou DeepSeek) ou gerar embeddings e reranking localmente, **é necessário alterar os arquivos `settings.py` e `nodes.py`**.

Substitua as implementações locais (`ChatOllama`, `OllamaEmbeddings`) por APIs gerenciadas:
* **LLM:** OpenAI (`ChatOpenAI`), Anthropic (`ChatAnthropic`) ou Google (`ChatVertexAI`).
* **Embeddings:** OpenAI (`OpenAIEmbeddings`) ou Google.
* **Reranker:** Cohere Rerank ou serviços similares.

## Configuração

### 1. Banco de Dados
O comando SQL abaixo ativa a extensão, mas requer que os binários do `pgvector` já estejam instalados na máquina host do banco de dados (consulte a [documentação oficial](https://github.com/pgvector/pgvector#installation) para instalação no Linux/Windows/Docker).

No banco de dados alvo:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Configuração do Backend

Clone o repositório e instale as dependências:

```Bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copie o arquivo .env.example na raiz do backend para .env. Exemplo de configuração:

```Ini, TOML
DB_CONNECTION=postgresql+psycopg://usuario:senha@localhost:5432/apita_db

# Modelos (Ajuste conforme o ambiente: Desktop ou Server)
LLM_MODEL_NAME=gpt-oss:20b
EMBEDDING_MODEL_NAME=mxbai-embed-large
OLLAMA_API_URL=http://localhost:11434
```

### 3. Ingestão de Dados

Execute o pipeline para popular o banco de dados:

```Bash
python indexing_pipeline.py
```

**Nota sobre a Base de Conhecimento**: O script de exemplo (indexing_pipeline.py) implementa um processo ETL simplificado que indexa apenas 5 normas federais específicas para fins de demonstração. Em um cenário de produção, é mandatório escalar este pipeline para ingerir um volume abrangente de legislação, garantindo que o agente de IA tenha respaldo jurídico suficiente para cobrir todos os tópicos esperados pela plataforma.

## Execução

### API (Backend)

```Bash
uvicorn main:app --reload --port 8000
```

### Interface (Frontend Exemplo)

```Bash
cd frontend
npm install
npm run dev
```