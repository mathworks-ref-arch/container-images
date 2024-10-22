"""Test class for matlab-deps:ubuntu Docker images."""

# Copyright 2023-2024 The MathWorks, Inc.

import re
import unittest
from . import base

UBUNTU = "ubuntu"


class TestUbuntu(base.TestCase):

    def test_packages_are_upgraded(self):
        """Test that the packages installed in the container are updated to the latest version"""
        # run `apt-get -s upgrade` to check if ANY package needs to be upgraded.
        # Alternatives are:
        # - `apt-get -s install DEPENDENCIES_LIST`: which will only run on the MATLAB dependencies packages
        # - `apt list --upgreadeable` which does not have a stable interface
        cmd = "apt-get -s upgrade"
        cmd_res = self.host.run(cmd)
        self.assertTrue(cmd_res.succeeded, f"command {cmd} failed:\n{cmd_res.stderr}")

        installable_pkg_re = "The following packages will be installed"
        upgradeable_pkg_re = "The following packages will be upgraded"
        self.assertNotRegex(
            cmd_res.stdout,
            re.compile(f"({installable_pkg_re})|({upgradeable_pkg_re})"),
            f"The command\n\n{cmd}\n\nshowed that some packages are not up-to-date. The output is:\n\n{cmd_res.stdout}",
        )

    def test_package_manager_cache_is_clean(self):
        """Test that the apt-get cache got cleaned after installation of the packages."""
        self.assertSetEqual(
            set(self.host.file("/var/cache/apt/archives").listdir()),
            {"lock", "partial"},
        )


######################################################################

if __name__ == "__main__":
    unittest.main()
