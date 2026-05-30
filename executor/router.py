import os
import sys
import platform
import time
from flask import Flask, request, jsonify, send_from_directory
from executor.kernel import handle
from executor.control_center import CONTROL_CENTER_HTML
from executor.security import check_token

app = Flask(__name__)

@app.route("/")
def home():
    return CONTROL_CENTER_HTML

@app.route("/chat", methods=["POST"])
def chat():
    if not check_token(request):
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    cmd = data.get("command", "")
    return jsonify(handle(cmd, {}))

from executor.health import backup as create_backup
from executor.health import status as health_status

@app.route("/health")
def health():
    return jsonify(health_status())


@app.route("/runtime")
def runtime_route():
    return jsonify({
        "system": "NOUS AI OS",
        "level": 22,
        "python": sys.version,
        "platform": platform.platform(),
        "time": time.time(),
        "cloud_ready": True,
        "host": "0.0.0.0",
        "port": int(os.environ.get("PORT", "5000")),
    })


@app.route("/cloud/status")
def cloud_status_route():
    return jsonify({
        "cloud_ready": True,
        "runtime_endpoint": "/runtime",
        "health_endpoint": "/health",
        "chat_endpoint": "/chat",
        "apps_endpoint": "/apps",
        "port_env": os.environ.get("PORT"),
        "default_port": 5000,
    })

@app.route("/backup")
def backup_route():
    return jsonify(create_backup())

from executor.file_reader import save_upload, read_text

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no_file"})
    return jsonify(save_upload(f))

@app.route("/read-file", methods=["POST"])
def read_file_route():
    data = request.get_json()
    path = data.get("path", "")
    return jsonify({"content": read_text(path)})


from executor.image_reader import save_image, image_preview

@app.route("/upload-image", methods=["POST"])
def upload_image():
    f = request.files.get("file")
    if not f:
        return jsonify({"error": "no_image"})
    return jsonify(save_image(f))

@app.route("/image-preview", methods=["POST"])
def image_preview_route():
    data = request.get_json()
    path = data.get("path", "")
    return jsonify(image_preview(path))


from executor.android_sense import sense as android_sense

@app.route("/sense")
def sense_route():
    return jsonify(android_sense())


from executor.app_builder import list_apps


@app.route("/remote/status")
def remote_status_route():
    from executor import autonomy as autonomy_state
    from executor.scheduler_agent import list_schedules
    from executor.battery_guard import battery_guard
    from executor.agent_review import review_last

    return jsonify({
        "system": "NOUS AI OS",
        "level": 22,
        "battery": battery_guard(),
        "autonomy": autonomy_state.status(),
        "schedules": list_schedules(),
        "review": review_last(),
        "time": time.time(),
    })


@app.route("/dashboard")
def dashboard_route():
    return """
<!doctype html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NOUS Remote Dashboard</title>
  <style>
    body { font-family: sans-serif; padding: 16px; background: #111; color: #eee; }
    .card { background: #1d1d1d; padding: 14px; margin: 12px 0; border-radius: 12px; }
    pre { white-space: pre-wrap; word-break: break-word; }
    button { padding: 10px 14px; border-radius: 10px; border: 0; }
  </style>
</head>
<body>
  <h2>🧠 NOUS AI OS</h2>
  <button onclick="loadStatus()">Refresh</button>
  <div class="card"><pre id="out">Loading...</pre></div>

<script>
async function loadStatus() {
  const r = await fetch('/remote/status');
  const j = await r.json();
  document.getElementById('out').textContent = JSON.stringify(j, null, 2);
}
loadStatus();
</script>
</body>
</html>
"""

@app.route("/apps")
def apps_list():
    return jsonify(list_apps())

@app.route("/apps/<name>/")
def open_generated_app(name):
    return send_from_directory(f"generated_apps/{name}", "index.html")

if __name__ == "__main__":
    print("🧠 NUS AI OS LEVEL 22 RUNNING")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
