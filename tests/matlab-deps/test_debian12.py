"""Test class for matlab-deps:debian12 Docker images."""

# Copyright 2026 The MathWorks, Inc.

import unittest
import importlib

test_apt = importlib.import_module("matlab-deps.utils.test_apt")


OS_TAG = "debian12"

class TestDebian12(test_apt.TestApt):
    def setUp(self):
        """Skip this test class unless the os tag is 'debian12'"""
        if not OS_TAG in self.os_tag:
            self.skipTest(
                f"skipping matlab-deps:{OS_TAG} test suite for {self.container.image.tags}"
            )

######################################################################

if __name__ == "__main__":
    unittest.main()
