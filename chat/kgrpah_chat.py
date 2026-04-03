# graph_bot.py
"""
Knowledge Graph Chatbot with Streamlit UI
Uses LangChain tool calling, Ollama LLM, NetworkX for graphs, and pyvis for visualization
"""

import streamlit as st
import networkx as nx
from pyvis.network import Network
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage

# ----------------------------
# 1. Graph Setup
# ----------------------------
@st.cache_resource
def init_graph():
    """Initialize the knowledge graph with sample data"""
    G = nx.Graph()
    
    # Sample graph - you can expand this
    G.add_edge("Alice", "Bob", relation="friend")
    G.add_edge("Bob", "Charlie", relation="colleague")
    G.add_edge("Alice", "David", relation="family")
    G.add_edge("Charlie", "David", relation="friend")
    G.add_edge("David", "Eve", relation="colleague")
    G.add_edge("Eve", "Alice", relation="friend")
    
    return G

G = init_graph()

# ----------------------------
# 2. Tool Functions (Proper LangChain Tools)
# ----------------------------
@tool
def get_neighbors(node: str) -> str:
    """Get all neighbors (connected nodes) of a given node in the graph with their relationship types"""
    if node in G:
        neighbors_info = []
        for neighbor in G.neighbors(node):
            relation = G[node][neighbor].get('relation', 'connected')
            neighbors_info.append(f"{neighbor} ({relation})")
        return f"Neighbors of {node}: {', '.join(neighbors_info)}"
    return f"Node '{node}' not found in the graph"

@tool
def shortest_path(source: str, target: str) -> str:
    """Find the shortest path between two nodes in the graph"""
    try:
        path = nx.shortest_path(G, source, target)
        return f"Shortest path from {source} to {target}: {' → '.join(path)}"
    except nx.NetworkXNoPath:
        return f"No path found between '{source}' and '{target}'"
    except nx.NodeNotFound as e:
        return f"Node not found: {e}"

@tool
def get_all_nodes() -> str:
    """Get a list of all nodes in the graph"""
    nodes = list(G.nodes())
    return f"All nodes in the graph: {', '.join(nodes)}"

@tool
def node_degree(node: str) -> str:
    """Get the degree (number of connections) of a node"""
    if node in G:
        degree = G.degree(node)
        return f"{node} has {degree} connection(s)"
    return f"Node '{node}' not found in the graph"

@tool
def get_relationship(node1: str, node2: str) -> str:
    """Get the type of relationship between two specific nodes"""
    if node1 not in G:
        return f"Node '{node1}' not found in the graph"
    if node2 not in G:
        return f"Node '{node2}' not found in the graph"
    
    if G.has_edge(node1, node2):
        relation = G[node1][node2].get('relation', 'connected')
        return f"{node1} and {node2} are {relation}"
    return f"No direct relationship found between {node1} and {node2}"

@tool
def get_friends(node: str) -> str:
    """Get all friends of a specific node"""
    if node not in G:
        return f"Node '{node}' not found in the graph"
    
    friends = []
    for neighbor in G.neighbors(node):
        relation = G[node][neighbor].get('relation', 'connected')
        if relation == 'friend':
            friends.append(neighbor)
    
    if friends:
        return f"{node}'s friends: {', '.join(friends)}"
    return f"{node} has no friends in the graph"

@tool
def get_family(node: str) -> str:
    """Get all family members of a specific node"""
    if node not in G:
        return f"Node '{node}' not found in the graph"
    
    family = []
    for neighbor in G.neighbors(node):
        relation = G[node][neighbor].get('relation', 'connected')
        if relation == 'family':
            family.append(neighbor)
    
    if family:
        return f"{node}'s family: {', '.join(family)}"
    return f"{node} has no family members in the graph"

@tool
def add_edge(source: str, target: str, relation: str = "connected") -> str:
    """Add a new edge (relationship) between two nodes"""
    G.add_edge(source, target, relation=relation)
    return f"Added edge: {source} --[{relation}]--> {target}"

# Tool registry
tools = [get_neighbors, shortest_path, get_all_nodes, node_degree, get_relationship, get_friends, get_family, add_edge]
tools_by_name = {t.name: t for t in tools}

# ----------------------------
# 3. Model Setup with Tool Binding
# ----------------------------
@st.cache_resource
def init_model():
    """Initialize Ollama model with tools"""
    model = ChatOllama(model="llama3.1:8b", temperature=0)
    return model.bind_tools(tools)

model_with_tools = init_model()

# ----------------------------
# 4. Graph Visualization
# ----------------------------
def create_graph_visualization():
    """Create an interactive graph visualization using pyvis"""
    net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white", notebook=True)
    net.force_atlas_2based()
    
    # Add nodes with colors
    for node in G.nodes():
        net.add_node(node, label=node, color="#00ff1e", size=25)
    
    # Add edges with labels
    for source, target, data in G.edges(data=True):
        relation = data.get('relation', 'connected')
        net.add_edge(source, target, title=relation, label=relation, color="#ffffff")
    
    # Generate HTML directly (notebook mode inlines everything)
    html = net.generate_html(notebook=True)
    
    return html

# ----------------------------
# 5. Chat Handler with Tool Calling
# ----------------------------
def process_message(user_message: str, chat_history: list):
    """Process user message with tool calling support"""
    
    # Add system message if this is the first message
    if len(chat_history) == 0:
        chat_history.append(SystemMessage(
            content="""You are a helpful assistant that answers questions about relationships and connections between people.

IMPORTANT GUIDELINES:
1. Always analyze the user's question carefully to understand what information they're seeking
2. Use the available tools to find accurate information - never guess or make assumptions
3. If you're unsure about what the user is asking, politely request clarification
4. Respond naturally and conversationally - do not mention "tools", "knowledge graphs", or technical implementation details
5. Base your answers solely on the information retrieved from the tools

Your goal is to provide helpful, accurate answers while maintaining a friendly, human-like conversation."""
        ))
    
    # Add user message
    chat_history.append(HumanMessage(content=user_message))
    
    # Get response from model
    response = model_with_tools.invoke(chat_history)
    chat_history.append(response)
    
    # If there are tool calls, execute them
    while hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # Execute the tool
            tool = tools_by_name[tool_name]
            tool_result = tool.invoke(tool_args)
            
            # Add tool result to history
            chat_history.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))
        
        # Get next response from model
        response = model_with_tools.invoke(chat_history)
        chat_history.append(response)
    
    return chat_history

# ----------------------------
# 6. Streamlit UI
# ----------------------------
def main():
    st.set_page_config(page_title="Knowledge Graph Chatbot", layout="wide", page_icon="🕸️")
    
    st.title("🕸️ Knowledge Graph Chatbot")
    st.markdown("Ask questions about the graph, find paths, explore connections!")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("💬 Chat")
        
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                role = msg["role"]
                content = msg["content"]
                
                if role == "user":
                    with st.chat_message("user"):
                        st.write(content)
                elif role == "assistant":
                    with st.chat_message("assistant"):
                        st.write(content)
                elif role == "tool":
                    with st.expander("🔧 Tool Call", expanded=False):
                        st.code(content)
        
        # Chat input
        if prompt := st.chat_input("Ask about the graph..."):
            # Add user message to display
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.spinner("Thinking..."):
                # Process with tool calling
                st.session_state.chat_history = process_message(
                    prompt, 
                    st.session_state.chat_history
                )
                
                # Extract assistant's final response
                last_msg = st.session_state.chat_history[-1]
                if isinstance(last_msg, AIMessage):
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": last_msg.content
                    })
                
                # Show tool calls if any
                for msg in st.session_state.chat_history[-10:]:  # Last few messages
                    if isinstance(msg, ToolMessage):
                        st.session_state.messages.append({
                            "role": "tool",
                            "content": msg.content
                        })
            
            st.rerun()
        
        # Clear button
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()
    
    with col2:
        st.subheader("🕸️ Knowledge Graph")
        
        # Graph stats
        st.info(f"**Nodes:** {G.number_of_nodes()} | **Edges:** {G.number_of_edges()}")
        
        # Visualize graph
        graph_html = create_graph_visualization()
        st.components.v1.html(graph_html, height=520)
        
        # Graph info
        with st.expander("📊 Graph Details", expanded=False):
            st.write("**All Nodes:**", ", ".join(list(G.nodes())))
            st.write("**All Edges:**")
            for source, target, data in G.edges(data=True):
                relation = data.get('relation', 'connected')
                st.write(f"- {source} --[{relation}]--> {target}")
    
    # Sidebar with examples
    with st.sidebar:
        st.header("💡 Example Queries")
        st.markdown("""
        Try asking:
        - "Who are Alice's neighbors?"
        - "What is the shortest path from Alice to Charlie?"
        - "Show me all nodes in the graph"
        - "How many connections does Bob have?"
        - "Add an edge between Alice and Eve with relation mentor"
        """)
        
        st.header("🛠️ Available Tools")
        for tool in tools:
            st.write(f"**{tool.name}**")
            st.caption(tool.description)

# ----------------------------
# Entry Point
# ----------------------------
if __name__ == "__main__":
    main()