#!/usr/bin/env bash
#
# Copyright 2023 The MathWorks Inc.

# This script increments the minor version in a version number vMAJOR.MINOR

# Retrieve the input
VERSION=$1

# Test if the input matches the expected format
if [[ "${VERSION}" =~ ^v([0-9]+).(-?[0-9]+)$ ]]; then
    # Extract major and minor levels
    MAJOR="${BASH_REMATCH[1]}"
    MINOR="${BASH_REMATCH[2]}"

    # Increment minor level
    echo "v${MAJOR}.$((++MINOR))"

else
    echo ">> ${VERSION} is not a valid version (expecting vX.X)."
    exit 1
fi
