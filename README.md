---
title: AI Agent Chatbot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# AI Agent Chatbot (Hugging Face + smolagents + Gradio)

A chatbot that isn't just a Q&A bot — it's an **agent**. It can decide on its
own when to do math, search the web, or look something up on Wikipedia,
then combine the results into an answer.

## Stack
- **Hugging Face Inference API** — the LLM brain (free tier works)
- **smolagents** — HF's official agent framework (handles the reasoning + tool-calling loop)
- **Gradio** — the chat UI

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Hugging Face token
cp .env.example .env
# then open .env and paste your token from https://huggingface.co/settings/tokens

# 3. Run it
python app.py
```

Gradio will print a local URL (usually `http://127.0.0.1:7860`) — open that in your browser.

## Project structure

```
hf-agent-chatbot/
├── app.py              # Gradio UI + agent wiring — run this
├── tools.py            # All tools the agent can use
├── requirements.txt
├── .env.example
└── README.md
```

## How the agent works

1. You send a message.
2. The agent (an LLM) reads it and decides: answer directly, or call a tool?
3. If a tool is needed (e.g. calculator), it calls it, reads the result, and repeats until it has a final answer.
4. `max_steps=6` in `app.py` caps how many tool calls it can make per question — raise this for more complex tasks.

## Adding your own tool

Open `tools.py` and follow the template at the bottom of the file:

```python
@tool
def my_tool(query: str) -> str:
    """
    One-line description of what this tool does.

    Args:
        query: description of this argument.

    Returns:
        description of what gets returned.
    """
    ...
    return "result"
```

Then add it to the `tools=[...]` list in `app.py`. The docstring is important —
the LLM reads it to decide when to use the tool.

## Swapping the model

Any Hugging Face model that supports tool/function calling works. Edit `MODEL_ID`
in `.env`, e.g.:
- `Qwen/Qwen2.5-72B-Instruct` (default)
- `meta-llama/Llama-3.3-70B-Instruct`
- `mistralai/Mistral-Small-24B-Instruct-2501`

## Common issues

| Problem | Fix |
|---|---|
| `HF_TOKEN not found` | Make sure `.env` exists (not just `.env.example`) and has your real token |
| 429 / rate limit errors | Free tier has rate limits — wait a bit or switch to a smaller model |
| Tool not being called | Check the tool's docstring is clear about *when* to use it |

## Next steps (matches your roadmap)

- Swap smolagents for **LangGraph** to build a multi-step / branching agent
- Add a custom tool that queries a database or CSV (great for your Data Analyst background)
- Deploy for free on **Hugging Face Spaces** (just push this folder + a `README.md` with Spaces metadata)
