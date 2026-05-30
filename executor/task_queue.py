import json
import os
import time

FILE = "data/agent_queue.json"


def _load():
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE, "r", encoding="utf-8"))
    except Exception:
        return []


def _save(items):
    os.makedirs("data", exist_ok=True)
    json.dump(items, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def add_task(title, kind="general", priority=5, payload=None):
    items = _load()
    item = {
        "id": int(time.time_ns()),
        "title": str(title),
        "kind": str(kind),
        "priority": int(priority),
        "payload": payload or {},
        "status": "pending",
        "created": time.time(),
        "started": None,
        "finished": None,
        "attempts": 0,
        "last_error": None,
        "result": None,
    }
    items.append(item)
    _save(items)
    return item


def list_queue(status=None):
    items = _load()
    if status:
        items = [x for x in items if x.get("status") == status]
    return sorted(items, key=lambda x: x.get("priority", 5))


def next_task():
    pending = list_queue("pending")
    return pending[0] if pending else None


def update_task(task_id, **updates):
    items = _load()
    for item in items:
        if str(item.get("id")) == str(task_id):
            item.update(updates)
            _save(items)
            return item
    return None


def clear_queue():
    _save([])
    return {"cleared": True}
