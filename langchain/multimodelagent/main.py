# main.py
"""
Main entry for multi-agent system (LangChain + Ollama + NetworkX + Streamlit)
"""
import streamlit as st
from agent import Agent
from graph_manager import GraphManager
from ui import render_input, render_status, render_graph, render_results
import json
import time
from langchain_community.llms import Ollama

# Constants
MAX_AGENTS = 60
MAX_DEPTH = 6
MAX_CHILDREN = 2

llm = Ollama(model="llama3")

# Simulate LLM call (replace with LangChain+Ollama integration)
def call_llm(task, depth):
    prompt = f"""
    You are an intelligent task agent.

    Task: {task}
    Depth: {depth}

    Rules:
    - If task is simple → solve directly
    - If complex → split into at most 2 subtasks
    - Avoid unnecessary recursion
    - Be concise and efficient

    Return ONLY valid JSON:
    {{
      "action": "solve" or "split",
      "subtasks": []
    }}
    """
    response = llm.invoke(prompt)
    return response

def agent_executor(agent, graph_manager, logs, agent_count, depth):
    if agent_count[0] >= MAX_AGENTS or depth > MAX_DEPTH:
        agent.complete("Limit reached or max depth")
        graph_manager.update_agent(agent)
        logs.append(f"Agent {agent.agent_id} stopped: limit/depth.")
        # Remove agent from graph
        graph_manager.graph.remove_node(agent.agent_id)
        return
    try:
        response = call_llm(agent.task, agent.depth)
        data = json.loads(response)
        action = data.get("action")
        if action == "split" and agent.depth < MAX_DEPTH:
            subtasks = data.get("subtasks", [])[:MAX_CHILDREN]
            for subtask in subtasks:
                if agent_count[0] >= MAX_AGENTS:
                    break
                child = Agent(subtask, agent.depth+1, parent_id=agent.agent_id)
                agent.add_child(child)
                graph_manager.add_agent(child)
                agent_count[0] += 1
                logs.append(f"Spawned agent {child.agent_id} for subtask '{subtask}'")
                agent_executor(child, graph_manager, logs, agent_count, depth+1)
            agent.complete("Subtasks completed.")
        else:
            agent.complete(f"Solved: {agent.task}")
        graph_manager.update_agent(agent)
        logs.append(f"Agent {agent.agent_id} completed.")
        # Remove agent from graph
        graph_manager.graph.remove_node(agent.agent_id)
    except Exception as e:
        agent.complete(f"Error: {e}")
        graph_manager.update_agent(agent)
        logs.append(f"Agent {agent.agent_id} error: {e}")
        # Remove agent from graph
        graph_manager.graph.remove_node(agent.agent_id)

def main():
    st.set_page_config(layout="wide")
    started, user_query = render_input()
    if started and user_query:
        graph_manager = GraphManager()
        logs = []
        agent_count = [1]
        root = Agent(user_query, 0, parent_id=None)
        graph_manager.add_agent(root)
        logs.append(f"Root agent {root.agent_id} created.")
        agent_executor(root, graph_manager, logs, agent_count, 0)
        render_status(agent_count[0], agent_count[0], logs)
        render_graph(graph_manager.get_graph())
        render_results(graph_manager.get_graph())

if __name__ == "__main__":
    main()
