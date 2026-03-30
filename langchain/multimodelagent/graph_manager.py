# graph_manager.py
"""
Manages the agent graph using NetworkX
"""
import networkx as nx

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_agent(self, agent):
        self.graph.add_node(agent.agent_id, **agent.to_node_attrs())
        if agent.parent_id:
            self.graph.add_edge(agent.parent_id, agent.agent_id)

    def update_agent(self, agent):
        for k, v in agent.to_node_attrs().items():
            self.graph.nodes[agent.agent_id][k] = v

    def get_agent(self, agent_id):
        return self.graph.nodes[agent_id]

    def get_graph(self):
        return self.graph
