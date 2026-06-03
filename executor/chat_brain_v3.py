from __future__ import annotations

import ast
import json
import operator as op
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from executor.document_chat_bridge import document_chat_answer, format_document_answer
from executor.internet_search_engine import answer_from_web
from executor.deep_research_engine import deep_research
from executor.url_reader_engine import summarize_url
from executor.chat_capabilities import capability_text
from executor.conversation_manager import append_turn, conversation_context
from executor.conversation_summary_engine import update_conversation_summary, summary_context
from executor.conversation_search_engine import answer_from_conversations, cross_conversation_context
from executor.conversation_title_engine import generate_conversation_title

DATA = Path("data")
REPORTS = DATA / "reports"
CHAT_MEMORY = DATA / "chat_memory_v3.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def remember_turn(user: str, answer: str, mode: str) -> None:
    memory = load_json(CHAT_MEMORY, [])
    if not isinstance(memory, list):
        memory = []

    memory.append({
        "time": now_iso(),
        "user": user,
        "answer": answer,
        "mode": mode,
    })

    save_json(CHAT_MEMORY, memory[-80:])


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
    return any(w in m for w in [
        "εγχειρίδιο", "εγχειριδιο", "manual",
        "pdf", "docx", "έγγραφο", "εγγραφο",
        "αρχείο", "αρχειο", "μαθημένο", "μαθημενο",
        "μαθημένα", "μαθημενα", "σύμφωνα με τα έγγραφα",
        "τι λένε τα έγγραφα", "τι λεει το εγχειριδιο",
        "τι λέει το εγχειρίδιο"
    ])






def has_conversation_search_intent(message: str) -> bool:
    m = norm(message)
    return any(x in m for x in [
        "βρες τη συνομιλία",
        "βρες την συνομιλία",
        "ψάξε στις συνομιλίες",
        "ψαξε στις συνομιλιες",
        "παλιά συνομιλία",
        "παλια συνομιλια",
        "παλιές συνομιλίες",
        "παλιες συνομιλιες",
        "σε ποια συνομιλία",
        "σε ποια συνομιλια",
        "conversation search"
    ])


def has_cross_memory_intent(message: str) -> bool:
    m = norm(message)
    return any(x in m for x in [
        "θυμάσαι τι αποφασίσαμε",
        "θυμασαι τι αποφασισαμε",
        "τι είχαμε πει",
        "τι ειχαμε πει",
        "παλιότερα",
        "παλιοτερα",
        "πριν καιρό",
        "πριν καιρο",
        "σε άλλη συνομιλία",
        "σε αλλη συνομιλια",
        "από παλιά συνομιλία",
        "απο παλια συνομιλια"
    ])


def has_deep_research_intent(message: str) -> bool:
    m = norm(message)
    return any(x in m for x in [
        "κάνε βαθιά έρευνα",
        "κανε βαθια ερευνα",
        "deep research",
        "ψάξε βαθιά",
        "ψαξε βαθια",
        "ερεύνησε αναλυτικά",
        "ερευνησε αναλυτικα",
        "άνοιξε πηγές",
        "ανοιξε πηγες"
    ])


def has_internet_intent(message: str) -> bool:
    m = norm(message)
    return any(w in m for w in [
        "ψάξε", "ψαξε", "αναζήτησε", "αναζητησε",
        "internet", "ίντερνετ", "ιντερνετ", "online", "web",
        "τελευταία", "τελευταια", "νέα", "νεα", "ειδήσεις", "ειδησεις",
        "τρέχον", "τρεχον", "σημεριν", "τιμή", "τιμη", "κόστος", "κοστος"
    ])


def has_calc_intent(message: str) -> bool:
    m = norm(message)
    if any(w in m for w in ["υπολόγισε", "υπολογισε", "πόσο κάνει", "ποσο κανει", "calculator"]):
        return True
    return bool(re.fullmatch(r"[0-9\s\+\-\*\/\.\,\(\)%]+", m))


_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
    ast.Mod: op.mod,
}


def safe_eval(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](safe_eval(node.left), safe_eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](safe_eval(node.operand))
    raise ValueError("unsafe_expression")


def calculator_answer(message: str) -> str:
    expr = norm(message)
    expr = expr.replace("υπολόγισε", "").replace("υπολογισε", "")
    expr = expr.replace("πόσο κάνει", "").replace("ποσο κανει", "")
    expr = expr.replace(",", ".")
    expr = expr.strip()

    tree = ast.parse(expr, mode="eval")
    result = safe_eval(tree)

    if int(result) == result:
        result = int(result)

    return f"Το αποτέλεσμα είναι: {result}"


def extract_urls(message: str) -> list[str]:
    return re.findall(r"https?://[^\s]+", message or "")


def link_answer(message: str) -> str | None:
    urls = extract_urls(message)
    if not urls:
        return None

    lines = ["Βρήκα τους συνδέσμους που έστειλες:"]
    for i, u in enumerate(urls, 1):
        lines.append(f"{i}. {u}")
    return "\n".join(lines)


def is_about_nous(message: str) -> bool:
    m = norm(message)
    return "νους" in m or "νουσ" in m or "nous" in m


def nous_status_answer() -> str:
    priorities = load_json(DATA / "executive_priorities.json", {})
    summary = load_json(DATA / "executive_state_summary.json", {})

    top = priorities.get("top_action") if isinstance(priorities, dict) else None

    missions = summary.get("missions", {}).get("total", 0) if isinstance(summary, dict) else 0
    reviews = summary.get("pending_reviews", {}).get("total", 0) if isinstance(summary, dict) else 0
    patches = summary.get("patch_proposals", {}).get("total", 0) if isinstance(summary, dict) else 0

    lines = [
        "Για να γίνει ο ΝΟΥΣ πιο κοντά σε πραγματικό AI Agent, οι βασικές βελτιώσεις είναι:",
        "",
        "• Καθαρό chat σαν ChatGPT, χωρίς να δημιουργεί αποστολές μόνος του.",
        "• Καλύτερη σύνθεση απαντήσεων από έγγραφα, μνήμη και internet.",
        "• Upload αρχείων και εικόνων με αυτόματη ανάλυση.",
        "• Web page reader για να διαβάζει ολόκληρες σελίδες και όχι μόνο αποτελέσματα αναζήτησης.",
        "• Conversational memory για συνέχεια στη συζήτηση.",
        "• Πιο αυστηρό mission mode μόνο με ρητή εντολή.",
        "",
        f"Τρέχουσα εικόνα: missions={missions}, pending reviews={reviews}, patch proposals={patches}."
    ]

    if top:
        lines.append("")
        lines.append("Πρώτη προτεραιότητα που βλέπει ο prioritizer:")
        lines.append(f"• {top.get('title', 'Άγνωστο')}")

    return "\n".join(lines)


def casual_answer(message: str) -> str | None:
    m = norm(message)

    if any(x in m for x in ["τι κάνεις", "τι κανεις", "πως είσαι", "πώς είσαι", "πως εισαι"]):
        return (
            "Είμαι εδώ φίλε μου και λειτουργώ κανονικά. "
            "Μπορείς να με ρωτήσεις, να μου δώσεις έγγραφο, να ζητήσεις αναζήτηση internet, "
            "ή να γράψεις /plan για να φτιάξω αποστολή."
        )

    if any(x in m for x in ["γεια", "γειά", "καλημέρα", "καλημερα", "καλησπέρα", "καλησπερα"]):
        return "Γεια σου φίλε μου. Είμαι έτοιμος. Τι θέλεις να δούμε;"

    if is_about_nous(message) and any(x in m for x in ["βελτι", "καλυτερ", "πρέπει", "πρεπει", "λείπει", "λειπει"]):
        return nous_status_answer()

    return None




def looks_corrupted_answer(text: str) -> bool:
    t = str(text or "").strip()

    if not t:
        return True

    if len(t) < 2:
        return True

    greek = sum(1 for ch in t if "\u0370" <= ch <= "\u03ff")
    latin = sum(1 for ch in t if ("a" <= ch.lower() <= "z"))
    letters = sum(1 for ch in t if ch.isalpha())
    weird = sum(1 for ch in t if ord(ch) > 127 and not ("\u0370" <= ch <= "\u03ff") and ch not in "€–—“”‘’•…")

    if letters >= 30 and greek < 6 and latin < 20:
        return True

    if weird > max(8, len(t) * 0.08):
        return True

    bad_fragments = [
        "επιδελιώστα",
        "κραταγωγή",
        "έπληθιστε",
        "ακριηζον",
        "ηπαγωγή",
        "ναιμησίας",
        "πлавή",
    ]

    low = t.lower()
    if any(x in low for x in bad_fragments):
        return True

    words = [w.strip(".,;:!?()[]{}\"'") for w in low.split()]
    if len(words) >= 8:
        short_or_odd = 0
        for w in words:
            if not w:
                continue
            has_letter = any(ch.isalpha() for ch in w)
            if has_letter and len(w) <= 2:
                short_or_odd += 1
        if short_or_odd > len(words) * 0.45:
            return True

    return False


def safe_llm_fallback() -> str:
    return (
        "Δεν είμαι βέβαιος για την απάντηση που πήγα να δώσω, "
        "οπότε δεν την κρατάω ως αξιόπιστη. Μπορείς να το διατυπώσεις λίγο πιο συγκεκριμένα;"
    )


def try_llm_answer(message: str, conversation_id: str | None = None) -> str | None:
    try:
        from executor.llm_core import ask
    except Exception:
        return None

    recent = recent_chat_context(6)
    selected_context = conversation_context(conversation_id, 10)
    selected_summary = summary_context(conversation_id)
    global_memory = cross_conversation_context(message, limit=3) if has_cross_memory_intent(message) else ""
    context = selected_context or selected_summary or global_memory or recent

    prompt = f"""
Απάντησε στα ελληνικά, καθαρά και σύντομα, σαν βοηθός τύπου ChatGPT.
Μην δημιουργείς αποστολή. Μην δίνεις JSON.
Μην εφευρίσκεις δυνατότητες, τεχνικές λεπτομέρειες ή χαρακτηριστικά που δεν υπάρχουν στο ιστορικό.
Αν κάτι δεν είναι γνωστό, πες καθαρά ότι δεν είναι επιβεβαιωμένο.

Ιστορικό ενεργής συνομιλίας:
{context}

Ερώτηση χρήστη:
{message}
""".strip()

    try:
        result = ask(prompt)
    except Exception:
        return None

    if isinstance(result, dict):
        for key in ["answer", "response", "text", "content"]:
            if isinstance(result.get(key), str) and result.get(key).strip():
                candidate = result[key].strip()
                if looks_corrupted_answer(candidate):
                    return safe_llm_fallback()
                return candidate
        return None

    if isinstance(result, str) and result.strip():
        candidate = result.strip()
        if looks_corrupted_answer(candidate):
            return safe_llm_fallback()
        return candidate

    return None






def recent_chat_context(limit: int = 3) -> str:
    memory = load_json(CHAT_MEMORY, [])

    if not isinstance(memory, list) or not memory:
        return ""

    clean_items = []

    for item in memory:
        if not isinstance(item, dict):
            continue

        u = str(item.get("user", "")).strip()
        a = str(item.get("answer", "")).strip()
        mode = str(item.get("mode", "")).strip()

        if not u or not a:
            continue

        ulow = u.lower()

        if any(x in ulow for x in ["θυμάσαι", "θυμασαι", "τι είπα", "τι ειπα"]):
            continue

        if mode in {"memory_recall"}:
            continue

        clean_items.append((u, a))

    recent = clean_items[-limit:]
    lines = []

    for u, a in recent:
        if len(a) > 180:
            a = a[:180].rstrip() + "..."

        lines.append(f"• Εσύ: {u}\n  ΝΟΥΣ: {a}")

    return "\n\n".join(lines)



def memory_question_answer(message: str, conversation_id: str | None = None) -> str | None:
    m = norm(message)

    if not any(x in m for x in [
        "τι είπα",
        "τι ειπα",
        "τι συζητάμε",
        "τι συζηταμε",
        "θυμάσαι",
        "θυμασαι",
        "πριν",
        "προηγουμένως",
        "προηγουμενως",
        "εδώ",
        "εδω"
    ]):
        return None

    active_ctx = conversation_context(conversation_id, 8) if conversation_id else ""

    if active_ctx:
        return "Στην ενεργή συνομιλία θυμάμαι:\n\n" + active_ctx

    ctx = recent_chat_context(3)

    if not ctx:
        return "Δεν έχω ακόμα αρκετό χρήσιμο πρόσφατο ιστορικό συνομιλίας."

    return "Από την πρόσφατη συνομιλία θυμάμαι:\n\n" + ctx


def summarize_search_results(web: dict[str, Any]) -> str:
    results = web.get("results", [])
    if not results:
        return web.get("answer", "Δεν βρήκα καθαρά αποτελέσματα.")

    lines = ["Βρήκα τα εξής βασικά σημεία:"]
    for item in results[:3]:
        title = item.get("title", "Αποτέλεσμα")
        snippet = item.get("snippet", "")
        url = item.get("url", "")
        if len(snippet) > 260:
            snippet = snippet[:260].rstrip() + "..."
        lines.append("")
        lines.append(f"• {title}")
        if snippet:
            lines.append(f"  {snippet}")
        if url:
            lines.append(f"  Πηγή: {url}")

    return "\n".join(lines)




def capability_answer(message: str) -> str | None:
    m = norm(message)
    keys = [
        "τι μπορείς", "τι μπορεις", "δυνατότητες", "δυνατοτητες",
        "διαβάζεις εικόνες", "διαβαζεις εικονες",
        "διαβάζεις αρχεία", "διαβαζεις αρχεια",
        "αρχεία και εικόνες", "αρχεια και εικονες",
        "υποστηρίζεις", "υποστηριζεις",
        "capabilities"
    ]
    if any(k in m for k in keys):
        return capability_text()
    return None




def user_statement_answer(message: str) -> str | None:
    m = norm(message)

    statement_starts = [
        "μιλάμε για", "μιλαμε για",
        "συζητάμε για", "συζηταμε για",
        "θέλω να θυμάσαι", "θελω να θυμασαι",
        "κρατάμε ότι", "κραταμε οτι",
        "σημείωσε", "σημειωσε",
        "να θυμάσαι", "να θυμασαι",
        "θέλω να", "θελω να",
        "επίσης θέλω", "επισης θελω",
        "θέλω επίσης", "θελω επισης"
    ]

    if any(m.startswith(x) for x in statement_starts):
        return (
            "Το κρατάω στην ενεργή συνομιλία. "
            "Όταν συνεχίσουμε από αυτή τη συνομιλία, θα μπορώ να το χρησιμοποιήσω ως πλαίσιο."
        )

    return None


def fallback_answer(message: str) -> str:
    return (
        "Σε ακούω. Μπορώ να απαντήσω σε απλή συζήτηση, να ψάξω στα μαθημένα έγγραφα, "
        "να κάνω internet search όταν μου το ζητήσεις, ή να δημιουργήσω αποστολή μόνο με /plan ή /run."
    )


def answer_chat(message: str, conversation_id: str | None = None) -> dict[str, Any] | None:
    if is_explicit_command(message):
        return None

    mode = "normal_chat"
    answer = None
    sources = []

    if has_document_intent(message):
        doc = document_chat_answer(message)
        if doc.get("used_documents") and doc.get("sources"):
            answer = format_document_answer(message)
            sources = [{"document": s.get("document")} for s in doc.get("sources", [])]
            mode = "document_recall"

    if answer is None and has_conversation_search_intent(message):
        conv_search = answer_from_conversations(message)
        answer = conv_search.get("answer") or "Δεν βρήκα σχετικές συνομιλίες."
        sources = [{"document": h.get("conversation_id")} for h in conv_search.get("hits", [])]
        mode = "conversation_search"

    if answer is None and has_cross_memory_intent(message):
        memory = cross_conversation_context(message, limit=5)
        if memory:
            answer = memory
            mode = "cross_conversation_memory"

    if answer is None and has_deep_research_intent(message):
        research = deep_research(message, max_results=5)
        answer = research.get("answer") or "Δεν μπόρεσα να ολοκληρώσω τη βαθιά έρευνα."
        sources = [{"document": s.get("url")} for s in research.get("sources", [])]
        mode = "deep_research"

    if answer is None and has_internet_intent(message):
        web = answer_from_web(message)
        answer = summarize_search_results(web)
        sources = [{"document": r.get("url")} for r in web.get("results", [])[:3]]
        mode = "internet_search"

    if answer is None and has_calc_intent(message):
        try:
            answer = calculator_answer(message)
            mode = "calculator"
        except Exception:
            answer = "Δεν μπόρεσα να υπολογίσω αυτή την έκφραση."
            mode = "calculator_error"

    if answer is None:
        urls = extract_urls(message)
        if urls:
            url_result = summarize_url(urls[0])
            answer = url_result.get("answer") or link_answer(message)
            sources = [{"document": urls[0]}]
            mode = "url_reader"

    if answer is None:
        answer = memory_question_answer(message, conversation_id=conversation_id)
        if answer is not None:
            mode = "memory_recall"

    if answer is None:
        answer = capability_answer(message)
        if answer is not None:
            mode = "capabilities"

    if answer is None:
        answer = user_statement_answer(message)
        if answer is not None:
            mode = "conversation_note"

    if answer is None:
        answer = casual_answer(message)

    if answer is None:
        answer = try_llm_answer(message, conversation_id=conversation_id)
        if answer:
            mode = "llm_chat"

    if answer is None:
        answer = fallback_answer(message)

    if looks_corrupted_answer(answer):
        answer = safe_llm_fallback()
        mode = "llm_guard"

    remember_turn(message, answer, mode)
    conv = append_turn(
        user_message=message,
        assistant_answer=answer,
        mode=mode,
        conversation_id=conversation_id,
        title=message,
    )

    try:
        if conv.get("conversation_id") and int(conv.get("messages", 0)) >= 10:
            update_conversation_summary(conv.get("conversation_id"))
            generate_conversation_title(conv.get("conversation_id"))
    except Exception:
        pass

    return {
        "ok": True,
        "executed": False,
        "source": "chat_brain_v3",
        "mode": mode,
        "answer": answer,
        "response": answer,
        "text": answer,
        "human_answer": answer,
        "sources": sources,
        "conversation": conv,
        "conversation_id": conv.get("conversation_id"),
        "timestamp": now_iso(),
    }


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "Τι κάνεις;"
    print(json.dumps(answer_chat(q), indent=2, ensure_ascii=False))
