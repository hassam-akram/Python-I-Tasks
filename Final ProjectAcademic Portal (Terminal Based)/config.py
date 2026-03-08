# ===== config.py =====
# Loads secure configuration from .env file

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read config values
PASS_MARKS = int(os.getenv("PASS_MARKS", 50))
FINE_PER_DAY = int(os.getenv("FINE_PER_DAY", 100))
REPORT_DIR = os.getenv("REPORT_DIR", "reports")
