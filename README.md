***Read the README first***  
For Xiaomi 12 (`cupid`) only. The workflow defaults to LineageOS 24.0 / Android 17.
For LineageOS 23.2 / Android 16, explicitly select `lineage-23.2` and `clang-r563880c`.
A successful build is not proof of boot compatibility; keep a matching stock boot image and backups.
How to use:

Fork this repo(remember to sync before using)  
Turn to Actions page in ur repo  
Select clang version (`clang-r596125` for LOS 24 / Android 17; `clang-r547379` for A16 QPR0; `clang-r563880`/`clang-r563880c` for A16 QPR2).
`clang-r596125` (22.0.2) matches the compiler string in the official 20261105 boot image. It is downloaded from AOSP prebuilt revision `29182889399818f97baa65ea238c80e8117981eb`, pinned by that ROM's build manifest; older selections retain the Android 16 QPR2 source.
Select the kernel source code  
Enter the matching kernel branch (`lineage-24.0` for LOS 24, `lineage-23.2` for LOS 23.2; check the source repository for other ROMs).
Select the KernelSU/KernelSU forks that u need(susfs maybe broken, it is controlled by simonpunk)  

## Upgrading from LOS 23.2 to 24.0

- Follow the [official cupid upgrade guide](https://wiki.lineageos.org/devices/cupid/upgrade/), not the first-install/factory-reset procedure.
- Back up important data and the current boot partitions. Do not relock the bootloader.
- Disable root modules before the Android major-version upgrade. Restore them individually only after checking compatibility.
- If GApps is already installed, install **Android 17 ARM64** GApps after the ROM and a reboot to recovery, **before the first Android boot**. Adding/removing GApps requires a factory reset; that is not a data-preserving upgrade.
- The custom kernel does not upgrade Android, firmware, vendor modules, or recovery. Install the matching ROM first; only use this kernel with a compatible ROM.
- The existing BakaSU + SUSFS + BBG + Re-Kernel + DroidSpaces combination remains selectable. These features are not enabled by default.
- Compiler changes use separate ccache keys and compiler-content checking. Build logs record the kernel/modules revisions and compiler version.

For the official `lineage-24.0-20261105-nightly-cupid-signed.zip`, the published build manifest references kernel `eff4b40407a1b6f1b1ab84554cbb540bcb495175` and modules `3b30ba7df6608c97c0ba2d55d679a6b5987c4c66` on `lineage-24.0` (kernel 5.10.269). The old `build.config.common` compiler is not the compiler selection used by LineageOS's full-ROM build. Kernel source branches remain floating: check the logged revisions against your ROM's manifest before flashing a later build.

## Workflow checks

With Python and PyYAML available, run `python -m unittest discover -s tests -v`.
These checks validate defaults, toolchain routing, and cache isolation, not kernel ABI or device bootability. Validate the YAML with `actionlint` and run the actual GitHub Actions build as well.

ksu toolkit:
https://github.com/backslashxx/ksu_toolkit

Inferno's build(ksu ksunext sukisu)
https://github.com/inferno0230/kernel_oneplus_sm8550-CI
Thank contribution from the author of original repo linx3141
