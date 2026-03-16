# SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only


class Target:
    def __init__(self, name: str, packaged: bool):
        # Target toolchain is provided by the package manager
        self.packaged: bool = packaged
        self.name: str = name

    def __str__(self):
        return f"{self.name} ({'packaged' if self.packaged else 'extern'})"


    def __eq__(self, other):
        if not isinstance(other, str):
            raise ValueError("Cmp failure")
        return self.name == other


SUPPORTED_TARGETS = [
    Target(name="aarch64-linux-gnu", packaged=True),
    Target(name="arm-linux-gnueabi", packaged=True),
    Target(name="arm-linux-gnueabihf", packaged=True),
    Target(name="i686-linux-gnu", packaged=True),
    Target(name="mips64el-linux-gnuabi64", packaged=True),
    Target(name="mips64-linux-gnuabi64", packaged=True),
    Target(name="mipsel-linux-gnu", packaged=True),
    Target(name="mipsisa32r6el-linux-gnu", packaged=True),
    Target(name="mipsisa32r6-linux-gnu", packaged=True),
    Target(name="mipsisa64r6el-linux-gnuabi64", packaged=True),
    Target(name="mipsisa64r6-linux-gnuabi64", packaged=True),
    Target(name="mips-linux-gnu", packaged=True),
    Target(name="powerpc64le-linux-gnu", packaged=True),
    Target(name="powerpc-linux-gnu", packaged=True),
    Target(name="riscv64-linux-gnu", packaged=True),
    Target(name="s390x-linux-gnu", packaged=True),
    Target(name="LOCAL_MACHINE", packaged=True),
]


def get_supported_targets():
    import setup_hexagon_toolchain
    tgs = SUPPORTED_TARGETS.copy()
    if setup_hexagon_toolchain.toolchain_present():
        tgs.append(setup_hexagon_toolchain.get_target())
    return tgs

