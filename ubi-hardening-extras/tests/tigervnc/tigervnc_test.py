# Copyright 2023 The MathWorks, Inc.

"""
Module for testing the "tigervnc" image 
"""

from utils import basetest
import unittest


class TigerVncTest(basetest.TestCase):
    """
    Test class to build a Docker image from the "tigervnc" one and test the resulting image
    """
    
    def test_packages_present(self):
        """Test that the tigervnc_* packages are installed"""
        packages = [
            "tigervnc-server-minimal",
            "tigervnc-license",
        ]
        for name in packages:
            with self.subTest(packagename=name):
                self.assertTrue(self.host.package(name).is_installed)


##################################################################################

if __name__ == "__main__":
    unittest.main()
