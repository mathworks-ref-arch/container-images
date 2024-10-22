# Copyright 2023-2024 The MathWorks, Inc.

"""Getter class to get platform and release info from a system-under-test (SUT) name."""

from pathlib import Path
import re
import os

_MATLAB_DEPS_ROOT_ = Path(__file__).parents[3] / "matlab-deps"
DEPENDENCIES_LIST_FILENAME = "base-dependencies.txt"

ubuntu_re = re.compile("ubuntu[0-9]{2}.[0-9]{2}")
ubi_re = re.compile("ubi[0-9]")
aws_re = re.compile("aws-batch")
platform_re = re.compile(f"({ubuntu_re.pattern})|({ubi_re.pattern})|({aws_re.pattern})")

release_re = re.compile("R20[0-9]{2}[ab]", re.IGNORECASE)


def is_valid_release(str):
    match = release_re.fullmatch(str)
    if match:
        return True
    else:
        return False


def get_deps_list_filepath(release, platform):
    return str(
        _MATLAB_DEPS_ROOT_ / release.lower() / platform / DEPENDENCIES_LIST_FILENAME
    )


class Getter:
    def __init__(self, name) -> None:
        self.name = name

    @property
    def release(self):
        """Get the release from the image's name. If not possible, get the release from the source repo"""
        match = release_re.search(self.name)
        if match:
            return match.group(0)
        else:  # by default, return the latest release available in the container-images repository
            release_subdirs = list(
                filter(
                    is_valid_release,
                    os.listdir(str(_MATLAB_DEPS_ROOT_)),
                )
            )
            release_subdirs.sort()
            return release_subdirs[-1]

    @property
    def platform(self):
        """Get the platform from the image's name. If not possible, get the platform from the source repo"""
        match = platform_re.search(self.name)
        if match:
            return match.group(0)
        else:  # if there is no match, look the ubuntu version for the tested release and return the latest
            matlab_deps_root = str(_MATLAB_DEPS_ROOT_)

            ubuntu_platforms = list(
                filter(
                    lambda x: ubuntu_re.fullmatch(x) is not None,
                    os.listdir(f"{matlab_deps_root}/{self.release.lower()}"),
                )
            )
            ubuntu_platforms.sort()
            return ubuntu_platforms[-1]

    @property
    def deps_list_filepath(self):
        return get_deps_list_filepath(self.release, self.platform)
