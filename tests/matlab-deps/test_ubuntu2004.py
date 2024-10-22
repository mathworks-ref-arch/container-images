"""Test class for matlab-deps:ubuntu20.04 Docker images."""

# Copyright 2024 The MathWorks, Inc.

import unittest
import importlib

test_ubuntu = importlib.import_module("matlab-deps.utils.test_ubuntu")
PLATFORM = "ubuntu20.04"


class TestUbuntu2004(test_ubuntu.TestUbuntu):
    def setUp(self):
        """Skip this test class unless the platform is 'ubuntu20.04'"""
        if not PLATFORM in self.platform:
            self.skipTest(
                f"skipping matlab-deps:{PLATFORM} test suite for {self.container.image.tags}"
            )

    def test_glibc_fix_packages_are_installed(self):
        """test that the packages required for the glibc fix are installed"""
        releases_to_skip = ["r2020b", "r2021a"]
        if self.release.lower() in releases_to_skip:
            self.skipTest(
                f"The glibc fix is not required for these MATLAB releases {self.release}"
            )

        packages = ["libcrypt-dev", "linux-libc-dev"]
        for pkg in packages:
            with self.subTest(package_name=pkg):
                self.assertTrue(self.host.package(pkg).is_installed)


######################################################################

if __name__ == "__main__":
    unittest.main()
