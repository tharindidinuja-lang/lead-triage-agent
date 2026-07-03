# tools/rag_mock.py
MOCK_KB = {
    "office hours": "Sat 10 AM – 4 PM, closed Sundays.",
    "refund policy": "Refunds are processed within 5-7 business days.",
    "enterprise demo": "We offer tailored demos for teams of 10+. Contact sales@catalyst.media.",
    "pricing": "Our standard plan is $29/user/month. Enterprise quotes are customized."
}

def search_kb(query: str) -> str:
    """Mock RAG retrieval – matches keywords to KB entries."""
    query_lower = query.lower()
    for key, value in MOCK_KB.items():
        if key in query_lower:
            return value
    return "I couldn't find that in our knowledge base."