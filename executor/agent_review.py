from executor.llm_core import ask
from executor.memory import load

def review_last():
    mem = load()[-10:]
    prompt = f"""
Είσαι reviewer agent.
Δες τα πρόσφατα γεγονότα του ΝΟΥΣ:
{mem}

Πες στα ελληνικά:
1. τι έγινε
2. αν πέτυχε
3. τι πρόβλημα βλέπεις
4. ποιο είναι το επόμενο βήμα
"""
    res = ask(prompt)
    return res.get("response", str(res)) if isinstance(res, dict) else str(res)
