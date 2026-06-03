from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from executor.document_chat_bridge import document_chat_answer, format_document_answer
from executor.internet_search_engine import answer_from_web

ROOT = Path.cwd()
DATA = ROOT / "data"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def norm(text: str) -> str:
    return (text or "").strip().lower()


def is_explicit_command(message: str) -> bool:
    m = norm(message)
    return (
        m.startswith("/")
        or m.startswith("plan ")
        or m.startswith("run ")
        or m.startswith("mission ")
        or m.startswith("task ")
        or m.startswith("deploy ")
        or m.startswith("φτιάξε αποστολή")
        or m.startswith("δημιούργησε αποστολή")
        or m.startswith("κανε αποστολη")
        or m.startswith("κάνε αποστολή")
    )


def has_document_intent(message: str) -> bool:
    m = norm(message)
    doc_words = [
        "εγχειρίδιο", "εγχειριδιο", "manual",
        "pdf", "docx", "έγγραφο", "εγγραφο",
        "αρχείο", "αρχειο", "μαθημένο", "μαθημενο",
        "μαθημένα", "μαθημενα"
    ]
    return any(w in m for w in doc_words)



def has_internet_intent(message: str) -> bool:
    m = norm(message)
    return any(w in m for w in [
        "ψάξε", "ψαξε", "αναζήτησε", "αναζητησε",
        "internet", "ίντερνετ", "ιντερνετ", "online", "web",
        "τελευταία", "τελευταια", "νέα", "νεα", "ειδήσεις", "ειδησεις",
        "τρέχον", "τρεχον", "τιμή", "τιμη"
    ])

def is_about_nous(message: str) -> bool:
    m = norm(message)
    return "νουσ" in m or "νους" in m or "nous" in m


def is_question_or_conversation(message: str) -> bool:
    m = norm(message)
    if not m:
        return True
    if "?" in m:
        return True
    starters = [
        "τι ", "πως ", "πώς ", "γιατι ", "γιατί ", "που ", "πού ",
        "ποιο ", "ποια ", "ποιος ", "μπορεις ", "μπορείς ",
        "θελω να ρωτησω", "θέλω να ρωτήσω"
    ]
    casual = [
        "γεια", "γειά", "καλημερα", "καλημέρα", "καλησπερα", "καλησπέρα",
        "τι κανεις", "τι κάνεις", "πως εισαι", "πώς είσαι", "πως είσαι",
        "οκ", "ωραια", "ωραία", "ευχαριστω", "ευχαριστώ"
    ]
    if any(m.startswith(s) for s in starters):
        return True
    if any(c in m for c in casual):
        return True
    if len(m.split()) <= 10:
        return True
    return False


def nous_improvement_answer() -> str:
    priorities = load_json(DATA / "executive_priorities.json", {})
    summary = load_json(DATA / "executive_state_summary.json", {})

    top = None
    if isinstance(priorities, dict):
        top = priorities.get("top_action")

    pending_reviews = 0
    patch_total = 0
    missions_total = 0

    if isinstance(summary, dict):
        pending_reviews = summary.get("pending_reviews", {}).get("total", 0)
        patch_total = summary.get("patch_proposals", {}).get("total", 0)
        missions_total = summary.get("missions", {}).get("total", 0)

    lines = [
        "Αυτή τη στιγμή, οι πιο χρήσιμες βελτιώσεις για τον ΝΟΥΣ είναι:",
        "",
        "• Να κρατήσουμε το chat καθαρό, σαν κανονικό βοηθό, και να δημιουργεί mission μόνο όταν του το ζητάς ρητά.",
        "• Να βελτιώσουμε το Document Intelligence ώστε να συνθέτει απαντήσεις από πολλά έγγραφα και όχι απλώς να επιστρέφει αποσπάσματα.",
        "• Να σταθεροποιήσουμε το Executive Prioritizer ώστε να δείχνει καθαρά τι έχει μεγαλύτερη αξία να γίνει μετά.",
        "• Να καθαρίσουμε τα παλιά duplicate missions/reviews/reports ώστε να μη φουσκώνει άσκοπα η μνήμη.",
        "• Να βάλουμε καθαρό UI mode: πρώτα ελληνική περίληψη, και τεχνικές λεπτομέρειες μόνο όταν τις ζητάς.",
    ]

    if top:
        lines += [
            "",
            "Τρέχουσα κορυφαία προτεραιότητα από τον prioritizer:",
            f"• {top.get('title', 'Άγνωστη προτεραιότητα')} ({top.get('kind', 'unknown')})"
        ]

    lines += [
        "",
        f"Σύνοψη κατάστασης: missions={missions_total}, patch proposals={patch_total}, pending reviews={pending_reviews}."
    ]

    return "\n".join(lines)


def simple_chat_answer(message: str) -> str:
    m = norm(message)

    if "τι κανεις" in m or "τι κάνεις" in m or "πως εισαι" in m or "πώς είσαι" in m:
        return "Είμαι εδώ φίλε μου και λειτουργώ κανονικά. Ρώτα με ό,τι θέλεις ή δώσε ρητή εντολή με /plan ή /run για να φτιάξω αποστολή."

    if "γεια" in m or "γειά" in m or "καλημερα" in m or "καλημέρα" in m or "καλησπερα" in m or "καλησπέρα" in m:
        return "Γεια σου φίλε μου. Είμαι έτοιμος. Τι θέλεις να δούμε;"

    if is_about_nous(message) and ("βελτιω" in m or "καλυτερ" in m or "πρέπει" in m or "πρεπει" in m):
        return nous_improvement_answer()

    return (
        "Σε ακούω. Θα σου απαντάω σαν κανονικό chat. "
        "Αν θέλεις να δημιουργήσω αποστολή ή να τρέξω ενέργεια, γράψε ρητά /plan ή /run."
    )


def chatgpt_style_response(message: str) -> dict[str, Any] | None:
    """
    None = allow old Executive/Mission flow.
    Dict = return clean ChatGPT-style answer.
    """

    if is_explicit_command(message):
        return None

    if has_document_intent(message):
        try:
            doc = document_chat_answer(message)
            formatted = format_document_answer(message)
            if doc.get("used_documents") and doc.get("sources"):
                return {
                    "ok": True,
                    "executed": False,
                    "source": "document_chat_bridge",
                    "mode": "document_recall",
                    "answer": formatted,
                    "response": formatted,
                    "text": formatted,
                    "human_answer": formatted,
                    "sources": [
                        {"document": s.get("document")}
                        for s in doc.get("sources", [])
                    ],
                    "timestamp": now_iso(),
                }
        except Exception as e:
            return {
                "ok": False,
                "executed": False,
                "source": "chat_response_engine",
                "mode": "document_error",
                "answer": f"Προσπάθησα να ψάξω στα έγγραφα, αλλά προέκυψε σφάλμα: {e!r}",
                "response": f"Προσπάθησα να ψάξω στα έγγραφα, αλλά προέκυψε σφάλμα: {e!r}",
                "text": f"Προσπάθησα να ψάξω στα έγγραφα, αλλά προέκυψε σφάλμα: {e!r}",
            }


    if has_internet_intent(message):
        web = answer_from_web(message)
        answer = web.get("answer", "Δεν μπόρεσα να πάρω απάντηση από το internet.")
        return {
            "ok": bool(web.get("ok", False)),
            "executed": False,
            "source": "internet_search_engine",
            "mode": "internet_search",
            "answer": answer,
            "response": answer,
            "text": answer,
            "human_answer": answer,
            "results": web.get("results", []),
            "timestamp": now_iso(),
        }

    if is_question_or_conversation(message):
        answer = simple_chat_answer(message)
        return {
            "ok": True,
            "executed": False,
            "source": "chat_response_engine",
            "mode": "normal_chat",
            "answer": answer,
            "response": answer,
            "text": answer,
            "human_answer": answer,
            "timestamp": now_iso(),
        }

    return None


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "Τι κάνεις;"
    print(json.dumps(chatgpt_style_response(q), indent=2, ensure_ascii=False))
