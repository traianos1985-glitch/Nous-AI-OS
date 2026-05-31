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
from executor.autonomy_service import enable as service_enable, disable as service_disable, status as service_status, run_cycle as service_run_cycle, watchdog_check
from executor.goal_executor import goal_executor_cycle
from executor.project_progress import list_progress, project_summary, sync_projects, mark_step
from executor.self_healing_runtime import self_heal_check
from executor.task_queue import list_queue, clear_queue, retry_failed, recover_dead_tasks
from executor.runtime_metrics import collect_metrics
from executor.curiosity_agent import curiosity_cycle, knowledge_status, load_queue, load_knowledge, add_topic, mark_learned, active_learning_topics
from executor.learning_engine import learning_status, learning_run
from executor.android_control import android_status, android_notify, android_safe_commands, android_open_url
from executor.app_evolver import app_evolution_status, queue_app_improvement
from executor.local_llm_adapter import local_llm_status, ask_local
from executor.decision_engine import decide_next_action, prioritize_goals
from executor.real_action_executor import agent_act_cycle
from executor.agent_journal import list_journal
from executor.progress_linker import progress_snapshot, link_task_to_project
from executor.goal_progress import list_goal_progress, refresh_goal_progress, goal_progress_summary
from executor.app_factory_v2 import create_app_from_idea, queue_app_idea, app_factory_status
from executor.code_assistant import code_health, code_advice
from executor.research_browser_agent import research_query, read_url
from executor.knowledge_research import research_next_topic, learning_cycle

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










@app.route("/remote/research/query", methods=["POST"])
def remote_research_query_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(research_query(
        data.get("query", ""),
        bool(data.get("learn", False)),
        data.get("topic")
    ))


@app.route("/remote/browser/read", methods=["POST"])
def remote_browser_read_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(read_url(
        data.get("url", ""),
        bool(data.get("learn", False)),
        data.get("topic")
    ))






@app.route("/remote/goals/progress")
def remote_goals_progress_route():
    return jsonify(list_goal_progress())


@app.route("/remote/goals/refresh", methods=["POST"])
def remote_goals_refresh_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(refresh_goal_progress())


@app.route("/remote/goals/summary")
def remote_goals_summary_route():
    return jsonify(goal_progress_summary())

@app.route("/remote/progress/snapshot")
def remote_progress_snapshot_route():
    return jsonify(progress_snapshot())


@app.route("/remote/progress/link-task", methods=["POST"])
def remote_progress_link_task_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(link_task_to_project(data))

@app.route("/remote/agent/decide")
def remote_agent_decide_route():
    return jsonify(decide_next_action())


@app.route("/remote/agent/act", methods=["POST"])
def remote_agent_act_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(agent_act_cycle())


@app.route("/remote/agent/goals")
def remote_agent_goals_route():
    return jsonify(prioritize_goals())


@app.route("/remote/agent/journal")
def remote_agent_journal_route():
    return jsonify(list_journal())

@app.route("/remote/local-llm/status")
def remote_local_llm_status_route():
    return jsonify(local_llm_status())


@app.route("/remote/local-llm/ask", methods=["POST"])
def remote_local_llm_ask_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(ask_local(data.get("prompt", ""), int(data.get("timeout", 60))))


@app.route("/remote/app-evolver/status")
def remote_app_evolver_status_route():
    return jsonify(app_evolution_status())


@app.route("/remote/app-evolver/queue", methods=["POST"])
def remote_app_evolver_queue_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(queue_app_improvement(
        data.get("app", ""),
        data.get("request", "βελτίωσε την εφαρμογή"),
        int(data.get("priority", 4))
    ))


@app.route("/remote/android/open-url", methods=["POST"])
def remote_android_open_url_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(android_open_url(data.get("url", "")))

@app.route("/remote/code/health")
def remote_code_health_route():
    return jsonify(code_health())


@app.route("/remote/code/advice")
def remote_code_advice_route():
    return jsonify(code_advice())


@app.route("/remote/app-factory/status")
def remote_app_factory_status_route():
    return jsonify(app_factory_status())


@app.route("/remote/app-factory/create", methods=["POST"])
def remote_app_factory_create_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(create_app_from_idea(data.get("idea", "")))


@app.route("/remote/app-factory/queue", methods=["POST"])
def remote_app_factory_queue_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(queue_app_idea(
        data.get("idea", ""),
        int(data.get("priority", 4))
    ))


@app.route("/remote/android/status")
def remote_android_status_route():
    return jsonify(android_status())


@app.route("/remote/android/safe-commands")
def remote_android_safe_commands_route():
    return jsonify(android_safe_commands())


@app.route("/remote/android/notify", methods=["POST"])
def remote_android_notify_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(android_notify(
        data.get("title", "ΝΟΥΣ AI"),
        data.get("message", "Ο ΝΟΥΣ είναι ενεργός")
    ))

@app.route("/remote/learning/status")
def remote_learning_status_route():
    return jsonify(learning_status())


@app.route("/remote/learning/run", methods=["POST"])
def remote_learning_run_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    max_topics = int(data.get("max_topics", 1))
    research = bool(data.get("research", False))

    return jsonify(learning_run(max_topics=max_topics, research=research))


@app.route("/remote/research/next", methods=["POST"])
def remote_research_next_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    return jsonify(research_next_topic())


@app.route("/remote/research/cycle", methods=["POST"])
def remote_research_cycle_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    max_topics = int(data.get("max_topics", 1))
    return jsonify(learning_cycle(max_topics=max_topics))

@app.route("/remote/knowledge")
def remote_knowledge_route():
    return jsonify(knowledge_status())


@app.route("/remote/knowledge/queue")
def remote_knowledge_queue_route():
    return jsonify(load_queue())


@app.route("/remote/knowledge/base")
def remote_knowledge_base_route():
    return jsonify(load_knowledge())


@app.route("/remote/knowledge/cycle", methods=["POST"])
def remote_knowledge_cycle_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(curiosity_cycle())


@app.route("/remote/knowledge/add", methods=["POST"])
def remote_knowledge_add_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(add_topic(
        data.get("topic", ""),
        data.get("reason", "manual"),
        data.get("priority", 5),
        "remote"
    ))


@app.route("/remote/knowledge/learned", methods=["POST"])
def remote_knowledge_learned_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    return jsonify(mark_learned(
        data.get("topic", ""),
        data.get("summary", ""),
        data.get("source", "remote")
    ))

@app.route("/remote/metrics")
def remote_metrics_route():
    return jsonify(collect_metrics())


@app.route("/remote/service/watchdog")
def remote_service_watchdog_route():
    return jsonify(watchdog_check())


@app.route("/remote/queue/retry-failed", methods=["POST"])
def remote_queue_retry_failed_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(retry_failed())


@app.route("/remote/queue/recover-dead", methods=["POST"])
def remote_queue_recover_dead_route():
    if not check_admin_token(request):
        return jsonify({"error": "unauthorized"}), 401
    return jsonify(recover_dead_tasks())

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
        "metrics": collect_metrics(),
        "knowledge": knowledge_status(),
        "learning": learning_status(),
        "code": code_health(),
        "app_factory": app_factory_status(),
        "app_evolver": app_evolution_status(),
        "local_llm": local_llm_status(),
        "agent": decide_next_action(),
        "progress": progress_snapshot(),
        "goal_progress": goal_progress_summary(),
        "android": android_safe_commands(),
        "active_learning_topics": active_learning_topics(),
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
