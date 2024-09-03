# Copyright 2023-2024 The MathWorks, Inc.

"""A test runner class for the AvailableProductsTest.m test file"""

import re
import unittest
from pathlib import Path

import docker
from pytools import dockertool, helper


class Run_AvailableProductsTest(unittest.TestCase):
    """A test runner class for the AvailableProductsTest.m test file"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = docker.from_env()
        cls.image_name = helper.get_image_name()
        cls.client.images.get(cls.image_name)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()

    def test_available_products(self):
        """Run the AvailableProductsTest.m MATLAB test file"""
        m_filename = "AvailableProductsTest.m"
        m_filepath = str(Path(__file__).parent.resolve() / m_filename)

        runner = dockertool.MATLABTestRunner(self.client, m_filepath)

        exit_code, logs = runner.run()
        self.assertNotRegex(
            logs, re.compile("At least one test failed", re.IGNORECASE), logs
        )
        self.assertEqual(
            exit_code, 0, "The Docker container exited with a non-zero status code"
        )


if __name__ == "__main__":
    unittest.main()
