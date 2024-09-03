# Copyright 2024 The MathWorks, Inc.

common_setup() {

    bats_load_library bats-support
    bats_load_library bats-assert

    #--- SET GLOBAL VARIABLES
    TESTDIR="$(dirname "$(realpath "${BATS_TEST_FILENAME}")")"
    SRCDIR="$(realpath "${TESTDIR}"/../src)"

    #--- SUPPORT PACKAGES, HELPER METHODS AND MOCKS
    for file in "${TESTDIR}"/shtools/*.sh; do
        if [ -f "${file}" ]; then
            load "${file}"
        fi
    done
}
