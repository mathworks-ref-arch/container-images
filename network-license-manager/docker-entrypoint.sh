#!/bin/bash

# Copyright 2024 The MathWorks, Inc.

LOG_FILE="/tmp/log/mathworks/logs.txt"
LICENSE_FILE="/usr/local/MATLAB/licenses/license.dat"

lmgrdPID="" # lmgrdPID will store the lmgrd PID once started

echo_and_log() {
    echo "$1" | tee -a "$LOG_FILE"
}

shutdown_run=0
_term () {
    if [[ $shutdown_run -eq 0 ]]; then
        shutdown_run=1
    else
        return
    fi

    # Only kill lmgrd if it is still running
    if kill -0 $lmgrdPID 2>/dev/null; then
        echo_and_log "Shutting down License Manager."
        runuser -u lmgr -- /nlm/etc/glnxa64/lmutil lmdown -q -force -c $LICENSE_FILE | tee -a $LOG_FILE &
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

touch $LOG_FILE
echo_and_log "Starting License Manager."
chown lmgr $LOG_FILE
chmod 666 $LOG_FILE
runuser -u lmgr -- /nlm/etc/glnxa64/lmgrd -z -2 -p -local -c $LICENSE_FILE | tee -a $LOG_FILE &
lmgrdPID=$!
wait "$lmgrdPID"
