#!/bin/bash

# Copyright 2024 The MathWorks, Inc.

# write the license file
mkdir -p "$(dirname "${LICENSE_FILE_PATH}")"
echo "${MATLAB_LICENSE_FILE}" >>"${LICENSE_FILE_PATH}"
