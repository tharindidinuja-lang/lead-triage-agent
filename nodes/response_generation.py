# nodes/response_generation.py
import os
from config import OPENAI_API_KEY, MODEL_NAME
from state import LeadState
from utils import get_message_content, OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# Load the prompt template from the text file
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
with open(os.path.join(PROMPT_DIR, "response_gen_prompt.txt"), "r") as f:
    RESPONSE_PROMPT_TEMPLATE = f.read()

def response_generation_node(state: LeadState) -> dict:
    print("\n--- [5] RESPONSE GENERATION NODE ---")
    last_msg = get_message_content(state["messages"][-1])
    tool_context = "\n".join([f"{r['tool']}: {r['result']}" for r in state["tool_results"]])
    
    # Inject all variables into the template
    prompt = RESPONSE_PROMPT_TEMPLATE.format(
        message=last_msg,
        context=tool_context if tool_context else "No additional context.",
        intent=state["intent"],
        urgency=state["urgency_score"],
        lead_score=state["lead_score"]
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    
    draft = response.choices[0].message.content
    print(f"  Draft: {draft[:100]}...")
    return {"draft_response": draft}
