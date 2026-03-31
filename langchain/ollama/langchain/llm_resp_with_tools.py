#pip3 install langchain langchain-community langchain-core
#pip3 install ollama
from langchain.tools import tool
from langchain_ollama import ChatOllama
import logging
from langchain_core.messages import  ToolMessage

logging.basicConfig(level=logging.INFO)
history = []
model = ChatOllama(model="llama3.1:8b",temperature=0,history=history)

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

query = "What is 2 multiplied by 3 and then added the result to 4?"
history.append({"role": "user", "content": query})

response = model.invoke(query)
logging.info(f"Response: {response}")

history.append({"role": "assistant", "content": str(response)})

if response is not None:
    if response.tool_calls:
        for tool_call in response.tool_calls:
            logging.info(f"Tool call: {tool_call}")
            toolname = tool_call["name"]
            args = tool_call["args"]
            result = tools_by_name[toolname].invoke(args)
            logging.info(f"Tool result: {result}")  
            history.append(
                ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            ))
            
        # Once all tool calls are done, we can invoke the model again to get the final response
        final_response = model.invoke(history)
        logging.info(f"Model response: {final_response.content}")
    else:
        logging.info(f"Model response: {response.text}")