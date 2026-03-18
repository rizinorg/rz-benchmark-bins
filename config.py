# SPDX-FileCopyrightText: 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only


BUILD_STYLES = {
    "ignored_warnings": [
        # We don't care about correct execution.
        # We only need binaries.
        "--no-warnings"
    ],
    # We take the extremes for testing.
    "optimzie": [
        "-Oz", # Optimize aggresively for size
        "-Ofast", # Optimize aggresively for speed
        "-O0", # No optimization
    ],
    "linking": [
        # Static building.
        "-static"
        # TODO: dynamic
    ]
}
