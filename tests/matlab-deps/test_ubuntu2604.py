"""Test class for matlab-deps:ubuntu26.04 Docker images."""

# Copyright 2026 The MathWorks, Inc.

import unittest
import importlib

test_apt = importlib.import_module("matlab-deps.utils.test_apt")

OS_TAG = "ubuntu26.04"

class TestUbuntu2604(test_apt.TestApt):
    def setUp(self):
        """Skip this test class unless the os tag contains 'ubuntu26.04'"""
        if not OS_TAG in self.os_tag:
            self.skipTest(
                f"skipping matlab-deps:{OS_TAG} test suite for {self.container.image.tags}"
            )

######################################################################

if __name__ == "__main__":
    unittest.main()
