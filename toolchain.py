# SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only

import platform
import enum

class ToolchainType(enum.Enum):
    Local = 0
    CrossPackaged = 1
    CrossExtern = 2

    def __str__(self) -> str:
        return self.name


class Toolchain:
    def __init__(self, name: str, toolchain_type: ToolchainType):
        self.toolchain_type: ToolchainType = toolchain_type
        self.name: str = name

    def __str__(self):
        return f"{self.name} ({self.toolchain_type})"


    def __eq__(self, other):
        if not isinstance(other, str):
            raise ValueError("Cmp failure")
        return self.name == other

LOCAL_MACHINE = platform.machine()

SUPPORTED_TARGETS = [
    Toolchain(name=f"{LOCAL_MACHINE}", toolchain_type=ToolchainType.Local),
    Toolchain(name="aarch64-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="arm-linux-gnueabi", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="arm-linux-gnueabihf", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="i686-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mips64el-linux-gnuabi64", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mips64-linux-gnuabi64", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mipsel-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mipsisa32r6el-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mipsisa32r6-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mipsisa64r6el-linux-gnuabi64", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mipsisa64r6-linux-gnuabi64", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="mips-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="powerpc64le-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="powerpc-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="riscv64-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
    Toolchain(name="s390x-linux-gnu", toolchain_type=ToolchainType.CrossPackaged),
]


def get_supported_targets():
    import setup_hexagon_toolchain
    tgs = SUPPORTED_TARGETS.copy()
    if setup_hexagon_toolchain.toolchain_present():
        tgs.append(setup_hexagon_toolchain.get_target())
    return tgs

