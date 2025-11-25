# api_client.py
import time
import requests

from config import SYSTEM_PROMPT, API_KEY


def call_gemini_api(api_key=API_KEY, user_query, system_prompt=SYSTEM_PROMPT, retries=3, delay=1):
    apiUrl = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash-preview-09-2025:generateContent"
        f"?key={api_key}"
    )

    payload = {
        "contents": [{"parts": [{"text": user_query}]}],
        "tools": [{"google_search": {}}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
    }

    for _ in range(retries):
        try:
            response = requests.post(apiUrl, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            return (
                result["candidates"][0]["content"]["parts"][0]["text"].strip()
                if "candidates" in result
                else "Sorry, I couldn't generate a valid response."
            )
        except Exception:
            time.sleep(delay)

    return "I'm having trouble processing your request right now."
