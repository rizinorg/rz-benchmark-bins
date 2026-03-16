# SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only

import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
SRC_DIR = BASE_DIR / "src"
ARCHIVES_DIR = BASE_DIR / "archives"
TOOLCHAINS_DIR = BASE_DIR / "toolchains"
TARGETS_DIR = BASE_DIR / "targets"

SUPPORTED_TARGETS = [
    "aarch64-linux-gnu",
    "arm-linux-gnueabi",
    "arm-linux-gnueabihf",
    "i686-linux-gnu",
    "mips64el-linux-gnuabi64",
    "mips64-linux-gnuabi64",
    "mipsel-linux-gnu",
    "mipsisa32r6el-linux-gnu",
    "mipsisa32r6-linux-gnu",
    "mipsisa64r6el-linux-gnuabi64",
    "mipsisa64r6-linux-gnuabi64",
    "mips-linux-gnu",
    "powerpc64le-linux-gnu",
    "powerpc-linux-gnu",
    "riscv64-linux-gnu",
    "s390x-linux-gnu",
    "LOCAL_MACHINE",
]


def get_supported_targets():
    # if Path("/usr/")
    return SUPPORTED_TARGETS


def check_sha256(file, expected_sha256):
    with open(file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    if digest.hexdigest() != expected_sha256:
        print("file hashes mismatch!")
        print(f"is:       {digest.hexdigest()}")
        print(f"expected: {expected_sha256}")
        exit(-1)
