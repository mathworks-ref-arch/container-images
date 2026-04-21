# Copyright 2025-2026 The MathWorks, Inc.

"""Run the tests for Docker images using a user specified username."""

import stat
import unittest
import time

import docker
import testinfra
from pytools import helper


class TestCustomUser(unittest.TestCase):
    """Test a Docker container running in shell mode with a non-default username.

    This suite of tests ensures that the image has been set up correctly to work with a non-default username.
    Additionally, checks are in place to verify build and test artifacts are removed from the final image.
    """

    USER_NAME = "myuser"
    USER_UID = 2000
    USER_GID = 3000

    @classmethod
    def setUpClass(cls):
        """Run the Docker container. Equivalent to

        'docker run -i -d --user root -e USER_NAME=myuser -e USER_UID=2000 -e USER_GID=3000 DOCKER_IMAGE'
        """
        cls.client = docker.from_env()
        image_name = helper.get_image_name()
        cls.client.images.get(image_name)

        cls.container = cls.client.containers.run(
            image=image_name,
            detach=True,
            stdin_open=True,
            user="root",
            environment={
                "USER_NAME": cls.USER_NAME,
                "USER_UID": str(cls.USER_UID),
                "USER_GID": str(cls.USER_GID),
            },
            command="-shell",
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id + "?cwd=/")
        # run.sh applies UID/GID first (usermod -u), then renames matlab → USER_NAME.
        # usermod -u can take many seconds on a large /home/matlab while passwd may
        # already show the new UID for name "matlab"; a short fixed sleep races that.
        deadline = time.monotonic() + 120
        while True:
            if (
                cls.host.user(cls.USER_NAME).exists
                and not cls.host.user("matlab").exists
            ):
                break
            if time.monotonic() >= deadline:
                raise RuntimeError(
                    "Timed out waiting for USER_NAME provisioning (matlab → "
                    f"{cls.USER_NAME})."
                )
            time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        """Stop and remove the container."""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ############################################################

    def test_user_exists(self):
        """Test that the expected user exists with correct UID/GID."""
        user = self.host.user(self.USER_NAME)
        self.assertTrue(user.exists)
        self.assertEqual(user.uid, self.USER_UID)
        self.assertEqual(user.gid, self.USER_GID)

    def test_home_directory_preserved(self):
        """Test that home directory stays at /home/matlab (not moved/renamed).

        usermod -l only renames the login name; it does not move the home directory.
        The /etc/passwd entry (and therefore $HOME / ~) must still point to /home/matlab.
        """
        self.assertTrue(self.host.file("/home/matlab").is_directory)
        # Verify /etc/passwd records /home/matlab as the home dir for the renamed user.
        # This is the value that $HOME and ~ expand to at runtime.
        self.assertEqual(self.host.user(self.USER_NAME).home, "/home/matlab")

    def test_matlab_username_removed(self):
        """Test that the initial username (matlab) no longer exists (renamed to custom user)."""
        self.assertFalse(self.host.user("matlab").exists)


class TestCustomUserErrors(unittest.TestCase):
    """Test common user error scenarios with clear error messages."""

    @classmethod
    def setUpClass(cls):
        cls.client = docker.from_env()
        cls.image_name = helper.get_image_name()
        cls.client.images.get(cls.image_name)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def test_missing_user_root_flag_rejected(self):
        """Test that setting USER_NAME without --user root fails with a helpful error."""
        container = self.client.containers.run(
            image=self.image_name,
            detach=True,
            environment={"USER_NAME": "myuser"},
            command="-shell",
        )
        try:
            result = container.wait(timeout=30)
            logs = container.logs().decode("utf-8")
            self.assertNotEqual(result["StatusCode"], 0)
            self.assertIn("requires root", logs)
        finally:
            container.remove(force=True)

    def test_uppercase_username_rejected(self):
        """Test that uppercase USER_NAME fails with a helpful error."""
        container = self.client.containers.run(
            image=self.image_name,
            detach=True,
            user="root",
            environment={"USER_NAME": "JohnSmith"},
            command="-shell",
        )
        try:
            result = container.wait(timeout=30)
            logs = container.logs().decode("utf-8")
            self.assertNotEqual(result["StatusCode"], 0)
            self.assertIn("USER_NAME must be 1-32 characters", logs)
        finally:
            container.remove(force=True)

    def test_email_style_username_rejected(self):
        """Test that email-style USER_NAME fails with a helpful error."""
        container = self.client.containers.run(
            image=self.image_name,
            detach=True,
            user="root",
            environment={"USER_NAME": "john.smith@company.com"},
            command="-shell",
        )
        try:
            result = container.wait(timeout=30)
            logs = container.logs().decode("utf-8")
            self.assertNotEqual(result["StatusCode"], 0)
            self.assertIn("USER_NAME must be 1-32 characters", logs)
        finally:
            container.remove(force=True)


##################################################################################

if __name__ == "__main__":
    unittest.main()
