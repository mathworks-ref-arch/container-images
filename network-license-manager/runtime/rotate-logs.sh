#!/bin/bash

# Copyright 2026 The MathWorks, Inc.

set -euo pipefail

source /shared.sh

rotate_logs() {
    local newlog=$(dirname "$LOG_FILE")"/mlm-$(date +%Y-%m-%d-%H%M%S).log"
    if [[ -e "$newlog" ]]; then
        echo_and_log "log file $newlog exists already"
        exit 1
    fi
    runuser -u lmgr -- /nlm/etc/glnxa64/lmutil lmswitch MLM "$newlog" >&2
}

ensure_perms
rotate_logs
