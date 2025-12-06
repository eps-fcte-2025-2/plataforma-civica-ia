import asyncio
import bs4

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
load_dotenv('.env')

from ai_agent.settings import get_vectorstore


def process_documents(urls: list[dict[str, str]], chunk_size: int, chunk_overlap: int) -> list[Document]:
    """
    Carrega URLs usando WebBaseLoader e divide em chunks preservando metadados.
    """
    print(f"--- Iniciando carregamento de {len(urls)} leis ---")
    
    docs = []
    
    bs4_strainer = bs4.SoupStrainer() 

    for item in urls:
        url = item["url"]
        nome_lei = item["nome"]
        
        print(f"Baixando: {nome_lei}")
        
        try:
            loader = WebBaseLoader(
                web_paths=(url,),
                bs_kwargs={"parse_only": bs4_strainer},
                requests_kwargs={
                    "headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
                    },
                    "timeout": 20,
                },
            )
            
            docs_temp = loader.load()
            
            for doc in docs_temp:
                doc.metadata["law_name"] = nome_lei
                doc.metadata["source_url"] = url
                
            docs.extend(docs_temp)
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

    print(f"Total de documentos brutos carregados: {len(docs)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"Documentos divididos em {len(chunks)} chunks.")
    
    return chunks


async def pipeline(urls: list[dict[str, str]], chunk_size: int, chunk_overlap: int):
    chunks = process_documents(urls, chunk_size, chunk_overlap)
    vector_store = get_vectorstore()

    if chunks:
        print("Inserindo chunks no PostgreSQL via PGVector...")
        await vector_store.aadd_documents(chunks)
        print("Inserção concluída.")
    else:
        print("Nenhum chunk para inserir.")


if __name__ == "__main__":
    LEIS = [
        {
            "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13756.htm",
            "nome": "Lei 13.756/2018 (Fundo Nacional de Segurança e Loterias)"
        },
        {
            "url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/L14790.htm",
            "nome": "Lei 14.790/2023 (Apostas Esportivas / Bets)"
        },
        {
            "url": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2024/decreto/D11935.htm",
            "nome": "Decreto 11.935/2024 (Regulamentação das Apostas)"
        },
        {
            "url": "https://www.planalto.gov.br/ccivil_03/leis/l9615consol.htm",
            "nome": "Lei Pelé (Lei 9.615/1998)"
        },
        {
            "url": "https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2013/lei/l12846.htm",
            "nome": "Lei Anticorrupção (Lei 12.846/2013)"
        }
    ]
    
    asyncio.run(pipeline(LEIS, chunk_size=1000, chunk_overlap=200))