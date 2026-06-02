import json
import os
import time

FILE = "data/upgrade_plans.json"


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


UPGRADES = [
    {
        "title": "True Patch Generator",
        "priority": 1,
        "reason": "Turns code analysis into concrete diffs.",
        "modules": ["deep_code_analyst", "patch_generator", "self_healing_loop"],
    },
    {
        "title": "Real Code Evolution Engine",
        "priority": 2,
        "reason": "Build route/UI/service dependency graph and multi-file patches.",
        "modules": ["repository_index", "route_graph", "ui_action_graph"],
    },
    {
        "title": "Cloud Brain Sync",
        "priority": 3,
        "reason": "Protects the brain from device loss.",
        "modules": ["brain_backup", "cloud_sync", "restore_verify"],
    },
    {
        "title": "Approval Center Actions",
        "priority": 4,
        "reason": "Approve/reject directly from Pending Inbox.",
        "modules": ["pending_review", "approval_router", "ui_buttons"],
    },
]


def propose_upgrade_plan():
    items = _load()
    existing_pending = [x for x in items if x.get("status") == "pending"]
    if existing_pending:
        return {"ok": True, "deduped": True, "plan": existing_pending[0]}

    plan = {
        "id": int(time.time_ns()),
        "created": time.time(),
        "status": "pending",
        "title": "NOUS Next Upgrade Plan",
        "upgrades": UPGRADES,
    }
    items.append(plan)
    _save(items)
    return {"ok": True, "plan": plan}


def upgrade_planner_status():
    items = _load()
    return {
        "time": time.time(),
        "total": len(items),
        "pending": len([x for x in items if x.get("status") == "pending"]),
        "plans": items[-20:],
    }


def list_upgrade_plans(limit=20):
    return _load()[-int(limit):]


def approve_upgrade_plan(plan_id):
    items = _load()
    for p in items:
        if str(p.get("id")) == str(plan_id):
            p["status"] = "approved"
            p["approved"] = time.time()
            _save(items)
            return {"ok": True, "plan": p}
    return {"ok": False, "error": "plan_not_found"}


def reject_upgrade_plan(plan_id, reason="User rejected upgrade plan"):
    items = _load()
    for p in items:
        if str(p.get("id")) == str(plan_id):
            p["status"] = "rejected"
            p["rejected"] = time.time()
            p["reject_reason"] = reason
            _save(items)
            return {"ok": True, "plan": p}
    return {"ok": False, "error": "plan_not_found"}
