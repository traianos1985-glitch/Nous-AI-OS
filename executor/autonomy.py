import time
from executor.memory import save

RUNNING=False

def start():

    global RUNNING
    RUNNING=True

    save({
        "event":"autonomy_started"
    })

    return "AUTONOMY_STARTED"

def stop():

    global RUNNING
    RUNNING=False

    save({
        "event":"autonomy_stopped"
    })

    return "AUTONOMY_STOPPED"

def status():

    return RUNNING
