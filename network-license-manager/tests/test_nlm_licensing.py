# Copyright 2024 The MathWorks, Inc.

import os
import pathlib
import stat
import tempfile
import unittest

import docker
import requests
import utils

HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")
MATLAB_RELEASE = os.getenv("MATLAB_RELEASE")
IMAGE_NAME = os.getenv("IMAGE_NAME")
LICENSE_FILE_DIR = str(pathlib.Path(os.getenv("LICENSE_FILE_PATH")).parent)


MATLAB_IMAGE = "mathworks/matlab"


class TestNLMLicensing(unittest.TestCase):
    """
    Test class to test the expected user workflow:
    run the network license manager docker image and use it to license matlab
    """

    @classmethod
    def setUpClass(cls):
        cls.client = docker.from_env()
        cls.addClassCleanup(lambda: cls.client.close())

        cls.license_mount = docker.types.Mount(
            target=f"/usr/local/MATLAB/licenses",
            source=LICENSE_FILE_DIR,
            read_only=True,
            type="bind",
        )

    def setUp(self):
        logdir = tempfile.mkdtemp()
        self.logs_mount = docker.types.Mount(
            target="/tmp/log/mathworks",
            source=logdir,
            type="bind",
        )
        logfilename = "logs.txt"
        self.logfilepath = pathlib.Path(self.logs_mount["Source"]) / logfilename
        self.addCleanup(lambda: self.logfilepath.unlink(missing_ok=True))

    def test_license_manager_is_running(self):
        """
        Test that FlexNet Licensing is started when the container is run
        and that the docker log is copied to the log file
        """
        nlm = self.client.containers.run(
            image=IMAGE_NAME,
            init=True,
            mounts=[self.license_mount, self.logs_mount],
            hostname=HOSTNAME,
            detach=True,
        )
        self.addCleanup(lambda: nlm.remove(force=True))
        utils.wait_for_logs(nlm, r"\(MLM\) Listener Thread: running")

        # refresh the status of the nlm container (nlm.status does not work)
        status = self.client.containers.get(nlm.id).status
        self.assertEqual(status, "running")

        nlm_logs = nlm.logs().decode()
        self.assertRegex(
            nlm_logs, r"\(lmgrd\) FlexNet Licensing \(.*\) started on " + HOSTNAME
        )

        self.assertTrue(self.logfilepath.is_file)
        with open(str(self.logfilepath), "r") as logfile:
            self.assertEqual(
                nlm_logs,
                logfile.read(),
                "The docker logs and the log file are not the same",
            )
        self.assertEqual(stat.filemode(self.logfilepath.stat().st_mode), "-rw-rw-rw-")

    def test_license_manager_shutdown(self):
        """
        Test that FlexLM is shutdown when the container is stopped
        """
        nlm = self.client.containers.run(
            image=IMAGE_NAME,
            init=True,
            mounts=[self.license_mount, self.logs_mount],
            hostname=HOSTNAME,
            detach=True,
        )
        self.addCleanup(lambda: nlm.remove())
        utils.wait_for_logs(nlm, r"\(MLM\) Listener Thread: running")

        # Stop the container now NLM is running
        nlm.stop()

        # Check FlexLM started and stopped
        nlm_logs = nlm.logs().decode()

        self.assertRegex(
            nlm_logs, r"\(lmgrd\) FlexNet Licensing \(.*\) started on " + HOSTNAME
        )

        # Check LMGRD shutdown and shutdown occurred only once
        self.assertEqual(nlm_logs.count("License Manager has shut down."), 1)

        self.assertTrue(self.logfilepath.is_file)
        with open(str(self.logfilepath), "r") as logfile:
            self.assertEqual(
                nlm_logs,
                logfile.read(),
                "The docker logs and the log file are not the same",
            )

    def test_nlm_can_license_matlab(self):
        """
        Test that the network license manager Docker container can be used to license
        a MATLAB docker container
        """
        pi_value = "3.1416"
        nlm = self.client.containers.run(
            image=IMAGE_NAME,
            init=True,
            mounts=[self.license_mount, self.logs_mount],
            hostname=HOSTNAME,
            detach=True,
        )
        self.addCleanup(lambda: nlm.remove(force=True))
        utils.wait_for_logs(nlm, r"\(MLM\) Listener Thread: running")

        output = self.client.containers.run(
            image=f"{MATLAB_IMAGE}:{MATLAB_RELEASE}",
            environment={"MLM_LICENSE_FILE": f"{PORT}@{HOSTNAME}"},
            network_mode=f"container:{nlm.id}",
            command="-batch pi",
            auto_remove=True,
        )

        self.assertIn(pi_value, output.decode(), output.decode())
        self.assertIn(f'(MLM) OUT: "MATLAB" matlab@{HOSTNAME}', nlm.logs().decode())
        self.assertIn(f'(MLM) IN: "MATLAB" matlab@{HOSTNAME}', nlm.logs().decode())

    def test_no_license(self):
        """
        Test that the container stops if no license is provided
        """
        timeout = 10

        nlm = self.client.containers.run(
            image=IMAGE_NAME,
            init=True,
            mounts=[self.logs_mount],
            detach=True,
        )
        self.addCleanup(lambda: nlm.remove(force=True))
        try:
            nlm_status = nlm.wait(timeout=timeout)
        except requests.exceptions.ReadTimeout:
            self.fail(
                f"The network license manager took more that ${timeout}s to exit when no license file is provided"
            )

        self.assertEqual(nlm_status["StatusCode"], 0)

        nlm_logs = nlm.logs().decode()
        self.assertIn("Cannot find license file", nlm_logs)

        self.assertTrue(self.logfilepath.is_file)
        with open(str(self.logfilepath), "r") as logfile:
            logfilecontent = logfile.read()
            self.assertEqual(
                nlm_logs,
                logfilecontent,
                "The docker logs and the log file are not the same",
            )
        self.assertEqual(stat.filemode(self.logfilepath.stat().st_mode), "-rw-rw-rw-")


if __name__ == "__main__":
    unittest.main()
