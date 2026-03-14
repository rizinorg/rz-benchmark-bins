#!/usr/bin/env python3

import os
import sys
import hashlib
import shutil
import subprocess
import urllib.request
import tarfile
import argparse
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent.resolve()
SRC_DIR = BASE_DIR / "src"
ARCHIVES_DIR = BASE_DIR / "archives"
TARGETS_DIR = BASE_DIR / "targets"

VERSION = "2.46.0"
BINUTILS_NAME = f"binutils-{VERSION}"
ARCHIVE_NAME = f"{BINUTILS_NAME}.tar.gz"
ARCHIVE_URL = f"https://sourceware.org/pub/binutils/releases/{ARCHIVE_NAME}"
ARCHIVE_SHA256 = "8608fe44ab7de645f6ad0a898313b75338842490d609adb85c9fb2827c376af2"

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

def log(msg):
    print(f"============================")
    print(msg)
    print(f"============================")

def prepare_source():
    """Download and extract binutils source."""
    archive_path = ARCHIVES_DIR / ARCHIVE_NAME
    source_path = SRC_DIR / BINUTILS_NAME

    ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)

    if not archive_path.exists():
        print(f"Downloading {ARCHIVE_NAME}...")
        urllib.request.urlretrieve(ARCHIVE_URL, archive_path)
        with open(archive_path, "rb") as f:
            digest = hashlib.file_digest(f, "sha256")
        if digest.hexdigest() != ARCHIVE_SHA256:
            print("tar archive sha mismatches!")
            print(f"is:       {digest.hexdigest()}")
            print(f"expected: {ARCHIVE_SHA256}")
            exit(-1)

    if not source_path.exists():
        print(f"Extracting {ARCHIVE_NAME}...")
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(SRC_DIR, filter="tar")

def build_target(target):
    """Configure, make, and copy outputs for a specific target."""
    log(f"Building for target: {target}")

    subprocess.run(["make", "clean"], check=False)
    subprocess.run(
        ["find", ".", "-type", "f", "-name", "config.cache", "-delete"],
        check=False
    )

    config_cmd = ["./configure", "--disable-shared"]
    if target != "LOCAL_MACHINE":
        config_cmd.append(f"--host={target}")

    subprocess.run(config_cmd, check=True)
    subprocess.run(["make"], check=True)

    log(f"Build done for {target}")

def copy_executables(target):
    """Copy relevant executables to the target directory."""
    output_dir = TARGETS_DIR / target / BINUTILS_NAME
    output_dir.mkdir(parents=True, exist_ok=True)

    local_arch = os.uname().machine.replace("_", "-").lower()
    binutils_path = Path("./binutils")

    if not binutils_path.exists():
        return

    for f in binutils_path.rglob("*"):
        if not f.is_file() or not os.access(f, os.X_OK):
            continue

        result = subprocess.run(
            ["file", str(f)],
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout and "ELF" in result.stdout and local_arch not in result.stdout.lower():
            print(f"{f} -> {output_dir}")
            shutil.copy(f, output_dir)

    log(f"Build and copy for {target} complete.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", help="Target architecture")
    try:
        args = parser.parse_args()
    except:
        print("\nSupported targets:")
        for t in SUPPORTED_TARGETS:
            print(f"\t{t}")
        sys.exit(0)

    targets = SUPPORTED_TARGETS
    if args.target:
        if args.target not in SUPPORTED_TARGETS:
            print(f"Unsupported target: {args.target}")
            print("Supported targets:")
            for t in SUPPORTED_TARGETS:
                print(t)
            sys.exit(1)
        targets = [args.target]

    prepare_source()

    os.chdir(SRC_DIR / BINUTILS_NAME)
    for target in targets:
        build_target(target)
        copy_executables(target)

if __name__ == "__main__":
    main()
