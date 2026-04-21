#!/usr/bin/env bash

# Copyright 2026 The MathWorks, Inc.

set -eu -o pipefail

. $(dirname "$0")/utils.sh

# This script is invoked via `sudo -u <user>` from run.sh, which means it runs
# with the correct UID but as a non-login, non-interactive shell. ~/.profile is
# therefore never sourced automatically, so environment variables set there at
# image build time (PATH additions, JAVA_HOME, etc.) would be missing. We
# source it manually here to replicate what a login shell would do.
# Temporarily disable -u while sourcing: profile scripts commonly reference
# variables like PS1 that are unset in non-interactive shells, which would
# otherwise cause an immediate abort under `set -u`.
set +u
. ~/.profile
set -u

# matlab-proxy-app is installed via pipx into /home/matlab/.local/bin.
# sudo resets PATH via secure_path, and root's ~/.profile does not restore it.
# Ensure it is always available regardless of which user runs this script.
export PATH="/home/matlab/.local/bin:${PATH}"

modes=0
HELP=false
VNC=false
BROWSER=false
SHELL_MODE=false

CUSTOM_ARGS=()

while [ $# -gt 0 ]; do
    case "$1" in
    -help)
        HELP=true
        modes=$((modes + 1))
        ;;
    -vnc | -shell)
        VNC=true
        modes=$((modes + 1))
        ;;
    -browser)
        BROWSER=true
        modes=$((modes + 1))
        ;;
    *)
        CUSTOM_ARGS+=("$1")
        ;;
    esac
    shift
done

validateInput
checkLicensing
checkSharedMemorySpace
checkEnvironmentVariables
startContainer

exit
