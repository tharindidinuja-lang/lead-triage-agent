# nodes/human_review.py
from state import LeadState
from utils import get_message_content

def human_review_routing_node(state: LeadState) -> dict:
    print("\n--- [8] HUMAN REVIEW ROUTING ---")
    print("[WARNING] HUMAN REVIEW REQUIRED")
    print(f"  Original Lead: {get_message_content(state['messages'][-1])}")

    print(f"  AI Draft Reply: {state['draft_response']}")
    print(f"  Risk Level: {state['risk_level']}")
    
    if state["risk_level"] == "high":
        print("  >> ACTION: Escalating to manager (AI blocked).")
        return {"final_action": "human_escalate", "draft_response": "[BLOCKED - Human Escalation Needed]"}
    else:
        print("  >> ACTION: Human reviewer approved draft.")
        return {"final_action": "auto_reply", "human_feedback": "Approved by human (simulated)."}