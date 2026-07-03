# 🤖 AI Lead & Message Triage Agent

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Tests](https://img.shields.io/badge/tests-pytest-yellow.svg)](https://docs.pytest.org/)

An intelligent AI agent that triages incoming sales leads and customer messages from WhatsApp, Instagram, website forms, and email. Built with **LangGraph** and **Streamlit**, this prototype automatically classifies intent, detects urgency, validates responses for hallucinations/PII, and routes high-risk cases to human review.

> **Submitted for:** Catalist Media - Agent Prototyping Intern Builder Challenge

---

## 📌 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)


---

## 📖 Overview

Small businesses struggle to manage leads scattered across multiple channels. This agent solves that by:

1. **Classifying** incoming messages (Sales, Support, Spam, Urgent).
2. **Scoring** urgency (1-5) and lead value (1-10).
3. **Searching** internal knowledge bases or the web (via Tavily) for answers.
4. **Looking up** lead history in a mock CRM.
5. **Drafting** intelligent replies using Google Gemini (or any LLM).
6. **Validating** drafts for PII (phone numbers, emails) and factual hallucinations.
7. **Routing** high-risk messages (e.g., "cancel", "refund", high-value quotes) to human review.

---

## 🏗️ Architecture

The agent is built as a directed graph using **LangGraph**:

```mermaid
flowchart TD
    A[User Input] --> B[Classifier Node]
    B --> C[Planner Node]
    C --> D[Tool Decision Node]
    D --> E[Tool Execution Node]
    E --> F[Response Generation Node]
    F --> G[Validation Node]
    G -->|Pass| H[Risk Check Node]
    G -->|Retry| C
    G -->|Fail| I[Human Review]
    H -->|Low Risk| J[Auto Reply]
    H -->|Medium/High Risk| I
    I --> K[Escalate / Approve]
