from executor.memory import load
from executor.personal_agent import load_db
from executor.android_sense import sense
from executor.curiosity_agent import active_learning_topics

def daily_brief():
    db = load_db()
    mem = load()[-10:]
    device = sense()
    return {
        "summary": "Ημερήσια εικόνα ΝΟΥΣ",
        "goals": db.get("goals", []),
        "projects": db.get("projects", []),
        "recent_memory": mem,
        "device": device,
        "active_learning_topics": active_learning_topics()
    }
