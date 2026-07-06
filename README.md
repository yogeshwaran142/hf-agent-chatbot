---
title: AI Agent Chatbot
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "5.23.1"
app_file: app.py
pinned: false
---

# 🚀 AI Agent Chatbot — Groq + smolagents + Gradio

A tool-calling AI agent built from scratch that reasons step-by-step, calls the right tool for the job, and answers in natural language — powered by **Groq's `llama-3.1-8b-instant`** for fast inference.

**🔗 Live Demo:** [huggingface.co/spaces/Tomyokesh33/ai-agent-chatbot](https://huggingface.co/spaces/Tomyokesh33/ai-agent-chatbot)

---

## ✨ Features

- **Agentic reasoning** — uses [smolagents](https://github.com/huggingface/smolagents)' `ToolCallingAgent` to decide which tool to call, execute it, and synthesize a final answer
- **Conversation memory** — remembers recent chat context, so follow-up questions work naturally
- **Data analysis tools** — explore, query, and aggregate any CSV file directly through chat
- **Chart generation** — ask for a visualization and get a real bar chart rendered inline
- **Resilient by design** — automatic retries with exponential backoff, and recovery from malformed model outputs
- **Fast** — direct connection to Groq's OpenAI-compatible API (no extra routing hops)

## 🛠️ Tools Available to the Agent

| Tool | What it does |
|---|---|
| `calculator` | Safely evaluates math expressions |
| `web_search` | DuckDuckGo web search |
| `wikipedia_lookup` | Wikipedia article search |
| `explore_csv` | Inspects a CSV's shape, columns, dtypes, and sample rows |
| `query_csv` | Filters CSV rows using a pandas query expression |
| `aggregate_csv` | Group-by + aggregate (mean/sum/count/min/max) on a CSV column |
| `chart_csv` | Generates and returns a bar chart image from grouped/aggregated CSV data |

The bundled dataset is **AI Job Market Trends 2026** — ask things like:

- *"Explore the CSV at AI_Job_Market_Trends_2026.csv"*
- *"What's the average salary by experience level?"*
- *"Create a chart of average salary by experience_level"*

## 🏗️ Architecture

```
User message (Gradio ChatInterface)
        │
        ▼
  respond() ── builds task with recent chat context
        │
        ▼
  ToolCallingAgent (smolagents)
        │
        ├── reasons about which tool to call
        ├── executes tool (calculator / CSV tools / search / chart)
        └── synthesizes final answer
        │
        ▼
  OpenAIServerModel → Groq API (llama-3.1-8b-instant)
        │
        ▼
  Response rendered in chat (text or image)
```

## ⚙️ Setup

```bash
git clone https://github.com/yogeshwaran142/hf-agent-chatbot.git
cd hf-agent-chatbot
pip install -r requirements.txt
```

Create a `.env` file with your free [Groq API key](https://console.groq.com/keys):

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

Run locally:

```bash
python app.py
```

## 📦 Tech Stack

- **Agent framework:** smolagents (`ToolCallingAgent`)
- **LLM:** Groq — `llama-3.1-8b-instant` via `OpenAIServerModel`
- **UI:** Gradio `ChatInterface`
- **Data:** pandas
- **Visualization:** matplotlib
- **Deployment:** Hugging Face Spaces (Docker)

## 🙋 About

Built by **Yogeshwaran J** — B.Tech AI & Data Science graduate, exploring agentic AI and LLM tooling on top of core data analytics skills (Python, SQL, Power BI, Excel).

- 📧 yokesh15811@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/yogeshwaran-j15811)
- 🧑‍💻 [GitHub](https://github.com/yogeshwaran142)
- 🤗 [HuggingFace](https://huggingface.co/Tomyokesh33)
