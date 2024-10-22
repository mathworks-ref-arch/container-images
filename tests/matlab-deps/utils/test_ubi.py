"""Test class for matlab-deps:ubi* Docker images."""

# Copyright 2023-2024 The MathWorks, Inc.

import unittest
from . import base

UBI = "ubi"


class TestUbi(base.TestCase):

    def test_packages_are_upgraded(self):
        """Test that the packages installed in the container are updated to the latest version"""
        cmd = "yum check-update"
        cmd_res = self.host.run(cmd)
        self.assertNotEqual(
            cmd_res.rc,
            100,  # YUM/DNF exit code will be 100 when there are updates available
            f"The command\n\n{cmd}\n\nshowed that some packages are not up-to-date. The output is:\n\n{cmd_res.stdout}",
        )

    def test_package_manager_cache_is_clean(self):
        """Test that the yum/dnf cache got cleaned after installation of the packages."""
        for filename in self.host.file("/var/cache/dnf").listdir():
            fullname = "/var/cache/dnf/" + filename
            if self.host.file(fullname).is_file:
                # no .solv/.solvx files in /var/cache/dnf
                with self.subTest(filename=filename):
                    self.assertNotRegex(filename, ".solv")
            elif self.host.file(fullname).is_directory:
                # var/cache/dnf/ubi-8-appstream-..../repodata is empty
                # var/cache/dnf/ubi-8-baseos-..../repodata is empty
                # var/cache/dnf/ubi-8-codeready-builder-..../repodata is empty
                fullname = fullname + "/repodata"
                with self.subTest(dirname=fullname):
                    self.assertEqual(
                        len(self.host.file(fullname).listdir()),
                        0,
                        f"{fullname} is not empty",
                    )


######################################################################

if __name__ == "__main__":
    unittest.main()
