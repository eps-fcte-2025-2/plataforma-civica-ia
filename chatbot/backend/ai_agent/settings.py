import os

from sqlalchemy.ext.asyncio import create_async_engine
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_postgres import PGVector

DB_CONNECTION = os.getenv("DB_CONNECTION")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "legal_docs")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "llama3")
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME", "llama3")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

engine = create_async_engine(DB_CONNECTION)


def get_embeddings():
    return OllamaEmbeddings(model=EMBEDDINGS_MODEL_NAME)


def get_llm(temperature=0):
    return ChatOllama(
        model=LLM_MODEL_NAME,
        reasoning=False,
        temperature=temperature,
        base_url=OLLAMA_API_URL,
    )


def get_reranker_model():
    return HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    

def get_vectorstore():
    return PGVector(
        embeddings=get_embeddings(),
        collection_name=COLLECTION_NAME,
        connection=engine,
        use_jsonb=True,
    )
