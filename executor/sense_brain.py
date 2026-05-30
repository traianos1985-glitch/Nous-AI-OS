from executor.android_sense import sense
from executor.llm_core import ask
from executor.memory import save

def sense_and_think():
    data = sense()

    prompt = f"""
Είσαι ο ΝΟΥΣ AI OS στο κινητό του χρήστη.

Αυτά είναι τα τρέχοντα δεδομένα συσκευής:
{data}

Απάντησε στα ελληνικά:
1. τι παρατηρείς
2. αν υπάρχει κάτι σημαντικό
3. τι προτείνεις να κάνει ο χρήστης
4. αν χρειάζεται κάποια αυτόματη ενέργεια
"""

    res = ask(prompt)
    out = res.get("response", str(res)) if isinstance(res, dict) else str(res)

    save({
        "event": "sense_thought",
        "sense": data,
        "thought": out
    })

    return out
