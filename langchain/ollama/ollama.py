#pip3 install langchain langchain-community langchain-core
#pip3 install ollama
from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

response = llm.invoke("Explain black holes in simple terms")
print(response)