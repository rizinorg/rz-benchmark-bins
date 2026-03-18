# SPDX-FileCopyrightText: 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
import subprocess
import os
from pathlib import Path

import platform
import enum


class ToolchainType(enum.Enum):
    Local = 0
    CrossPackaged = 1
    CrossExtern = 2

    def __str__(self) -> str:
        return self.name


class Toolchain:
    def __init__(
        self,
        target_name: str,
        toolchain_type: ToolchainType,
        sysroot: Path | None = None,
        env: dict[str, str] | None = None,
        inc_dirs: list[str] | None = None,
    ):
        self.toolchain_type: ToolchainType = toolchain_type
        self.target_name: str = target_name
        self.sysroot = sysroot

        # The environment to use. Overwrites the process environment.
        self.env = env
        self.inc_dirs = inc_dirs

    def __str__(self):
        return f"{self.target_name} ({self.toolchain_type})"

    def get_disabled_features_binutils(self) -> list[str]:
        return []

    def get_strip(self) -> str:
        if self.target_name == LOCAL_MACHINE:
            return "strip"
        return f"{self.target_name}-strip"

    def is_compatible_binary(self, file: Path) -> bool:
        if not file.is_file() or not os.access(file, os.X_OK):
            return False

        result = subprocess.run(
            ["file", str(file)], capture_output=True, text=True, check=False)

        if (
            result.stdout
            and "ELF" in result.stdout
            and (self.target_name == LOCAL_MACHINE or
            # Cross builds also place binaries of the local architecture in the
            # build directory.
            LOCAL_MACHINE.replace("_", "-").lower() not in result.stdout.lower())
        ):
            return True
        return False

LOCAL_MACHINE = platform.machine()

SUPPORTED_TOOLCHAINS = [
    Toolchain(target_name=f"{LOCAL_MACHINE}", toolchain_type=ToolchainType.Local),
    Toolchain(
        target_name="aarch64-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    ),
    Toolchain(
        target_name="arm-linux-gnueabi", toolchain_type=ToolchainType.CrossPackaged
    ),
    # Toolchain(
    #     target_name="arm-linux-gnueabihf", toolchain_type=ToolchainType.CrossPackaged
    # ),
    Toolchain(target_name="i686-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(
        target_name="mips64el-linux-gnuabi64",
        toolchain_type=ToolchainType.CrossPackaged,
    ),
    # Toolchain(
    #     target_name="mips64-linux-gnuabi64", toolchain_type=ToolchainType.CrossPackaged
    # ),
    # Toolchain(
    #     target_name="mipsel-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    # ),
    # Toolchain(
    #     target_name="mipsisa32r6el-linux-gnu",
    #     toolchain_type=ToolchainType.CrossPackaged,
    # ),
    # Toolchain(
    #     target_name="mipsisa32r6-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    # ),
    # Toolchain(
    #     target_name="mipsisa64r6el-linux-gnuabi64",
    #     toolchain_type=ToolchainType.CrossPackaged,
    # ),
    # Toolchain(
    #     target_name="mipsisa64r6-linux-gnuabi64",
    #     toolchain_type=ToolchainType.CrossPackaged,
    # ),
    Toolchain(target_name="mips-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(
        target_name="powerpc64le-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    ),
    Toolchain(
        target_name="powerpc-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    ),
    Toolchain(
        target_name="riscv64-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    ),
    Toolchain(
        target_name="s390x-linux-gnu", toolchain_type=ToolchainType.CrossPackaged
    ),
]


def get_supported_toolchains():
    import setup_hexagon_toolchain

    tgs = SUPPORTED_TOOLCHAINS.copy()
    if setup_hexagon_toolchain.toolchain_present():
        tgs.append(setup_hexagon_toolchain.get_target())
    return tgs


def get_toolchain_by_name(name: str) -> Toolchain:
    import setup_hexagon_toolchain

    for tc in SUPPORTED_TOOLCHAINS:
        if tc.target_name == name:
            return tc

    if (
        setup_hexagon_toolchain.toolchain_present()
        and setup_hexagon_toolchain.get_target().target_name == name
    ):
        return setup_hexagon_toolchain.get_target()
    raise ValueError(f"Cannot get toolchain '{name}'. It doens't exist.")
