#!/usr/bin/env bash

# Copyright 2024-2026 The MathWorks, Inc.

load common_setup.sh
common_setup

#--- TEST FIXTURES
setup_file() {
    # Add a mock MATLAB, vnc server, noVNC, and license file to the Docker container.
    create_mock_matlab
    create_mock_license
    create_mock_vnc_novnc

    # Array of mock scripts to be created
    # Create each mock file with its content
    mocks=("sudo" "exec" "launch")
    for mock in "${mocks[@]}"; do
        create_mock "${mock}"
    done

    # Create .profile for setup_session.sh
    touch ~/.profile
}

teardown_file() {
    # cleanup the mock MATLAB, vnc server, noVNC, and license file.
    remove_mock_matlab
    remove_mock_license
    remove_mock_vnc_novnc

    # remove all mocks created in the default mock location
    remove_all_default_mocks
}

#--- TESTS

@test "setup_session.sh without options should launch matlab" {
    run "${SRCDIR}"/setup_session.sh

    assert_success
    assert_line "Mocking matlab -licmode online"
}

@test "setup_session.sh -help should display the readme file" {
    local README_FILE="/etc/help_readme"
    local message="this is a fake readme!"
    create_file_with_content "${README_FILE}" "${message}"

    run "${SRCDIR}"/setup_session.sh -help

    # teardown - delete file
    rm "${README_FILE}"

    # assert the output of the setup_session.sh -help command
    assert_success
    assert_line "${message}"
}

@test "setup_session.sh -batch without license file should work" {
    run "${SRCDIR}"/setup_session.sh -batch rand

    assert_success
    assert_line "Mocking matlab -licmode online -batch rand"
    run pgrep "matlab"
    assert_equal $status 1
}

# We expect MATLAB to then fail but this is outside the scope of this test
@test "setup_session.sh -batch without MATLAB command should run matlab" {
    export MLM_LICENSE_FILE=$LICENSEFILE

    run "${SRCDIR}"/setup_session.sh -batch

    assert_success
    assert_line "Mocking matlab -batch"
}

@test "setup_session.sh -batch with valid license and command should work" {
    export MLM_LICENSE_FILE=$LICENSEFILE

    run "${SRCDIR}"/setup_session.sh -batch rand

    assert_success
    assert_line --partial "Licensing MATLAB using the license manager"
    assert_line "Mocking matlab -batch rand"
    refute_line --partial '-licmode online'
}

@test "setup_session.sh -vnc should print a message and start a noVNC server" {
    local README_FILE="/etc/vnc_readme"
    local message="this is a fake readme!"
    create_file_with_content "${README_FILE}" "${message}"

    create_mock "bash"
    create_mock_df

    run "${SRCDIR}/setup_session.sh" -vnc

    # teardown - delete files
    remove_mock "bash"
    remove_mock_df
    rm $README_FILE

    # assert the output of the setup_session.sh -vnc command
    assert_success
    assert_line "${message}"
}

@test "setup_session.sh -vnc -browser should error" {
    run "${SRCDIR}"/setup_session.sh -vnc -browser

    # We would expect a failure here because of validate input
    assert_failure
    assert_line "Error: -help, -vnc, -shell and -browser are mutually exclusive."
}

@test "setup_session.sh -batch -c should work" {
    run "${SRCDIR}"/setup_session.sh -batch rand -c licenseserver

    assert_success
    assert_line "Mocking matlab -licmode online -batch rand -c licenseserver"
}
