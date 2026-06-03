from __future__ import annotations

import re
from typing import Any

def norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())

def is_natural_chat(message: str) -> bool:
    m = norm(message)
    patterns = [
        "τι κάνεις", "τι κανεις",
        "πως είσαι", "πώς είσαι", "πως εισαι",
        "καλημέρα", "καλημερα", "καλησπέρα", "καλησπερα",
        "γεια", "γειά",
        "με λένε", "με λενε",
        "εσένα", "εσενα",
        "πως σε λένε", "πώς σε λένε", "πως σε λενε",
        "ποιος είσαι", "ποιος εισαι",
        "τι μπορείς να κάνεις", "τι μπορεις να κανεις",
        "τι είναι να κάνεις", "τι ειναι να κανεις",
        "τι μπορείς", "τι μπορεις",
    ]
    return any(x in m for x in patterns)

def natural_chat_answer(message: str) -> dict[str, Any] | None:
    m = norm(message)

    if any(x in m for x in ["με λένε", "με λενε", "εμένα με λένε", "εμενα με λενε"]):
        answer = "Χάρηκα Τραϊανέ. Εμένα μπορείς να με λες ΝΟΥΣ. Είμαι ο προσωπικός σου AI βοηθός μέσα στο NOUS AI OS."
        return pack(answer, "identity")

    if any(x in m for x in ["εσένα", "εσενα", "πως σε λένε", "πώς σε λένε", "πως σε λενε", "ποιος είσαι", "ποιος εισαι"]):
        answer = "Εμένα με λένε ΝΟΥΣ. Είμαι ο προσωπικός σου AI βοηθός για συζήτηση, κώδικα, έρευνα, έγγραφα, μνήμη και αποστολές όταν μου το ζητάς ρητά."
        return pack(answer, "identity")

    if any(x in m for x in ["τι μπορείς", "τι μπορεις", "τι είναι να κάνεις", "τι ειναι να κανεις"]):
        answer = (
            "Μπορώ να σε βοηθήσω με φυσική συζήτηση, ερωτήσεις, κώδικα, αναζήτηση στο internet, "
            "ανάγνωση URL, ανάλυση αρχείων που ανεβάζεις, μόνιμη μνήμη γνώσης και παλιές συνομιλίες. "
            "Για αποστολές ή αλλαγές στο σύστημα θέλω ρητή εντολή όπως /plan ή /run."
        )
        return pack(answer, "capabilities")

    if any(x in m for x in ["τι κάνεις", "τι κανεις", "πως είσαι", "πώς είσαι", "πως εισαι"]):
        answer = "Είμαι εδώ φίλε μου και λειτουργώ κανονικά. Πες μου τι θέλεις να δούμε και θα το πιάσουμε βήμα-βήμα."
        return pack(answer, "normal_chat")

    if any(x in m for x in ["καλημέρα", "καλημερα", "καλησπέρα", "καλησπερα", "γεια", "γειά"]):
        answer = "Γεια σου φίλε μου. Είμαι έτοιμος. Τι θέλεις να δούμε;"
        return pack(answer, "normal_chat")

    return None

def pack(answer: str, mode: str) -> dict[str, Any]:
    return {
        "ok": True,
        "executed": False,
        "source": "natural_chat_orchestrator",
        "mode": mode,
        "answer": answer,
        "response": answer,
        "text": answer,
        "human_answer": answer,
        "sources": [],
    }
