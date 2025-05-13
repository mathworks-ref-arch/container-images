# Copyright 2024-2025 The MathWorks, Inc.

MATLAB_RELEASE="R2023a"

MATLAB_DEPS_OS="ubuntu20.04"

# Using gcc-9 instead of gcc-11 as it is not available on Ubuntu 20.04
GCC="gcc-9"
GPP="g++-9"

# Ubuntu 20.04 requires python3.8-venv when using pipx
APT_ADDITIONAL_PACKAGES="python3.8-venv"

# Ubuntu 20.04 has vncpasswd provided by tigervnc-common so don't need tigervnc-tools
APT_ADDITIONAL_PACKAGES_VNC=""
