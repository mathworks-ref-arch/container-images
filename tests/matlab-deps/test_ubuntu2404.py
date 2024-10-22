"""Test class for matlab-deps:ubuntu24.04 Docker images."""

# Copyright 2024 The MathWorks, Inc.

import unittest
import importlib

test_ubuntu = importlib.import_module("matlab-deps.utils.test_ubuntu")


PLATFORM = "ubuntu24.04"


class TestUbuntu2404(test_ubuntu.TestUbuntu):
    def setUp(self):
        """Skip this test class unless the platform is 'ubuntu24.04'"""
        if not PLATFORM in self.platform:
            self.skipTest(
                f"skipping matlab-deps:{PLATFORM} test suite for {self.container.image.tags}"
            )


######################################################################

if __name__ == "__main__":
    unittest.main()
