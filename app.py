"""
AI Agent Chatbot — Groq + smolagents + Gradio
Run: python app.py
"""

import os
from dotenv import load_dotenv
import gradio as gr
from smolagents import ToolCallingAgent, OpenAIServerModel
import pandas as pd

from tools import calculator, web_search, wikipedia_lookup, explore_csv, query_csv, aggregate_csv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "llama-3.1-8b-instant"

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "1) Get a free key from https://console.groq.com/keys\n"
        "2) Add it to .env as GROQ_API_KEY=gsk_xxxx"
    )

model = OpenAIServerModel(
    model_id=MODEL_ID,
    api_base="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)

agent = ToolCallingAgent(
    tools=[calculator, web_search, wikipedia_lookup, explore_csv, query_csv, aggregate_csv],
    model=model,
    max_steps=3,
)


import re
import time


def _extract_answer_from_error(error_text: str):
    """Some models occasionally wrap the final answer in a malformed
    nested tool call instead of calling final_answer correctly. If that
    happens, pull the actual answer straight out of the error text
    instead of failing."""
    match = re.search(r'"answer"\s*:\s*"([^"]*)"', error_text)
    if match:
        return match.group(1)
    return None


def respond(message, history):
    for attempt in range(2):
        try:
            return str(agent.run(message))
        except Exception as e:
            recovered = _extract_answer_from_error(str(e))
            if recovered:
                return recovered
            if attempt == 0:
                time.sleep(2)
                continue
            return f"⚠️ That attempt failed: {e}\n\nPlease try asking again."

demo = gr.ChatInterface(
    fn=respond,
    type="messages",
    title="🚀 THE ZOARA AI 🤖",
    description=f"Powered by **{MODEL_ID}** via Groq. Math, web search, Wikipedia, and CSV analysis.",
    examples=[
        "What is 245 * 89 + 12?",
        "Explore the CSV at AI_Job_Market_Trends_2026.csv",
    ],
    cache_examples=False,
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)