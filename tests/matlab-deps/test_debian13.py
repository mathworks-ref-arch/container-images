"""Test class for matlab-deps:debian13 Docker images."""

# Copyright 2026 The MathWorks, Inc.

import unittest
import importlib

test_apt = importlib.import_module("matlab-deps.utils.test_apt")


PLATFORM = "debian13"


class TestDebian13(test_apt.TestApt):
    def setUp(self):
        """Skip this test class unless the platform is 'debian13'"""
        if not PLATFORM in self.platform:
            self.skipTest(
                f"skipping matlab-deps:{PLATFORM} test suite for {self.container.image.tags}"
            )


######################################################################

if __name__ == "__main__":
    unittest.main()
