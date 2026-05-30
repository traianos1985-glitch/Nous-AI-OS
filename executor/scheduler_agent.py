import json, os, time

FILE = "data/scheduled_tasks.json"

def _load():
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE, "r", encoding="utf-8"))
    except:
        return []

def _save(tasks):
    os.makedirs("data", exist_ok=True)
    json.dump(tasks, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def add_schedule(text):
    tasks = _load()
    item = {
        "id": int(time.time()),
        "task": text,
        "status": "scheduled",
        "created": time.time()
    }
    tasks.append(item)
    _save(tasks)
    return item

def list_schedules():
    return _load()

def clear_schedules():
    _save([])
    return {"cleared": True}
