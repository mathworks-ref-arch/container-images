#!/usr/bin/env bash

# Copyright 2026 The MathWorks, Inc.

# Tests for run.sh user modification logic and argument forwarding.
# Session startup tests are in tSetupSession.bats.

load common_setup.sh
common_setup

#--- TEST FIXTURES

# Common UID/GID values used in mocks and tests
MATLAB_UID=1000
MATLAB_GID=1000
CONFLICTING_UID=2000
CONFLICTING_GID=3000
CONFLICTING_USER="existinguser"
CONFLICTING_GROUP="existinggroup"
BUMP_OFFSET=10000
TEST_USER="myuser"
TEST_UID=4000
TEST_GID=5000

setup_file() {
    # Export variables for use in tests
    export MATLAB_UID MATLAB_GID CONFLICTING_UID CONFLICTING_GID CONFLICTING_USER CONFLICTING_GROUP BUMP_OFFSET TEST_USER TEST_UID TEST_GID

    # Mock setup_session.sh so run.sh tests are isolated
    create_mock "setup_session.sh" "/bin"
    
    # Create mock id that simulates running as root and returns matlab user info
    create_mock_with_output "id" "/tmp/mocks" "#!/bin/bash
case \"\$1\" in
    -u)
        if [ -n \"\$2\" ]; then
            echo \"${MATLAB_UID}\"
        else
            echo \"0\"
        fi
        ;;
    -g) echo \"${MATLAB_GID}\" ;;
    \"\") echo \"uid=0(root) gid=0(root)\" ;;
    \"matlab\") echo \"uid=${MATLAB_UID}(matlab) gid=${MATLAB_GID}(matlab)\" ;;
    *) /usr/bin/id \"\$@\" ;;
esac"

    # Create mock getent
    create_mock_with_output "getent" "/tmp/mocks" "#!/bin/bash
case \"\$1:\$2\" in
    passwd:matlab) echo \"matlab:x:${MATLAB_UID}:${MATLAB_GID}::/home/matlab:/bin/bash\" ;;
    passwd:root) echo \"root:x:0:0:root:/root:/bin/bash\" ;;
    passwd:nobody) echo \"nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin\" ;;
    passwd:${CONFLICTING_UID}) echo \"${CONFLICTING_USER}:x:${CONFLICTING_UID}:${CONFLICTING_UID}::/home/${CONFLICTING_USER}:/bin/bash\" ;;
    group:${MATLAB_GID}) echo \"matlab:x:${MATLAB_GID}:\" ;;
    group:matlab) echo \"matlab:x:${MATLAB_GID}:\" ;;
    group:${CONFLICTING_GID}) echo \"${CONFLICTING_GROUP}:x:${CONFLICTING_GID}:\" ;;
    passwd:*) exit 2 ;;
    group:*) exit 2 ;;
esac"

    # Create mocks that log their calls
    create_mock "usermod"
    create_mock "groupmod"
    create_mock "chown"
    create_mock "sudo"
    create_mock "script"
    
    # Create mock home directory
    mkdir -p /home/matlab/Documents/MATLAB
    
    # Create mock sudoers file
    mkdir -p /etc/sudoers.d
    echo "matlab ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/matlab
}

teardown_file() {
    remove_all_default_mocks
    remove_mock "setup_session.sh" "/bin"
    rm -rf /home/matlab
    rm -f /etc/sudoers.d/matlab /etc/sudoers.d/myuser
}

setup() {
    # Restore default id mock before each test (some tests override it)
    remove_mock "id"
    create_mock_with_output "id" "/tmp/mocks" "#!/bin/bash
case \"\$1\" in
    -u)
        if [ -n \"\$2\" ]; then
            echo \"${MATLAB_UID}\"
        else
            echo \"0\"
        fi
        ;;
    -g) echo \"${MATLAB_GID}\" ;;
    \"\") echo \"uid=0(root) gid=0(root)\" ;;
    \"matlab\") echo \"uid=${MATLAB_UID}(matlab) gid=${MATLAB_GID}(matlab)\" ;;
    *) /usr/bin/id \"\$@\" ;;
esac"
    
    # Remove any whoami mock from previous tests
    remove_mock "whoami"

    # Restore sudoers file (may have been renamed by a previous test)
    rm -f /etc/sudoers.d/matlab /etc/sudoers.d/${TEST_USER}
    echo "matlab ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/matlab
}

#--- TESTS

@test "run.sh rejects USER_UID=0 and suggests --user root" {
    export USER_UID="0"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_failure
    assert_output --partial "use '--user root'"
}

@test "run.sh rejects USER_GID=0 and suggests --user root" {
    export USER_GID="0"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_failure
    assert_output --partial "use '--user root'"
}

@test "run.sh runs as user matlab and not root, when no customisation is provided" {
    # Override id mock to simulate running as matlab user
    remove_mock "id" "/tmp/mocks"
    create_mock_with_output "id" "/tmp/mocks" "#!/bin/bash
case \"\$1\" in
    -u) if [ -n \"\$2\" ]; then echo \"${MATLAB_UID}\"; else echo \"${MATLAB_UID}\"; fi ;;
    -g) echo \"${MATLAB_GID}\" ;;
    *) echo \"uid=${MATLAB_UID}(matlab) gid=${MATLAB_GID}(matlab)\" ;;
esac"
    create_mock_with_output "whoami" "/tmp/mocks" '#!/bin/bash
echo "matlab"'
    
    unset USER_NAME USER_UID USER_GID
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_success
    assert_output --partial "sudo --preserve-env --user matlab"
    refute_output --partial "WARNING"
}

@test "run.sh rejects USER_NAME that conflicts with existing user (nobody)" {
    export USER_NAME="nobody"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_failure
    assert_output --partial "conflicts with existing user"
}

@test "run.sh applies USER_NAME, USER_UID and USER_GID customisation correctly" {
    local failures=()

    export USER_NAME="${TEST_USER}"
    export USER_UID="${TEST_UID}"
    export USER_GID="${TEST_GID}"
    run "${SRCDIR}"/run.sh -shell

    if [[ "$status" -ne 0 ]]; then
        fail "command failed with status $status: $output"
    fi

    # Verify user rename
    [[ "$output" == *"usermod -l ${TEST_USER} matlab"* ]] || failures+=("expected user rename")
    [[ "$output" == *"groupmod -n ${TEST_USER} matlab"* ]] || failures+=("expected group rename")

    # Verify UID/GID changes
    [[ "$output" == *"usermod -u ${TEST_UID} matlab"* ]] || failures+=("expected UID change")
    [[ "$output" == *"groupmod -g ${TEST_GID} matlab"* ]] || failures+=("expected GID change")

    # Verify ownership and session
    [[ "$output" == *"chown -R ${TEST_USER}:${TEST_USER} /home/matlab"* ]] || failures+=("expected home ownership change")
    [[ "$output" == *"sudo --preserve-env --user ${TEST_USER}"* ]] || failures+=("expected session as new user")

    # Verify home directory is not moved
    [[ "$output" != *"usermod -d"* ]] && [[ "$output" != *"usermod -m"* ]] || failures+=("home directory should not be moved")

    # Verify sudoers file was updated
    [[ ! -f /etc/sudoers.d/matlab ]] || failures+=("sudoers file should be renamed from matlab")
    [[ -f /etc/sudoers.d/${TEST_USER} ]] || failures+=("sudoers file should exist for ${TEST_USER}")

    [[ ${#failures[@]} -eq 0 ]] || fail "$(printf '%s\n' "${failures[@]}")"
}

@test "run.sh skips usermod when USER_UID matches current UID" {
    export USER_UID="${MATLAB_UID}"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_success
    refute_output --partial "usermod -u"
}

@test "run.sh skips groupmod when USER_GID matches current GID" {
    export USER_GID="${MATLAB_GID}"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_success
    refute_output --partial "groupmod -g"
}

@test "run.sh bumps conflicting UID before applying new UID" {
    export USER_UID="${CONFLICTING_UID}"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_success
    assert_output --partial "usermod -u $((CONFLICTING_UID + BUMP_OFFSET)) ${CONFLICTING_USER}"
}

@test "run.sh bumps conflicting GID before applying new GID" {
    export USER_GID="${CONFLICTING_GID}"
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_success
    assert_output --partial "groupmod -g $((CONFLICTING_GID + BUMP_OFFSET)) ${CONFLICTING_GROUP}"
}

@test "run.sh reports and continues when running as root without customisation" {
    unset USER_NAME USER_UID USER_GID
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_success
    assert_output --partial "Running as root"
    assert_output --partial "sudo --preserve-env --user root"
}

@test "run.sh forwards arguments to setup_session" {
    export USER_NAME="${TEST_USER}"
    
    run "${SRCDIR}"/run.sh -vnc -batch test
    
    assert_success
    assert_output --partial "setup_session.sh -vnc -batch test"
}

@test "run.sh rejects invalid USER_NAME formats" {
    local cases=(
        "Invalid-User-123|contains invalid characters"
        "1user|starts with digit"
        "abcdefghijklmnopqrstuvwxyz1234567|exceeds 32 characters"
    )
    local failures=()

    for case in "${cases[@]}"; do
        IFS='|' read -r username description <<< "$case"
        export USER_NAME="$username"

        run "${SRCDIR}"/run.sh -shell

        if [[ "$status" -eq 0 ]]; then
            failures+=("$description: expected failure but got success")
        elif [[ "$output" != *"USER_NAME must be 1-32 characters"* ]]; then
            failures+=("$description: wrong message - got: $output")
        fi
    done

    [[ ${#failures[@]} -eq 0 ]] || fail "$(printf '%s\n' "${failures[@]}")"
}

@test "run.sh rejects non-root non-matlab user" {
    # Override id mock to simulate running as unknown user (UID 1234)
    remove_mock "id"
    create_mock_with_output "id" "/tmp/mocks" '#!/bin/bash
case "$1" in
    -u) echo "1234" ;;
    *) echo "uid=1234(unknownuser) gid=1234(unknownuser)" ;;
esac'
    create_mock_with_output "whoami" "/tmp/mocks" '#!/bin/bash
echo "unknownuser"'
    
    run "${SRCDIR}"/run.sh -shell
    
    assert_failure
    assert_output --partial "Running as user 'unknownuser' is not supported"
}
