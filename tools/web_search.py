# tools/web_search.py
import os
import json
import requests
from config import TAVILY_API_KEY, SERPER_API_KEY
from tools.rag_mock import search_kb as mock_search

def search_web(query: str) -> str:
    """
    Perform a web search using Tavily (preferred) or Google Serper.
    Falls back to mock KB if no API keys are available.
    """
    # ---- 1. Try Tavily (Best for Agents) ----
    if TAVILY_API_KEY:
        try:
            import requests
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": TAVILY_API_KEY,
                "query": query,
                "search_depth": "basic",
                "max_results": 3,
                "include_answer": True
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Return the AI-generated answer + top result snippets
                answer = data.get("answer", "")
                results = data.get("results", [])
                snippets = "\n".join([r.get("content", "") for r in results[:3]])
                if answer:
                    return f"Tavily Answer: {answer}\n\nSources:\n{snippets}"
                return f"Search Results:\n{snippets}"
            else:
                print(f"  ⚠️ Tavily API error: {response.status_code}")
        except Exception as e:
            print(f"  ⚠️ Tavily search failed: {e}")

    # ---- 2. Fallback: Google Serper ----
    if SERPER_API_KEY:
        try:
            url = "https://google.serper.dev/search"
            headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
            payload = json.dumps({"q": query, "num": 3})
            response = requests.post(url, headers=headers, data=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                organic = data.get("organic", [])
                snippets = "\n".join([r.get("snippet", "") for r in organic[:3]])
                return f"Google Search Results:\n{snippets}"
            else:
                print(f"  ⚠️ Serper API error: {response.status_code}")
        except Exception as e:
            print(f"  ⚠️ Serper search failed: {e}")

    # ---- 3. Final Fallback: Mock KB ----
    print("  ℹ️ No search API keys found. Using mock knowledge base.")
    return mock_search(query)