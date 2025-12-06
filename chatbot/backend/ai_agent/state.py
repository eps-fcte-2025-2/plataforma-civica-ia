from typing import TypedDict

from langchain_core.documents import Document


class GraphState(TypedDict):
    """
    Define o estado do grafo.
    Este dicionário é passado entre todos os nós.
    """
    question: str
    generation: str
    documents: list[Document]
    loop_count: int
