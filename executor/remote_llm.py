import requests
import os

API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = [
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "meta-llama/llama-3.3-8b-instruct:free",
    "google/gemma-3-12b-it:free",
    "openrouter/auto",
]

TIMEOUT = 45

SYSTEM_PROMPT = (
    "Είσαι ο ΝΟΥΣ, ένας έξυπνος AI βοηθός στα ελληνικά. "
    "Απάντα πάντα σε φυσικά, σωστά ελληνικά. "
    "Μην απαντάς με JSON εκτός αν σου ζητηθεί ρητά. "
    "Δώσε σαφή, ολοκληρωμένη αλλά σύντομη απάντηση."
)


def _post(messages: list, max_tokens: int = 2200) -> dict:
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        return {"success": False, "error": "no_api_key"}

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nous.local",
        "X-Title": "NOUS-AI-OS",
    }

    last_error = None
    for model in MODELS:
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
            data = r.json()
            if "choices" in data and data["choices"]:
                text = data["choices"][0]["message"]["content"].strip()
                if text:
                    return {"success": True, "model": model, "response": text}
            last_error = str(data)
        except Exception as e:
            last_error = str(e)
            continue

    return {"success": False, "error": last_error or "no_response"}


def ask_remote_llm(prompt: str) -> dict:
    """Single-turn: send one user message."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    return _post(messages)


def ask_with_turns(turns: list[dict], system: str | None = None) -> dict:
    """Multi-turn: pass a list of {role, content} dicts (user/assistant alternating).
    System prompt is prepended automatically."""
    messages = [{"role": "system", "content": system or SYSTEM_PROMPT}]
    messages.extend(turns)
    return _post(messages)
