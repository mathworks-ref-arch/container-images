#!/usr/bin/env bash
# Copyright 2024-2026 The MathWorks, Inc.

matlab_path="/opt/matlab/R2099a/bin/matlab"
matlab_symlink_path="/usr/local/bin"

# create_mock_matlab creates a mocked version of MATLAB.
# The mock-matlab is a script that will print "MATLAB"
# followed by the arguments it was called with
create_mock_matlab() {
    create_mock "matlab" "${matlab_path}" "${matlab_symlink_path}"
    mkdir -p ~/Documents/MATLAB
}

remove_mock_matlab() {
    remove_mock "matlab" "${matlab_path}" "${matlab_symlink_path}"
}
