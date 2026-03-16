<!--
SPDX-FileCopyrightText: 2026 2026 Rot127 <rot127@posteo.com>

SPDX-License-Identifier: LGPL-3.0-only
-->

# Rizin's Binary Analysis Benchmark Binaries

This repository contains scripts to build binaries for several different architectures.
The binaries are meant for comparative testing of Rizin's and other
reverse engineering frameworks' binary analysis.

The comparison tool can be found at https://github.com/rizinorg/rz-framework-cmp

## Binary building

Scripts here require a **Debian**.
Simply because it has a good collection out-of-the-box working cross compilers with `libc`.

### Install dependencies

```bash
uv venv
source .venv/bin/activate
uv sync
# Hexagon
sudo apt install musl zstd
```

### Install cross compilers

```bash
sudo apt install crossbuild-essential-* build-essential
./setup_hexagon_toolchain.py
```

### Clean up everything (delete all untracked files)

```
git clean -dfx targets/ src/ archives/
```

### Binutils

```bash
# Help
./build_binutils_variants.py -h
# Builds all
./build_binutils_variants.py
# Builds a single architecuture
./build_binutils_variants.py arm-linux-gnu
# Builds a for the local machine
./build_binutils_variants.py LOCAL_MACHINE
```

