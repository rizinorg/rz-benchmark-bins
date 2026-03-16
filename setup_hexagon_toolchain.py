#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only

from tarfile import CompressionError
import shutil

from pathlib import Path
import platform
import subprocess
import tarfile
import sys
from helpers import check_sha256, ARCHIVES_DIR, TOOLCHAINS_DIR

HEXAGON_TARGET_NAME = "hexagon-unknown-linux-musl"


def get_architecture():
    arch = platform.machine()
    if arch == "x86_64":
        return (
            "eb96c5dcd9a563ec09d829aed0546bb3b0387036fd560592f5161199c71306a8",
            "x86_64-linux-musl",
        )
    elif arch == "aarch64":
        return (
            "70e691db76a9fca9c7b075fd0db52573d1c8f36e0a706ff95d857cacf02e457e",
            "aarch64-linux-musl",
        )
    else:
        print(
            f"Error: Unsupported architecture '{arch}'.\n"
            "Hexagon toolchains are prebuilt for x86_64 and aarch64."
        )
        sys.exit(1)


def main():
    # Determine the correct file based on local architecture
    base_url = "https://artifacts.codelinaro.org/artifactory/codelinaro-toolchain-for-hexagon/22.1.0_/"
    sha, arch = get_architecture()
    toolchain_name = Path("clang+llvm-22.1.0-cross-hexagon-unknown-linux-musl")
    file_name = f"{toolchain_name}_{arch}"
    archive_name = f"{file_name}.tar.zst"
    url = base_url + archive_name

    print(f"Archive: {archive_name}")

    archive_path = ARCHIVES_DIR / archive_name
    if not archive_path.exists():
        print(f"Downloading from {url}...")
        subprocess.run(["curl", "-Lfo", archive_path, url], check=True)
        print("Download complete.")

    check_sha256(archive_path, sha)

    if (
        not (TOOLCHAINS_DIR / toolchain_name).exists()
        and not (TOOLCHAINS_DIR / HEXAGON_TARGET_NAME).exists()
    ):
        print(f"Unpacking {archive_path}...")
        try:
            with tarfile.open(archive_path, "r:zst") as tar:
                tar.extractall(TOOLCHAINS_DIR, filter="tar")
        except CompressionError as e:
            if "zst" in str(e):
                print(
                    "ztsd is not supported by tarfile. Please check if you are using Python 3.14"
                )
                exit(1)
            else:
                raise e

    if (TOOLCHAINS_DIR / toolchain_name).exists():
        print(f"Move {toolchain_name} -> {HEXAGON_TARGET_NAME}")
        # Move the toolchain dir in clang+llvm-.... to the target name dir.
        shutil.move(
            TOOLCHAINS_DIR / toolchain_name / arch,
            TOOLCHAINS_DIR / HEXAGON_TARGET_NAME,
        )
        shutil.rmtree(TOOLCHAINS_DIR / toolchain_name)


if __name__ == "__main__":
    main()
