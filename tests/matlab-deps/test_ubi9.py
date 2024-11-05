"""Test class for matlab-deps:ubi9 Docker images."""

# Copyright 2024 The MathWorks, Inc.

import unittest
import importlib

test_ubi = importlib.import_module("matlab-deps.utils.test_ubi")
PLATFORM = "ubi9"


class TestUbi9(test_ubi.TestUbi):
    def setUp(self):
        """Skip this test class unless the platform is 'ubi9'"""
        if not PLATFORM in self.platform:
            self.skipTest(
                f"skipping matlab-deps:{PLATFORM} test suite for {self.container.image.tags}"
            )


######################################################################

if __name__ == "__main__":
    unittest.main()