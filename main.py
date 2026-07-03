import sys
from graph_builder import build_graph
from state import LeadState
from utils import setup_logger

# Initialize logger
logger = setup_logger("Main")

def run_demo():
    logger.info("=" * 60)
    logger.info(" LEAD TRIAGE AGENT - LangGraph Demo")
    logger.info("=" * 60)
    
    agent = build_graph()
    
    samples = [
        {
            "name": "Sample 1: High Urgency + High Risk",
            "message": "I'm the CTO of FinTech Corp. Your platform crashed during our pilot. We have 200 users waiting. Fix this NOW or we cancel our $50k contract."
        },
        {
            "name": "Sample 2: FAQ / Low Priority",
            "message": "Hi, what are your office hours on weekends?"
        },
        {
            "name": "Sample 3: Strong Sales Lead",
            "message": "Hi, we're a team of 15 designers looking for a yearly subscription. Need collaborative editing. Please send us a custom quote and a demo link."
        }
    ]
    
    for i, sample in enumerate(samples, 1):
        logger.info(f"\n--- SAMPLE {i}: {sample['name']} ---")
        logger.info(f"Input: {sample['message']}")
        
        initial_state: LeadState = {
            "messages": [{"role": "user", "content": sample["message"]}],
            "intent": "support_issue",
            "urgency_score": 0,
            "lead_score": 0,
            "plan": [],
            "tool_calls": [],
            "tool_results": [],
            "draft_response": "",
            "validation_status": False,
            "risk_level": "low",
            "human_feedback": None,
            "retry_count": 0,
            "final_action": "auto_reply"
        }
        
        # MemorySaver requires a thread_id in the config
        config = {"configurable": {"thread_id": f"demo_thread_{i}"}}
        final_state = agent.invoke(initial_state, config=config)
        
        logger.info(f"Final Action: {final_state['final_action']}")
        logger.info(f"Final Reply: {final_state['draft_response'][:200]}...")
        logger.info("-" * 40)

if __name__ == "__main__":
    run_demo()
