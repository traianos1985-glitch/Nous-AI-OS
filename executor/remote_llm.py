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


def ask_remote_llm(prompt):
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
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Είσαι ο ΝΟΥΣ, ένας έξυπνος AI βοηθός. "
                        "Απάντα πάντα σε φυσικά, σωστά ελληνικά. "
                        "Μην απαντάς με JSON εκτός αν σου ζητηθεί ρητά. "
                        "Δώσε σαφή, ολοκληρωμένη αλλά σύντομη απάντηση."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 2200,
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
