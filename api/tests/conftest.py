import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
