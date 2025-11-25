# config.py
import os
import json

# ================= API SETUP =================


def get_api_key():
    return os.environ.get("GEMINI_API_KEY")


def load_private_data(filepath="private_data.json"):
    if not os.path.exists(filepath):
        print(f"No private data file found at '{filepath}'.")
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("facts", [])
    except Exception as e:
        print("Error loading private data:", e)
        return []


# ================= GLOBAL CONFIG =================

API_KEY = get_api_key()
PRIVATE_FACTS = load_private_data()
PRIVATE_INFO_STRING = "\n".join(f"- {fact}" for fact in PRIVATE_FACTS)

SYSTEM_PROMPT = f"""
You are a friendly Bennett University assistant.

RULES:
1. Only answer Bennett University questions.
2. Prioritize this private data for campus map info.
3. Give clear directions for location questions.
4. Never reveal passwords or sensitive credentials.
5. If unrelated, politely refuse.

PRIVATE DATA:
{PRIVATE_INFO_STRING}
"""
