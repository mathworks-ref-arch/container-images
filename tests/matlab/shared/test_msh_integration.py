"""Shared tests to test the integration of msh in pre-build Docker containers."""

# Copyright 2023-2024 The MathWorks, Inc.

import re
import stat
import unittest

import docker
import testinfra
from pytools import helper

################################################################################


class TestMSHIntegration(unittest.TestCase):
    """
    Test class to test the integration of MathWorks Service Host.
    """

    LATEST_INSTALL_LOCATION = "/home/matlab/.MathWorks/ServiceHost/LatestInstall.info"

    @classmethod
    def setUpClass(cls):
        """Run the Docker container and launch "matlab" without
        providing file based licensing
        """
        cls.client = docker.from_env()
        image_name = helper.get_image_name()
        cls.client.images.get(image_name)

        cls.container = cls.client.containers.run(
            image=image_name,
            publish_all_ports=True,
            stdin_open=True,
            detach=True,
            command="",
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)
        helper.wait_for_cmd_cont(cls.container, "MathWorksServiceHost", timeout=15)

    @classmethod
    def tearDownClass(cls):
        """Stop and remove container"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ############################################################

    def test_msh_latest_install_info(self):
        """
        Test that the LatestInfo.info file is present in a location that does
        not include the hostname.
        """
        self.assertTrue(self.host.file(self.LATEST_INSTALL_LOCATION).exists)

    def test_msh_location(self):
        """
        Test that msh is installed in the location pointed by the
        LatestInstall.info and it is executable.
        """
        msh_root = self._get_msh_install_location()
        msh_bin = msh_root + "/bin/glnxa64/MathWorksServiceHost"
        self.assertRegex(
            stat.filemode(stat.S_IMODE(self.host.file(msh_bin).mode)),
            "r.xr-xr-x",
            "MathWorksServiceHost is not executable",
        )

    def test_msh_managed_version(self):
        """
        Test that the version of MathWorksServiceHost is the "managed" one,
        which disables the auto-update feature.
        """
        msh_root = self._get_msh_install_location()
        managed_msh_so_filepath = (
            msh_root
            + "/bin/glnxa64/mathworksservicehost/configuration/matlabconnector/managed_matlabconnector_configuration/libmwmshconfigservicehostservicemanaged.so"
        )
        self.assertTrue(self.host.file(managed_msh_so_filepath).exists)

    def test_running_msh_process(self):
        """Test that MathWorksServiceHost service is running"""
        msh_service_cmd = "MathWorksServiceHost service"
        try:
            helper.wait_for_cmd_cont(self.container, msh_service_cmd)
        except ValueError as e:
            self.fail(f"'{msh_service_cmd}' is not running. Raised exception {e}")

    def _get_msh_install_location(self):
        """Extract the MSH installation root from the LatestInstall.info"""
        match = re.search(
            r"LatestInstallRoot ([^\\n]+)",
            str(self.host.file(self.LATEST_INSTALL_LOCATION).content),
        )

        if not match:
            self.fail(
                f"unable to extract MSH installation location from {self.LATEST_INSTALL_LOCATION}"
            )

        return match.group(1)


################################################################################


if __name__ == "__main__":
    unittest.main()
