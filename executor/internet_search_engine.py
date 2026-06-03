from __future__ import annotations

import json, re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

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

def clean_duck_url(url: str) -> str:
    url = url or ""
    if url.startswith("//"):
        url = "https:" + url
    try:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if "uddg" in qs and qs["uddg"]:
            return unquote(qs["uddg"][0])
    except Exception:
        pass
    return url

def search_web(query: str, limit: int = 5) -> dict[str, Any]:
    try:
        import requests
        from bs4 import BeautifulSoup
    except Exception as e:
        return {"ok": False, "error": "missing_dependencies", "detail": repr(e)}

    q = clean(query)
    if not q:
        return {"ok": False, "error": "empty_query"}

    url = "https://duckduckgo.com/html/?q=" + quote_plus(q)

    try:
        r = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0 NOUS"})
    except Exception as e:
        return {"ok": False, "error": "request_failed", "detail": repr(e)}

    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for item in soup.select(".result"):
        a = item.select_one(".result__a")
        sn = item.select_one(".result__snippet")
        if not a:
            continue

        results.append({
            "title": clean(a.get_text(" ", strip=True)),
            "url": clean_duck_url(a.get("href", "")),
            "snippet": clean(sn.get_text(" ", strip=True)) if sn else "",
        })

        if len(results) >= limit:
            break

    payload = {
        "ok": True,
        "tool": "Internet Search Engine",
        "timestamp": now_iso(),
        "query": q,
        "results": results,
    }

    cache = load_json(CACHE, [])
    if not isinstance(cache, list):
        cache = []
    cache.append(payload)
    save_json(CACHE, cache[-100:])

    return payload

def answer_from_web(query: str) -> dict[str, Any]:
    res = search_web(query)
    if not res.get("ok"):
        return {
            "ok": False,
            "mode": "internet_search",
            "answer": "Δεν μπόρεσα να ολοκληρώσω την αναζήτηση στο internet.",
            "results": [],
            "raw": res,
        }

    results = res.get("results", [])
    if not results:
        return {
            "ok": True,
            "mode": "internet_search",
            "answer": "Έψαξα στο internet αλλά δεν βρήκα καθαρά αποτελέσματα.",
            "results": [],
            "raw": res,
        }

    lines = ["Βρήκα αυτά τα σχετικά αποτελέσματα στο internet:"]
    for i, x in enumerate(results[:3], 1):
        lines.append(f"\n{i}. {x.get('title')}")
        sn = x.get("snippet", "")
        if sn:
            if len(sn) > 240:
                sn = sn[:240].rstrip() + "..."
            lines.append(f"   {sn}")
        if x.get("url"):
            lines.append(f"   Πηγή: {x.get('url')}")

    return {
        "ok": True,
        "mode": "internet_search",
        "answer": "\n".join(lines),
        "results": results[:3],
        "raw": {
            "ok": True,
            "query": res.get("query"),
            "results_count": len(results),
        },
    }

if __name__ == "__main__":
    import sys
    print(json.dumps(answer_from_web(" ".join(sys.argv[1:])), indent=2, ensure_ascii=False))
