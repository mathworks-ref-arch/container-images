# Copyright 2024 The MathWorks, Inc.

import os
import docker
import testinfra
import unittest
import utils


IMAGE_NAME = os.getenv('IMAGE_NAME')


class TestNLMImage(unittest.TestCase):
    """Test the network license manager image without starting the lmgrd process"""

    @classmethod
    def setUpClass(cls):
        client = docker.from_env()
        cls.addClassCleanup(lambda: client.close())

        container = client.containers.run(
            image=IMAGE_NAME,
            entrypoint="/bin/bash",
            stdin_open=True,
            detach=True,
        )
        cls.addClassCleanup(lambda: container.remove(force=True))

        utils.wait_for_container_status(client, container.id, "running")
        cls.host = testinfra.get_host("docker://" + container.id)

    def test_tmp_dir_exists(self):
        "Test that the /usr/tmp directory exists. It is required by the network license manager"
        self.assertTrue(self.host.file("/usr/tmp").exists)

    def test_binaries_are_installed(self):
        """Test that the executables called in the entrypoint are actually installed"""
        expected_binpaths = ["/nlm/etc/glnxa64/lmgrd", "/nlm/etc/glnxa64/lmutil"]
        for binpath in expected_binpaths:
            with self.subTest(binary=binpath):
                self.assertTrue(self.host.file(binpath).is_executable)

    def test_user(self):
        """Test that the expected username exists and it belongs to the expected group"""
        expected_user = "lmgr"
        expected_group = "lmadmin"
        self.assertTrue(self.host.user(expected_user).exists)
        self.assertIn(expected_group, self.host.user(expected_user).groups)

    def test_archives_are_deleted(self):
        """Test that the archive files downloaded while building the image are removed"""
        find = self.host.run("find -name *.zip")
        self.assertEqual(0, find.exit_status, find.stderr)
        self.assertEqual("", find.stdout)


if __name__ == "__main__":
    unittest.main()
