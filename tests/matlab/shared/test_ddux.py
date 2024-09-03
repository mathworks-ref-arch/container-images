# Copyright 2021-2024 The MathWorks, Inc.

"""Run the tests to check for DDUX information set in the image"""

import unittest

import docker
import testinfra
from pytools import helper


class TestDDUX(unittest.TestCase):
    """Test the DDUX information set when running the container

    When running the container the `MW_CONTEXT_TAGS` and `MHLM_CONTEXT`
    environment variables should be set to identify the images deployed by
    MathWorks on Docker Hub.

    This test class is designed to be inherited from rather than used directly.
    """

    @classmethod
    def setUpClass(cls):
        """Run the container"""
        cls.client = docker.from_env()

        image_name = helper.get_image_name()
        cls.client.images.get(image_name)

        cls.container = cls.client.containers.run(
            image=image_name,
            detach=True,
            stdin_open=True,
            command="-shell",
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)

    @classmethod
    def tearDownClass(cls):
        """Remove the container and close client connection"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ############################################################

    def test_ddux(self):
        """Test that the MW_CONTEXT_TAGS and MHLM_CONTEXT variables for DDUX are
        correctly set"""
        for tag, value in self.get_tag_value_pairs().items():
            with self.subTest(tag=tag):
                mw_context_tags = self.host.environment().get(tag, "unset_variable")
                self.assertEqual(value, mw_context_tags)

    ############################################################

    def get_tag_value_pairs(self):
        """Override this method in subclasses to provide different tag-value pairs"""
        raise NotImplementedError
