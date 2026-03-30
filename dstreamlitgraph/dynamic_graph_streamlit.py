import streamlit as st
import networkx as nx 
from pyvis.network  import Network
import tempfile


# Init graph as a singletone  object in session 
if "graph" not in st.session_state:
    st.session_state.graph = nx.DiGraph()
    
Graph = st.session_state.graph 

st.title("Dynamic Knowledge graph")


# Define node types and their colors
NODE_TYPES = {
    "Person": "#FF5733",
    "Organization": "#33C1FF",
    "Concept": "#33FF57",
    "Event": "#FFC300"
}

node_name = st.text_input("Enter node name")
node_type = st.selectbox("Select node type", list(NODE_TYPES.keys()))

if st.button("Add node"):
    if node_name:
        Graph.add_node(node_name, type=node_type, color=NODE_TYPES[node_type])
        
        
source = st.text_input("Source")
target = st.text_input("Target")

if st.button("Add edge"):
    if source and target:
        Graph.add_edge(source,target)
        

# Generate visualizationo 


net = Network(height="500px", width="100%", directed=True)

for node, data in Graph.nodes(data=True):
    node_color = data.get("color", "#97C2FC")
    node_type = data.get("type", "")
    net.add_node(node, label=node, color=node_color, title=f"Type: {node_type}")

for edge in Graph.edges:
    net.add_edge(edge[0], edge[1])
    

# build a temp file 
tmp_file = tempfile.NamedTemporaryFile(delete=False,suffix=".html")
net.save_graph(tmp_file.name)

st.components.v1.html(open(tmp_file.name).read(),height=500)