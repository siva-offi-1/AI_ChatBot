import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    DOCUMENTS_DIR = os.getenv("DOCUMENTS_DIR", str(ROOT / "documents"))
    TOP_K = int(os.getenv("TOP_K", "4"))
    RETRIEVAL_THRESHOLD = float(os.getenv("RETRIEVAL_THRESHOLD", "0.12"))
