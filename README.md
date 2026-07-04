---
title: AI Agent Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
python_version: "3.10"
---

# 🤖 AI Agent Chatbot

A tool-calling AI agent built with **smolagents**, powered by a Groq-hosted LLM (`openai/gpt-oss-120b`), wrapped in a **Gradio** chat interface. The agent reasons step-by-step over each user query and autonomously decides which tool to call — math, web search, Wikipedia lookup, or CSV data analysis — before returning a final answer.

**🔗 Live Demo:** https://huggingface.co/spaces/Tomyokesh33/ai-agent-chatbot

## Features

- **Tool-calling agent** (`ToolCallingAgent`) that reasons step-by-step and picks the right tool for each query
- **6 integrated tools:**
  - `calculator` — evaluates math expressions
  - `web_search` — live web search for current information
  - `wikipedia_lookup` — fetches Wikipedia summaries
  - `explore_csv` — inspects shape, columns, dtypes, and sample rows of a CSV
  - `query_csv` — filters/queries rows from a CSV
  - `aggregate_csv` — group-by aggregations (mean, sum, count, etc.) on a CSV
- **Fault-tolerant execution** — automatic retry logic plus a step-callback-based fallback that recovers the last successful tool result if the LLM produces a malformed final-answer call, so the user still gets a correct answer instead of an error
- **Fast inference** via Groq's LPU-hosted `openai/gpt-oss-120b` model
- **Production deployment** on HuggingFace Spaces with environment-variable-based secrets management (no API keys ever committed to source control)

## Tech Stack

| Layer | Technology |
|---|---|
| Agent framework | [smolagents](https://github.com/huggingface/smolagents) (`ToolCallingAgent`) |
| LLM | `openai/gpt-oss-120b` via [Groq](https://groq.com) Inference API |
| UI | [Gradio](https://gradio.app) `ChatInterface` |
| Deployment | [HuggingFace Spaces](https://huggingface.co/spaces) |
| Language | Python 3.10 |

## Architecture

```
User query
   │
   ▼
ToolCallingAgent (reasoning loop, max 5 steps)
   │
   ├─▶ selects a tool (calculator / web_search / wikipedia_lookup / explore_csv / query_csv / aggregate_csv)
   ├─▶ executes the tool, observes the result
   └─▶ synthesizes a final_answer
   │
   ▼
Gradio ChatInterface → response returned to user
```

If the LLM fails to call `final_answer` correctly on the first attempt, the app retries once, then falls back to the last successful tool observation captured via a step callback — so a transient LLM formatting error never surfaces as a broken response.

## Setup Locally

```bash
git clone https://github.com/yogeshwaran142/hf-agent-chatbot.git
cd hf-agent-chatbot
pip install -r requirements.txt
```

Get a free Groq API key: https://console.groq.com/keys

Create a `.env` file in the project root:
```
GROQ_API_KEY=gsk_your_key_here
```

Run the app:
```bash
python app.py
```

## Example Queries

- `What is 245 * 89 + 12?`
- `Explore the CSV at AI_Job_Market_Trends_2026.csv`
- `What's the weather forecast for Melbourne today?`

## Project Structure

```
hf-agent-chatbot/
├── app.py                          # Gradio UI, agent orchestration, error recovery
├── tools.py                        # Custom tool definitions (calculator, web_search, CSV tools, etc.)
├── requirements.txt                 # Python dependencies
├── .env.example                    # Template for required environment variables
└── AI_Job_Market_Trends_2026.csv   # Sample dataset for CSV tool demos
```

## Author

**Yogeshwaran J**
[GitHub](https://github.com/yogeshwaran142) · [LinkedIn](https://linkedin.com/in/yogeshwaran-j15811)
