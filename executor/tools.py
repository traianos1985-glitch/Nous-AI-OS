from executor.personal_agent import remember_fact, add_goal, add_project, list_state, plan_goal
from executor.thinking_tools import think_deep, solve_problem, decide
from executor.plugin_ai import generate_plugin
from executor.plugin_tester import test_plugin
from executor.plugin_quarantine import quarantine
from executor.plugin_registry import run_plugin
from executor.plugin_registry import list_plugins
from executor.memory import load
from executor.notifications import notify
from executor.web_agent import web_command
from executor.command_tools import run_command
from executor.system_info import info as system_info
from executor.project_snapshot import snapshot as project_snapshot
from executor.compile_check import check as compile_check
from executor.memory_tools import recent as memory_recent, summary as memory_summary
from executor.planner import make_plan
from executor.task_state import add_task, list_tasks
from executor.source_reader import read_source
from executor.stability import stable_point

def run_tool(intent, context=None):

    action = intent.get("action")

    if action == "plugin":
        return "Plugins: " + ", ".join(list_plugins())

    if action == "memory":
        return load()[-20:]

    if action == "notify":
        notify("ΝΟΥΣ AI", "Ο ΝΟΥΣ είναι ενεργός")
        return "notification_sent"

    if action == "internet":
        return "Internet gateway module installed"

    
    if action == "web":
        return web_command(context.get("command", "") if isinstance(context, dict) else "")

    
    if action == "cmd":
        c = context.get("command", "").replace("cmd ", "", 1)
        return run_command(c)

    
    if action == "sysinfo":
        return system_info()

    
    if action == "snapshot":
        return project_snapshot()

    
    if action == "compile":
        return compile_check()

    
    if action == "memory_summary":
        return memory_summary()

    
    if action == "plan":
        return make_plan(context.get("command", ""))

    
    if action == "task":
        return add_task(context.get("command", ""))

    if action == "tasks":
        return list_tasks()

    
    if action == "read_source":
        cmd = context.get("command", "")
        path = cmd.replace("read source ", "").replace("/read-source ", "").strip()
        return read_source(path)

    
    if action == "stable":
        return stable_point()

    
    if action == "make_plugin":
        goal = context.get("command", "").replace("make plugin ", "").replace("φτιάξε plugin ", "").strip()
        return generate_plugin(goal)

    if action == "run_plugin":
        name = context.get("command", "").replace("run plugin ", "").replace("/plugin ", "").strip()
        return run_plugin(name)

    if action == "test_plugin":
        name = context.get("command", "").replace("test plugin ", "").strip()
        return test_plugin(name)

    if action == "quarantine_plugin":
        name = context.get("command", "").replace("quarantine plugin ", "").strip()
        return quarantine(name)

    
    if action == "think_deep":
        return think_deep(context.get("command", ""))

    if action == "solve_problem":
        return solve_problem(context.get("command", ""))

    if action == "decide":
        return decide(context.get("command", ""))

    
    if action == "remember_fact":
        text = context.get("command", "").replace("θυμήσου ", "").replace("remember ", "").strip()
        return remember_fact(text)

    if action == "add_goal":
        text = context.get("command", "").replace("στόχος ", "").replace("goal ", "").strip()
        return add_goal(text)

    if action == "add_project":
        text = context.get("command", "").replace("project ", "").replace("έργο ", "").strip()
        return add_project(text)

    if action == "personal_state":
        return list_state()

    if action == "plan_goal":
        text = context.get("command", "").replace("σχέδιο στόχου ", "").replace("plan goal ", "").strip()
        return plan_goal(text)

    return "UNKNOWN TOOL"










