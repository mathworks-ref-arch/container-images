#! /bin/sh

# Copyright 2024 The MathWorks, Inc.

# Get the current directory
REPO_ROOT=$(git rev-parse --show-toplevel)

OFFERING="matlab"

# Get test directory
TEST_DIR="${REPO_ROOT}/tests/${OFFERING}"

# Get the source code directory
BUILD_DIR="${REPO_ROOT}/${OFFERING}/build"

# Run the Docker command with the resolved path
docker run --rm --shm-size=512M -v "$TEST_DIR:/home/test" -v "$BUILD_DIR:/home/src" bats/bats:latest /home/test/tUtils.bats

docker run --rm --shm-size=512M -v "$TEST_DIR:/home/test" -v "$BUILD_DIR:/home/src" bats/bats:latest /home/test/tRun.bats
