"""Test class for matlab-deps:aws-batch Docker images."""

# Copyright 2024-2026 The MathWorks, Inc.

from pytools import helper
import unittest
import importlib

release_os = importlib.import_module("matlab-deps.utils.release_os")
test_apt = importlib.import_module("matlab-deps.utils.test_apt")

OS_TAG = "aws-batch"

BASE_OS_DICT = {
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
    "r2025a": "ubuntu22.04",
    "r2025b": "ubuntu22.04",
    "r2026a": "ubuntu24.04",
}

class TestAWSBatch(test_apt.TestApt):
    
    def setUp(self):
        """Skip this test class unless the os tag contains 'aws-batch'"""
        if not OS_TAG in self.os_tag:
            self.skipTest(
                f"skipping matlab-deps:{OS_TAG} test suite for {self.container.image.tags}"
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
        """Test that each package installed in matlab-deps for ubuntuXX.04 is also present in aws-batch"""
        base_platform_deps_list = helper.parse_file_to_list(
            release_os.build_deps_list_filepath(
                release=self.release.lower(), 
                os=BASE_OS_DICT.get(self.release.lower()),
                arch=self.arch
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
