import time

from executor import autonomy
from executor.autonomy_v3 import autonomy_cycle


def run_once():
    result = autonomy_cycle()
    return autonomy.mark_run(result)


def run(goal="keep alive", interval=300, max_cycles=None):
    """
    Safe autonomy loop.

    interval:
        seconds between cycles. Default 300 = 5 minutes.

    max_cycles:
        None = run until stopped
        number = stop after that many cycles, useful for tests
    """
    autonomy.start()

    cycles = 0

    while autonomy.status().get("running"):
        result = run_once()
        print("[AUTONOMY LOOP]", result)

        cycles += 1
        if max_cycles is not None and cycles >= int(max_cycles):
            autonomy.stop()
            break

        time.sleep(interval)

    return {
        "stopped": True,
        "cycles": cycles,
        "status": autonomy.status(),
    }
