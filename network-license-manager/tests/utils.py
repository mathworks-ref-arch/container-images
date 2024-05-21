# Copyright 2024 The MathWorks, Inc.

import re
import time


def wait_for_logs(container, msg, timeout=60):
    logs = container.logs(stream=True)
    start = time.time()
    while time.time() - start < timeout:
        if re.search(msg, next(logs).decode()):
            logs.close()
            return
    else:
        logs.close()
        raise TimeoutError(f"Timeout reached while waiting for message '{msg}'")


def wait_for(bool_fnc, timeout=60, interval=0.3):
    start = time.time()
    while time.time() - start <= timeout and not bool_fnc():
        time.sleep(interval)
    if time.time() - start > timeout:
        raise TimeoutError(
            f"The condition {bool_fnc.__name__} is still false after {timeout} seconds"
        )


def wait_for_container_status(client, id, status, timeout=30):
    """Wait until the container is in a desired state"""

    def container_in_desired_state():
        return client.containers.get(id).status == status

    try:
        wait_for(container_in_desired_state, timeout)
    except TimeoutError:
        raise RuntimeError(f"The container {id} is {client.containers.get(id).status}.")
