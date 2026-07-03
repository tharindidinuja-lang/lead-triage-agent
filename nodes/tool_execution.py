# nodes/tool_execution.py
from state import LeadState
from tools import search_kb, lookup_crm, search_web

def tool_execution_node(state: LeadState) -> dict:
    print("\n--- [4] TOOL EXECUTION NODE ---")
    results = []
    
    for call in state["tool_calls"]:
        if call["name"] == "search_kb":
            res = search_kb(call["args"]["query"])
            results.append({"tool": "search_kb", "result": res})
        elif call["name"] == "lookup_crm":
            res = lookup_crm(call["args"]["email"])
            results.append({"tool": "lookup_crm", "result": res})
    
    print(f"  Tool Results: {results}")
    return {"tool_results": results}