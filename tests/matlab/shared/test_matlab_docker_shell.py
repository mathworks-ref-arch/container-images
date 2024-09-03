# Copyright 2021-2024 The MathWorks, Inc.

"""Run the tests for Docker images when they run in standard mode."""

import stat
import unittest

import docker
import testinfra
from pytools import helper


class TestBasicFeatures(unittest.TestCase):
    """Test a Docker container running in shell mode.

    This suite of test ensures that the image has been set up correctly so that
    all functionality will be present when a container is run. Additionally
    checks are in place that build artifacts and test do not remain in the final
    image.
    """

    @classmethod
    def setUpClass(cls):
        """Run the Docker container. Equivalent to

        'docker run -i -d DOCKER_IMAGE -shell'
        """
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
        """Stop and remove the container."""
        cls.container.stop()
        cls.container.remove()
        cls.client.close()

    ############################################################

    def test_packages_present(self):
        """Test that the software packages listed below are installed in the
        container. The list is taken from the Dockerfile for matlab-docker
        """

        packages = [
            "tini",
            "sudo",
            "curl",
            "wget",
            "nano",
            "xfce4-terminal",
            "psmisc",
            "less",
            "libglu1-mesa",
            "libosmesa6",
            "xfce4",
            "xscreensaver",
            "ca-certificates",
            "python3",
            "xvfb",
        ]
        for name in packages:
            with self.subTest(packagename=name):
                self.assertTrue(self.host.package(name).is_installed)

    def test_packages_absent(self):
        """Test that the software packages are NOT installed in the container.
        Docker containers should be as small as possible. Installing useless
        packages is a waste of space.
        """

        packages = ["tumbler", "pulseaudio", "gvfs", "gnome-screensaver", "git"]
        for name in packages:
            with self.subTest(packagename=name):
                self.assertFalse(self.host.package(name).is_installed)

    def test_libstdc_absent(self):
        """libstdc++ is causing some bugs with GpuCoder. We want to make sure
        that it is not installed.
        """
        matlab_release = helper.get_release_from_dir(self.host)
        pathlist = self.host.file(
            f"/opt/matlab/{matlab_release}/sys/os/glnxa64"
        ).listdir()
        for path in pathlist:
            self.assertNotRegex(path, r"libstdc\+\+")

    def test_users(self):
        """Test that the expected users exist."""
        users = ["root", "matlab"]
        for user in users:
            with self.subTest(username=user):
                self.assertTrue(self.host.user(user).exists)

    def test_removed_files(self):
        """Test that the licenses file directory has been removed during the
        Docker-build and it does not exist in the container
        """

        matlab_release = helper.get_release_from_dir(self.host)
        files = [
            "/home/matlab/licenses",
            "/usr/share/matlab/licenses",
            "/home/matlab/REMOVE_BEFORE_FLIGHT",
            "/opt/matlab/" + matlab_release + "/REMOVE_BEFORE_FLIGHT",
            "/usr/share/matlab/REMOVE_BEFORE_FLIGHT",
        ]
        for file in files:
            with self.subTest(filename=file):
                self.assertFalse(self.host.file(file).exists)

    def test_absent_license_file(self):
        """Search for all .LIC files and for all .DAT files containing "licen"
        in the path (e.g. license, licenses, licence, ...). Error messages are
        redirected to the STDOUT and those containing 'Permission denied' are
        ignored. Ignore license files from the ignorableLicfilename list. The
        test passes if the count of matched lines (grep -c) is 0.
        """

        ignorable_files = ["AHFormatter.lic", "license_info.xml"]
        if len(ignorable_files) >= 0:
            grep_args = '"Permission denied|' + "|".join(ignorable_files) + '"'
        else:
            grep_args = '"Permission denied"'
        cmd = self.host.run(
            "find /opt/matlab -iname *.lic -o -ipath *licen*.dat   2>&1 | \
                grep -c -vE "
            + grep_args
        )
        self.assertEqual(cmd.stdout.rstrip("\n"), "0")

    def test_files_in_directory(self):
        """Test that the following files are present."""
        matlab_release = helper.get_release_from_dir(self.host)
        paths = [
            ("/home/matlab/.vnc", "xstartup"),
            ("/home/matlab/Desktop", "MATLAB.desktop"),
            ("/home/matlab/.config", "xfce4"),
            ("/home/matlab/.matlab/" + matlab_release, "matlab.prf"),
            ("/etc/sudoers.d", "localsudo"),
            ("/bin", "run.sh"),
            ("/home/matlab/Documents/MATLAB", "startup.m"),
            ("/opt/noVNC", "redirect.html"),
            ("/opt", "noVNC"),
            ("/opt/noVNC/utils", "websockify"),
            ("/etc", "help_readme"),
            ("/etc", "vnc_readme"),
        ]
        for dirname, file in paths:
            with self.subTest(dirname=dirname, filename=file):
                self.assertIn(file, self.host.file(dirname).listdir())

    def test_permissions(self):
        """Test that the listed files have the right permissions."""
        pairs = [
            ("/home/matlab/.vnc/xstartup", "r.xr-xr-x"),
            ("/home/matlab/Desktop/MATLAB.desktop", "r.xr-xr-x"),
            ("/home/matlab/.matlab/", "r.xr-xr-x"),
            ("/bin/run.sh", "r.xr-xr-x"),
        ]
        for file, perm in pairs:
            with self.subTest(filename=file, permission=perm):
                self.assertRegex(
                    stat.filemode(stat.S_IMODE(self.host.file(file).mode)), perm
                )


##################################################################################

if __name__ == "__main__":
    unittest.main()
