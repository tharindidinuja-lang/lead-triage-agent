# nodes/planner.py
import os
import json
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from state import LeadState
from utils import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# Load prompt from text file
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
with open(os.path.join(PROMPT_DIR, "planner_prompt.txt"), "r") as f:
    PLANNER_PROMPT_TEMPLATE = f.read()

def planner_node(state: LeadState) -> dict:
    print("\n--- [2] PLANNER NODE (LLM-powered) ---")
    
    # Format the prompt with classified data
    prompt = PLANNER_PROMPT_TEMPLATE.format(
        intent=state["intent"],
        urgency=state["urgency_score"],
        lead_score=state["lead_score"]
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,  # Low temp for deterministic planning
        response_format={"type": "json_object"}
    )
    
    try:
        result = json.loads(response.choices[0].message.content)
        # Handle both {"plan": [...]} and just [...] format
        if isinstance(result, list):
            plan = result
        elif isinstance(result, dict) and "plan" in result:
            plan = result["plan"]
        else:
            plan = ["draft_response"]  # Fallback
    except:
        # Fallback if the LLM fails
        plan = ["draft_response"]
    
    print(f"  LLM Generated Plan: {plan}")
    return {"plan": plan}
