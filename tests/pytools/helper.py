"""Helper functions for testing cloud platforms"""

# Copyright 2021-2024 The MathWorks, Inc.

import os
import re
import time

#########################################################
# Helper functions to interpret the current environment #
#########################################################


def get_image_name():
    """Get the name of the Docker image from the environment"""
    return _get_env("IMAGE_NAME")


def get_license_filepath():
    """Get the path of the license file from the environment"""
    filepath = _get_env("LICENSE_FILE_PATH")
    if filepath == "":
        raise ValueError("Environment variable 'LICENSE_FILE_PATH' is empty")
    if not os.path.exists(filepath):
        raise ValueError(f"License file {filepath} does not exist")
    if os.stat(filepath).st_size <= 1:
        raise ValueError(f"License file {filepath} is empty")
    return filepath


def _get_env(env):
    """Internal function for getting environment variable"""
    if env in os.environ:
        return os.environ[env]
    else:
        raise ValueError(f"Environment variable {env} expected.")


#####################################
# Helper functions for Docker tests #
#####################################

## Get functions ##


def get_release_from_dir(host, base_dir="/opt/matlab"):
    """MATLAB in the Docker container images is installed under /opt/matlab/r20xyz.
    Thus, it is possible to get the MATLAB release simply just by reading the
    name of the subdirectories of /opt/matlab.

    HOST is a testinfra.Host object
    BASE_DIR is the directory where matlab in installed.

    If BASE_DIR has more than one subdirectory, an error is raised.
    """
    subdirs = host.file(base_dir).listdir()
    if len(subdirs) == 1:
        return subdirs[0]
    else:
        raise ValueError(
            "Too many subdirs of {base_dir}. Correct release cannot be determined"
        )


def get_bound_port(client, container_id, port):
    """Get the port on the localhost that is bound to the PORT of the container
    with id CONTAINER_ID"""
    host_port = client.api.port(container_id, port)
    return host_port[0]["HostPort"]


def get_process_env_variables(host, pid):
    """Read the file `/proc/PID/environ` and get the environment variables for
    the process with pid PID
    """

    # cat /proc/PID/environ
    envs_list = host.file(f"/proc/{pid}/environ").content_string.split("\x00")

    # parse the content of /proc/PID/environ
    envs = {}
    for env_var in envs_list:
        if env_var:
            if "=" in env_var:
                var_name, var_val = env_var.split("=", 1)
                envs[var_name] = var_val
    return envs


def parse_file_to_list(filepath):
    list = []
    with open(filepath) as file:
        for line in file:
            list.extend(line.split())
    return list


release_re = re.compile("R20[0-9]{2}[ab]", re.IGNORECASE)


def is_valid_release(str):
    match = release_re.fullmatch(str)
    if match:
        return True
    else:
        return False


## Wait functions ##


def wait_for_file(host, filepath, timeout=30):
    """Wait for a file to be created in a 'testinfra.Host' object.

    HOST is a testinfra.Host object
    FILEPATH is the full path of the file to be waited for

    If the file is not found after TIMEOUT seconds, an error is raised.
    """

    def file_exists():
        return host.file(filepath).exists

    try:
        _wait_for(file_exists, timeout)
    except TimeoutError as e:
        raise ValueError(f"The file {filepath} does not exists.") from e


def wait_for_container_status(client, container_id, status, timeout=30):
    """Wait until the container is in a desired state"""

    def container_in_desired_state():
        return client.containers.get(container_id).status == status

    try:
        _wait_for(container_in_desired_state, timeout)
    except TimeoutError as e:
        raise RuntimeError(
            f"The container {container_id} is {client.containers.get(container_id).status}."
        ) from e


def wait_for_cmd_cont(container, cmd, timeout=30):
    """
    Wait until a process is started in the container CONTAINER. The process that
    is waited for has a "CMD" that regex-matches the input CMD.
    CONTAINER is a Container class from the docker package.
    """

    def update_cmd_list():
        ps_res = container.top(ps_args="-o pid,cmd")
        idx = ps_res["Titles"].index("CMD")
        return [proc[idx] for proc in ps_res["Processes"]]

    def cmd_has_started():
        return "\n".join(update_cmd_list()).count(cmd) != 0

    try:
        _wait_for(cmd_has_started, timeout)
    except TimeoutError as e:
        raise ValueError(
            f"The following process did not start running within {timeout}s:\n\n\t{cmd}"
        ) from e


def wait_for_process_num(container, comm, number, timeout=30):
    """
    Wait until the specified process is running with the specified number of
    instances in the CONTAINER.
    CONTAINER is a Container class from the docker package.
    """

    def has_process_num():
        return len(container.process.filter(comm=comm)) == number

    try:
        _wait_for(has_process_num, timeout)
    except TimeoutError as e:
        raise ValueError(
            f"The following process did not have {number} instance(s) running within {timeout}s:\n\n\t{comm}"
        ) from e


def _wait_for(bool_fnc, timeout=60, interval=0.3):
    start = time.time()
    while time.time() - start <= timeout and not bool_fnc():
        time.sleep(interval)
    if time.time() - start > timeout:
        raise TimeoutError(
            f"The condition {bool_fnc.__name__} is still false after {timeout} seconds"
        )
