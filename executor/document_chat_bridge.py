from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from executor.document_intelligence_engine import answer_from_documents, status


def now_iso():
    return datetime.now(timezone.utc).isoformat()


DOC_TRIGGERS = [
    "έγγραφο", "εγχειρίδιο", "manual", "pdf", "docx",
    "αρχείο", "αρχεία", "μαθημένα", "τι λέει",
    "σύμφωνα με", "θυμάσαι από το αρχείο"
]


def should_use_documents(message: str) -> bool:
    m = (message or "").lower()
    return any(t in m for t in DOC_TRIGGERS)


def document_chat_answer(message: str) -> dict[str, Any]:
    if not should_use_documents(message):
        return {
            "ok": True,
            "used_documents": False,
            "answer": None,
            "sources": [],
        }

    result = answer_from_documents(message)

    return {
        "ok": True,
        "used_documents": True,
        "timestamp": now_iso(),
        "question": message,
        "document_status": status(),
        "answer": result.get("answer"),
        "sources": result.get("sources", []),
        "raw": result,
    }


def format_document_answer(message: str) -> str:
    result = document_chat_answer(message)

    if not result.get("used_documents"):
        return ""

    sources = result.get("sources", [])
    if not sources:
        return "Δεν βρήκα σχετική πληροφορία στα μαθημένα έγγραφα."

    parts = ["Βρήκα σχετική πληροφορία στα μαθημένα έγγραφα:\n"]

    for i, src in enumerate(sources, 1):
        parts.append(
            f"\n[{i}] {src.get('document')} / chunk {src.get('chunk')}\n"
            f"{src.get('excerpt')}"
        )

    return "\n".join(parts)


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "status"
    print(json.dumps(document_chat_answer(q), indent=2, ensure_ascii=False))
