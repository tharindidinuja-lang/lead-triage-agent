from typing import TypedDict, List, Optional, Literal, Annotated
from langgraph.graph.message import add_messages

class LeadState(TypedDict):
    # Core input (uses LangGraph's built-in message reducer)
    messages: Annotated[List[dict], add_messages]
    
    # Classifier output
    intent: Literal["sales_inquiry", "support_issue", "spam", "urgent_order"]
    urgency_score: int      # 1-5
    lead_score: int         # 1-10
    
    # Planning & Tools
    plan: List[str]         # e.g., ["search_kb", "lookup_crm"]
    tool_calls: List[dict]
    tool_results: List[dict]
    
    # Response & Safety
    draft_response: str
    validation_status: bool
    risk_level: Literal["low", "medium", "high"]
    human_feedback: Optional[str]
    
    # Control flow
    retry_count: int
    final_action: Literal["auto_reply", "human_escalate", "block"]