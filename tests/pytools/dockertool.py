# Copyright 2023-2024 The MathWorks, Inc.

"""Helper class to run matlab tests in a Docker container"""

import logging
import os

import docker
import requests
from pytools import helper

# package-level logging configuration
logging.basicConfig(
    level=logging.INFO, format="\n%(asctime)s - %(levelname)s: %(message)s"
)

# Number of seconds to wait for a return status from the Docker containers
DOCKER_RUN_TIMEOUT = 300


class MATLABTestRunner:
    """
    Class to run MATLAB tests in a Docker container
    """

    def __init__(self, client, m_test_filepath, image_name=""):
        if not os.path.isfile(m_test_filepath):
            raise ValueError(f"The path {m_test_filepath} does not exist")
        if image_name == "":
            image_name = helper.get_image_name()
        self.client = client
        self.image_name = image_name
        self.environment = {}
        self.mounts = []
        self.device_requests = None
        self._set_license()
        self._set_target_cmd(m_test_filepath)

    def _set_target_cmd(self, m_test_srcpath):
        """mount the test file and set the command to run"""
        m_test_dstpath = "/tmp/" + os.path.basename(m_test_srcpath)

        self.mounts.append(
            docker.types.Mount(
                target=m_test_dstpath,
                source=m_test_srcpath,
                read_only=True,
                type="bind",
            )
        )
        self.command = f"-batch \"assertSuccess(runtests('{m_test_dstpath}'))\""

    def _set_license(self):
        """mount the license file and set the MLM_LICENSE_FILE env"""
        src_lic_filepath = helper.get_license_filepath()
        dst_lic_filepath = "/licenses/license.dat"

        self.environment.update({"MLM_LICENSE_FILE": dst_lic_filepath})
        self.mounts.append(
            docker.types.Mount(
                target=dst_lic_filepath,
                source=src_lic_filepath,
                read_only=True,
                type="bind",
            ),
        )

    def mount(self, src_list, dst_list):
        """list of additional directories/files to mount in the container"""
        for src, dst in zip(src_list, dst_list):
            self.mounts.append(
                docker.types.Mount(
                    target=dst,
                    source=src,
                    read_only=True,
                    type="bind",
                )
            )

    def set_env(self, additional_env):
        """list of additional environment variables to be set in the container"""
        self.environment.update(additional_env)

    def set_command(self, command):
        """set a custom command to run in docker, instead of the default one"""
        self.command = command

    def run(self, timeout=DOCKER_RUN_TIMEOUT):
        """run the tests in the Docker container and report the logs"""
        container = self.client.containers.run(
            image=self.image_name,
            detach=True,
            environment=self.environment,
            mounts=self.mounts,
            device_requests=self.device_requests,
            command=self.command,
        )
        try:
            result = container.wait(timeout=timeout)
            status_code = result.get("StatusCode")
            logs = container.logs().strip().decode("utf-8")
            return status_code, logs
        except requests.exceptions.ReadTimeout as exc:
            raise TimeoutError(
                f"MATLAB tests took longer than {timeout} s to complete"
            ) from exc
        finally:
            container.stop()
            container.remove()
            self.client.close()
