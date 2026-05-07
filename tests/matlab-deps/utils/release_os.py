# Copyright 2023-2026 The MathWorks, Inc.

"""Getter class to get OS and release info from the image's tags."""

from pathlib import Path
import re

def build_deps_list_filepath(release, os, arch=""):
    """Build the filepath to the dependencies list file based on the release and os."""
    matlab_deps_root = Path(__file__).parents[3] / "matlab-deps"
    default_deps_list_filename = "base-dependencies.txt"
    arm64_deps_list_filename = "base-dependencies-arm64.txt"
    amd64_deps_list_filename = "base-dependencies-amd64.txt"

    if arch == "arm64":
        deps_list_filename = arm64_deps_list_filename
    elif arch == "amd64":        
        deps_list_filename = amd64_deps_list_filename
    else:
        deps_list_filename = default_deps_list_filename

    candidate_path = Path(matlab_deps_root / release.lower() / os.lower() / deps_list_filename)
    if not candidate_path.is_file():
        return str(matlab_deps_root / release.lower() / os.lower() / default_deps_list_filename)
    return str(candidate_path)

def extract_release_from_tags(tags):
    release_pattern = re.compile(r"R20[0-9]{2}[ab]", re.IGNORECASE)
    # releases is an empty set
    releases = set()
    # collect all releases mentioned in the tags
    for tag in tags:
        match = release_pattern.search(tag)
        if match:
            releases.add(match.group().lower())
    if len(releases) == 0:
        raise ValueError(f"No release found in tags: {tags}")
    # check that all releases are the same, if not raise an error
    if len(set(releases)) > 1:
        raise ValueError(f"Multiple different releases found in tags: {releases}")
    # return the only release found
    return releases.pop()

def extract_os_from_tags(tags):
    ubuntu_pattern = re.compile("ubuntu[0-9]{2}.[0-9]{2}")
    ubi_pattern = re.compile("ubi[0-9]")
    aws_pattern = re.compile("aws-batch")
    debian_pattern = re.compile("debian[0-9]{2}")
    os_pattern = re.compile(f"({ubuntu_pattern.pattern})|({ubi_pattern.pattern})|({aws_pattern.pattern})|({debian_pattern.pattern})", re.IGNORECASE)
    # os is an empty set
    oses = set()
    # collect all oses mentioned in the tags
    for tag in tags:
        match = os_pattern.search(tag)
        if match:
            oses.add(match.group().lower())
    if len(oses) == 0:
        raise ValueError(f"No OS found in tags: {tags}")
    # check that all oses are the same, if not raise an error
    if len(set(oses)) > 1:
        raise ValueError(f"Multiple different OSes found in tags: {oses}")
    # return the only OS found
    return oses.pop()


class Getter:
    def __init__(self, image) -> None:
        self.image = image

    @property
    def tags(self):
        """Get the tags of the image, excluding the image's name."""
        return [t.split(":", 1)[1] for t in self.image.tags if t != "<none>" and ":" in t]

    @property
    def release(self):
        """Get the release from the image's name."""
        return extract_release_from_tags(self.tags)

    @property
    def os_tag(self):
        """Get the OS tag from the image's name."""
        return extract_os_from_tags(self.tags)

    @property
    def arch(self):
        """Get the architecture from the image's name."""
        # Implementation for extracting architecture from tags
        return self.image.attrs.get("Architecture", "")

    @property
    def deps_list_filepath(self):
        """Get the filepath to the dependencies list file based on the release, os and architecture."""
        return build_deps_list_filepath(self.release, self.os_tag, self.arch)
