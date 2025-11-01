import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

PROVIDER = "openai" 

CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
COLLECTION_NAME = "doc_chunks"

if not CONNECTION_STRING:
    raise ValueError("DB_CONNECTION_STRING não encontrada no .env")

PROMPT_TEMPLATE = """
CONTEXTO:
{context}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{question}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_rag_chain():
    """
    Monta e retorna a RAG chain completa (Retriever -> Prompt -> LLM).
    """
    
    if PROVIDER == "openai":
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        llm = ChatOpenAI(model="gpt-5-nano")
    elif PROVIDER == "gemini":
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    else:
        raise ValueError(f"Provedor '{PROVIDER}' desconhecido.")

    vector_store = PGVector(
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        embeddings=embeddings,
    )

    retriever = vector_store.as_retriever(
        search_type="mmr", 
        search_kwargs={'k': 10}
    )

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain