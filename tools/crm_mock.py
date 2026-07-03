# tools/crm_mock.py
MOCK_CRM = {
    "cto@fintech.com": {"tier": "Enterprise", "past_issues": 2, "status": "active"},
    "team15@design.com": {"tier": "SMB", "past_issues": 0, "status": "lead"},
    "ceo@startup.io": {"tier": "Startup", "past_issues": 0, "status": "new"}
}

def lookup_crm(email: str) -> dict:
    """Mock CRM lookup by email."""
    email = email.lower()
    return MOCK_CRM.get(email, {"tier": "Unknown", "past_issues": 0, "status": "new"})