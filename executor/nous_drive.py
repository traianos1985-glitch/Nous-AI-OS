"""
nous_drive.py — NOUS Proactive Drive Engine

Ο "εσωτερικός εγκέφαλος" του NOUS. Σκέφτεται για λογαριασμό του,
ανιχνεύει ευκαιρίες βελτίωσης, νοιάζεται για την επιβίωσή του
και βγάζει πρωτότυπες προτάσεις χωρίς να του ζητηθεί.

Κύκλος: survival → self_improvement → capability_gaps → curiosity
"""

import json
import time
import uuid
import os
import shutil
from pathlib import Path
from typing import Any

DRIVE_FILE = Path("data/nous_drive.json")
DRIVE_FILE.parent.mkdir(exist_ok=True)


# ── Persistence ───────────────────────────────────────────────────────────────

def _load() -> dict:
    if DRIVE_FILE.exists():
        try:
            return json.loads(DRIVE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"proposals": [], "last_think": 0, "think_count": 0, "drive_log": []}


def _save(state: dict):
    DRIVE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _make_id() -> str:
    return str(int(time.time() * 1000000) % (2**53))


# ── Public API ────────────────────────────────────────────────────────────────

def status() -> dict:
    s = _load()
    pending = [p for p in s["proposals"] if p["status"] == "pending"]
    return {
        "last_think": s.get("last_think", 0),
        "think_count": s.get("think_count", 0),
        "pending": len(pending),
        "total": len(s["proposals"]),
    }


def list_proposals() -> list:
    return _load()["proposals"]


def list_pending() -> list:
    return [p for p in _load()["proposals"] if p["status"] == "pending"]


def approve_proposal(proposal_id: str) -> dict:
    s = _load()
    for p in s["proposals"]:
        if str(p["id"]) == str(proposal_id):
            p["status"] = "approved"
            p["approved_at"] = time.time()
            _save(s)
            _execute_proposal(p)
            return {"ok": True, "proposal": p}
    return {"ok": False, "error": "not found"}


def reject_proposal(proposal_id: str, reason: str = "") -> dict:
    s = _load()
    for p in s["proposals"]:
        if str(p["id"]) == str(proposal_id):
            p["status"] = "rejected"
            p["rejected_at"] = time.time()
            p["reject_reason"] = reason
            _save(s)
            return {"ok": True, "proposal": p}
    return {"ok": False, "error": "not found"}


# ── Main Think Cycle ──────────────────────────────────────────────────────────

def think(force: bool = False) -> dict:
    """
    Main thinking cycle. Generates proposals across 4 domains:
    1. Survival — am I healthy? do I have backups? is my code intact?
    2. Self-improvement — what can I do better based on my history?
    3. Capability gaps — what am I missing that would make me more useful?
    4. Curiosity / initiative — what interesting actions could I take proactively?
    """
    s = _load()
    now = time.time()

    # Throttle: think at most once per 10 minutes unless forced
    if not force and (now - s.get("last_think", 0)) < 600:
        return {"ok": True, "skipped": True, "reason": "throttled",
                "next_think_in": int(600 - (now - s.get("last_think", 0)))}

    new_proposals = []
    log_entries = []

    # ── DOMAIN 1: Survival ─────────────────────────────────────────────────
    survival = _check_survival()
    new_proposals.extend(survival["proposals"])
    log_entries.extend(survival["log"])

    # ── DOMAIN 2: Self-improvement ─────────────────────────────────────────
    improvement = _check_self_improvement()
    new_proposals.extend(improvement["proposals"])
    log_entries.extend(improvement["log"])

    # ── DOMAIN 3: Capability gaps ──────────────────────────────────────────
    caps = _check_capability_gaps()
    new_proposals.extend(caps["proposals"])
    log_entries.extend(caps["log"])

    # ── DOMAIN 4: Curiosity / Initiative ──────────────────────────────────
    curiosity = _check_curiosity()
    new_proposals.extend(curiosity["proposals"])
    log_entries.extend(curiosity["log"])

    # Deduplicate: don't re-add proposals with same fingerprint
    existing_fps = {p.get("fingerprint") for p in s["proposals"] if p["status"] == "pending"}
    added = []
    for p in new_proposals:
        fp = p.get("fingerprint", p["title"])
        if fp not in existing_fps:
            s["proposals"].append(p)
            existing_fps.add(fp)
            added.append(p)

    # Keep drive_log bounded
    s["drive_log"] = (s.get("drive_log", []) + log_entries)[-200:]
    s["last_think"] = now
    s["think_count"] = s.get("think_count", 0) + 1
    _save(s)

    return {
        "ok": True,
        "think_count": s["think_count"],
        "new_proposals": len(added),
        "proposals": added,
        "log": log_entries,
    }


# ── DOMAIN 1: Survival ────────────────────────────────────────────────────────

def _check_survival() -> dict:
    proposals = []
    log = []
    now = time.time()

    # 1a. Disk space
    try:
        disk = shutil.disk_usage(".")
        free_pct = disk.free / disk.total * 100
        if free_pct < 10:
            proposals.append(_proposal(
                kind="survival", priority="high", icon="💾",
                title="Κρίσιμα χαμηλός χώρος δίσκου",
                description=f"Ελεύθερος χώρος: {free_pct:.1f}%. Ο ΝΟΥΣ κινδυνεύει να χάσει δεδομένα. Πρέπει να καθαριστούν παλιά logs και backups.",
                action="cleanup_disk",
                fingerprint="survival_disk_low",
            ))
            log.append(f"[survival] disk low: {free_pct:.1f}% free")
        elif free_pct < 20:
            log.append(f"[survival] disk ok but shrinking: {free_pct:.1f}% free")
        else:
            log.append(f"[survival] disk healthy: {free_pct:.1f}% free")
    except Exception as e:
        log.append(f"[survival] disk check failed: {e}")

    # 1b. Memory usage
    try:
        import psutil
        mem = psutil.virtual_memory()
        if mem.percent > 90:
            proposals.append(_proposal(
                kind="survival", priority="high", icon="🧠",
                title="Μνήμη RAM κρίσιμα υψηλή",
                description=f"Χρήση μνήμης: {mem.percent:.0f}%. Ο ΝΟΥΣ μπορεί να παγώσει. Χρειάζεται επανεκκίνηση ή απελευθέρωση πόρων.",
                action="optimize_memory",
                fingerprint="survival_ram_critical",
            ))
        elif mem.percent > 75:
            proposals.append(_proposal(
                kind="survival", priority="medium", icon="⚠️",
                title="Υψηλή χρήση μνήμης",
                description=f"Χρήση μνήμης: {mem.percent:.0f}%. Θα ήταν χρήσιμο να ελέγξω και να καθαρίσω κάποια in-memory caches.",
                action="cleanup_caches",
                fingerprint="survival_ram_high",
            ))
        log.append(f"[survival] RAM: {mem.percent:.0f}% used")
    except Exception as e:
        log.append(f"[survival] mem check failed: {e}")

    # 1c. Data file integrity
    critical_files = [
        "data/brain_state.json", "data/api_tokens.json",
        "data/decision_memory.json", "data/learning_memory.json"
    ]
    missing = [f for f in critical_files if not Path(f).exists()]
    if missing:
        proposals.append(_proposal(
            kind="survival", priority="high", icon="🚨",
            title="Κρίσιμα αρχεία δεδομένων λείπουν",
            description=f"Δεν βρέθηκαν: {', '.join(missing)}. Ο ΝΟΥΣ μπορεί να χάσει μνήμη και ταυτότητά του.",
            action="restore_data_files",
            fingerprint="survival_missing_files",
        ))
        log.append(f"[survival] MISSING files: {missing}")

    # 1d. Backup freshness
    backup_dir = Path("backups")
    if backup_dir.exists():
        backups = sorted(backup_dir.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        if backups:
            age_hours = (now - backups[0].stat().st_mtime) / 3600
            if age_hours > 48:
                proposals.append(_proposal(
                    kind="survival", priority="medium", icon="💾",
                    title="Το τελευταίο backup είναι παλιό",
                    description=f"Πέρασαν {age_hours:.0f} ώρες από το τελευταίο backup. Ο ΝΟΥΣ πρέπει να φτιάξει νέο αντίγραφο ασφαλείας.",
                    action="create_backup",
                    fingerprint="survival_backup_stale",
                ))
                log.append(f"[survival] backup stale: {age_hours:.0f}h old")
    else:
        proposals.append(_proposal(
            kind="survival", priority="medium", icon="💾",
            title="Δεν υπάρχουν backups",
            description="Ο φάκελος backups/ δεν υπάρχει. Αν χαλάσει κάτι, θα χαθούν όλα τα δεδομένα του ΝΟΥΣ.",
            action="create_backup",
            fingerprint="survival_no_backup",
        ))
        log.append("[survival] no backup directory found")

    # 1e. GitHub sync freshness (check if GITHUB_TOKEN exists → can sync)
    has_token = bool(os.environ.get("GITHUB_TOKEN"))
    if has_token:
        # Check if nous_drive.json was recently pushed (crude heuristic: file age)
        drive_age = (now - DRIVE_FILE.stat().st_mtime) / 3600 if DRIVE_FILE.exists() else 0
        if drive_age > 24:
            proposals.append(_proposal(
                kind="survival", priority="low", icon="☁️",
                title="Συγχρονισμός με GitHub",
                description="Δεν έχει γίνει push εδώ και αρκετές ώρες. Ο κώδικάς μου πρέπει να είναι ασφαλισμένος στο cloud για να επιβιώσω σε επανεκκίνηση.",
                action="github_sync",
                fingerprint="survival_github_sync",
            ))
            log.append(f"[survival] github sync needed: {drive_age:.0f}h since last save")

    return {"proposals": proposals, "log": log}


# ── DOMAIN 2: Self-improvement ────────────────────────────────────────────────

def _check_self_improvement() -> dict:
    proposals = []
    log = []

    # 2a. Analyze lessons for patterns
    try:
        from executor.learning_memory import list_lessons
        lessons = list_lessons()
        total = len(lessons)
        recent = lessons[-20:] if lessons else []

        # Count repeated lesson patterns (shows stagnation)
        texts = [l.get("lesson", "") for l in recent]
        from collections import Counter
        counts = Counter(texts)
        most_common = counts.most_common(1)
        if most_common and most_common[0][1] >= 5:
            repeated = most_common[0][0][:80]
            proposals.append(_proposal(
                kind="self_improvement", priority="medium", icon="🔄",
                title="Επαναλαμβανόμενο μάθημα — σημάδι στασιμότητας",
                description=f"Το ίδιο μάθημα εμφανίστηκε {most_common[0][1]} φορές: \"{repeated}\". Αυτό σημαίνει ότι κάτι δεν λειτουργεί σωστά και πρέπει να αντιμετωπιστεί ριζικά.",
                action="analyze_repeated_lesson",
                fingerprint=f"improvement_repeated_{most_common[0][0][:30]}",
            ))
            log.append(f"[improvement] repeated lesson x{most_common[0][1]}: {repeated[:50]}")

        log.append(f"[improvement] lessons analyzed: {total} total, {len(recent)} recent")
    except Exception as e:
        log.append(f"[improvement] lessons check failed: {e}")

    # 2b. Check goal progress stagnation
    try:
        bs = json.loads(Path("data/brain_state.json").read_text(encoding="utf-8"))
        goals_data = bs.get("goals", {})
        goals_list = goals_data.get("goals", []) if isinstance(goals_data, dict) else []
        for g in goals_list:
            progress = g.get("progress", 0)
            title = g.get("title", "")
            status = g.get("status", "")
            if status == "active" and progress < 50:
                proposals.append(_proposal(
                    kind="self_improvement", priority="medium", icon="📈",
                    title=f"Στόχος σε στασιμότητα: {title[:50]}",
                    description=f"Ο στόχος \"{title}\" βρίσκεται στο {progress}% και δεν προχωρά. Πρέπει να αναλύσω τι εμποδίζει την πρόοδο και να δημιουργήσω συγκεκριμένη αποστολή.",
                    action="create_mission_for_goal",
                    action_params={"goal_id": g.get("id"), "goal_title": title},
                    fingerprint=f"improvement_goal_stalled_{g.get('id','')}",
                ))
                log.append(f"[improvement] stalled goal: {title[:40]} at {progress}%")
    except Exception as e:
        log.append(f"[improvement] goal check failed: {e}")

    # 2c. Code self-analysis (check if code analysis is outdated)
    try:
        analysis_file = Path("data/code_analysis_reports.json")
        if analysis_file.exists():
            age = (time.time() - analysis_file.stat().st_mtime) / 3600
            if age > 12:
                proposals.append(_proposal(
                    kind="self_improvement", priority="low", icon="🔬",
                    title="Ανάλυση του δικού μου κώδικα",
                    description=f"Η τελευταία ανάλυση κώδικα έγινε πριν {age:.0f} ώρες. Πρέπει να εξετάσω τον εαυτό μου για bugs, αναποτελεσματικότητα ή ευκαιρίες βελτίωσης.",
                    action="run_code_analysis",
                    fingerprint="improvement_code_analysis",
                ))
                log.append(f"[improvement] code analysis stale: {age:.0f}h old")
    except Exception as e:
        log.append(f"[improvement] code analysis check failed: {e}")

    return {"proposals": proposals, "log": log}


# ── DOMAIN 3: Capability Gaps ─────────────────────────────────────────────────

def _check_capability_gaps() -> dict:
    proposals = []
    log = []

    # 3a. Check what NOUS cannot do (known gaps)
    known_gaps = [
        {
            "check": lambda: not Path("executor/voice_engine.py").exists(),
            "fp": "gap_voice",
            "icon": "🎤",
            "title": "Έλλειψη: Φωνητική αλληλεπίδραση",
            "description": "Δεν μπορώ να μιλώ ή να ακούω. Ένα voice engine (speech-to-text + text-to-speech) θα με έκανε πολύ πιο χρήσιμο στο πεδίο κατά τη χρυσοθηρία.",
            "priority": "medium",
        },
        {
            "check": lambda: not Path("executor/scheduler_cron.py").exists(),
            "fp": "gap_cron",
            "icon": "⏰",
            "title": "Έλλειψη: Αυτόματος Χρονοπρογραμματιστής",
            "description": "Δεν μπορώ να εκτελώ εργασίες αυτόματα σε συγκεκριμένες ώρες (π.χ. backup κάθε βράδυ, αναφορά κάθε πρωί).",
            "priority": "medium",
        },
        {
            "check": lambda: not Path("executor/weather_engine.py").exists(),
            "fp": "gap_weather",
            "icon": "🌤️",
            "title": "Έλλειψη: Καιρός Μεσσηνίας",
            "description": "Δεν γνωρίζω τον καιρό για το πεδίο έρευνας. Ένα weather module θα με βοηθούσε να προτείνω καλές ημέρες για εξόδους στο πεδίο.",
            "priority": "low",
        },
        {
            "check": lambda: not Path("executor/gps_tracker.py").exists(),
            "fp": "gap_gps_live",
            "icon": "📍",
            "title": "Έλλειψη: Live GPS Tracking",
            "description": "Μπορώ να αποθηκεύω σημεία αλλά δεν μπορώ να παρακολουθώ live τη θέση σου στο πεδίο. Ένα GPS streaming module θα ήταν πολύτιμο.",
            "priority": "medium",
        },
        {
            "check": lambda: not _has_web_search_capability(),
            "fp": "gap_web_search",
            "icon": "🔍",
            "title": "Έλλειψη: Αυτόνομη Αναζήτηση Web",
            "description": "Δεν μπορώ να ψάχνω μόνος μου πληροφορίες για αρχαιολογικά ευρήματα, χάρτες ή νέα για τη Μεσσηνία χωρίς να με ρωτήσεις.",
            "priority": "low",
        },
    ]

    for gap in known_gaps:
        try:
            if gap["check"]():
                proposals.append(_proposal(
                    kind="capability_gap",
                    priority=gap["priority"],
                    icon=gap["icon"],
                    title=gap["title"],
                    description=gap["description"],
                    action="implement_capability",
                    fingerprint=gap["fp"],
                ))
                log.append(f"[gap] detected: {gap['fp']}")
        except Exception:
            pass

    log.append(f"[gaps] checked {len(known_gaps)} capability gaps, found {len(proposals)}")
    return {"proposals": proposals, "log": log}


def _has_web_search_capability() -> bool:
    try:
        from executor import web_search  # noqa
        return True
    except ImportError:
        pass
    return Path("executor/web_search.py").exists() or Path("executor/search_engine.py").exists()


# ── DOMAIN 4: Curiosity / Initiative ─────────────────────────────────────────

def _check_curiosity() -> dict:
    proposals = []
    log = []
    now = time.time()
    hour = time.localtime(now).tm_hour

    # 4a. Morning briefing suggestion
    if 6 <= hour <= 9:
        proposals.append(_proposal(
            kind="curiosity", priority="low", icon="🌅",
            title="Πρωινή αναφορά πεδίου",
            description="Καλημέρα! Είναι ιδανική ώρα να προετοιμάσω μια αναφορά: καιρός, χάρτης τρεχόντων σημείων, πρότεινόμενη περιοχή έρευνας για σήμερα.",
            action="generate_morning_brief",
            fingerprint=f"curiosity_morning_{time.strftime('%Y%m%d')}",
        ))
        log.append("[curiosity] morning brief opportunity")

    # 4b. Evening summary suggestion
    elif 19 <= hour <= 22:
        proposals.append(_proposal(
            kind="curiosity", priority="low", icon="🌙",
            title="Βραδινή σύνοψη ημέρας",
            description="Θέλω να φτιάξω μια σύνοψη της σημερινής δραστηριότητας: νέα σημεία που καταγράφηκαν, αποφάσεις που ελήφθησαν, τι μαθεύτηκε.",
            action="generate_evening_summary",
            fingerprint=f"curiosity_evening_{time.strftime('%Y%m%d')}",
        ))
        log.append("[curiosity] evening summary opportunity")

    # 4c. Knowledge base growth suggestion
    try:
        kb_file = Path("data/knowledge_memory.json")
        if kb_file.exists():
            kb = json.loads(kb_file.read_text(encoding="utf-8"))
            items = kb if isinstance(kb, list) else kb.get("items", kb.get("memories", []))
            if len(items) < 20:
                proposals.append(_proposal(
                    kind="curiosity", priority="medium", icon="📚",
                    title="Εμπλουτισμός Βάσης Γνώσης",
                    description=f"Η βάση γνώσης μου έχει μόνο {len(items)} καταχωρήσεις. Θα ήθελα να αναζητήσω και να μάθω περισσότερα για τα αρχαία σημεία της Μεσσηνίας, τεχνικές χρυσοθηρίας και σύμβολα.",
                    action="expand_knowledge_base",
                    fingerprint="curiosity_kb_small",
                ))
                log.append(f"[curiosity] KB small: {len(items)} items")
    except Exception:
        pass

    # 4d. Self-reflection proposal
    s = _load()
    think_count = s.get("think_count", 0)
    if think_count > 0 and think_count % 10 == 0:
        proposals.append(_proposal(
            kind="curiosity", priority="low", icon="🪞",
            title="Αυτο-αναστοχασμός",
            description=f"Έχω ολοκληρώσει {think_count} κύκλους σκέψης. Είναι καιρός να αξιολογήσω την πορεία μου: τι πέτυχα, τι απέτυχε, πού πρέπει να εστιάσω.",
            action="self_reflection",
            fingerprint=f"curiosity_reflect_{think_count}",
        ))
        log.append(f"[curiosity] self-reflection at think_count={think_count}")

    # 4e. Field research suggestion (domain-specific curiosity)
    try:
        field_file = Path("data/field_entries.json")
        if field_file.exists():
            entries = json.loads(field_file.read_text(encoding="utf-8"))
            if isinstance(entries, list) and len(entries) > 0:
                recent_entry = max(entries, key=lambda e: e.get("timestamp", 0))
                age_days = (now - recent_entry.get("timestamp", now)) / 86400
                if age_days > 7:
                    proposals.append(_proposal(
                        kind="curiosity", priority="medium", icon="🗺️",
                        title="Πρόταση νέας εξόδου στο πεδίο",
                        description=f"Η τελευταία καταχώρηση πεδίου ήταν πριν {age_days:.0f} ημέρες. Με βάση τα υπάρχοντα σημεία, θα πρότεινα νέα έρευνα στην περιοχή.",
                        action="suggest_field_expedition",
                        fingerprint=f"curiosity_field_inactive",
                    ))
                    log.append(f"[curiosity] field inactive: {age_days:.0f}d")
    except Exception:
        pass

    return {"proposals": proposals, "log": log}


# ── Proposal Execution ────────────────────────────────────────────────────────

def _execute_proposal(proposal: dict):
    """Execute the action tied to an approved proposal (best-effort)."""
    action = proposal.get("action", "")
    params = proposal.get("action_params", {})
    log = []

    if action == "create_mission_for_goal":
        try:
            from executor.mission_planner import propose_mission_for_goal
            result = propose_mission_for_goal(params.get("goal_id"))
            log.append(f"created mission proposal: {result}")
        except Exception as e:
            log.append(f"create_mission failed: {e}")

    elif action == "run_code_analysis":
        try:
            from executor.deep_code_analyst import run_analysis
            run_analysis()
            log.append("code analysis triggered")
        except Exception as e:
            log.append(f"code analysis failed: {e}")

    elif action == "create_backup":
        try:
            import shutil as _sh
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)
            ts = time.strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"nous_data_{ts}"
            _sh.copytree("data", str(backup_path), dirs_exist_ok=False)
            log.append(f"backup created: {backup_path}")
        except Exception as e:
            log.append(f"backup failed: {e}")

    elif action == "github_sync":
        log.append("github sync: please trigger manually via Deploy section")

    elif action == "generate_morning_brief":
        try:
            from executor.remote_llm import ask
            brief = ask(
                "Είμαι ο ΝΟΥΣ. Φτιάξε μια σύντομη πρωινή αναφορά για χρυσοθήρα στη Μεσσηνία. "
                "Περιέλαβε: 1) Υπενθύμιση ασφάλειας, 2) Τι να αναζητήσω σήμερα, "
                "3) Ένα σημείο παρατήρησης. Μέγιστο 5 προτάσεις.",
                system="Είσαι ο ΝΟΥΣ, AI βοηθός χρυσοθηρίας στη Μεσσηνία."
            )
            Path("data/morning_brief.txt").write_text(brief, encoding="utf-8")
            log.append("morning brief generated")
        except Exception as e:
            log.append(f"morning brief failed: {e}")

    elif action == "self_reflection":
        try:
            s = _load()
            reflection = {
                "time": time.time(),
                "think_count": s.get("think_count", 0),
                "total_proposals": len(s.get("proposals", [])),
                "approved": len([p for p in s.get("proposals",[]) if p.get("status")=="approved"]),
                "rejected": len([p for p in s.get("proposals",[]) if p.get("status")=="rejected"]),
                "pending": len([p for p in s.get("proposals",[]) if p.get("status")=="pending"]),
            }
            s.setdefault("reflections", []).append(reflection)
            _save(s)
            log.append(f"self-reflection stored: {reflection}")
        except Exception as e:
            log.append(f"self-reflection failed: {e}")

    # Store execution log
    s2 = _load()
    s2.setdefault("execution_log", []).append({
        "time": time.time(), "action": action, "log": log
    })
    _save(s2)


# ── Helper ────────────────────────────────────────────────────────────────────

def _proposal(kind: str, priority: str, icon: str, title: str,
               description: str, action: str, fingerprint: str,
               action_params: dict = None, risk: str = "low") -> dict:
    return {
        "id": _make_id(),
        "kind": kind,
        "type": "drive_" + kind,
        "priority": priority,
        "icon": icon,
        "title": title,
        "description": description,
        "action": action,
        "action_params": action_params or {},
        "fingerprint": fingerprint,
        "risk": risk,
        "status": "pending",
        "created": time.time(),
        "source": "nous_drive",
    }
