from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from executor.smart_garbage_collector import run_smart_garbage_collector
from executor.self_maintenance_engine import run_self_maintenance
from executor.patch_proposal_enricher import run_patch_proposal_enricher
from executor.patch_pipeline_manager import run_patch_pipeline_manager

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
    patch_enrichment = run_patch_proposal_enricher()
    patch_pipeline = run_patch_pipeline_manager()

    result = {
        "loop": "Executive Loop V4",
        "timestamp": now_iso(),
        "rule": "maintenance_and_patch_pipeline_before_creation",
        "phase_order": [
            "smart_garbage_collection",
            "basic_self_maintenance",
            "patch_proposal_enrichment",
            "patch_pipeline_manager",
            "deduplicate",
            "archive_completed",
            "brain_backup_retention",
            "safe_observe",
            "safe_recommend"
        ],
        "smart_garbage_collection": smart_cleanup,
        "basic_self_maintenance": basic_maintenance,
        "patch_proposal_enrichment": patch_enrichment,
        "patch_pipeline_manager": patch_pipeline,
        "summary": {
            "patch_proposals_total": patch_pipeline.get("total_patch_proposals"),
            "patch_pipeline_policy": patch_pipeline.get("policy"),
            "repository_validation_ok": (
                patch_pipeline.get("repository_validation", {}).get("ok")
            ),
            "maintenance_before_creation": True,
            "approval_first": True,
            "no_diff_no_apply": True,
        },
        "recommendations": [
            "Do not create duplicate proposals before cleanup has run.",
            "Enrich patch proposals before sending them to approval/apply flow.",
            "Never apply a patch that has no concrete diff, patches list, or file changes.",
            "Run repository validation before and after any patch application.",
            "Rollback must remain automatic on failed validation.",
        ],
    }

    result["report_path"] = save_report("executive_loop_v4", result)
    return result


if __name__ == "__main__":
    print(json.dumps(run_executive_loop_v4(), indent=2, ensure_ascii=False))
