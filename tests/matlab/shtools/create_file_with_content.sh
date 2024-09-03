#!/usr/bin/env bash
# Copyright 2024 The MathWorks, Inc.

# create_file_with_content writes the content of the second argument 
# to the file pointed by the first argument
create_file_with_content() {
    mkdir -p "$(dirname "$1")"
    echo "$2" >"$1"
}
