import os
import sys
import platform
import time
from flask import Flask, request, jsonify, send_from_directory
from executor.kernel import handle
from executor.control_center import CONTROL_CENTER_HTML
from executor.security import check_token, check_admin_token
from executor.api_tokens import create_token, list_tokens, revoke_token, token_stats
from executor import autonomy as autonomy_state
from executor.autonomy_service import enable as service_enable, disable as service_disable, status as service_status, run_cycle as service_run_cycle
from executor.goal_executor import goal_executor_cycle
from executor.project_progress import list_progress, project_summary, sync_projects, mark_step
from executor.self_healing_runtime import self_heal_check
from executor.task_queue import list_queue, clear_queue

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



@app.route("/token/create", methods=["POST"])
def token_create_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    name = data.get("name", "remote")
    return jsonify(create_token(name))


@app.route("/token/list")
def token_list_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    return jsonify(list_tokens())


@app.route("/token/revoke", methods=["POST"])
def token_revoke_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    token_id = data.get("id")
    return jsonify(revoke_token(token_id))

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
        "tokens": token_stats(),
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






@app.route("/remote/projects")
def remote_projects_route():
    return jsonify(list_progress())


@app.route("/remote/projects/summary")
def remote_projects_summary_route():
    return jsonify(project_summary())


@app.route("/remote/projects/sync", methods=["POST"])
def remote_projects_sync_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(sync_projects())


@app.route("/remote/projects/mark-step", methods=["POST"])
def remote_projects_mark_step_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(mark_step(
        data.get("project", ""),
        data.get("step", ""),
        data.get("status", "done")
    ))


@app.route("/remote/self-heal/check", methods=["POST"])
def remote_self_heal_check_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(self_heal_check())

@app.route("/remote/queue")
def remote_queue_route():
    return jsonify(list_queue())


@app.route("/remote/queue/clear", methods=["POST"])
def remote_queue_clear_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(clear_queue())


@app.route("/remote/goals/run", methods=["POST"])
def remote_goals_run_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(goal_executor_cycle())

@app.route("/remote/service/status")
def remote_service_status_route():
    return jsonify(service_status())


@app.route("/remote/service/enable", methods=["POST"])
def remote_service_enable_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    interval = int(data.get("interval", 300))
    return jsonify(service_enable(interval))


@app.route("/remote/service/disable", methods=["POST"])
def remote_service_disable_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    return jsonify(service_disable())


@app.route("/remote/service/run-once", methods=["POST"])
def remote_service_run_once_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    return jsonify(service_run_cycle())

@app.route("/remote/autonomy/start", methods=["POST"])
def remote_autonomy_start_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"result": autonomy_state.start()})


@app.route("/remote/autonomy/stop", methods=["POST"])
def remote_autonomy_stop_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"result": autonomy_state.stop()})


@app.route("/remote/autonomy/status")
def remote_autonomy_status_route():
    return jsonify(autonomy_state.status())

@app.route("/remote/status")
def remote_status_route():
    from executor.scheduler_agent import list_schedules
    from executor.battery_guard import battery_guard
    from executor.agent_review import review_last

    return jsonify({
        "system": "NOUS AI OS",
        "level": 22,
        "battery": battery_guard(),
        "autonomy": autonomy_state.status(),
        "service": service_status(),
        "schedules": list_schedules(),
        "queue": list_queue(),
        "projects_progress": project_summary(),
        "review": review_last(),
        "time": time.time(),
        "tokens": token_stats(),
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
    input { width: 100%; padding: 10px; border-radius: 10px; border: 0; margin: 6px 0; }
    button { padding: 10px 14px; border-radius: 10px; border: 0; margin: 4px; }
  </style>
</head>
<body>
  <h2>🧠 NOUS AI OS</h2>

  <div class="card">
    <h3>Token</h3>
    <input id="token" placeholder="X-NOUS-TOKEN">
  </div>

  <div class="card">
    <h3>Controls</h3>
    <button onclick="loadStatus()">Refresh</button>
    <button onclick="autonomyStart()">Autonomy Start</button>
    <button onclick="autonomyStop()">Autonomy Stop</button>
    <button onclick="autonomyStatus()">Autonomy Status</button>
  </div>

  <div class="card">
    <h3>Command</h3>
    <input id="command" placeholder="π.χ. τι θυμάσαι?">
    <button onclick="sendCommand()">Send</button>
  </div>

  <div class="card"><pre id="out">Loading...</pre></div>

<script>
function getToken() {
  return document.getElementById('token').value.trim();
}

function show(obj) {
  document.getElementById('out').textContent = JSON.stringify(obj, null, 2);
}

async function loadStatus() {
  const r = await fetch('/remote/status');
  show(await r.json());
}

async function autonomyStatus() {
  const r = await fetch('/remote/autonomy/status');
  show(await r.json());
}

async function autonomyStart() {
  const r = await fetch('/remote/autonomy/start', {
    method: 'POST',
    headers: {'X-NOUS-TOKEN': getToken()}
  });
  show(await r.json());
}

async function autonomyStop() {
  const r = await fetch('/remote/autonomy/stop', {
    method: 'POST',
    headers: {'X-NOUS-TOKEN': getToken()}
  });
  show(await r.json());
}

async function sendCommand() {
  const command = document.getElementById('command').value;
  const r = await fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-NOUS-TOKEN': getToken()
    },
    body: JSON.stringify({command})
  });
  show(await r.json());
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
