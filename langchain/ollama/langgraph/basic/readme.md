# LangGraph Tutorial: Building Agent Workflows with LangChain and Ollama

A comprehensive beginner's guide to building stateful, tool-using AI agents with LangGraph, LangChain, and Ollama.

---

## Table of Contents
1. [What is LangGraph?](#what-is-langgraph)
2. [Quick Start](#quick-start)
3. [Understanding the Code](#understanding-the-code)
4. [Understanding langgraph.json](#understanding-langgraphjson)
5. [Running Your Agent](#running-your-agent)
6. [LangGraph Studio (Visual Debugging)](#langgraph-studio-visual-debugging)
7. [Multiple Graphs and Flows](#multiple-graphs-and-flows)
8. [Multi-Agent Graphs](#multi-agent-graphs)
9. [Advanced Patterns](#advanced-patterns)
10. [Troubleshooting](#troubleshooting)
11. [References](#references)

---

## What is LangGraph?

**LangGraph** is a framework for building stateful, multi-step agent workflows using graphs. Think of it as a state machine where:
- **Nodes** are functions that do work (LLM calls, tool execution, data processing)
- **Edges** define the flow between nodes
- **State** is shared data that flows through the graph

### Why Use LangGraph?
- **Stateful**: Maintains conversation history and context across multiple steps
- **Controllable**: You define the exact flow, not the LLM
- **Debuggable**: Visual graph structure makes it easy to understand and debug
- **Reliable**: Tool calls and multi-step reasoning are predictable and testable

### Use Cases
- Tool-using agents (calculators, API calls, database queries)
- Multi-step reasoning workflows
- Agentic systems with multiple specialized agents
- Chatbots with complex conversation flows
- Research assistants that gather and synthesize information

---

## Quick Start

### Prerequisites
1. Install Python 3.8+
2. Install and run [Ollama](https://ollama.com/) with a model (e.g., `llama3.1:8b`)
   ```sh
   # Install Ollama from https://ollama.com/
   # Then pull a model:
   ollama pull llama3.1:8b
   ```

### Installation
```sh
pip install langchain langchain_ollama langgraph typing_extensions
```

### Run the Example
```sh
python agent.py
```

You should see the agent multiply 5 and 6 using a tool, returning 30.

---

## Understanding the Code

This example builds a **math assistant agent** that uses Python tools for calculations.

### 1. Model Setup
```python
from langchain_ollama import ChatOllama
model = ChatOllama(model="llama3.1:8b", temperature=0)
```
- Creates a connection to your local Ollama model
- `temperature=0` makes responses deterministic

### 2. Tools (Python Functions)
```python
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
```
- The `@tool` decorator exposes functions to the LLM
- Docstrings help the LLM understand when to use each tool
- Tools are bound to the model: `model_with_tools = model.bind_tools(tools)`

### 3. State (Shared Data)
```python
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
```
- State is a typed dictionary that flows through the graph
- `messages` accumulates the conversation (user messages, LLM responses, tool results)
- `operator.add` means new messages append to the list

### 4. Nodes (Functions That Do Work)

**LLM Node** - Calls the LLM and returns a response:
```python
def llm_call(state: MessagesState):
    response = model_with_tools.invoke(
        [SystemMessage(content="You are a math assistant...")] + state["messages"]
    )
    return {"messages": [response]}
```

**Tool Node** - Executes tools called by the LLM:
```python
def tool_node(state: MessagesState):
    last_message = state["messages"][-1]
    results = []
    for call in last_message.tool_calls:
        tool = tools_by_name[call["name"]]
        output = tool.invoke(call["args"])
        results.append(ToolMessage(content=str(output), tool_call_id=call["id"]))
    return {"messages": results}
```

### 5. Routing (Conditional Edges)
```python
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"  # More work to do
    return END  # We're done
```
- Routes to `tool_node` if the LLM called a tool
- Otherwise, ends the graph

### 6. Building the Graph
```python
builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
builder.add_edge("tool_node", "llm_call")
agent = builder.compile()
```

**Flow:**
1. `START` → `llm_call`
2. `llm_call` → `tool_node` (if tools needed) OR `END`
3. `tool_node` → `llm_call` (loop back for next step)

---

## Understanding langgraph.json

`langgraph.json` is a configuration file that tells the LangGraph CLI and Studio how to find and load your graphs.

### Basic Example
```json
{
  "dependencies": ["./"],
  "graphs": {
    "math-agent": "agent:agent"
  }
}
```

### Fields Explained

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `dependencies` | Array | Folders/packages to add to Python path | `["./", "../shared"]` |
| `graphs` | Object | Maps graph names to Python modules | `{"math-agent": "agent:agent"}` |

**Graph Format:** `"graph-name": "module:variable"`
- `"agent:agent"` means: `from agent import agent`
- The graph name is what you'll see in the Studio UI

### Multiple Graphs Example
```json
{
  "dependencies": ["./", "../shared_utils"],
  "graphs": {
    "math-agent": "agent:agent",
    "research-agent": "research:research_graph",
    "qa-bot": "qa_module:qa_agent"
  }
}
```

This allows you to:
- Define multiple agents in different files
- Switch between them in the Studio UI
- Share code via `dependencies`

---

## Running Your Agent

### Method 1: Direct Python Execution
```sh
python agent.py
```
- Runs the code directly
- Good for testing and debugging
- No visual interface

### Method 2: LangGraph CLI (Recommended)
```sh
# Install CLI
pip install -U "langgraph-cli[inmem]"

# Run dev server
langgraph dev
```

Output:
```
Ready!
- API: http://localhost:2024
- Docs: http://localhost:2024/docs
- LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

---

## LangGraph Studio (Visual Debugging)

LangGraph Studio lets you visualize and interact with your graphs in a web UI.

### Setup Steps
1. **Start the dev server:**
   ```sh
   langgraph dev
   ```

2. **Open Studio in your browser:**
   ```
   https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
   ```

3. **Connect:** Click "Connect" and allow the local server connection.

### What You Can Do
- **Visualize:** See your graph structure (nodes, edges, flow)
- **Debug:** Step through execution node by node
- **Test:** Send messages and see state changes in real-time
- **Inspect:** View message history, tool calls, and state at each step

### Troubleshooting Studio
- **Can't connect?** Ensure `langgraph dev` is running and the port (2024) is correct
- **Import errors?** Check `langgraph.json` dependencies and module paths
- **Graph not showing?** Verify the module:variable format in `graphs`

---

## Multiple Graphs and Flows

### Scenario: Multiple Specialized Agents

**File Structure:**
```
project/
├── langgraph.json
├── math_agent.py      # Math specialist
├── research_agent.py  # Research specialist
└── coordinator.py     # Orchestrator
```

**langgraph.json:**
```json
{
  "dependencies": ["./"],
  "graphs": {
    "math": "math_agent:agent",
    "research": "research_agent:agent",
    "coordinator": "coordinator:orchestrator"
  }
}
```

**Benefits:**
- Each agent has a focused purpose
- Switch between agents in Studio
- Share tools and utilities

### Workflow: Sequential Agents
Create a coordinator that routes tasks:
```python
def route_task(state):
    task_type = classify_task(state["query"])
    if task_type == "math":
        return "math_agent"
    elif task_type == "research":
        return "research_agent"
    else:
        return "general_agent"

builder.add_conditional_edges("router", route_task, 
                               ["math_agent", "research_agent", "general_agent"])
```

---

## Multi-Agent Graphs

Multi-agent graphs have multiple agents that collaborate or work in parallel.

### Pattern 1: Manager-Worker (Hierarchical)
```python
# Manager decides what to do, workers execute
builder.add_node("manager", manager_node)
builder.add_node("worker_1", worker_1_node)
builder.add_node("worker_2", worker_2_node)

builder.add_edge(START, "manager")
builder.add_conditional_edges("manager", route_to_worker, 
                               ["worker_1", "worker_2", END])
builder.add_edge("worker_1", "manager")  # Report back
builder.add_edge("worker_2", "manager")
```

**Use Case:** Research assistant where manager breaks down questions, workers gather data, manager synthesizes.

### Pattern 2: Parallel Execution
```python
# Multiple agents work simultaneously
from langgraph.graph import StateGraph
from concurrent.futures import ThreadPoolExecutor

def parallel_node(state):
    with ThreadPoolExecutor() as executor:
        results = executor.map(agent_fn, state["tasks"])
    return {"results": list(results)}
```

**Use Case:** Data validation where multiple checkers run in parallel.

### Pattern 3: Agent Communication
Agents can share state and communicate:
```python
class SharedState(TypedDict):
    query: str
    agent_1_output: str
    agent_2_output: str
    final_answer: str

def agent_1(state):
    # Agent 1 does its work
    return {"agent_1_output": "..."}

def agent_2(state):
    # Agent 2 can see agent_1's output
    context = state.get("agent_1_output", "")
    return {"agent_2_output": "..."}
```

### Example: Multi-Expert Opinion System
```python
# Like your multimodelagent_vibecode project!
# Multiple experts (stock market, software engineers, etc.) 
# give opinions, then a synthesizer combines them

builder.add_node("expert_1", expert_1_node)
builder.add_node("expert_2", expert_2_node)
builder.add_node("expert_3", expert_3_node)
builder.add_node("synthesizer", synthesizer_node)

# All experts run, then synthesizer combines
builder.add_edge(START, "expert_1")
builder.add_edge(START, "expert_2")
builder.add_edge(START, "expert_3")
builder.add_edge("expert_1", "synthesizer")
builder.add_edge("expert_2", "synthesizer")
builder.add_edge("expert_3", "synthesizer")
builder.add_edge("synthesizer", END)
```

---

## Advanced Patterns

### 1. Loops and Iteration
```python
def should_continue(state):
    if state["iteration"] < 3:
        return "process"  # Loop back
    return END

builder.add_edge("process", "process")  # Self-loop
builder.add_conditional_edges("process", should_continue, ["process", END])
```

### 2. Checkpointing (Memory)
```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
agent = builder.compile(checkpointer=memory)

# Now your agent remembers state between calls
agent.invoke({"messages": [...]}, config={"configurable": {"thread_id": "user123"}})
```

### 3. Human-in-the-Loop
```python
from langgraph.prebuilt import ToolNode

def human_approval(state):
    # Pause and wait for human input
    return state

builder.add_node("human_approval", human_approval)
```

### 4. Error Handling
```python
def safe_tool_node(state):
    try:
        return tool_node(state)
    except Exception as e:
        return {"messages": [{"error": str(e)}]}
```

---

## Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | Check `dependencies` in `langgraph.json` |
| Graph doesn't show in Studio | Verify `module:variable` format |
| Tool calls fail | Ensure tools are bound: `model.bind_tools(tools)` |
| State not updating | Return a dict from nodes: `return {"key": value}` |
| Infinite loop | Add a counter to state and check in routing |
| Studio won't connect | Check `langgraph dev` is running on port 2024 |

### Debugging Tips
1. **Add logging:** Print state in each node
2. **Use Studio:** Step through execution visually
3. **Check state:** Use `agent.get_state()` to inspect current state
4. **Simplify:** Test nodes individually before connecting them

---

## References

### Official Documentation
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/) - Comprehensive guide
- [LangGraph Studio](https://smith.langchain.com/studio/) - Visual debugger
- [LangChain Docs](https://python.langchain.com/) - LangChain framework
- [Ollama Docs](https://ollama.com/docs) - Local LLM setup

### GitHub
- [LangGraph Repo](https://github.com/langchain-ai/langgraph)
- [LangGraph CLI](https://github.com/langchain-ai/langgraph/tree/main/langgraph-cli)

### Tutorials
- [LangGraph Quickstart](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- [Building Multi-Agent Systems](https://langchain-ai.github.io/langgraph/tutorials/multi-agent/)

---

## Next Steps

1. **Modify the example:** Add your own tools (e.g., weather API, database queries)
2. **Build a multi-agent system:** Create specialized agents for different tasks
3. **Add memory:** Use checkpointing for persistent conversations
4. **Deploy:** Package your agent for production use

Happy building! 🚀
