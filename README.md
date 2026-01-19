# MCP_assignment

A **read-only corporate AI assistant** built using **LangChain** and **FastMCP**, designed to retrieve and summarize internal corporate data stored in a **SQLite database** via **MCP (JSON-RPC over stdio)**.

---

## 📑 Table of Contents
- Features
- Installation
- Configuration
- Usage
- Tools & Capabilities
- Learning Outcomes

---

## ✨ Features

- LangChain-based AI agent with a structured system prompt
- FastMCP server exposing approved internal tools
- SQLite-backed corporate data store (read-only)
- JSON-RPC communication over `stdio`
- Centralized, **stdio-safe logging** (logs to file and `stderr`)
- Robust error handling with full stack traces
- Professional, factual, corporate-safe responses

---

## 🛠 Installation

### 1. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install langchain fastmcp langchain-google-genai python-dotenv
```

---

## ⚙️ Configuration

### 1. API Credentials

Create a `.env` file:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

### 2. Model Configuration

Update `config.py`:

```python
MODEL_ID = "gemini-1.5-pro"
TEMPERATURE = 0.2
TOP_P = 0.95
TOP_K = 40
MAX_TOKEN = 1024
```

### 3. Logging

Logging is centrally configured in `logger_config.py`:

- Rotating file logs (`agent_app.log`)
- Console logs directed to **stderr only**
- Safe for MCP / JSON-RPC over `stdio`

---

## ▶️ Usage

### Step 1: Start the FastMCP Server

```bash
python corporate_mcp_server.py
```

### Step 2: Run the Client Application

```bash
python main.py
```

---

## 🧰 Tools & Capabilities

### Available Tools

- **search_documents**
- **query_employees**
- **get_department_stats**

---

## 🎓 Learning Outcomes

- LangChain agent design
- FastMCP & MCP protocol usage
- JSON-RPC over stdio
- Stdio-safe logging
- Async Python architecture
- Production-grade error handling