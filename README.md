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
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)

---

# 🤖 AI Lead & Message Triage Agent

> **Submitted for:** Catalist Media - Agent Prototyping Intern Builder Challenge

---

## 📌 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)

---

## 📖 Overview

> [!NOTE]
> **What does this agent do?**  
> Small businesses struggle to manage leads scattered across WhatsApp, Instagram, email, and web forms.  
> This AI agent automatically:
> - **Classifies** intent (Sales, Support, Spam, Urgent).
> - **Scores** urgency (1-5) and lead value (1-10).
> - **Searches** internal KB or the web (Tavily) for answers.
> - **Validates** drafts for PII (phone numbers) and hallucinations.
> - **Routes** high-risk messages (cancellations, refunds) to human review.

---

## 🏗️ Architecture

<details>
<summary><b>Click to expand the LangGraph workflow diagram</b></summary>
<br>

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
---
