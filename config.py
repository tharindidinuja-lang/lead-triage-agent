import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "mock-placeholder-key")


# Tavily (recommended for agents)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Or Google Serper
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

MODEL_NAME = "gpt-4o-mini"  # Cheap, fast, and smart enough for triage
TEMPERATURE = 0.3           # Keep it deterministic for classification