# SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
from tarfile import CompressionError

import hashlib
from pathlib import Path
import tarfile

BASE_DIR = Path(__file__).parent.resolve()
SRC_DIR = BASE_DIR / "src"
ARCHIVES_DIR = BASE_DIR / "archives"
TOOLCHAINS_DIR = BASE_DIR / "toolchains"
TARGETS_DIR = BASE_DIR / "targets"


def check_sha256(file, expected_sha256):
    with open(file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
    if digest.hexdigest() != expected_sha256:
        print(f"File hashes of '{file}' mismatch!")
        print(f"is:       {digest.hexdigest()}")
        print(f"expected: {expected_sha256}")
        exit(-1)


def unpack_tar(archive_file: Path, out_path: Path):
    print(f"Extracting {archive_file.name}...")
    try:
        with tarfile.open(name=archive_file, mode="r:*") as tar:
            tar.extractall(out_path, filter="tar")
    except CompressionError as e:
        if "zst" in str(e):
            print(
                "ztsd is not supported by tarfile. Please check if you are using Python 3.14"
            )
            exit(1)
        else:
            raise e
