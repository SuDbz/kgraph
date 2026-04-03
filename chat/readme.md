# Knowledge Graph Chatbot

An interactive knowledge graph chatbot with visual graph exploration, built with LangChain, Ollama, Streamlit, NetworkX, and pyvis.

## Features

- 🕸️ **Interactive Graph Visualization**: See the knowledge graph in real-time using pyvis
- 💬 **Natural Language Interface**: Ask questions about the graph in plain English
- 🛠️ **Proper Tool Calling**: Uses LangChain's tool calling pattern for reliable operations
- 🔄 **Live Updates**: Graph updates are reflected immediately in the UI
- 📊 **Graph Analytics**: Query neighbors, shortest paths, node degrees, and more

## Prerequisites

1. **Ollama**: Install and run Ollama with the llama3.1:8b model
   ```bash
   # Install Ollama from https://ollama.com/
   ollama pull llama3.1:8b
   ```

2. **Python 3.8+**

## Installation

```bash
pip install streamlit networkx pyvis langchain langchain_ollama langchain-core
```

## Running the Application

```bash
streamlit run kgrpah_mcp.py
```

The app will open in your browser at `http://localhost:8501`

## How It Works

### 1. Tool Calling Architecture

The chatbot uses LangChain's `@tool` decorator to define graph operations:

```python
@tool
def get_neighbors(node: str) -> str:
    """Get all neighbors of a given node"""
    # Implementation
```

These tools are bound to the Ollama model, allowing the LLM to:
- Understand when to use tools based on user queries
- Extract correct parameters from natural language
- Execute tools and incorporate results into responses

### 2. Available Tools

| Tool | Description | Example Query |
|------|-------------|---------------|
| `get_neighbors` | Find all connected nodes | "Who are Alice's neighbors?" |
| `shortest_path` | Find shortest path between nodes | "Path from Alice to Charlie?" |
| `get_all_nodes` | List all nodes in graph | "Show me all nodes" |
| `node_degree` | Get number of connections | "How many connections does Bob have?" |
| `add_edge` | Add new relationships | "Connect Alice to Eve as mentor" |

### 3. Graph Visualization

The graph is visualized using **pyvis**, which provides:
- Interactive node dragging
- Zoom and pan controls
- Edge labels showing relationships
- Physics-based layout

### 4. Chat Flow

1. User enters a question
2. LLM analyzes the question and decides if tools are needed
3. If tools are required, LLM makes tool calls with extracted parameters
4. Tools execute and return results
5. LLM incorporates tool results into a natural language response
6. Response is displayed to the user

## Example Queries

Try these questions:

**Basic Queries:**
- "Who are Alice's neighbors?"
- "What nodes are in the graph?"
- "How many connections does Bob have?"

**Path Finding:**
- "What is the shortest path from Alice to Charlie?"
- "Find a path between David and Eve"

**Graph Modification:**
- "Add an edge between Alice and Charlie with relation colleague"
- "Connect Bob to Eve as friend"

**Complex Questions:**
- "Who has the most connections?"
- "Are Alice and Charlie connected?"
- "Who can Alice reach through Bob?"

## Code Structure

```
kgrpah_mcp.py
├── Graph Setup          # Initialize NetworkX graph with sample data
├── Tool Functions       # LangChain @tool decorated functions
├── Model Setup          # Ollama model with tool binding
├── Graph Visualization  # Pyvis network rendering
├── Chat Handler         # Message processing with tool execution
└── Streamlit UI         # Two-column layout (chat + graph)
```

## Customization

### Adding New Tools

```python
@tool
def custom_tool(param: str) -> str:
    """Description of what the tool does"""
    # Your implementation
    return result

# Add to tools list
tools = [get_neighbors, shortest_path, custom_tool, ...]
```

### Expanding the Graph

```python
def init_graph():
    G = nx.Graph()
    # Add your nodes and edges
    G.add_edge("Node1", "Node2", relation="custom_relation")
    return G
```

### Changing the Model

```python
model = ChatOllama(
    model="llama3.2:latest",  # Different model
    temperature=0.7            # Adjust creativity
)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Model not found" | Run `ollama pull llama3.1:8b` |
| Tools not being called | Check tool descriptions are clear |
| Graph not rendering | Ensure pyvis is installed correctly |
| Streamlit errors | Check all dependencies are installed |

## Architecture Benefits

### Why LangChain Tool Calling?

- **Type Safety**: Parameters are validated automatically
- **Discoverability**: LLM can see all available tools and their descriptions
- **Reliability**: Tool calls are structured and predictable
- **Maintainability**: Easy to add, remove, or modify tools

### Why Streamlit?

- **Rapid Development**: Build UIs with Python code
- **Interactive**: Real-time updates and user interactions
- **No Frontend Code**: No HTML/CSS/JavaScript required
- **Built-in Components**: Chat interface, columns, expandable sections

### Why NetworkX + pyvis?

- **NetworkX**: Powerful graph algorithms and analysis
- **pyvis**: Beautiful, interactive visualizations
- **Integration**: Easy to convert NetworkX graphs to pyvis

## Next Steps

1. **Add More Graph Data**: Expand the knowledge graph with your domain data
2. **Advanced Tools**: Add graph algorithms (centrality, clustering, etc.)
3. **Persistence**: Save graph state to database or file
4. **Multi-Graph Support**: Allow users to create and switch between graphs
5. **Import/Export**: Load graphs from CSV, JSON, or GraphML files

## References

- [LangChain Tools Documentation](https://python.langchain.com/docs/modules/tools/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [NetworkX Documentation](https://networkx.org/)
- [pyvis Documentation](https://pyvis.readthedocs.io/)
- [Ollama Documentation](https://ollama.com/docs)

---

Happy graph exploration! 🕸️
