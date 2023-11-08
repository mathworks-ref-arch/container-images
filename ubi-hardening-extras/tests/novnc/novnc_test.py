# Copyright 2023 The MathWorks, Inc.

"""
Module for testing the "novnc" image 
"""

from utils import basetest
import unittest


class NoVncTest(basetest.TestCase):
    """
    Test class to build a Docker image from the "novnc" one and test the resulting image
    """
    dockerfile = "Dockerfile.novnc"

    def test_can_launch(self):
        """Test that the launch.sh executable exists"""
        self.assertTrue(self.host.file("/tmp/novnc/utils/launch.sh").exists)


##################################################################################

if __name__ == "__main__":
    unittest.main()
