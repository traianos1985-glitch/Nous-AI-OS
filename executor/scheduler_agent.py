import json
import os
import time
import re
from datetime import datetime, timedelta

FILE = "data/scheduled_tasks.json"


def _load():
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE, "r", encoding="utf-8"))
    except Exception:
        return []


def _save(tasks):
    os.makedirs("data", exist_ok=True)
    json.dump(tasks, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def _today_at(hour, minute):
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
    return target.timestamp()


def parse_schedule(text):
    raw = str(text).strip()
    lower = raw.lower()

    time_match = re.search(r"(\d{1,2}):(\d{2})", lower)
    hour = None
    minute = None

    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2))

    if "κάθε μέρα" in lower or "daily" in lower or "every day" in lower:
        if hour is None:
            hour = 9
            minute = 0

        task = raw
        task = re.sub(r"κάθε μέρα", "", task, flags=re.I).strip()
        task = re.sub(r"^\s*(daily|every day)\s+", "", task, flags=re.I).strip()
        task = re.sub(r"στις\s+\d{1,2}:\d{2}", "", task, flags=re.I).strip()
        task = re.sub(r"at\s+\d{1,2}:\d{2}", "", task, flags=re.I).strip()

        return {
            "task": task or raw,
            "schedule_type": "daily",
            "hour": hour,
            "minute": minute,
            "next_run": _today_at(hour, minute),
        }

    return {
        "task": raw,
        "schedule_type": "manual",
        "hour": None,
        "minute": None,
        "next_run": None,
    }


def add_schedule(text):
    tasks = _load()
    parsed = parse_schedule(text)

    item = {
        "id": int(time.time()),
        "task": parsed["task"],
        "raw": str(text).strip(),
        "status": "scheduled",
        "schedule_type": parsed["schedule_type"],
        "hour": parsed["hour"],
        "minute": parsed["minute"],
        "next_run": parsed["next_run"],
        "created": time.time(),
        "last_run": None,
    }

    tasks.append(item)
    _save(tasks)
    return item


def list_schedules():
    return _load()


def clear_schedules():
    _save([])
    return {"cleared": True}
