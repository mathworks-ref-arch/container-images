# Copyright 2024 The MathWorks, Inc.

MATLAB_RELEASE="R2023a"

# Ubuntu 20.04 requires python3.8-venv when using pipx
APT_ADDITIONAL_PACKAGES="python3.8-venv"

# Ubuntu 20.04 has vncpasswd provided by tigervnc-common so don't need tigervnc-tools
APT_ADDITIONAL_PACKAGES_VNC=""