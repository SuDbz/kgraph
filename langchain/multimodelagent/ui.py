# ui.py
"""
Streamlit UI for multi-agent system
"""
import streamlit as st
import networkx as nx
from pyvis.network import Network

def render_input():
    st.title("Multi-Agent System")
    user_query = st.text_area("Enter your query")
    if st.button("Start Execution"):
        st.session_state["start_execution"] = True
        st.session_state["user_query"] = user_query
    return st.session_state.get("start_execution", False), st.session_state.get("user_query", "")

def render_status(agent_count, active_agents, logs):
    st.subheader("Live Execution View")
    st.write(f"Current agent count: {agent_count}")
    st.write(f"Active agents: {active_agents}")
    st.write("Logs:")
    for log in logs:
        st.write(log)

def render_graph(graph):
    st.subheader("Agent Graph")
    net = Network(height="500px", width="100%", directed=True)
    color_map = {"running": "#FFD700", "completed": "#32CD32"}
    for node, data in graph.nodes(data=True):
        color = color_map.get(data.get("status", "running"), "#97C2FC")
        label = data.get("task", data.get("agent_id", ""))
        title = f"ID: {data.get('agent_id', '')}<br>Task: {data.get('task', '')}<br>Status: {data.get('status', '')}<br>Depth: {data.get('depth', '')}"
        net.add_node(node, label=label, color=color, title=title)
    for edge in graph.edges:
        net.add_edge(edge[0], edge[1])
    tmp_file = "tmp_graph.html"
    net.save_graph(tmp_file)
    st.components.v1.html(open(tmp_file).read(), height=500)

def render_results(graph):
    st.subheader("Results")
    for node, data in graph.nodes(data=True):
        with st.expander(f"Agent {data.get('agent_id', '')}"):
            st.write(f"Task: {data.get('task', '')}")
            st.write(f"Result: {data.get('result', '')}")
            st.write(f"Status: {data.get('status', '')}")
            st.write(f"Depth: {data.get('depth', '')}")
