#!/bin/bash

# Copyright 2024-2026 The MathWorks, Inc.

source /shared.sh

LICENSE_FILE=""
lmgrdPID="" # lmgrdPID will store the lmgrd PID once started

usage() {
    printf 'Usage: %s [--licenseFile filepath]\n' "$0" >&2
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --licenseFile) LICENSE_FILE="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) printf 'Unrecognized option: %s\n' "$1" >&2; usage; exit 1 ;;
    esac
done

# Apply default only if the user didn't provide one
if [[ -z "$LICENSE_FILE" ]]; then
    if [[ -f /usr/local/MATLAB/licenses/license.lic ]]; then
        LICENSE_FILE="/usr/local/MATLAB/licenses/license.lic"
    else
        LICENSE_FILE="/usr/local/MATLAB/licenses/license.dat"
    fi
fi

shutdown_run=0
_term() {
    if [[ $shutdown_run -eq 0 ]]; then
        shutdown_run=1
    else
        return
    fi

    # Only kill lmgrd if it is still running
    if [[ -n "$lmgrdPID" ]] && kill -0 "$lmgrdPID" 2>/dev/null; then
        echo_and_log "Shutting down License Manager."
        runuser -u lmgr -- /nlm/etc/glnxa64/lmutil lmdown -q -force -c "$LICENSE_FILE" | tee -a "$LOG_FILE" &
        shutdown_status=$?
        if [ $shutdown_status -ne 0 ]; then
            echo_and_log "Unable to shut down License Manager."
        else
            echo_and_log "License Manager has shut down."
        fi
        # Propagate shutdown exit code in case of errors
        exit $shutdown_status
    fi
}

trap _term SIGTERM EXIT

ensure_perms

echo_and_log "Starting License Manager."
chown lmgr $LOG_FILE
chmod 666 $LOG_FILE

runuser -u lmgr -- /nlm/etc/glnxa64/lmgrd -z -2 -p -local -c "$LICENSE_FILE" > >(tee -a "$LOG_FILE") &
lmgrdPID=$!
wait "$lmgrdPID"
