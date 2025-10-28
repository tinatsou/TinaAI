# TinaAI

**An Experimental Collection of AI Projects: Edge, Cloud & Creativity**

TinaAI is a sandbox that brings together multiple AI driven experiments exploring creativity, reasoning, and intelligent automation, from personal productivity tools to distributed AI edge platforms.

---

## 🧩 Projects in This Repository

### 🧠 AI Agent Platform
**Edge & Open Source Focus**  
Integrates **LlamaIndex** with edge AI components to enable retrieval augmented workflows and robotic/voice interfaces.  
Includes backend APIs, data orchestration, and distributed cloud support for open-source ecosystems.

Folder: [`ai-agent-platform/`](./ai-agent-platform)

---

### ✈️ Travel Planner
An AI travel assistant that builds itineraries based on destination, season, and user preferences.  
Combines structured travel data, weather APIs, and LLM reasoning.

Folder: [`Travel planner/`](./Travel%20planner)

---

### 📖 ChatGPT Storytelling
An interactive story generator powered by prompt chaining and user feedback loops.  
Explores creative writing with character memory and adaptive tone.

Folder: [`chatgpt_storytelling/`](./chatgpt_storytelling)

---

### 💰 Expense Tracker
A smart ledger that uses natural language input and classification to organize personal expenses.  
Supports JSON export and quick analytics.

Folder: [`expense_tracker/`](./expense_tracker)

---

## 🧱 Tech Stack
- **Python 3.10+**
- **LlamaIndex** and **LangChain**
- **FastAPI** for backend components
- **OpenAI / Ollama** for model endpoints
- **PostgreSQL / pgVector** for vectorized retrieval
- **Edge orchestration** via distributed microservices

---

## 🚀 Quick Start
```bash
git clone https://github.com/tinatsou/TinaAI.git
cd TinaAI/ai-agent-platform
pip install -r requirements.txt
python backend/api.py
