#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only

from toolchain import Toolchain, ToolchainType

import shutil

from pathlib import Path
import platform
import sys
from helpers import (
    ARCHIVES_DIR,
    TOOLCHAINS_DIR,
    unpack_tar,
    curl_download,
)

HEXAGON_TARGET_NAME = "hexagon-unknown-linux-musl"
TOOLCHAIN_NAME = Path("clang+llvm-22.1.0-cross-hexagon-unknown-linux-musl")
HEXAGON_TOOLCHAIN_DIR = Path(TOOLCHAINS_DIR / HEXAGON_TARGET_NAME)
HEXAGON_TOOLCHAIN_BIN_DIR = Path(TOOLCHAINS_DIR / HEXAGON_TARGET_NAME / "bin")
HEXAGON_TOOLCHAIN_TARGET_DIR = Path(
    TOOLCHAINS_DIR / HEXAGON_TARGET_NAME / "target" / "hexagon"
)


class HexagonToolchain(Toolchain):
    def get_disabled_features_binutils(self) -> list[str]:
        return ["--disable-bfd", "--disable-libiberty", "--disable-bootstrap"]


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
    file_name = f"{TOOLCHAIN_NAME}_{arch}"
    archive_name = f"{file_name}.tar.zst"
    url = base_url + archive_name

    print(f"Archive: {archive_name}")

    archive_path = ARCHIVES_DIR / archive_name
    curl_download(url, archive_path, sha)

    if (
        not (TOOLCHAINS_DIR / TOOLCHAIN_NAME).exists()
        and not (HEXAGON_TOOLCHAIN_DIR).exists()
    ):
        unpack_tar(archive_path, TOOLCHAINS_DIR)
    else:
        print("Toolchain was already extracted.")

    if (TOOLCHAINS_DIR / TOOLCHAIN_NAME).exists():
        print(f"Move {TOOLCHAIN_NAME} -> {HEXAGON_TARGET_NAME}")
        # Move the toolchain dir in clang+llvm-.... to the target name dir.
        shutil.move(
            TOOLCHAINS_DIR / TOOLCHAIN_NAME / arch,
            HEXAGON_TOOLCHAIN_DIR,
        )
        shutil.rmtree(TOOLCHAINS_DIR / TOOLCHAIN_NAME)


def toolchain_present() -> bool:
    return HEXAGON_TOOLCHAIN_DIR.exists()


def get_target() -> Toolchain:
    return HexagonToolchain(
        target_name=HEXAGON_TARGET_NAME,
        toolchain_type=ToolchainType.CrossExtern,
        # sysroot=HEXAGON_TOOLCHAIN_DIR / "target" / "hexagon",
        env={
            "CC": str(HEXAGON_TOOLCHAIN_BIN_DIR / "hexagon-unknown-linux-musl-clang"),
            "AR": str(HEXAGON_TOOLCHAIN_BIN_DIR / "hexagon-unknown-linux-musl-ar"),
            "LD": str(HEXAGON_TOOLCHAIN_BIN_DIR / "hexagon-unknown-linux-musl-ld"),
            "NM": str(HEXAGON_TOOLCHAIN_BIN_DIR / "hexagon-unknown-linux-musl-nm"),
            "CPP": str(HEXAGON_TOOLCHAIN_BIN_DIR / "hexagon-unknown-linux-musl-clang"),
            "CXX": str(
                HEXAGON_TOOLCHAIN_BIN_DIR / "hexagon-unknown-linux-musl-clang++"
            ),
            "LDFLAGS": "-L" + str(HEXAGON_TOOLCHAIN_TARGET_DIR / "lib"),
        },
        inc_dirs=["/usr/include"],
    )


if __name__ == "__main__":
    main()
