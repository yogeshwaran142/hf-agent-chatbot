"""
AI Agent Chatbot — Groq + smolagents + Gradio
Run: python app.py
"""

import os
from dotenv import load_dotenv
import gradio as gr
from smolagents import ToolCallingAgent, InferenceClientModel

from tools import calculator, web_search, wikipedia_lookup, explore_csv, query_csv, aggregate_csv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "openai/gpt-oss-120b"

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found.\n"
        "1) Get a free key from https://console.groq.com/keys\n"
        "2) Add it to .env as GROQ_API_KEY=gsk_xxxx"
    )

model = InferenceClientModel(model_id=MODEL_ID, provider="groq", token=GROQ_API_KEY)

_last_observation = {"value": None}

def _capture_step(memory_step, agent=None):
    obs = getattr(memory_step, "observations", None)
    if obs:
        _last_observation["value"] = str(obs)

agent = ToolCallingAgent(
    tools=[calculator, web_search, wikipedia_lookup, explore_csv, query_csv, aggregate_csv],
    model=model,
    max_steps=5,
    step_callbacks=[_capture_step],
)

import re
import time


def _extract_answer_from_error(error_text: str):
    match = re.search(r'"answer"\s*:\s*"([^"]*)"', error_text)
    if match:
        return match.group(1)
    return None

def _get_last_tool_observation(agent):
    """If the agent errors out after a tool already ran successfully,
    grab that tool's result directly from memory instead of failing."""
    try:
        for step in reversed(agent.memory.steps):
            obs = getattr(step, "observations", None)
            if obs:
                return str(obs)
    except Exception:
        pass
    return None

def respond(message, history):
    for attempt in range(2):
        _last_observation["value"] = None
        try:
            return str(agent.run(message))
        except Exception as e:
            error_str = str(e)
            print(f"DEBUG - Error caught: {error_str}")
            recovered = _extract_answer_from_error(error_str)
            if recovered:
                print(f"DEBUG - Recovered from error text: {recovered}")
                return recovered
            if _last_observation["value"]:
                print(f"DEBUG - Recovered from step callback: {_last_observation['value']}")
                return _last_observation["value"]
            if attempt == 0:
                time.sleep(2)
                continue
            return f"⚠️ That attempt failed: {e}\n\nPlease try asking again."

demo = gr.ChatInterface(
    fn=respond,
    title="🚀 THE ZOARA AI 🤖",
    description=f"Powered by **{MODEL_ID}** via Groq. Math, web search, Wikipedia, and CSV analysis.",
    examples=[
        "What is 245 * 89 + 12?",
        "Explore the CSV at AI_Job_Market_Trends_2026.csv",
    ],
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    demo.launch()