"""Test class for matlab-deps:almalinux8 Docker images."""

# Copyright 2026 The MathWorks, Inc.

import unittest
import importlib

test_yum = importlib.import_module("matlab-deps.utils.test_yum")

OS_TAG = "almalinux8"

class TestAlmaLinux8(test_yum.TestYum):
    def setUp(self):
        """Skip this test class unless the os tag contains 'almalinux8'"""
        if not OS_TAG in self.os_tag:
            self.skipTest(
                f"skipping matlab-deps:{OS_TAG} test suite for {self.container.image.tags}"
            )

######################################################################

if __name__ == "__main__":
    unittest.main()
