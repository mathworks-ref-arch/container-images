# Copyright 2023 The MathWorks, Inc.

"""
Module for testing the "xterm" image 
"""

from utils import basetest
import unittest


class XtermVncTest(basetest.TestCase):
    """
    Test class to build a Docker image from the "xterm" one and test the resulting image
    """

    def test_packages_present(self):
        """Test that the xterm-* packages are installed"""
        packages = [
            "xterm",
            "xterm-resize",
        ]
        for name in packages:
            with self.subTest(packagename=name):
                self.assertTrue(self.host.package(name).is_installed)


##################################################################################

if __name__ == "__main__":
    unittest.main()
