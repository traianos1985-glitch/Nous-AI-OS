from executor.intent_v2 import detect

def tick(command):
    intent = detect(command)

    if intent == "status":
        return "OK"

    if intent == "evolve":
        return {"agent": "thinking", "next": "noop"}

    return {"agent": "idle"}
