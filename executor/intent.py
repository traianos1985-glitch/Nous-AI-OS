def detect_intent(text):

    t = str(text).lower().strip()

    if t in ["/status", "status", "κατάσταση"]:
        return {"type": "system", "action": "status"}

    if t in ["/evolve", "evolve", "εξέλιξη"]:
        return {"type": "system", "action": "evolve"}

    if t in ["/plugins", "plugins", "plugin"] or "plugins" in t:
        return {"type": "tool", "action": "plugin"}

    if t in ["/memory", "memory", "μνήμη"] or "μνήμη" in t:
        return {"type": "tool", "action": "memory"}

    if "ειδοποίηση" in t or "notification" in t:
        return {"type": "tool", "action": "notify"}

    if "internet" in t or "ίντερνετ" in t or "διαδίκτυο" in t:
        return {"type": "tool", "action": "internet"}

    
    if t.startswith("web ") or t.startswith("/web "):
        return {"type": "tool", "action": "web"}

    
    if t.startswith("cmd "):
        return {"type": "tool", "action": "cmd"}

    
    if t in ["sysinfo", "/sysinfo", "system info"]:
        return {"type": "tool", "action": "sysinfo"}

    
    if t in ["snapshot", "/snapshot", "project snapshot"]:
        return {"type": "tool", "action": "snapshot"}

    
    if t in ["compile", "/compile", "check code"]:
        return {"type": "tool", "action": "compile"}

    
    if t in ["memory summary", "σύνοψη μνήμης"]:
        return {"type": "tool", "action": "memory_summary"}

    
    if t.startswith("σχέδιο στόχου ") or t.startswith("plan goal "):
        return {"type": "tool", "action": "plan_goal"}

    if t.startswith("plan ") or t.startswith("σχέδιο "):
        return {"type": "tool", "action": "plan"}

    
    if t.startswith("task ") or t.startswith("εργασία "):
        return {"type": "tool", "action": "task"}

    if t in ["tasks", "εργασίες"]:
        return {"type": "tool", "action": "tasks"}

    
    if t.startswith("read source ") or t.startswith("/read-source "):
        return {"type": "tool", "action": "read_source"}

    
    if t in ["stable", "backup stable", "σταθερο"]:
        return {"type": "tool", "action": "stable"}

    
    if t.startswith("make plugin ") or t.startswith("φτιάξε plugin "):
        return {"type": "tool", "action": "make_plugin"}

    if t.startswith("run plugin ") or t.startswith("/plugin "):
        return {"type": "tool", "action": "run_plugin"}

    if t.startswith("test plugin "):
        return {"type": "tool", "action": "test_plugin"}

    if t.startswith("quarantine plugin "):
        return {"type": "tool", "action": "quarantine_plugin"}

    
    if t.startswith("σκέψου ") or t.startswith("think "):
        return {"type": "tool", "action": "think_deep"}

    if t.startswith("λύσε ") or t.startswith("solve "):
        return {"type": "tool", "action": "solve_problem"}

    if t.startswith("απόφαση ") or t.startswith("decide "):
        return {"type": "tool", "action": "decide"}

    
    if t.startswith("θυμήσου ") or t.startswith("remember "):
        return {"type": "tool", "action": "remember_fact"}

    if t.startswith("στόχος ") or t.startswith("goal "):
        return {"type": "tool", "action": "add_goal"}

    if t.startswith("project ") or t.startswith("έργο "):
        return {"type": "tool", "action": "add_project"}

    if t in ["profile", "state", "personal state", "κατάσταση νου"]:
        return {"type": "tool", "action": "personal_state"}

    if t.startswith("σχέδιο στόχου ") or t.startswith("plan goal "):
        return {"type": "tool", "action": "plan_goal"}

    
    if t in ["sense", "/sense", "αισθήσεις", "android sense"]:
        return {"type": "tool", "action": "sense"}

    
    if t in ["sense think", "σκέψου αισθήσεις", "ανάλυσε κινητό"]:
        return {"type": "tool", "action": "sense_think"}

    return {"type": "chat", "action": "chat"}










