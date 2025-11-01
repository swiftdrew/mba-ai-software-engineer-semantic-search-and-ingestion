import sys
from search import get_rag_chain

def main():

    print("Inicializando o assistente...")
    print("Conectando ao banco de dados e carregando modelos...")
    
    try:
        rag_chain = get_rag_chain()
        print("---")
        print("Assistente pronto. Faça sua pergunta.")
        print("Digite 'sair' a qualquer momento para terminar.")
        print("---")
    except Exception as e:
        print(f"\n[ERRO FATAL] Não foi possível inicializar a RAG chain:")
        print(f"Erro: {e}")
        print("\nVerifique:")
        print("1. Se suas API Keys (OPENAI_API_KEY/GOOGLE_API_KEY) estão corretas no .env")
        print("2. Se o Docker está rodando ('docker compose up -d')")
        print("3. Se a ingestão foi executada ('python src/ingest.py')")
        sys.exit(1)

    while True:
        try:
            question = input("\nFaça sua pergunta:\n\nPERGUNTA: ")
            
            if question.lower().strip() in ['sair', 'exit', 'quit']:
                print("\nAté logo!")
                break
            
            if not question.strip():
                continue
                
            print("\nBuscando no documento...")
            response = rag_chain.invoke(question)
            
            print(f"\nRESPOSTA: {response}")
        
        except KeyboardInterrupt:
            print("\n\nAté logo!")
            break
        except Exception as e:
            print(f"\n[ERRO] Ocorreu um problema ao processar sua pergunta:")
            print(f"Erro: {e}")
            print("Por favor, tente novamente.")

if __name__ == "__main__":
    main()