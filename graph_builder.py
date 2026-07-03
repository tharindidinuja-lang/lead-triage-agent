# graph_builder.py
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver   # ✅ Correct import

from state import LeadState
from nodes import (
    classifier_node,
    planner_node,
    tool_decision_node,
    tool_execution_node,
    response_generation_node,
    validation_node,
    risk_check_node,
    human_review_routing_node
)

# ---------- CONDITIONAL EDGES ----------
def check_validation_retry(state: LeadState) -> Literal["pass", "retry", "fail"]:
    if state["validation_status"]:
        return "pass"
    elif state.get("retry_count", 0) < 2:
        state["retry_count"] = state.get("retry_count", 0) + 1
        return "retry"
    else:
        return "fail"

def check_risk_route(state: LeadState) -> Literal["human_review", "end"]:
    if state["risk_level"] in ["medium", "high"]:
        return "human_review"
    return "end"

# ---------- BUILD GRAPH ----------
def build_graph():
    workflow = StateGraph(LeadState)

    # Add all nodes (imported from nodes/)
    workflow.add_node("classifier", classifier_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("tool_decision", tool_decision_node)
    workflow.add_node("tool_execution", tool_execution_node)
    workflow.add_node("response_generation", response_generation_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("risk_check", risk_check_node)
    workflow.add_node("human_review", human_review_routing_node)

    # Set entry
    workflow.set_entry_point("classifier")

    # Edges
    workflow.add_edge("classifier", "planner")
    workflow.add_edge("planner", "tool_decision")
    workflow.add_edge("tool_decision", "tool_execution")
    workflow.add_edge("tool_execution", "response_generation")
    workflow.add_edge("response_generation", "validation")

    # Conditional: validation -> risk_check / retry / human_review
    workflow.add_conditional_edges(
        "validation",
        check_validation_retry,
        {
            "pass": "risk_check",
            "retry": "planner",
            "fail": "human_review"
        }
    )

    # Conditional: risk_check -> human_review or END
    workflow.add_conditional_edges(
        "risk_check",
        check_risk_route,
        {
            "human_review": "human_review",
            "end": END
        }
    )

    workflow.add_edge("human_review", END)

    return workflow.compile(checkpointer=MemorySaver())