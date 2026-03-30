# 🧠 Multi-Agent System Builder Prompt (LangChain + Ollama + NetworkX + Streamlit)

## 🎯 Objective

Build a hierarchical, dynamic multi-agent system using:

* LangChain for LLM orchestration
* Ollama for local model inference
* NetworkX for graph tracking
* Streamlit for UI visualization

---

## 🧩 Core Requirements

You must implement a system with the following behavior:

### 1. Root Agent

* Accepts a user query
* Decides whether to:

  * Solve directly OR
  * Decompose into subtasks
* Spawns child agents dynamically

---

### 2. Agent Hierarchy Rules

* Maximum total agents: **60**
* Maximum depth: **6 levels**
* Each agent can create **at most 2 sub-agents**
* Each agent must:

  * Have a unique ID (UUID)
  * Track parent-child relationships
  * Return results to parent

---

### 3. Dynamic Agent Behavior

Each agent must:

* Receive a **task-specific prompt**
* Decide:

  * `"solve"` → solve directly
  * `"split"` → break into subtasks
* Output MUST be valid JSON:

```json
{
  "action": "solve" | "split",
  "subtasks": ["subtask1", "subtask2"]
}
```

* Prompts must adapt based on:

  * task complexity
  * depth level
  * parent context

---

### 4. Graph Representation (NetworkX)

Use NetworkX to maintain a directed graph:

* Nodes represent agents
* Edges represent parent → child relationships

Each node must store:

* agent_id
* parent_id
* depth
* task
* status ("running", "completed")
* result
* start_time
* end_time

---

### 5. Execution Flow

* Root agent starts execution
* Agents recursively spawn children (if needed)
* All results propagate upward
* System must enforce limits strictly

---

### 6. Streamlit UI

Build an interactive UI that includes:

#### Input Section

* Text box for user query
* Button to start execution

#### Live Execution View

* Show current agent count
* Show active agents
* Display logs (agent creation, completion)

#### Graph Visualization

* Render NetworkX graph
* Show:

  * node labels (task or ID)
  * color by status
  * hierarchical layout if possible

#### Results Section

* Final aggregated output
* Expandable view for each agent’s result

---

### 7. Error Handling

* Prevent infinite recursion
* Handle invalid JSON from LLM safely
* Fallback to "solve" if parsing fails

---

### 8. Performance Constraints

* Avoid redundant agent creation
* Cache repeated tasks if possible
* Limit LLM calls when depth is high

---

## 🧠 Prompt Template for Each Agent

Each agent must use this decision prompt:

```
You are an intelligent task agent.

Task: {task}
Depth: {depth}

Rules:
- If task is simple → solve directly
- If complex → split into at most 2 subtasks
- Avoid unnecessary recursion
- Be concise and efficient

Return ONLY valid JSON:
{
  "action": "solve" or "split",
  "subtasks": []
}
```

---

## ⚙️ Tech Stack Constraints

* Use LangChain with Ollama (local model like llama3)
* Use NetworkX for graph
* Use Streamlit for UI
* Code must be modular:

  * agent.py
  * graph_manager.py
  * ui.py
  * main.py

---

## 🚀 Expected Output

A working application where:

* User enters a query
* System dynamically spawns agents
* Graph updates in real-time
* Final answer is composed from all agents

---

## 🔒 Constraints

* Max agents: 60
* Max depth: 6
* Max children per agent: 2
* Must not crash if limits are hit

---

## 💡 Bonus (Optional)

* Add agent roles (planner, executor, reviewer)
* Add caching layer
* Add streaming responses
* Save graph to file (JSON or GML)

---

## 🧪 Example Input

"Explain how black holes work and their effects on time"

## ✅ Expected Behavior

* Root splits into:

  * "What are black holes?"
  * "How do they affect time?"
* Sub-agents solve each
* Results combined into final answer

---

## 📌 Important Notes

* Prioritize stability over complexity
* Ensure reproducibility
* Keep logs for debugging
* Ensure clean UI updates in Streamlit

---

Build the full system following these specifications.
