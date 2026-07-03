# nodes/classifier.py
import json
import os
from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE
from state import LeadState
from utils import get_logger, get_message_content, OpenAI


logger = get_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

# Load the prompt template from the text file
PROMPT_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
with open(os.path.join(PROMPT_DIR, "classifier_prompt.txt"), "r") as f:
    CLASSIFIER_PROMPT_TEMPLATE = f.read()

def classifier_node(state: LeadState) -> dict:
    logger.info("--- [1] CLASSIFIER NODE ---")
    last_msg = get_message_content(state["messages"][-1])
    
    # Inject the message into the template
    prompt = CLASSIFIER_PROMPT_TEMPLATE.format(message=last_msg)

    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        response_format={"type": "json_object"}
    )
    
    result = json.loads(response.choices[0].message.content)
    
    logger.info(f"  Intent: {result['intent']}, Urgency: {result['urgency_score']}, Lead Score: {result['lead_score']}")
    logger.debug(f"  Full LLM Response: {response}")
    
    return {
        "intent": result["intent"],
        "urgency_score": result["urgency_score"],
        "lead_score": result["lead_score"],
        "retry_count": 0
    }

