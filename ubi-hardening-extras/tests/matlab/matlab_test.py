# Copyright 2024 The MathWorks, Inc.

"""
Module for testing the "matlab" image
"""

from utils import basetest
import unittest


class MATLABTest(basetest.TestCase):
    """
    Test class to build a Docker image from the "matlab" one and test the resulting image
    """
    dockerfile = "Dockerfile.matlab"

    def test_matlab_present(self):
        """Test that MATLAB is installed and available"""
        self.assertTrue(self.host.exists(command="matlab"))


##################################################################################

if __name__ == "__main__":
    unittest.main()
