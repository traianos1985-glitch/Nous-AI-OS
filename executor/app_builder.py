import os, time

APP_DIR = "generated_apps"

def make_web_app(name, title="ΝΟΥΣ App", body="Hello from ΝΟΥΣ"):
    safe = "".join(c for c in name if c.isalnum() or c in "-_") or f"app_{int(time.time())}"
    path = os.path.join(APP_DIR, safe)
    os.makedirs(path, exist_ok=True)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
body{{font-family:Arial;background:#111;color:white;padding:20px}}
.card{{background:#1e1e1e;border-radius:16px;padding:20px}}
button{{padding:12px;border:0;border-radius:10px;background:#00ff88}}
</style>
</head>
<body>
<div class="card">
<h1>{title}</h1>
<p>{body}</p>
<button onclick="alert('ΝΟΥΣ app active')">OK</button>
</div>
</body>
</html>"""

    open(os.path.join(path, "index.html"), "w", encoding="utf-8").write(html)
    return {"created": True, "path": path, "entry": os.path.join(path, "index.html")}
