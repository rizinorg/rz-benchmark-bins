<!--
SPDX-FileCopyrightText: 2026 Rot127 <rot127@posteo.com>

SPDX-License-Identifier: LGPL-3.0-only
-->

# Generated with Kagi Assistant.


<hr>

# Test Binaries For Binary Analysis Algorithm
Created at 2026-03-17 18:02:04 UTC

> @ 2026-03-17 18:02:05 UTC
>
> I need to test my binary analysis algorithm I implemented.
> It runs on an intermediate language which lifts several different CPU architectures.
> 
> I need test binaries I can build in several different optimization levels.
> 
> What open source software can you suggest which builds well for all kind of different architectures (even obscure or rare ones like Hexagon or Alpha).
> 
> Please recommend me a few projects I can use for testing.
> From complex to small software, and different kind (software running in userland, kernel, and firmware).
> 
> The tools I build don't need to be the same for each arch. But it would simplify the building script a lot if I can build the same tool for multiple different architectures.

Here are my recommendations organized by complexity and domain, focusing on projects with excellent cross-architecture support:

---

## Small Userland Tools (Easiest to Build)

### **BusyBox / Toybox**
The gold standard for portable multi-call binaries. Both combine many Unix utilities into a single executable.[^5][^6]

- **Architectures**: Virtually any architecture with a C compiler and Linux support
- **Why it's great**: Simple build system, minimal dependencies, produces small binaries perfect for testing
- **Build**: `make CROSS_COMPILE=<prefix>- defconfig && make`

### **zlib**
Extremely portable compression library, pure C with no assembly requirements.[^2]

- **Architectures**: Platform-independent, works on any architecture
- **Why it's great**: Small codebase (~15K lines), no external dependencies, widely tested

### **SQLite**
Single-file database engine, designed for extreme portability.[^4]

- **Architectures**: Any architecture with a C99 compiler
- **Why it's great**: The amalgamation build is a single `sqlite3.c` file, compiles without changes on virtually any platform

---

## C Libraries

### **musl libc**
Lightweight, standards-compliant C library.[^11][^20]

- **Architectures**: x86, x86_64, ARM, AArch64, MIPS (o32/n32/n64), PowerPC, PowerPC64, RISC-V, m68k, MicroBlaze, OpenRISC, s390x, SuperH
- **Why it's great**: Clean codebase, good for understanding libc internals

### **Newlib**
C library specifically designed for embedded systems.[^12][^16]

- **Architectures**: Compiles for virtually any architecture with GCC support
- **Why it's great**: Standard embedded C library, used by many commercial toolchains

---

## Cryptographic Libraries

### **LibTomCrypt**
Modular, portable cryptographic toolkit in pure C.[^15][^19]

- **Architectures**: Any architecture with a C compiler
- **Why it's great**: No assembly, highly modular, good for testing crypto code paths

### **wolfSSL / mbedTLS**
Lightweight TLS libraries designed for embedded systems.[^9][^13]

- **Architectures**: Designed for embedded, works on ARM, MIPS, RISC-V, x86, and many others
- **Why it's great**: Small footprint, configurable features

---

## FFI / Runtime Libraries

### **libffi**
Foreign function interface library with exceptional architecture coverage.[^3][^22]

- **Architectures**: **Alpha**, AArch64, ARM, ARC, AVR32, Blackfin, CSKY, HPPA, IA-64, KVX, LoongArch, **M68K**, **M88K**, Meta, MicroBlaze, MIPS, Moxie, OpenRISC, PowerPC, RISC-V, S390, SuperH, SPARC, TILE-Gx, **VAX**, WASM, x86, Xtensa
- **Why it's great**: One of the most architecture-diverse projects; includes many rare/obscure architectures

---

## Firmware / Bootloaders

### **U-Boot**
Universal bootloader for embedded systems.[^8]

- **Architectures**: **M68000**, ARM, **Blackfin**, MicroBlaze, AArch64, MIPS, **Nios II**, **SuperH**, PowerPC, RISC-V, LoongArch, x86
- **Why it's great**: Real firmware code, supports many board configurations, good for testing boot-stage binaries

### **coreboot**
Open-source firmware replacement.[^10]

- **Architectures**: Primarily x86, some ARM support
- **Why it's great**: Real firmware with complex initialization code

---

## Real-Time Operating Systems

### **Zephyr RTOS**
Modern RTOS with excellent architecture support.[^7]

- **Architectures**: **ARC** (v2/v3), ARM (Cortex-M/A/R), x86, **MIPS**, **Renesas RX**, RISC-V, **SPARC V8**, **Xtensa**
- **Why it's great**: Active development, clean codebase, supports many exotic embedded architectures

### **FreeRTOS**
Market-leading embedded RTOS.[^17][^18]

- **Architectures**: 40+ architectures including ARM, RISC-V, Xtensa, and many microcontroller families
- **Why it's great**: Widely deployed, extensive port library

### **seL4**
Formally verified microkernel.[^14][^21]

- **Architectures**: ARM (Cortex-A), AArch64, RISC-V (32/64-bit), x86, x86_64
- **Why it's great**: High-assurance code, interesting for security-focused analysis

---

## Kernel

### **Linux Kernel**
The most architecture-diverse kernel.[^1]

- **Architectures**: **Alpha**, ARC, ARM, AArch64, AVR, **Hexagon** (user-mode via QEMU), HPPA, LoongArch, **m68k**, MicroBlaze, MIPS, **Nios II**, **OpenRISC**, PowerPC, RISC-V, RX, s390, **SuperH**, SPARC, Tricore, x86, Xtensa
- **Why it's great**: Maximum architecture coverage, can build individual subsystems

---

## For Hexagon Specifically

QEMU supports **Hexagon for user-mode emulation**, which means you can run Hexagon binaries on x86.[^1] The Linux kernel has some Hexagon support, though it's limited. For Hexagon test binaries, you'll likely need the Qualcomm Hexagon SDK.

---

## Recommended Build Strategy

For maximum simplicity with your build scripts, I'd suggest:

| Category | Primary Choice | Reason |
|----------|---------------|--------|
| Small userland | **Toybox** | Single makefile, `CROSS_COMPILE=` support |
| Library | **zlib** + **SQLite** | Pure C, no arch-specific code |
| Crypto | **LibTomCrypt** | No assembly, modular |
| RTOS | **Zephyr** | CMake-based, excellent cross-compile support |
| Firmware | **U-Boot** | Kconfig-based, similar to Linux |
| Kernel | **Linux** | Kconfig, `ARCH=` and `CROSS_COMPILE=` |

All of these support `-O0`, `-O1`, `-O2`, `-O3`, and `-Os` optimization levels through standard compiler flags.


_References_:
[^1]: [Emulation — QEMU documentation](https://www.qemu.org/docs/master/about/emulation.html)
[^2]: [zlib - Wikipedia](https://en.wikipedia.org/wiki/Zlib)
[^3]: [libffi GitHub Repo](https://github.com/libffi/libffi)
[^4]: [Custom Builds Of SQLite or Porting SQLite To New Operating Systems](https://sqlite.org/custombuild.html)
[^5]: [GitHub - landley/toybox: toybox · GitHub](https://github.com/landley/toybox)
[^6]: [Multi-Architecture Support | prometheus/busybox | DeepWiki](https://deepwiki.com/prometheus/busybox/3.3-multi-architecture-support)
[^7]: [Introduction — Zephyr Project Documentation](https://docs.zephyrproject.org/latest/introduction/index.html)
[^8]: [Das U-Boot - Wikipedia](https://en.wikipedia.org/wiki/Das_U-Boot)
[^9]: [wolfSSL Embedded SSL/TLS Library - wolfSSL](https://www.wolfssl.com/)
[^10]: [coreboot - Wikipedia](https://en.wikipedia.org/wiki/Coreboot)
[^11]: [musl libc - Supported Platforms](https://wiki.musl-libc.org/supported-platforms)
[^12]: [Newlib - Wikipedia](https://en.wikipedia.org/wiki/Newlib)
[^13]: [Mbed TLS - Wikipedia](https://en.wikipedia.org/wiki/Mbed_TLS)
[^14]: [Supported platforms | seL4 docs](https://docs.sel4.systems/Hardware/)
[^15]: [LibTomCrypt](https://www.libtom.net/LibTomCrypt/)
[^16]: [The Newlib Homepage - sourceware.org](https://sourceware.org/newlib/)
[^17]: [FreeRTOS™ - FreeRTOS™](https://www.freertos.org/)
[^18]: [FreeRTOS](https://en.wikipedia.org/wiki/FreeRTOS)
[^19]: [GitHub - libtom/libtomcrypt: LibTomCrypt is a fairly comprehensive ...](https://github.com/libtom/libtomcrypt)
[^20]: [musl - Wikipedia](https://en.wikipedia.org/wiki/Musl)
[^21]: [seL4 - Wikipedia](https://en.wikipedia.org/wiki/SeL4)
[^22]: [libffi - Wikipedia](https://en.wikipedia.org/wiki/Libffi)


---

_Generated by [Kagi Assistant](https://kagi.com/assistant)_
