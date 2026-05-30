from executor.personal_agent import load_db
from executor.memory import load

def recall(query=""):
    db = load_db()
    mem = load()

    q = str(query).lower()

    results = {
        "profile": [],
        "goals": [],
        "projects": [],
        "memory": []
    }

    for k, v in db.get("profile", {}).items():
        if not q or q in str(v).lower():
            results["profile"].append(v)

    for g in db.get("goals", []):
        if not q or q in str(g).lower():
            results["goals"].append(g)

    for p in db.get("projects", []):
        if not q or q in str(p).lower():
            results["projects"].append(p)

    for item in mem[-100:]:
        if q and q in str(item).lower():
            results["memory"].append(item)

    return results
