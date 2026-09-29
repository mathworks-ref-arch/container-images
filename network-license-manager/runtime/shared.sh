#!/bin/bash

# Copyright 2026 The MathWorks, Inc.

LOG_FILE="/tmp/log/mathworks/lmgrd.log"

echo_and_log() {
    printf '%s\n' "$1" | tee -a "$LOG_FILE"
}

ensure_perms() {
    setfacl -m u:lmgr:rwx $(dirname "$LOG_FILE")
    setfacl -d -m u:lmgr:rwx $(dirname "$LOG_FILE")
}
