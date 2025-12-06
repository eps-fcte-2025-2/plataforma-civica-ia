from typing import Literal

from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ai_agent.state import GraphState
from ai_agent.settings import get_llm, get_vectorstore, get_reranker_model


llm = get_llm()
reranker_model = get_reranker_model() 
vectorstore = get_vectorstore()


async def general_conversation(state: GraphState, config: RunnableConfig):
    """
    Responde a saudações ou perguntas fora do escopo jurídico sem usar o banco.
    """
    print("--- NODE: GENERAL CONVERSATION ---")
    question = state["question"]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente jurídico prestativo da plataforma de participação cívil Apita Cidadão. O usuário iniciou uma conversa casual. "
                   "Responda educadamente, se apresente e pergunte como pode ajudar com questões jurídicas. "
                   "Não invente leis nem fatos."),
        ("human", "{question}")
    ])
    
    chain = prompt | llm
    response = await chain.ainvoke({"question": question}, config=config)
    return {"generation": response.content}


async def route_question(state: GraphState) -> Literal["vectorstore", "general_conversation"]:
    print("--- ROTEAMENTO ---")
    question = state["question"]

    system = """Você é um classificador de intenções.
    Sua tarefa é decidir para onde encaminhar a pergunta do usuário.
    
    Se a pergunta for sobre leis, direitos, processos, jurídico ou técnica:
    Responda exatamente: vectorstore
    
    Se a pergunta for uma saudação (oi, olá, tudo bem), despedida ou conversa casual:
    Responda exatamente: general_conversation

    NÃO explique nada. Retorne APENAS a palavra-chave.
    """
    
    route_prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{question}")
    ])

    chain = route_prompt | llm | StrOutputParser()
    
    try:
        response = await chain.ainvoke({"question": question})
        decision = response.strip().lower()

        if "general_conversation" in decision:
            print("   -> ROTA: CONVERSA GERAL")
            return "general_conversation"
        print("   -> ROTA: BUSCA VETORIAL")
        return "vectorstore"

    except Exception as e:
        print(f"Erro no Router: {e}")
        return "vectorstore"
    

async def retrieve(state: GraphState):
    print("--- NODE: RETRIEVE ---")
    question = state["question"]
    retriever = vectorstore.as_retriever(search_kwargs={"k": 15})
    documents = await retriever.ainvoke(question) 
    return {"documents": documents, "question": question}


def rerank_documents(state: GraphState):
    print("--- NODE: RERANK DOCUMENTS ---")
    question = state["question"]
    documents = state["documents"]
    
    if not documents:
        return {"documents": [], "question": question}

    pairs = [[question, doc.page_content] for doc in documents]
    scores = reranker_model.score(pairs)
    
    ranked_docs = []
    for doc, score in zip(documents, scores):
        doc.metadata["relevance_score"] = score
        if score > -2.0:
            ranked_docs.append(doc)
            
    ranked_docs.sort(key=lambda x: x.metadata["relevance_score"], reverse=True)

    final_docs = ranked_docs[:5]

    return {"documents": final_docs, "question": question}


async def generate(state: GraphState, config: RunnableConfig):
    print("--- NODE: GENERATE ---")
    question = state["question"]
    documents = state["documents"]
    
    system_prompt = """Você é um assistente jurídico sênior e preciso da plataforma de participação cívil Apita Cidadão. 
    Use os seguintes pedaços de contexto recuperado para responder à pergunta. 
    
    Regras Estritas:
    1. Se você não souber a resposta baseada no contexto, diga apenas "Não possuo informações suficientes no contexto fornecido para responder com precisão jurídica."
    2. Cite explicitamente as leis ou artigos mencionados no contexto (ex: "Conforme Art. 5 da CF...").
    3. Mantenha a resposta em linguagem simples e acessível para leigos, sem vocabulário jurídico complexo. Porém, em tom formal e conciso;
    
    Contexto:
    {context}
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}")
    ])
    
    rag_chain = prompt | llm
    
    context_text = "\n\n".join([
        f"FONTE: {doc.metadata.get('law_name', '')}\nCONTEÚDO: {doc.page_content}"
        for doc in documents
    ])

    response = await rag_chain.ainvoke({"context": context_text, "question": question}, config=config)
    
    return {"generation": response.content}


async def transform_query(state: GraphState):
    print("--- NODE: REWRITE QUERY ---")
    question = state["question"]
    loop_count = state.get("loop_count", 0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um especialista em otimização de buscas para banco de dados vetorial jurídico. "
                   "Sua tarefa é reescrever a pergunta para torná-la mais específica e técnica, "
                   "visando encontrar leis e jurisprudências relevantes."),
        ("human", "Pergunta Original: {question}\n\nRetorne apenas a pergunta melhorada, sem explicações.")
    ])
    
    chain = prompt | llm
    better_question = chain.invoke({"question": question})
    
    return {"question": better_question.content, "loop_count": loop_count + 1}
