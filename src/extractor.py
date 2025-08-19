import os, json
from typing import Dict, Any, List
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv  # <-- keep this

from .schemas import ExtractedDoc, FieldKV, QAReport

# Load .env locally (ignored on Streamlit Cloud, but fine)
load_dotenv()

# Try secrets first (Cloud), fallback to .env (local)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY is missing. Add it to .env (local) or Streamlit Secrets (Cloud).")

client = OpenAI(api_key=api_key)
