# utils/logger.py
import logging
import os
from datetime import datetime

# Create a logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Generate a log file name with timestamp (e.g., agent_20260702_153045.log)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = os.path.join(LOG_DIR, f"agent_{timestamp}.log")

# ANSI color codes for terminal output
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GREY = "\033[90m"

# Custom formatter that adds colors for console
class ColoredFormatter(logging.Formatter):
    """Add colors to the log level name."""
    level_colors = {
        logging.DEBUG: Colors.GREY,
        logging.INFO: Colors.GREEN,
        logging.WARNING: Colors.YELLOW,
        logging.ERROR: Colors.RED,
        logging.CRITICAL: Colors.MAGENTA,
    }

    def format(self, record):
        # Color the level name
        color = self.level_colors.get(record.levelno, Colors.WHITE)
        record.levelname = f"{color}{record.levelname}{Colors.RESET}"
        return super().format(record)


def setup_logger(name: str = "LeadTriageAgent") -> logging.Logger:
    """
    Set up and return a logger instance.
    Usage: logger = setup_logger(__name__)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture everything

    # Prevent duplicate handlers if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    # ---- 1. FILE HANDLER (Detailed, no colors) ----
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # ---- 2. CONSOLE HANDLER (Colored, cleaner) ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only show INFO+ on console to keep it clean
    console_formatter = ColoredFormatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger

# Convenience function to get the root logger
def get_logger(name: str = "LeadTriageAgent") -> logging.Logger:
    return setup_logger(name)