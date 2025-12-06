from typing import Literal
from langgraph.graph import END, StateGraph, START

from ai_agent.state import GraphState
from ai_agent.nodes import (
    retrieve,
    rerank_documents,
    generate,
    transform_query,
    general_conversation,
    route_question 
)


def decide_to_generate(state: GraphState) -> Literal["transform_query", "generate"]:
    """Lógica condicional (Edge)"""
    filtered_documents = state["documents"]
    loop_count = state.get("loop_count", 0)
    
    if not filtered_documents:
        if loop_count >= 2:
            return "generate"
        return "transform_query"
    return "generate"


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("retrieve", retrieve)
    workflow.add_node("rerank_documents", rerank_documents)
    workflow.add_node("generate", generate)
    workflow.add_node("transform_query", transform_query)
    workflow.add_node("general_conversation", general_conversation)

    workflow.add_conditional_edges(
        START,
        route_question,
        {
            "vectorstore": "retrieve",
            "general_conversation": "general_conversation",
        },
    )

    workflow.add_edge("retrieve", "rerank_documents")
    
    workflow.add_conditional_edges(
        "rerank_documents",
        decide_to_generate,
        {
            "transform_query": "transform_query",
            "generate": "generate",
        },
    )
    
    workflow.add_edge("transform_query", "retrieve")

    workflow.add_edge("generate", END)
    workflow.add_edge("general_conversation", END)

    return workflow.compile()
