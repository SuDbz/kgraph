# agent.py
"""
Agent logic for multi-agent system (LangChain + Ollama + NetworkX)
"""
import uuid
import time

class Agent:
    def __init__(self, task, depth, parent_id=None):
        self.agent_id = str(uuid.uuid4())
        self.parent_id = parent_id
        self.depth = depth
        self.task = task
        self.status = "running"
        self.result = None
        self.start_time = time.time()
        self.end_time = None
        self.children = []

    def complete(self, result):
        self.status = "completed"
        self.result = result
        self.end_time = time.time()

    def add_child(self, child_agent):
        self.children.append(child_agent.agent_id)

    def to_node_attrs(self):
        return {
            "agent_id": self.agent_id,
            "parent_id": self.parent_id,
            "depth": self.depth,
            "task": self.task,
            "status": self.status,
            "result": self.result,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
