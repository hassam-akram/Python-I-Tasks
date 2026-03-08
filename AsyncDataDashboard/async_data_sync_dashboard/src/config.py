"""
config.py - Loads credentials from the .env file

Key Concept:
  - The .env file lives OUTSIDE the project folder (at e:\\courses\\.env)
  - We use python-dotenv to load it so secrets stay out of the codebase
  - os.getenv() reads environment variables set by dotenv
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ── Locate the .env file (one level above the project folder) ──
# __file__  = .../async_data_sync_dashboard/src/config.py
# parent x2 = .../async_data_sync_dashboard/
# parent x3 = .../courses/           <-- this is where .env lives
env_path = Path(__file__).resolve().parent.parent.parent / ".env"

# Load the .env file into the environment
load_dotenv(dotenv_path=env_path)

# ── Read credentials from environment variables ──
SOURCE1_API_KEY = os.getenv("SOURCE1_API_KEY", "NOT_SET")
SOURCE2_API_KEY = os.getenv("SOURCE2_API_KEY", "NOT_SET")
SOURCE3_API_KEY = os.getenv("SOURCE3_API_KEY", "NOT_SET")


def show_config():
    """Print loaded config (for debugging only)."""
    print(f"  SOURCE1_API_KEY = {SOURCE1_API_KEY}")
    print(f"  SOURCE2_API_KEY = {SOURCE2_API_KEY}")
    print(f"  SOURCE3_API_KEY = {SOURCE3_API_KEY}")


# Quick test when running this file directly
if __name__ == "__main__":
    print("Loaded configuration:")
    show_config()
