# Copyright 2022-2024 The MathWorks, Inc.

"""Shared tests to test the integration of the matlab-proxy feature into the
dl-docker and matlab-docker containers.
"""

import json
import stat
import time
import unittest

import docker
import testinfra
import urllib3
from pytools import helper

DEFAULT_MWI_APP_PORT = 8888


def _get_status_json(client, container_id, port, mwi_base_url=""):
    """Get the result of the curl request http://localhost:8888/matlab/get_status"""
    bound_port = helper.get_bound_port(client, container_id, port)
    uri = f"http://localhost:{bound_port}{mwi_base_url}/get_status"

    with urllib3.PoolManager(retries=urllib3.Retry(backoff_factor=0.1)) as http:
        res = http.request("GET", uri)
        return json.loads(res.data.decode("utf-8"))


def _setup_and_run_container(license_filepath=None, **kwargs):
    """Module method to set up and run the container with the -browser option."""

    client = docker.from_env()
    image_name = helper.get_image_name()
    client.images.get(image_name)

    mount = []
    if isinstance(license_filepath, str):
        mount = [
            docker.types.Mount(
                target=license_filepath,
                source=helper.get_license_filepath(),
                read_only=True,
                type="bind",
            )
        ]
        envs = {"MLM_LICENSE_FILE": license_filepath}
    else:
        envs = {}

    port = {f"{DEFAULT_MWI_APP_PORT}/tcp": None}
    # if kwargs is not empty
    if kwargs:
        envs.update(kwargs)
        # a random localhost port is assigned to the mwi_app_port of the Docker container
        if "MWI_APP_PORT" in kwargs:
            port = {str(kwargs["MWI_APP_PORT"]) + "/tcp": None}

    container = client.containers.run(
        image=helper.get_image_name(),
        command="-browser",
        mounts=mount,
        environment=envs,
        ports=port,
        detach=True,
    )
    return client, container


################################################################################


class TestMatlabProxyInteg(unittest.TestCase):
    """
    Test class to test the integration of matlab-proxy. Advanced environment
    variables are not provided.
    """

    license_filepath = "/licenses/license.dat"
    mwi_app_port = DEFAULT_MWI_APP_PORT

    @classmethod
    def setUpClass(cls):
        """
        Start the container with the -browser option before running any test. The
        equivalent cli command is

        docker run -d -p ${mwi_app_port} -v path/to/license.file:${license_filepath}
        -e MLM_LICENSE_FILE=${license_filepath} image_name -browser
        """

        cls.client, cls.container = _setup_and_run_container(
            license_filepath=cls.license_filepath
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)
        helper.wait_for_cmd_cont(cls.container, "matlab-proxy-app")
        helper.wait_for_cmd_cont(cls.container, "MATLAB")

    @classmethod
    def tearDownClass(cls):
        """Stop and remove container"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ############################################################

    def test_package_requirements(self):
        """Test that xvfb and python are installed"""
        packages = ["xvfb", "python3", "pipx"]
        for pkg in packages:
            with self.subTest(package=pkg):
                self.assertTrue(self.host.package(pkg).is_installed)

    def test_pipx_packages(self):
        """Test that matlab-proxy is installed"""
        packages = ["matlab-proxy"]
        for pkg in packages:
            with self.subTest(pipx_package=pkg):
                cmd = self.host.run(f"pipx list | grep {pkg}")
                self.assertTrue(cmd.succeeded)

    def test_matlab_proxy_version(self):
        """Test that the matlab-proxy module in the container has the latest version"""
        cmd = self.host.run("pipx upgrade matlab-proxy")
        self.assertIn("matlab-proxy is already at latest version", cmd.stdout)

    def test_matlab_proxy_app_installed(self):
        """Test that the executable matlab_proxy_app is located on PATH and executable"""
        cmd = self.host.run("which matlab-proxy-app")
        self.assertTrue(cmd.succeeded)
        matlabproxyapp_path = cmd.stdout.replace("\n", "")
        self.assertRegex(
            stat.filemode(stat.S_IMODE(self.host.file(matlabproxyapp_path).mode)),
            "r.xr-xr-x",
        )

    def test_running_processes(self):
        """Test that matlab-proxy-app and MATLAB are running"""
        expected_cmds = ["matlab-proxy-app", "MATLAB"]
        running_cmds = self.host.check_output("ps -x -o cmd")
        for cmd in expected_cmds:
            with self.subTest(comand=cmd):
                self.assertGreaterEqual(running_cmds.count(cmd), 1)

    def test_env_variable(self):
        """Test that the MWI_APP_PORT env variables is set"""
        if "MWI_APP_PORT" in self.host.environment():
            self.assertEqual(
                self.host.environment()["MWI_APP_PORT"], str(self.mwi_app_port)
            )
        else:
            self.fail("MWI_APP_PORT is not an environment variable")

    def test_matlabproxy_status(self):
        """Test if the MLM_LICENSE_FILE is being picked up by matlab-proxy"""
        res = _get_status_json(
            self.client,
            self.container.id,
            self.mwi_app_port,
            mwi_base_url=self.host.environment().get("MWI_BASE_URL", ""),
        )
        valid_status = ("up", "starting")
        self.assertIn(res["matlab"]["status"], valid_status)
        self.assertEqual(res["licensing"]["connectionString"], self.license_filepath)

    def test_matlab_is_up(self):
        """Test that the status switches from 'starting' to 'up' within a timeout"""
        res = _get_status_json(
            self.client,
            self.container.id,
            self.mwi_app_port,
            mwi_base_url=self.host.environment().get("MWI_BASE_URL", ""),
        )
        matlab_status = res["matlab"]["status"]
        timeout = 60
        start_time = time.time()
        while matlab_status == "starting" and (time.time() - start_time < timeout):
            time.sleep(0.5)
            res = _get_status_json(
                self.client,
                self.container.id,
                self.mwi_app_port,
                mwi_base_url=self.host.environment().get("MWI_BASE_URL", ""),
            )
            matlab_status = res["matlab"]["status"]
        self.assertEqual(matlab_status, "up", f"matlab is not up after {timeout} s")

    def test_print_message(self):
        """Test if the right message is printed"""
        mwi_base_url = self.host.environment().get("MWI_BASE_URL", "")
        printed_endpoint1 = f"http://0.0.0.0:{self.mwi_app_port}{mwi_base_url}"
        printed_endpoint2 = f"http://127.0.0.1:{self.mwi_app_port}{mwi_base_url}"
        printed_endpoint3 = f"http://localhost:{self.mwi_app_port}{mwi_base_url}"
        printed_endpoint4 = f"http://hostname:{self.mwi_app_port}{mwi_base_url}"
        container_logs = self.container.logs().decode()
        self.assertTrue(
            printed_endpoint1 in container_logs
            or printed_endpoint2 in container_logs
            or printed_endpoint3 in container_logs
            or printed_endpoint4 in container_logs,
            container_logs,
        )

    def test_env_for_ddux_is_set(self):
        """Test that the MW_CONTEXT_TAGS environment variable for DDUX is set
        correctly. The variable is not global, but it is only set for the MATLAB
        process.
        """
        expected_mw_context_tag = "MATLAB_PROXY"

        # read the PID of MATLAB
        helper.wait_for_process_num(self.host, "MATLAB", 1, timeout=60)
        matlab_proc = self.host.process.filter(comm="MATLAB")
        matlab_pid = matlab_proc[0]["pid"]

        # get the variable values for the MATLAB process
        matlab_envs = helper.get_process_env_variables(host=self.host, pid=matlab_pid)
        actual_mw_context_tags = matlab_envs.get("MW_CONTEXT_TAGS", "unset_variable")
        self.assertIn(expected_mw_context_tag, actual_mw_context_tags)


################################################################################


class TestMatlabProxyIntegAdvanced(unittest.TestCase):
    """Test class to test the integration of matlab-proxy when advanced environment
    variables are provided.
    """

    license_filepath = "/licenses/license.dat"
    mwi_app_port = 8889
    mwi_base_url = "/custom"

    @classmethod
    def setUpClass(cls):
        """
        Start the container with the -browser option before running any test. The
        equivalent cli command is

        docker run -d -p ${mwi_app_port} -v path/to/license.file:${license_filepath}
        -e MLM_LICENSE_FILE=${license_filepath} -e MWI_APP_PORT=${mwi_app_port}
        -e MWI_BASE_URL=${mwi_base_url} image_name -browser
        """

        cls.client, cls.container = _setup_and_run_container(
            license_filepath=cls.license_filepath,
            MWI_APP_PORT=str(cls.mwi_app_port),
            MWI_BASE_URL=cls.mwi_base_url,
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)
        helper.wait_for_cmd_cont(cls.container, "matlab-proxy-app")

    @classmethod
    def tearDownClass(cls):
        """Stop and remove container"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ############################################################

    def test_matlabproxy_status(self):
        """Test if the MLM_LICENSE_FILE is being picked up by matlab-proxy"""
        TestMatlabProxyInteg.test_matlabproxy_status(self)

    def test_print_message(self):
        """Test that the right message is printed"""
        TestMatlabProxyInteg.test_print_message(self)


################################################################################


class TestMatlabProxyIntegNoLic(unittest.TestCase):
    """Test class to test that we cannot use MATLAB if we do not provide any
    licensing option
    """

    mwi_app_port = DEFAULT_MWI_APP_PORT

    @classmethod
    def setUpClass(cls):
        """Start the container with the -browser option but no license file"""
        cls.client, cls.container = _setup_and_run_container()
        cls.host = testinfra.get_host("docker://" + cls.container.id)
        helper.wait_for_cmd_cont(cls.container, "matlab-proxy-app")

    @classmethod
    def tearDownClass(cls):
        """Stop and remove the container."""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    def test_matlab_down(self):
        """Test that MATLAB is down and no license is picked up"""
        res = _get_status_json(
            self.client,
            self.container.id,
            self.mwi_app_port,
            mwi_base_url=self.host.environment().get("MWI_BASE_URL", ""),
        )
        self.assertEqual(res["matlab"]["status"], "down")
        self.assertIsNone(res["licensing"])


################################################################################


if __name__ == "__main__":
    unittest.main()
