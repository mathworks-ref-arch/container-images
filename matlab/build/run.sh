#!/bin/sh

# Copyright 2021-2024 The MathWorks, Inc.

set -e

. $(dirname "$0")/utils.sh

modes=0

CUSTOM_COMMAND=""

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
        CUSTOM_COMMAND="${CUSTOM_COMMAND} $(build_cmd "$1")"
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
