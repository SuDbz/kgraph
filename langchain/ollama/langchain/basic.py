#pip3 install langchain langchain-community langchain-core
#pip3 install ollama
from langchain.tools import tool
from langchain_ollama import ChatOllama
import logging

logging.basicConfig(level=logging.INFO)

model = ChatOllama(model="llama3.1:8b",temperature=0)


@tool("multiply")
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers."""
    return a * b

@tool("add")
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

tools = [multiply, add]
tools_by_name = {t.name: t for t in tools}

model = model.bind_tools(tools)


response = model.invoke("What is 2 multiplied by 3?")
# chain of tools
# response = model.invoke("What is 2 multiplied by 3 and then added the result to 4?")
logging.info(f"Response: {response}")

if response is not None:
    if response.tool_calls:
        for tool_call in response.tool_calls:
            logging.info(f"Tool call: {tool_call}")
            toolname = tool_call["name"]
            args = tool_call["args"]
            result = tools_by_name[toolname].invoke(args)
            logging.info(f"Tool result: {result}")  
    else:
        logging.info(f"Model response: {response.text}")