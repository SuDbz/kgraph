# LangGraph Studio Integration & `langgraph.json` Guide

This guide explains how to view and interact with your LangGraph graphs in the Studio UI, what the `langgraph.json` file is, its options, and how to run your code and visualize your agent.

---

## What is `langgraph.json`?

`langgraph.json` is a configuration file that tells the LangGraph dev server and Studio UI how to find and load your graph code. It specifies:
- **dependencies**: Local Python packages or folders to include.
- **graphs**: Maps a graph name to a Python module and variable (format: `module:variable`).

### Example: Simple `langgraph.json`
```json
{
  "dependencies": ["./"],
  "graphs": {
    "math-agent": "agent:agent"
  }
}
```
- **dependencies**: ["./"] includes your current folder as a package.
- **graphs**: "math-agent" is the name shown in Studio; it loads the `agent` variable from `agent.py`.

### Example: Complex `langgraph.json`
```json
{
  "dependencies": ["./", "../shared", "some_pypi_package"],
  "graphs": {
    "math-agent": "agent:agent",
    "qa-agent": "qa_module:qa_graph",
    "custom": "custom_folder.custom_mod:custom_graph"
  }
}
```
- **dependencies**: Includes current folder, a shared folder, and a PyPI package.
- **graphs**: Loads multiple graphs from different modules and variables.

#### Field Explanations
- **dependencies**: List of folders or packages to add to Python path for imports.
- **graphs**: Key is the graph name (shown in Studio); value is `module:variable` (e.g., `agent:agent` means `from agent import agent`).

---

## How to Run and View Your Graph in Studio

### 1. Create `langgraph.json`
Place your config in the project root. Example:
```json
{
  "dependencies": ["./"],
  "graphs": {
    "math-agent": "agent:agent"
  }
}
```

### 2. Install LangGraph CLI with In-Memory Support
```sh
pip install -U "langgraph-cli[inmem]"
```

### 3. Start the Dev Server
```sh
langgraph dev
```
You should see logs like:
```
Ready!
- API: http://localhost:2024
- Docs: http://localhost:2024/docs
- LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

### 4. Open Studio in Your Browser
Open:
```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```
Click **Connect** and allow the local server. This lets you view and interact with your graph visually.

---

## Troubleshooting
- If Studio doesn't connect, ensure your server is running and the `baseUrl` matches your local API URL.
- If you see import errors, check that your `dependencies` and `graphs` fields are correct and that your Python files/modules are in the right place.

---

## How to Run the Code (Locally)

1. Make sure you have all dependencies installed:
   ```sh
   pip install langchain langchain_ollama langgraph typing_extensions
   pip install -U "langgraph-cli[inmem]"
   ```
2. Start Ollama and ensure your model (e.g., `llama3.1:8b`) is available.
3. Run your agent directly for local testing:
   ```sh
   python agent.py
   ```
   This will run the sample math question in the script.
4. For Studio UI, follow the steps above to start the dev server and open the Studio URL.

---

## Summary Table: `langgraph.json` Fields
| Field         | Type     | Example Value                  | Description                                      |
|---------------|----------|-------------------------------|--------------------------------------------------|
| dependencies  | list     | ["./", "../shared"]           | Folders/packages to add to Python path            |
| graphs        | object   | {"math-agent": "agent:agent"} | Maps graph name to module:variable for Studio     |

---

## References
- [LangGraph Studio](https://smith.langchain.com/studio/)
- [LangGraph CLI Docs](https://github.com/langchain-ai/langgraph/tree/main/langgraph-cli)
- [LangGraph Python Docs](https://langchain-ai.github.io/langgraph/)
