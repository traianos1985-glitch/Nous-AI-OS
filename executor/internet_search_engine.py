from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

CACHE = Path("data/internet_search_cache.json")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def _ddg_instant(query: str) -> list[dict]:
    """DuckDuckGo Instant Answer API — free, no key needed."""
    try:
        import requests
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_redirect": 1, "no_html": 1, "skip_disambig": 1}
        r = requests.get(url, params=params, timeout=12, headers={"User-Agent": "NOUS-AI-OS/1.0"})
        data = r.json()
        results = []

        abstract = clean(data.get("AbstractText", ""))
        if abstract:
            results.append({
                "title": clean(data.get("Heading", query)),
                "url": data.get("AbstractURL", ""),
                "snippet": abstract,
                "source": "ddg_instant",
            })

        for rel in data.get("RelatedTopics", [])[:6]:
            if isinstance(rel, dict) and rel.get("Text"):
                url_link = rel.get("FirstURL", "")
                results.append({
                    "title": clean(rel.get("Text", "")[:80]),
                    "url": url_link,
                    "snippet": clean(rel.get("Text", "")),
                    "source": "ddg_related",
                })

        return results
    except Exception:
        return []


def _ddg_html(query: str, limit: int = 5) -> list[dict]:
    """DuckDuckGo HTML fallback with rotating user agents."""
    try:
        import requests
        from bs4 import BeautifulSoup

        agents = [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
        for agent in agents:
            url = "https://duckduckgo.com/html/?q=" + quote_plus(query)
            r = requests.get(url, timeout=15, headers={
                "User-Agent": agent,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "el,en-US;q=0.9",
            })
            if r.status_code != 200:
                time.sleep(1)
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            results = []

            # Try multiple possible selectors
            for item in soup.select(".result, .web-result, article"):
                a = item.select_one("a.result__a, a[href], h2 a")
                sn = item.select_one(".result__snippet, .snippet, p")
                if not a:
                    continue
                href = a.get("href", "")
                if not href or href.startswith("/"):
                    continue
                results.append({
                    "title": clean(a.get_text(" ", strip=True)),
                    "url": href,
                    "snippet": clean(sn.get_text(" ", strip=True)) if sn else "",
                    "source": "ddg_html",
                })
                if len(results) >= limit:
                    break

            if results:
                return results

    except Exception:
        pass
    return []


def _llm_web_answer(query: str) -> str | None:
    """Use the LLM to answer if web search fails."""
    try:
        from executor.remote_llm import ask_remote_llm
        prompt = (
            f"Ερώτηση χρήστη για αναζήτηση στο internet: {query}\n\n"
            "Απάντησε με βάση τις γνώσεις σου. Αν δεν ξέρεις σίγουρα, πες το ξεκάθαρα. "
            "Μην επινοείς συνδέσμους. Απάντα σύντομα και ουσιαστικά στα ελληνικά."
        )
        r = ask_remote_llm(prompt)
        if r.get("success") and r.get("response"):
            return r["response"]
    except Exception:
        pass
    return None


def search_web(query: str, limit: int = 5) -> dict[str, Any]:
    q = clean(query)
    if not q:
        return {"ok": False, "error": "empty_query"}

    results = _ddg_instant(q)

    if not results:
        results = _ddg_html(q, limit)

    payload = {
        "ok": True,
        "tool": "Internet Search Engine",
        "timestamp": now_iso(),
        "query": q,
        "results": results[:limit],
    }

    cache = load_json(CACHE, [])
    if not isinstance(cache, list):
        cache = []
    cache.append(payload)
    save_json(CACHE, cache[-100:])

    return payload


def answer_from_web(query: str) -> dict[str, Any]:
    res = search_web(query)
    results = res.get("results", [])

    if results:
        lines = ["Βρήκα αυτά τα σχετικά αποτελέσματα:"]
        for i, x in enumerate(results[:4], 1):
            lines.append(f"\n{i}. **{x.get('title', 'Αποτέλεσμα')}**")
            sn = x.get("snippet", "")
            if sn:
                if len(sn) > 240:
                    sn = sn[:240].rstrip() + "..."
                lines.append(f"   {sn}")
            if x.get("url"):
                lines.append(f"   🔗 {x.get('url')}")
        answer = "\n".join(lines)
    else:
        # Fall back to LLM
        llm_ans = _llm_web_answer(query)
        if llm_ans:
            answer = f"Δεν βρήκα live αποτελέσματα, αλλά με βάση τις γνώσεις μου:\n\n{llm_ans}"
        else:
            answer = "Δεν μπόρεσα να βρω αποτελέσματα γι' αυτή την αναζήτηση."

    return {
        "ok": True,
        "mode": "internet_search",
        "answer": answer,
        "results": results[:4],
        "raw": {"ok": True, "query": res.get("query"), "results_count": len(results)},
    }


if __name__ == "__main__":
    import sys
    print(json.dumps(answer_from_web(" ".join(sys.argv[1:])), indent=2, ensure_ascii=False))
