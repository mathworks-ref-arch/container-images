#!/usr/bin/env bash
# Copyright 2024-2026 The MathWorks, Inc.

create_mock_vnc_novnc() {
    create_mock "vncserver" "/usr/bin"
    # Create mock noVNC files at the hardcoded path used by utils.sh,
    # which references /home/matlab/apps/noVNC/ regardless of $HOME.
    mkdir -p /home/matlab/apps/noVNC/utils
    create_mock "launch.sh" "/home/matlab/apps/noVNC/utils"
    touch /home/matlab/apps/noVNC/index.html
    touch /home/matlab/apps/noVNC/redirect.html
}

remove_mock_vnc_novnc() {
    remove_mock "vncserver" "/usr/bin"
    remove_mock "launch.sh" "/home/matlab/apps/noVNC/utils"
    rm -f /home/matlab/apps/noVNC/index.html /home/matlab/apps/noVNC/redirect.html
    rmdir /home/matlab/apps/noVNC/utils /home/matlab/apps/noVNC /home/matlab/apps 2>/dev/null || true
}
