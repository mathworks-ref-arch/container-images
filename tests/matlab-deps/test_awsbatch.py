"""Test class for matlab-deps:aws-batch Docker images."""

# Copyright 2024-2025 The MathWorks, Inc.

from pytools import helper
import unittest
import importlib

release_platform = importlib.import_module("matlab-deps.utils.release_platform")
test_ubuntu = importlib.import_module("matlab-deps.utils.test_ubuntu")

PLATFORM = "aws-batch"

BASE_PLATFORM_DICT = {
    "r2019b": "ubuntu18.04",
    "r2020a": "ubuntu18.04",
    "r2020b": "ubuntu20.04",
    "r2021a": "ubuntu20.04",
    "r2021b": "ubuntu20.04",
    "r2022a": "ubuntu20.04",
    "r2022b": "ubuntu20.04",
    "r2023a": "ubuntu20.04",
    "r2023b": "ubuntu22.04",
    "r2024a": "ubuntu22.04",
    "r2024b": "ubuntu22.04",
    "r2025a": "ubuntu24.04",
}


class TestAWSBatch(test_ubuntu.TestUbuntu):

    def setUp(self):
        """Skip this test class unless the platform contains 'aws-batch'"""
        if not PLATFORM in self.platform:
            self.skipTest(
                f"skipping matlab-deps:{PLATFORM} test suite for {self.container.image.tags}"
            )

    def test_additional_packages_installed(self):
        """Test that the software packages listed below are installed in the container"""
        extra_pkgs = [
            "csh",
            "g++",
            "gcc",
            "gfortran",
            "python3",
            "python3-pip",
            "sudo",
            "unzip",
            "zip",
        ]
        for name in extra_pkgs:
            with self.subTest(package_name=name):
                self.assertTrue(self.host.package(name).is_installed)

    def test_packages_are_upgraded(self):
        """Skip parent's method for some releases."""
        releases_to_skip = ["r2022b", "r2023a"]
        if self.release.lower() in releases_to_skip:
            self.skipTest("Some packages are allowed to install downgraded versions")

        super().test_packages_are_upgraded()

    def test_awscli_is_installed(self):
        """Test that the AWS CLI tool is installed"""
        cmd = self.host.run("aws --version")
        self.assertEqual(cmd.rc, 0)

    def test_same_packages_as_base_image(self):
        """Test that each package installed in matlab-deps is also present in aws-batch"""
        base_platform_deps_list = helper.parse_file_to_list(
            release_platform.get_deps_list_filepath(
                self.release, BASE_PLATFORM_DICT[self.release]
            )
        )
        for name in base_platform_deps_list:
            with self.subTest(package_name=name):
                self.assertTrue(self.host.package(name).is_installed)

    def test_entrypoint_script_present(self):
        entry_script_path = "/usr/local/stageDataAndRunJob.sh"
        self.assertTrue(self.host.file(entry_script_path).exists)
        self.assertTrue(self.host.file(entry_script_path).is_executable)


######################################################################

if __name__ == "__main__":
    unittest.main()
