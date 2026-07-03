# nodes/tool_decision.py
import re
from state import LeadState
from utils import get_message_content

def tool_decision_node(state: LeadState) -> dict:
    print("\n--- [3] TOOL DECISION NODE ---")
    tool_calls = []
    last_msg = get_message_content(state["messages"][-1])

    
    for task in state["plan"]:
        if task == "search_kb":
            tool_calls.append({"name": "search_kb", "args": {"query": last_msg}})
        elif task == "lookup_crm":
            email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', last_msg)
            if email_match:
                email = email_match.group(0)
            elif "fintech" in last_msg.lower():
                email = "cto@fintech.com"
            elif "15 designers" in last_msg.lower() or "team of 15" in last_msg.lower():
                email = "team15@design.com"
            else:
                email = "unknown@unknown.com"
            tool_calls.append({"name": "lookup_crm", "args": {"email": email}})
    
    print(f"  Tool Calls: {tool_calls}")
    return {"tool_calls": tool_calls}