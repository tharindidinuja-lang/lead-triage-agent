# nodes/validation.py
import re
from state import LeadState

def validation_node(state: LeadState) -> dict:
    print("\n--- [6] VALIDATION NODE ---")
    draft = state["draft_response"]
    validation_status = True
    
    # PII check: phone numbers or credit cards
    if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', draft) or re.search(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', draft):
        validation_status = False
        print("  [FAILED] Validation Failed: PII detected in draft.")
    
    # Hallucinated pricing check
    if "$" in draft and not any("$" in str(r.get("result", "")) for r in state["tool_results"]):
        if "price" in draft.lower() or "cost" in draft.lower():
            validation_status = False
            print("  [FAILED] Validation Failed: AI invented pricing without KB source.")
    
    if validation_status:
        print("  [PASSED] Validation Passed.")
    
    return {"validation_status": validation_status}