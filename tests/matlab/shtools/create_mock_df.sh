#!/usr/bin/env bash
# Copyright 2024 The MathWorks, Inc.

create_mock_df() {
    mock_output="$(
        cat <<EOF
#!/bin/sh
# Copyright 2024 The MathWorks, Inc.
echo -e "1K-blocks\n    65536"
EOF
    )"

    create_mock_with_output "df" "/tmp" "${mock_output}"
}

remove_mock_df() {
    remove_mock "df" "/tmp"
}
