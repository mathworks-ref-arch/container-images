# Copyright 2023 The MathWorks, Inc.

import testinfra
import docker
import unittest
import pathlib
import os


class TestCase(unittest.TestCase):
    """Base test class"""

    # default parameters (can be overridden in derived test classes)
    buildargs = {"IMAGE_UNDER_TEST": os.getenv("IMAGE_NAME")}
    dockerfile = "Dockerfile"

    @classmethod
    def setUpClass(cls):
        """
        Build a Docker image from the Dockerfile contained in this directory.
        To choose which image use as a base image, set the buildargs "IMAGE_UNDER_TEST"
        """
        cls.client = docker.from_env()
        cls.image, _ = cls.client.images.build(
            path=str(pathlib.Path(__file__).parent.resolve()),
            buildargs=cls.buildargs,
            dockerfile=cls.dockerfile,
            rm=True,
        )

    def setUp(self):
        """Run the docker container. Equivalent to

        'docker run --rm -i -d DOCKER_IMAGE '
        """
        self.container = self.client.containers.run(
            image=self.image.id, detach=True, stdin_open=True
        )
        self.host = testinfra.get_host("docker://" + self.container.id)

    def tearDown(self):
        """Stop and remove the container."""
        self.container.stop()
        self.container.remove()

    @classmethod
    def tearDownClass(cls):
        """Remove the image and the client."""
        cls.client.images.remove(cls.image.id, force=True)
        cls.client.close()
