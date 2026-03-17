#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Rot127 <rot127@posteo.com>
#
# SPDX-License-Identifier: LGPL-3.0-only
from setup_hexagon_toolchain import HEXAGON_TARGET_NAME

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
from toolchain import (
    LOCAL_MACHINE,
    Toolchain,
    get_supported_toolchains,
    get_toolchain_by_name,
)
from helpers import (
    unpack_tar,
    SRC_DIR,
    ARCHIVES_DIR,
    TARGETS_DIR,
    curl_download,
)

VERSION = "2.46.0"
BINUTILS_NAME = f"binutils-{VERSION}"
ARCHIVE_NAME = f"{BINUTILS_NAME}.tar.gz"
ARCHIVE_URL = f"https://sourceware.org/pub/binutils/releases/{ARCHIVE_NAME}"
ARCHIVE_SHA256 = "8608fe44ab7de645f6ad0a898313b75338842490d609adb85c9fb2827c376af2"


def log(msg):
    print("============================")
    print(msg)
    print("============================")


def prepare_source():
    """Download and extract binutils source."""
    archive_path = ARCHIVES_DIR / ARCHIVE_NAME

    ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    curl_download(ARCHIVE_URL, archive_path, ARCHIVE_SHA256)

    src_dir = SRC_DIR / BINUTILS_NAME
    if not src_dir.exists():
        unpack_tar(archive_path, SRC_DIR)


def build_target(toolchain: Toolchain):
    """Configure, make, and copy outputs for a specific target."""
    log(f"Building for target: {toolchain}")

    subprocess.run(["make", "clean"], check=False)
    subprocess.run(
        ["find", ".", "-type", "f", "-name", "config.cache", "-delete"], check=False
    )

    config_cmd = [
        "./configure",
        "--disable-shared",
    ] + toolchain.get_disabled_features_binutils()

    if toolchain.target_name != LOCAL_MACHINE:
        config_cmd.append(f"--host={toolchain.target_name}")

    if toolchain.inc_dirs:
        for d in toolchain.inc_dirs:
            config_cmd.append(f"--includedir={d}")

    if toolchain.env:
        env = toolchain.env
    else:
        env = os.environ

    if toolchain.sysroot:
        if "CFLAGS" not in env:
            env["CFLAGS"] = ""
        env["CFLAGS"] = f"--sysroot={toolchain.sysroot} " + env["CFLAGS"]

    print("\nRun configure")
    env_str = " ".join(f"{k}={v}" for k, v in env.items())
    print(f"{env_str} {' '.join(config_cmd)}")
    print("\n\n")

    subprocess.run(config_cmd, env=env, check=True)
    subprocess.run(["make"], env=env, check=True)

    log(f"Build done for {toolchain}")


def copy_executables(toolchain: Toolchain):
    """Copy relevant executables to the target directory."""
    output_dir = TARGETS_DIR / str(toolchain) / BINUTILS_NAME
    output_dir.mkdir(parents=True, exist_ok=True)

    local_arch = os.uname().machine.replace("_", "-").lower()
    binutils_path = Path("./binutils")

    if not binutils_path.exists():
        return

    for f in binutils_path.rglob("*"):
        if not f.is_file() or not os.access(f, os.X_OK):
            continue

        result = subprocess.run(
            ["file", str(f)], capture_output=True, text=True, check=False
        )

        if (
            result.stdout
            and "ELF" in result.stdout
            and local_arch not in result.stdout.lower()
        ):
            print(f"{f} -> {output_dir}")
            shutil.copy(f, output_dir)

    log(f"Build and copy for {toolchain} complete.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", help="Target architecture")
    parser.add_argument("-l", action="store_true", help="List target toolchains")
    args = parser.parse_args()

    toolchains = get_supported_toolchains()
    if args.l or args.target:
        if args.l or args.target not in [tc.target_name for tc in toolchains]:
            if not args.l:
                print(f"Unsupported target: {args.target}\n")

            print("Supported targets:")
            for t in toolchains:
                print(f"\t{t}")
            sys.exit(1)
        toolchains = [get_toolchain_by_name(args.target)]

    prepare_source()

    os.chdir(SRC_DIR / BINUTILS_NAME)
    for tc in toolchains:
        if tc.target_name in [HEXAGON_TARGET_NAME]:
            print(f"A {tc} build for binutils is broken currently.")
            continue
        build_target(tc)
        copy_executables(tc)


if __name__ == "__main__":
    main()
