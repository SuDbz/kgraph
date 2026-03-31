# agent.py

from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.messages import HumanMessage, SystemMessage, ToolMessage, AnyMessage
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated
import operator

# ---------------------------
# 1. Model (Ollama)
# ---------------------------
model = ChatOllama(model="llama3.1:8b",temperature=0)

# ---------------------------
# 2. Tools
# ---------------------------
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return a / b

tools = [add, multiply, divide]
tools_by_name = {t.name: t for t in tools}

model_with_tools = model.bind_tools(tools)

# ---------------------------
# 3. State
# ---------------------------
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# ---------------------------
# 4. LLM Node
# ---------------------------
def llm_call(state: MessagesState):
    response = model_with_tools.invoke(
        [
            SystemMessage(
                content=(
                    "You are a math assistant.\n"
                    "You MUST use tools for calculations.\n"
                    "Do NOT compute manually.\n"
                )
            )
        ]
        + state["messages"]
    )
    return {"messages": [response]}

# ---------------------------
# 5. Tool Node
# ---------------------------
def tool_node(state: MessagesState):
    last_message = state["messages"][-1]
    results = []

    for call in last_message.tool_calls:
        tool = tools_by_name[call["name"]]
        output = tool.invoke(call["args"])

        results.append(
            ToolMessage(
                content=str(output),
                tool_call_id=call["id"]
            )
        )

    return {"messages": results}

# ---------------------------
# 6. Router
# ---------------------------
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "tool_node"

    return END

# ---------------------------
# 7. Build Graph
# ---------------------------
builder = StateGraph(MessagesState)

builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)

builder.add_edge(START, "llm_call")
builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
builder.add_edge("tool_node", "llm_call")

agent = builder.compile()

# ---------------------------
# 8. Local test (optional)
# ---------------------------
if __name__ == "__main__":
    result = agent.invoke({
        "messages": [HumanMessage(content="Multiply 5 and 6")]
    })

    for msg in result["messages"]:
        msg.pretty_print()