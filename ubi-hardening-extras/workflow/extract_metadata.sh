#!/usr/bin/env bash
#
# Copyright 2023 The MathWorks Inc.

# This script extracts the .sha256 and .version files from a Docker image.
# The files are saved to /tmp/latest.

# Get script location and Docker image to extract from
SCRIPTPATH=$(dirname $0)
BASE_IMAGE=$1

# Extract signature and version files from Docker image
docker build \
  --build-arg BASE_IMAGE=${BASE_IMAGE} \
  --file ${SCRIPTPATH}/extraction.Dockerfile \
  --output /tmp/latest/ \
  ${SCRIPTPATH}

# Output version
VERSION=$(cat /tmp/latest/*.version)
echo "${VERSION}"
