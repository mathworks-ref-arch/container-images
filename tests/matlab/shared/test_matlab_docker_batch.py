# Copyright 2021-2024 The MathWorks, Inc.

"""Run the tests for Docker images which can run in -batch mode"""

import re
import unittest

import docker
import testinfra
from pytools import helper

VER_OUTPUT_FILE = "/home/matlab/ver.output"


class TestBatchMode(unittest.TestCase):
    """Test a Docker container when running in -batch mode.

    Running a Docker container in -batch mode will run the specified MATLAB
    commands in batch mode (matlab -batch COMMANDS) within the Docker container.
    MATLAB is licensed by mounting the license file and using the
    MLM_LICENSE_FILE environment variable to point to the license file location.
    The MATLAB command provided will write the MATLAB release to the file
    speficied by the global variable VER_OUTPUT_FILE. After the file has been
    written, the 'pause(Inf)' command is run, in order to keep the docker
    container running (once the 'matlab -batch COMMAND' has been completed,
    the container is stopped).
    """

    @classmethod
    def setUpClass(cls):
        """Run the Docker container specifying the '-batch' mode in command"""
        mount = [
            docker.types.Mount(
                target="/licenses/license.dat",
                source=helper.get_license_filepath(),
                read_only=True,
                type="bind",
            )
        ]
        env = {"MLM_LICENSE_FILE": "/licenses/license.dat"}
        cmd = f"-batch \"fid=fopen('{VER_OUTPUT_FILE}','w'); \
            fprintf(fid,version('-release')); \
            fclose(fid); \
            pause(Inf);\""  # pause(Inf) to keep the container running

        cls.client = docker.from_env()
        image_name = helper.get_image_name()
        cls.client.images.get(image_name)

        cls.container = cls.client.containers.run(
            image=image_name,
            detach=True,
            mounts=mount,
            environment=env,
            command=cmd,
        )
        cls.host = testinfra.get_host("docker://" + cls.container.id)

    @classmethod
    def tearDownClass(cls):
        """Stop and remove the Docker container"""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ##################################################################################

    def test_environment_variables(self):
        """Test that the environment variable "MLM_LICENSE_FILE" is correctly set"""
        self.assertEqual(
            self.host.environment()["MLM_LICENSE_FILE"], "/licenses/license.dat"
        )

    def test_matlab_runs(self):
        """Test that matlab is running"""
        helper.wait_for_cmd_cont(self.container, "MATLAB")
        self.assertGreater(
            len(self.host.process.filter(user="matlab", comm="MATLAB")), 0
        )

    def test_output_file_created(self):
        """Test that the VER_OUTPUT_FILE was created"""
        helper.wait_for_file(self.host, VER_OUTPUT_FILE, timeout=120)
        self.assertTrue(self.host.file(VER_OUTPUT_FILE).exists)

    def test_matlab_version(self):
        """Test that the release number written to the VER_OUTPUT_FILE file and
        the one from /opt/ver coincide"""
        ver_from_dir = helper.get_release_from_dir(self.host).replace("R", "")
        helper.wait_for_file(self.host, VER_OUTPUT_FILE, timeout=120)
        ver_from_mat = self.host.file(VER_OUTPUT_FILE).content_string.rstrip("\n")
        self.assertEqual(ver_from_dir, ver_from_mat)

    def test_version_image_name(self):
        """Test that the version reported by 'ver' in MATLAB is the same as the
        version used in naming the container image."""
        pattern = re.compile("r20[2-9][0-9][ab]", re.IGNORECASE)
        for tag in self.container.image.tags:
            match = pattern.search(tag)
            if match:
                break
        if match:
            ver_in_image_name = match.group(0)
            helper.wait_for_file(self.host, VER_OUTPUT_FILE, timeout=120)
            ver_from_mat = self.host.file(VER_OUTPUT_FILE).content_string.rstrip("\n")
            self.assertEqual(ver_in_image_name.lstrip("Rr"), ver_from_mat)


##################################################################################


if __name__ == "__main__":
    unittest.main()
