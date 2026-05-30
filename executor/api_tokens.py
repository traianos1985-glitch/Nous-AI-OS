import json
import os
import time
import secrets
import hashlib

FILE = "data/api_tokens.json"


def _load():
    if not os.path.exists(FILE):
        return []
    try:
        return json.load(open(FILE, "r", encoding="utf-8"))
    except Exception:
        return []


def _save(tokens):
    os.makedirs("data", exist_ok=True)
    json.dump(tokens, open(FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def _hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_token(name="remote"):
    token = "nous_" + secrets.token_urlsafe(32)
    item = {
        "id": int(time.time_ns()),
        "name": str(name).strip() or "remote",
        "token_hash": _hash(token),
        "created": time.time(),
        "revoked": False,
        "last_used": None,
    }

    tokens = _load()
    tokens.append(item)
    _save(tokens)

    return {
        "id": item["id"],
        "name": item["name"],
        "token": token,
        "created": item["created"],
    }


def list_tokens():
    return [
        {
            "id": item.get("id"),
            "name": item.get("name"),
            "created": item.get("created"),
            "revoked": item.get("revoked", False),
            "last_used": item.get("last_used"),
        }
        for item in _load()
    ]


def revoke_token(token_id):
    tokens = _load()
    found = False

    for item in tokens:
        if str(item.get("id")) == str(token_id):
            item["revoked"] = True
            found = True

    _save(tokens)
    return {"revoked": found, "id": token_id}


def token_allowed(token):
    if not token:
        return False

    h = _hash(str(token))
    tokens = _load()
    changed = False

    for item in tokens:
        if item.get("revoked"):
            continue

        if item.get("token_hash") == h:
            item["last_used"] = time.time()
            changed = True
            _save(tokens)
            return True

    if changed:
        _save(tokens)

    return False
