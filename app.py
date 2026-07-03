# app.py
import streamlit as st
from graph_builder import build_graph
from state import LeadState

# Page configuration
st.set_page_config(page_title="AI Lead Triage Agent", layout="wide")
st.title("🤖 AI Lead & Message Triage Agent")
st.markdown("Paste a customer message below and let the AI analyze, prioritize, and route it.")

# Sidebar for instructions
with st.sidebar:
    st.header("⚙️ How it works")
    st.write("""
    1. **Classifier** – Identifies intent, urgency, and lead score.
    2. **Planner** – Decides which tools to use.
    3. **Tools** – Searches KB and looks up CRM.
    4. **Response Generator** – Drafts a reply.
    5. **Validator** – Checks for PII and hallucinations.
    6. **Risk Check** – Flags urgent or sensitive cases.
    7. **Human Review** – Blocks high-risk replies.
    """)
    
    st.divider()
    st.caption("Built with LangGraph + Streamlit")

# Main chat input
user_input = st.text_area(
    "📩 Paste the lead message here:",
    height=150,
    placeholder="e.g., I'm the CTO of FinTech Corp. Your platform crashed during our pilot..."
)

# Three sample buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📌 Sample 1 (Urgent)"):
        user_input = "I'm the CTO of FinTech Corp. Your platform crashed during our pilot. We have 200 users waiting. Fix this NOW or we cancel our $50k contract."
with col2:
    if st.button("📌 Sample 2 (FAQ)"):
        user_input = "Hi, what are your office hours on weekends?"
with col3:
    if st.button("📌 Sample 3 (Sales)"):
        user_input = "Hi, we're a team of 15 designers looking for a yearly subscription. Need collaborative editing. Please send us a custom quote and a demo link."

# Process button
if st.button("🔍 Analyze Lead", type="primary"):
    if not user_input.strip():
        st.warning("Please paste a message or click a sample button.")
    else:
        with st.spinner("🧠 Agent is processing..."):
            # Build the agent
            agent = build_graph()
            
            # Initialize state
            initial_state: LeadState = {
                "messages": [{"role": "user", "content": user_input}],
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
            
            # Run the agent
            final_state = agent.invoke(initial_state)
            
            # --- Display Results ---
            st.divider()
            st.subheader("📊 Analysis Results")
            
            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Intent", final_state["intent"].replace("_", " ").title())
            with col2:
                st.metric("Urgency", f"{final_state['urgency_score']}/5")
            with col3:
                st.metric("Lead Score", f"{final_state['lead_score']}/10")
            with col4:
                risk_color = "🟢" if final_state["risk_level"] == "low" else "🟡" if final_state["risk_level"] == "medium" else "🔴"
                st.metric("Risk Level", f"{risk_color} {final_state['risk_level'].upper()}")
            
            # Tool Results
            with st.expander("🔧 Tool Results", expanded=True):
                for tool in final_state.get("tool_results", []):
                    st.write(f"- **{tool['tool']}**: {tool['result']}")
            
            # AI Draft
            st.subheader("📝 AI Draft Reply")
            st.text_area("Draft Response", final_state["draft_response"], height=150)
            
            # Validation Status
            if final_state["validation_status"]:
                st.success("✅ Validation Passed (No PII or hallucinations detected)")
            else:
                st.error("❌ Validation Failed (PII or hallucination detected)")
            
            # Human Review Section
            if final_state["risk_level"] in ["medium", "high"]:
                st.subheader("👤 Human Review Required")
                st.warning(f"This message requires human review. Risk Level: **{final_state['risk_level'].upper()}**")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve & Send", key="approve"):
                        st.success("✅ Message approved and sent to customer!")
                        st.balloons()
                with col2:
                    if st.button("❌ Reject & Escalate", key="reject"):
                        st.error("❌ Message rejected. Escalating to manager.")
                
                if final_state["final_action"] == "human_escalate":
                    st.error("🚨 **Escalated to Manager** – AI reply was blocked.")
            else:
                st.success("✅ **Auto-replied** – No human review needed.")
            
            # Final Action
            st.caption(f"Final Action: `{final_state['final_action']}`")