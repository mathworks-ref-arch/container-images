# Copyright 2022-2024 The MathWorks, Inc.

"""Test suite manager for Python unittest in BaT"""

import unittest


class TestSuite:
    """Extends the unittest.TestSuite"""

    def __init__(self, *args) -> None:
        self.runner = unittest.TextTestRunner()
        self.loader = unittest.TestLoader()
        self.suite = self.create_test_suite(*args)

    def create_test_suite(self, *args):
        """Create test suite and add tests to suite"""
        suite = unittest.TestSuite()
        for arg in args:
            suite.addTest(self.loader.loadTestsFromTestCase(arg))
        return suite

    def run(self):
        """Run tests and exit"""
        return self.runner.run(self.suite)
