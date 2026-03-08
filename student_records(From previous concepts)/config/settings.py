"""
config/settings.py — Application Configuration
=================================================
Concepts demonstrated:
  - python-dotenv (.env file loading)
  - os.getenv() for environment variables
  - os.path for path construction
  - Module-level constants
"""

import os
from dotenv import load_dotenv

# ── Load .env file ───────────────────────────────────────────
# load_dotenv() reads the .env file from the project root
# and adds the key=value pairs as environment variables
load_dotenv()

# ── Read environment variables ───────────────────────────────
APP_NAME = os.getenv("APP_NAME", "Student Records System")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
DATA_DIR = os.getenv("DATA_DIR", "data")

# ── Construct paths using os.path ────────────────────────────
# os.path.dirname(__file__) → gives directory of THIS file (config/)
# os.path.join() → safely joins paths for any OS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, DATA_DIR)
STUDENTS_FILE = os.path.join(DATA_PATH, "students.json")
EXPORTS_DIR = os.path.join(DATA_PATH, "exports")
