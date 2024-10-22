"""Base test class for matlab-deps Docker images."""

# Copyright 2021-2024 The MathWorks, Inc.

import unittest
import docker
import testinfra
from . import release_platform
from pytools import helper


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        image_name = helper.get_image_name()
        getter = release_platform.Getter(image_name)

        cls.dependencies_list = helper.parse_file_to_list(getter.deps_list_filepath)
        cls.release = getter.release
        cls.platform = getter.platform
        cls.client = docker.from_env()
        cls.container = cls.client.containers.run(
            image=image_name,
            detach=True,
            stdin_open=True,
            entrypoint="/bin/bash",
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)

    @classmethod
    def tearDownClass(cls):
        cls.container.stop(timeout=0)
        cls.container.remove()
        cls.client.close()

    ######################################################################

    def test_packages_present(self):
        """Test that the software packages listed below are installed in the container"""
        for name in self.dependencies_list:
            with self.subTest(package_name=name):
                self.assertTrue(self.host.package(name).is_installed)

    def test_absent_matlab_dir(self):
        """Test that matlab is not install in container"""
        dirlist = ["/usr/local/bin", "/usr/bin", "/opt"]
        for dir in dirlist:
            with self.subTest(dir=dir):
                self.assertNotIn("matlab", self.host.file(dir).listdir())

    def test_matlab_absent(self):
        """Test that the command 'matlab' does not work"""
        self.assertNotEqual(self.host.run("matlab").rc, 0)

    def test_unset_envs(self):
        """Test that some environment variables are not persisted in the images."""
        envs = ["DEBIAN_FRONTEND", "TZ"]
        for env in envs:
            with self.subTest(env=env):
                val = self.host.environment().get(env)
                self.assertIsNone(val, f"{env} was expected to be unset but got {val}")


######################################################################

if __name__ == "__main__":
    unittest.main()
