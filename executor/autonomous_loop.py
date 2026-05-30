import time
from executor.agent_core import act

def run(goal="keep alive", interval=15):

    while True:
        result = act(goal)
        print("[AGENT LOOP]", result)
        time.sleep(interval)
