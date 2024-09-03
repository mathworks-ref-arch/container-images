#!/usr/bin/env bash
# Copyright 2024 The MathWorks, Inc.

create_mock_vnc_novnc() {
    create_mock "vncserver" "/usr/bin"
    create_mock "launch.sh" "/opt/noVNC/utils"
}

remove_mock_vnc_novnc() {
    remove_mock "vncserver" "/usr/bin"
    remove_mock "launch.sh" "/opt/noVNC/utils"
}
