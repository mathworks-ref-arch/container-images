# Copyright 2023 The MathWorks, Inc.

"""
Module for testing the "icewm" image 
"""

from utils import basetest
import unittest


class IcewmTest(basetest.TestCase):
    """
    Test class to build a Docker image from the "icewm" one and test the resulting image
    """

    def test_packages_present(self):
        """Test that the icewm-* packages are installed"""
        packages = ["icewm", "icewm-data", "icewm-themes"]
        for name in packages:
            with self.subTest(packagename=name):
                self.assertTrue(self.host.package(name).is_installed)


##################################################################################

if __name__ == "__main__":
    unittest.main()
