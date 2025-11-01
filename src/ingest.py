import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROVIDER = "openai" 

PDF_PATH = "document.pdf"

CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
COLLECTION_NAME = "doc_chunks"

if not CONNECTION_STRING:
    raise ValueError("DB_CONNECTION_STRING não encontrada no .env")


def get_embeddings_model():
    """Retorna o modelo de embeddings com base no provedor."""
    if PROVIDER == "openai":
        print("Usando embeddings da OpenAI (text-embedding-3-small)")
        return OpenAIEmbeddings(model="text-embedding-3-small")
    elif PROVIDER == "gemini":
        print("Usando embeddings do Google (models/embedding-001)")
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    else:
        raise ValueError(f"Provedor '{PROVIDER}' desconhecido.")

def main():
    print(f"Iniciando ingestão do arquivo: {PDF_PATH}\n")

    print("Carregando PDF...")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()
    print(f"PDF carregado, {len(docs)} páginas encontradas.")

    print("Dividindo documento em chunks (1000/150)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = text_splitter.split_documents(docs)
    print(f"Total de {len(chunks)} chunks criados.")

    embeddings = get_embeddings_model()

    print(f"Salvando vetores no PGVector (Coleção: {COLLECTION_NAME})...")
    PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True 
    )

    print("\n--- Ingestão Concluída com Sucesso ---")

if __name__ == "__main__":
    main()