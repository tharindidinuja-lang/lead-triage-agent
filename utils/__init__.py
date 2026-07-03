# utils/__init__.py
from .logger import setup_logger, get_logger
from .llm import OpenAI

def get_message_content(message) -> str:
    if hasattr(message, "content"):
        return message.content
    elif isinstance(message, dict):
        return message.get("content", "")
    return str(message)

# Optional: Export a default logger for simple imports
__all__ = ["setup_logger", "get_logger", "get_message_content", "OpenAI"]

