# Copyright 2024 The MathWorks, Inc.

load common_setup.sh
common_setup

#--- IMPORT THE UTILS FILE
. "${SRCDIR}"/utils.sh

#--- TEST FIXTURES
setup_file() {
    # Add mock matlab() to the Docker container.
    create_mock_matlab

    # Create a mock for sudo
    create_mock "sudo"
}

teardown_file() {
    # remove all mocks setup for this test file
    remove_mock_matlab
    remove_default_mocks
}

#--- TESTS

@test "printMessage prints file content" {
    local FILENAME="/etc/newfile.txt"
    local message="hello world!"

    # setup - create file
    create_file_with_content "${FILENAME}" "${message}"

    # the output of the command 'printMessage $FILENAME' is the content of FILENAME
    # or the error message
    run printMessage "$(basename "${FILENAME}")"

    # teardown - delete file
    rm "${FILENAME}"

    # assert the output of the printMessage command
    assert_line "${message}"
}

@test "printMessage cannot access non-existing file" {
    run printMessage "non/existing.file"
    assert_line --partial "No such file or directory"
}

@test "exportInBashrc function adds specified environment variables to the ~/.bashrc file." {
    VAR1="foo"
    VAR2="bar"

    run exportInBashrc VAR1 VAR2
    run cat ~/.bashrc

    assert_line "export VAR1=foo"
    assert_line "export VAR2=bar"
}

@test "validateInput errors out when too many modes are supplied" {
    local modes=2

    run validateInput

    assert_failure
    assert_line "Error: -help, -vnc, -shell and -browser are mutually exclusive."
}

@test "validateInput batch no license file" {
    local modes=1
    local BATCH=true
    local MLM_LICENSE_FILE=
    local BATCH_COMMAND="rand"

    run validateInput

    assert_success
}

@test "validateInput batch no command" {
    local modes=1
    local BATCH=true
    local MLM_LICENSE_FILE="mock/license.file"
    local BATCH_COMMAND=

    run validateInput

    assert_success
}

@test "checkEnvironmentVariables set proxy host and port" {
    export PROXY_SETTINGS="proxy.fqdn.com:12345"

    checkEnvironmentVariables

    assert_equal "${MW_PROXY_HOST}" "proxy.fqdn.com"
    assert_equal "${MW_PROXY_PORT}" "12345"
}

@test "checkEnvironmentVariables set proxy host, port, username, and password" {
    export PROXY_SETTINGS="http://user:Test!#\'password@proxy.fqdn.com:12345"

    checkEnvironmentVariables

    assert_equal "${MW_PROXY_HOST}" "proxy.fqdn.com"
    assert_equal "${MW_PROXY_PORT}" "12345"
    assert_equal "${MW_PROXY_USERNAME}" "user"
    assert_equal "${MW_PROXY_PASSWORD}" "Test!#'password"
}

@test "getMATLABversion" {
    run getMATLABVersion

    assert_output --partial "R20"
}
