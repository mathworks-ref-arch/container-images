"""Test class for matlab-deps:ubi8 Docker images."""

# Copyright 2024-2026 The MathWorks, Inc.

import unittest
import importlib

test_yum = importlib.import_module("matlab-deps.utils.test_yum")
PLATFORM = "ubi8"


class TestUbi8(test_yum.TestYum):
    def setUp(self):
        """Skip this test class unless the platform is 'ubi8'"""
        if not PLATFORM in self.platform:
            self.skipTest(
                f"skipping matlab-deps:{PLATFORM} test suite for {self.container.image.tags}"
            )


######################################################################

if __name__ == "__main__":
    unittest.main()
