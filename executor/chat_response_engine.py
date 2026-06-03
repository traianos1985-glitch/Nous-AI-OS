from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any

from executor.document_chat_bridge import document_chat_answer, format_document_answer


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


COMMAND_PREFIXES = (
    "/", "plan ", "run ", "task ", "mission ", "deploy ",
    "φτιάξε αποστολή", "δημιούργησε αποστολή", "τρέξε ",
    "κάνε mission", "κανε mission"
)


DOC_WORDS = [
    "έγγραφο", "εγγραφο", "εγχειρίδιο", "εγχειριδιο", "manual",
    "pdf", "docx", "αρχείο", "αρχειο", "μαθημένα", "μαθημενα",
    "τι λέει", "τι λεει", "σύμφωνα με", "συμφωνα με",
]


QUESTION_WORDS = [
    "τι", "πώς", "πως", "γιατί", "γιατι", "πού", "που",
    "πότε", "ποτε", "ποιο", "ποια", "ποιος", "μπορείς",
    "μπορεις", "ξέρεις", "ξερεις", "θυμάσαι", "θυμασαι"
]


CASUAL_PATTERNS = [
    "γεια", "γειά", "καλημέρα", "καλημερα", "καλησπέρα", "καλησπερα",
    "τι κάνεις", "τι κανεις", "πως είσαι", "πώς είσαι", "πως εισαι",
    "έλα", "ελα", "φίλε", "φιλε", "οκ", "ευχαριστώ", "ευχαριστω"
]


def norm(text: str) -> str:
    return (text or "").strip().lower()


def is_explicit_command(message: str) -> bool:
    m = norm(message)
    return any(m.startswith(x) for x in COMMAND_PREFIXES)


def has_document_intent(message: str) -> bool:
    m = norm(message)
    return any(w in m for w in DOC_WORDS)


def is_question_or_chat(message: str) -> bool:
    m = norm(message)
    if not m:
        return True
    if "?" in m:
        return True
    if any(p in m for p in CASUAL_PATTERNS):
        return True
    first = m.split()[0] if m.split() else ""
    if first in QUESTION_WORDS:
        return True
    # Short messages should be chat, not missions.
    if len(m.split()) <= 8 and not is_explicit_command(m):
        return True
    return False


def simple_chat_answer(message: str) -> str:
    m = norm(message)

    if any(x in m for x in ["τι κάνεις", "τι κανεις", "πως είσαι", "πώς είσαι", "πως εισαι"]):
        return (
            "Είμαι εδώ και λειτουργώ κανονικά. "
            "Μπορείς να με ρωτήσεις κάτι, να μου ζητήσεις να αναλύσω έγγραφα, "
            "ή να μου δώσεις ρητή εντολή για αποστολή με /plan ή /run."
        )

    if any(x in m for x in ["γεια", "γειά", "καλημέρα", "καλημερα", "καλησπέρα", "καλησπερα"]):
        return "Γεια σου φίλε μου. Είμαι έτοιμος. Τι θέλεις να δούμε;"

    if not m:
        return "Γράψε μου τι θέλεις να κάνουμε."

    return (
        "Σε ακούω. Για απλή συζήτηση θα σου απαντάω εδώ σαν κανονικό chat. "
        "Για να δημιουργήσω αποστολή, γράψε ρητά /plan ή /run."
    )


def chatgpt_style_response(message: str) -> dict[str, Any] | None:
    """
    Returns a clean chat response when the message should NOT become a mission.
    Returns None when the old Executive/Mission flow should continue.
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
                        {
                            "document": s.get("document"),
                            "chunk": s.get("chunk"),
                        }
                        for s in doc.get("sources", [])
                    ],
                    "timestamp": now_iso(),
                }
        except Exception as e:
            return {
                "ok": False,
                "executed": False,
                "source": "chat_response_engine",
                "mode": "document_recall_error",
                "answer": f"Προσπάθησα να ψάξω στα έγγραφα, αλλά προέκυψε σφάλμα: {e!r}",
                "response": f"Προσπάθησα να ψάξω στα έγγραφα, αλλά προέκυψε σφάλμα: {e!r}",
                "text": f"Προσπάθησα να ψάξω στα έγγραφα, αλλά προέκυψε σφάλμα: {e!r}",
            }

    if is_question_or_chat(message):
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
