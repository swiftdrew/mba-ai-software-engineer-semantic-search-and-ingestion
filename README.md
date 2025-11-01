# Desafio Técnico: Ingestão e Busca Semântica com LangChain e pgVector

Este projeto implementa um pipeline completo de RAG (Retrieval-Augmented Generation) focado em responder perguntas com base em um documento PDF.

O software é capaz de:
1.  **Ingestão:** Ler um arquivo PDF (`document.pdf`), dividi-lo em *chunks*, gerar *embeddings* (vetores) e armazená-los em um banco de dados PostgreSQL com a extensão `pgVector`.
2.  **Busca:** Permitir que um usuário faça perguntas via CLI (linha de comando) e receber respostas geradas por uma LLM (OpenAI ou Gemini), com base *estritamente* no contexto encontrado no documento.

---

## ⚙️ Tecnologias Utilizadas

* **Linguagem:** Python 3.9+
* **Framework:** LangChain
* **Banco de Dados:** PostgreSQL + pgVector
* **Orquestração:** Docker & Docker Compose
* **APIs de IA:** OpenAI (Embeddings & Chat) ou Google Gemini (Embeddings & Chat)

---

## 🔧 Pré-requisitos

Para executar este projeto, você precisará ter as seguintes ferramentas instaladas em sua máquina:

* **Python 3.9 ou superior**
* **Docker e Docker Compose**
* **Uma Chave de API da OpenAI:** É necessário ter uma conta na [OpenAI Platform](https://platform.openai.com/) com faturamento ativo (mínimo de $5 em créditos) para que a API de embeddings funcione.
* **(Opcional) Uma Chave de API do Google Gemini:** Como alternativa, você pode usar uma API Key do [Google AI Studio](https://aistudio.google.com/) com faturamento habilitado no Google Cloud.

---

## 🚀 Guia de Instalação e Execução

Siga estes passos na ordem correta para configurar e executar o projeto.

1. Clonar o repositorio 

```bash
git clone [https://github.com/](https://github.com/)[SEU_USUARIO]/[NOME_DO_REPOSITORIO].git
cd [NOME_DO_REPOSITORIO]
```

2. Configurar o Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

4. Configurar as Variáveis de Ambiente (Passo Crítico)

As chaves de API e a conexão com o banco são gerenciadas por variáveis de ambiente.
Copie o template .env.example para criar seu arquivo .env local. Este arquivo é ignorado pelo Git e nunca será comitado.

```bash
cp .env.example .env
```

5. Iniciar o Banco de Dados (Docker)

```bash
docker compose up -d
```

6. Executar a Ingestão do PDF

Este script irá ler o document.pdf, processá-lo e salvar os vetores no banco de dados.

Importante: O script de ingestão (src/ingest.py) e o script de busca (src/search.py) possuem uma variável PROVIDER no topo do arquivo. Ela deve ser definida como "openai" ou "gemini". O provedor deve ser o mesmo em ambos os arquivos.

O padrão do repositório é "openai".

```bash
python src/ingest.py
```

7. Iniciar o Chat (CLI)

```bash
python src/chat.py
```

## Exemplo de Uso e Validação
Para validar que o sistema está funcionando conforme os requisitos, utilize os testes abaixo:

#### Teste 1: Pergunta Dentro do Contexto
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?

RESPOSTA: O faturamento consolidado da Empresa SuperTechIABrazil no ano fiscal de 2023 atingiu a marca de 10 milhões de reais.

#### Teste 2: Pergunta Fora do Contexto
PERGUNTA: Quantos clientes temos em 2024?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.

#### Teste 3: Pergunta de Conhecimento Geral (Fora do Contexto)
PERGUNTA: Qual a capital da França?

RESPOSTA: Não tenho informações necessárias para responder sua pergunta.