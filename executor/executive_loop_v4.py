from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from executor.smart_garbage_collector import run_smart_garbage_collector
from executor.self_maintenance_engine import run_self_maintenance

ROOT = Path.cwd()
DATA = ROOT / "data"
REPORTS = DATA / "reports"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_report(name: str, payload: dict) -> str:
    REPORTS.mkdir(parents=True, exist_ok=True)
    path = REPORTS / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def run_executive_loop_v4() -> dict:
    smart_cleanup = run_smart_garbage_collector()
    basic_maintenance = run_self_maintenance()

    result = {
        "loop": "Executive Loop V4",
        "timestamp": now_iso(),
        "rule": "maintenance_before_creation",
        "phase_order": [
            "smart_garbage_collection",
            "basic_self_maintenance",
            "deduplicate",
            "archive_completed",
            "brain_backup_retention",
            "safe_observe",
            "safe_recommend"
        ],
        "smart_garbage_collection": smart_cleanup,
        "basic_self_maintenance": basic_maintenance,
        "recommendations": [
            "Before creating a mission proposal, check for equivalent existing proposals.",
            "Before creating a repair proposal, check for same fix_id, title, description and patch_type.",
            "Before creating patch proposals, check existing pending patches for same root cause.",
            "Before expanding dashboards, stabilize lifecycle, cleanup and patch pipeline.",
            "Patch pipeline must remain approval-first and rollback-protected."
        ],
    }

    result["report_path"] = save_report("executive_loop_v4", result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_executive_loop_v4(), indent=2, ensure_ascii=False))
