#!/usr/bin/env bash
# Copyright 2024 The MathWorks, Inc.

default_mock_path="/tmp/mocks"
default_mock_symlink_path="/usr/local/sbin"

create_mock() {
    mock=$1
    mocksdir=${2:-"${default_mock_path}"}
    mock_output="$(
        cat <<EOF
#!/bin/sh
# Copyright 2024 The MathWorks, Inc.
echo "Mocking ${mock} \$@"
EOF
    )"

    create_mock_with_output "${mock}" "${mocksdir}" "${mock_output}"
}

create_mock_with_output() {
    mock=$1
    mocksdir=$2
    mock_output=$3
    mock_path="${mocksdir}/${mock}"
    # Create each mock file with its content
    create_file_with_content "${mock_path}" "$(cat <<<"${mock_output}")"

    # Copy each mock script to the target directory and make it executable
    chmod +x "${mock_path}"

    mkdir -p "${default_mock_symlink_path}"
    # Add a softlink so that the mock is on PATH
    ln -s "${mock_path}" "${default_mock_symlink_path}/${mock}"

}

remove_all_default_mocks() {
    for mock in "${default_mock_path}"/*; do
        if [ -f "$mock" ]; then
            remove_mock "$(basename "$mock")" "${default_mock_path}"
        fi
    done
}

remove_mock() {
    mock=$1
    mocksdir=${3:-"${default_mock_symlink_path}"}
    symlinikdir=${2:-"${default_mock_path}"}
    mock_path="${mocksdir}/${mock}"
    mock_symlink_path="${symlinikdir}/${mock}"

    # Remove the mock script and its symlink
    rm -f "${mock_symlink_path}" "${mock_path}"
}
