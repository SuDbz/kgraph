# Math Assistant Agent with LangGraph, LangChain, and Ollama

This project demonstrates how to build a tool-using math assistant agent using [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://github.com/langchain-ai/langchain), and [Ollama](https://ollama.com/). The agent is designed to answer math questions by invoking Python tools for calculations, rather than computing manually.

## Features
- **Ollama LLM Integration:** Uses a local Ollama model (e.g., `llama3.1:8b`) for language understanding and orchestration.
- **Tool Binding:** Binds Python functions (tools) for mathematical operations (add, multiply, divide) to the LLM.
- **LangGraph State Machine:** Implements a stateful agent using LangGraph, with nodes for LLM calls, tool execution, and routing.
- **Automatic Tool Use:** The agent is instructed to always use tools for calculations, never manual computation.

---

## File Overview

### agent.py
This is the main agent definition. It contains:
- **Model Setup:**
  - Loads the Ollama model via `ChatOllama` from `langchain_ollama`.
- **Tool Definitions:**
  - `add(a, b)`, `multiply(a, b)`, `divide(a, b)` are Python functions decorated with `@tool` to expose them to the agent.
- **Tool Binding:**
  - The tools are bound to the model using `model.bind_tools(tools)`.
- **State Definition:**
  - `MessagesState` tracks the conversation as a list of messages.
- **LLM Node:**
  - Handles LLM calls, always prepending a system prompt instructing the agent to use tools for math.
- **Tool Node:**
  - Executes any tool calls returned by the LLM, returning results as `ToolMessage` objects.
- **Router:**
  - Decides whether to continue (if more tool calls are needed) or end the conversation.
- **Graph Construction:**
  - Uses LangGraph's `StateGraph` to wire up the nodes and transitions.
- **Local Test:**
  - If run directly, tests the agent with a sample math question.

### langgraph.json
Defines the graph for LangGraph's runtime, mapping the `math-agent` graph to the `agent` object in `agent.py`.

---

## When and Why to Use This Pattern
- **When:**
  - You want an LLM agent to reliably use Python functions (tools) for specific tasks (e.g., math, API calls, database queries).
  - You need a stateful, multi-step workflow (e.g., tool use, reasoning, and response) managed by a graph.
- **Why:**
  - Ensures correctness by delegating calculations to code, not the LLM's internal reasoning.
  - Enables complex, multi-step tool use and orchestration.
  - Provides a clear, extensible structure for adding more tools or workflow steps.

---

## How It Works (Step-by-Step)
1. **User asks a math question.**
2. **LLM Node:**
   - The agent receives the question and a system prompt instructing it to use tools.
   - The LLM generates a response, possibly with tool calls (e.g., `multiply(a=5, b=6)`).
3. **Tool Node:**
   - If tool calls are present, the agent executes them using the bound Python functions.
   - Results are returned as messages.
4. **Router:**
   - If more tool calls are needed, the process repeats; otherwise, the agent returns the final answer.

---

## Requirements
- Python 3.8+
- [Ollama](https://ollama.com/) running locally with the desired model (e.g., `llama3.1:8b`)
- Install dependencies:
  ```sh
  pip install langchain langchain_ollama langgraph typing_extensions
  ```

---

## Extending This Agent
- Add more tools by defining new `@tool`-decorated functions and including them in the `tools` list.
- Modify the system prompt to change agent behavior.
- Add more nodes or transitions in the graph for advanced workflows.

---

## References
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.com/docs)
