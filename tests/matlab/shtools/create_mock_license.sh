#!/usr/bin/env bash
# Copyright 2024 The MathWorks, Inc.

default_license_file_path=/licenses/1234@server.com

# create_mock_license creates a mock license file
# with path LICENSEFILE
create_mock_license() {
    export LICENSEFILE="$1:-${default_license_file_path}"
    create_file_with_content "${LICENSEFILE}" "$(
        cat <<-EOM
# BEGIN--------------BEGIN--------------BEGIN
# Mock license file.
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
# END-----------------END-----------------END
EOM
    )"
}

remove_mock_license() {
    rm -f "${LICENSEFILE}"
}
