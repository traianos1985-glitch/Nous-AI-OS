from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

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
    result = {
        "loop": "Executive Loop V4",
        "timestamp": now_iso(),
        "phase_order": [
            "self_maintenance_first",
            "deduplicate",
            "archive_completed",
            "backup_retention",
            "safe_observe",
            "safe_recommend"
        ],
        "self_maintenance": run_self_maintenance(),
        "recommendations": [
            "Do not create new proposals before checking duplicates.",
            "Do not add dashboard features before data cleanup is stable.",
            "Next upgrade should connect this loop to Flask route and pending review inbox.",
            "Patch pipeline should remain approval-first."
        ],
    }

    result["report_path"] = save_report("executive_loop_v4", result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_executive_loop_v4(), indent=2, ensure_ascii=False))
