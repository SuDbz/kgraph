# LangChain + Ollama (Local LLM Setup Guide)

## 1. Install Dependencies

```bash
# Install core LangChain packages
pip install langchain langchain-community langchain-core
# langchain           → main framework
# langchain-community → integrations (like Ollama)
# langchain-core      → base abstractions used internally

# Install Ollama Python client
pip install ollama
# ollama → lets Python talk to the local Ollama server
```

---

## 2. Install & Run Ollama

```bash
# Download Ollama from official site (manual step)
# Provides local LLM runtime (runs models on your machine)

# Pull a model (example: llama3)
ollama pull llama3
# Downloads the model locally so it can be used offline

# Start the Ollama server
ollama serve
# Starts a local API (usually at http://localhost:11434)
# LangChain connects to this server to run models
```

---

## 3. Basic LLM Usage

```python
from langchain_community.llms import Ollama
# Import Ollama LLM wrapper for LangChain

llm = Ollama(model="llama3")
# Create an LLM instance using the llama3 model
# "model" specifies which local model to use

response = llm.invoke("Explain black holes in simple terms")
# Sends a prompt to the model and gets a response

print(response)
# Prints the generated text output
```

---

## 4. Chat मॉडल (Recommended)

```python
from langchain_community.chat_models import ChatOllama
# Chat-based interface (better for conversations)

chat = ChatOllama(model="llama3")
# Initialize chat model with the same local model

response = chat.invoke("Write a short poem about AI")
# Send a chat-style prompt

print(response.content)
# Chat responses return an object → .content gives text
```

---

## 5. Prompt Templates (Dynamic Inputs)

```python
from langchain_core.prompts import ChatPromptTemplate
# Used to create reusable prompts with variables

from langchain_community.chat_models import ChatOllama

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms"
)
# {topic} is a placeholder that will be filled dynamically

model = ChatOllama(model="llama3")
# Same chat model setup

chain = prompt | model
# Pipe operator → connects prompt to model (LangChain style)

print(chain.invoke({"topic": "quantum computing"}).content)
# Pass dictionary → replaces {topic} with actual value
```

---

## 6. Document Search (RAG Setup)

```bash
pip install chromadb
# Vector database for storing embeddings (semantic search)
```

```python
from langchain_community.document_loaders import TextLoader
# Loads text files into LangChain document format

from langchain_community.vectorstores import Chroma
# Vector database to store and search embeddings

from langchain_community.embeddings import OllamaEmbeddings
# Converts text → numerical vectors using Ollama model

loader = TextLoader("data.txt")
# Load your document file

docs = loader.load()
# Convert file into document objects

embeddings = OllamaEmbeddings(model="llama3")
# Create embedding model using Ollama

db = Chroma.from_documents(docs, embeddings)
# Store documents as vectors in database

query = "What is this document about?"
# User question

results = db.similarity_search(query)
# Finds most relevant document chunks

print(results[0].page_content)
# Print best matching result
```

---

## 7. Useful Models

```bash
ollama pull llama3   # General purpose (balanced)
ollama pull mistral  # Fast + efficient
ollama pull phi      # Very lightweight (low RAM)
ollama pull gemma    # Google's model
```

---

## 8. Common Issues

* Connection refused
  → Make sure `ollama serve` is running

* Model not found
  → Run `ollama pull <model>`

* Slow performance
  → Use smaller models like `phi` or `mistral`

---

## 9. Pro Tips

* Use `llama3:8b` → smaller & faster variant
* GPU is auto-used if available
* Larger models need more RAM

---

## 10. Summary

* Ollama → runs models locally
* LangChain → connects and builds workflows
* Together → create offline AI apps (chatbots, RAG, tools)

```
```