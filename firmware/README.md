# INAV Firmware Directory

This directory documents the firmware builds for the STM32F411CEU6 Black Pill.

## Subdirectories

- **`custom-builds/`**: Contains notes and references for the 96 MHz MPU-6050 clone build (`inav_5.1.0_BLACKPILL_QUAD_NO_OVERCLOCK_96MHZ_MPU6050_PB6_PB7.hex`).
- **`official-releases/`**: Upstream INAV releases and targets.

## Critical Flashing Rule:
Always flash the **`96MHZ` build**, NOT an overclocked 108MHz build. Overclocking to 108MHz breaks the 48MHz USB OTG clock divider and freezes serial communication with INAV Configurator.
