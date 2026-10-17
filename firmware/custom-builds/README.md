# Custom Patched INAV 5.1.0 Firmware

## Target Configuration:
- **Build Target:** `inav_5.1.0_BLACKPILL_QUAD_NO_OVERCLOCK_96MHZ_MPU6050_PB6_PB7`
- **Core Clock:** 96 MHz (Exact 48 MHz USB OTG PLL divider)
- **Primary IMU:** MPU-6050 (accepts both authentic `0x68` and clone `0x98` / `0x70`)
- **I2C Bus:** `PB6` (SCL) and `PB7` (SDA)
- **Motors:** `PB4` (Motor 0), `PB5` (Motor 1), `PB8` (Motor 2), `PB9` (Motor 3)

## How to Apply:
1. Put the Black Pill in DFU mode by holding `BOOT0` and connecting USB.
2. Load the firmware in INAV Configurator and flash with **Full chip erase**.
3. Apply the CLI master backup from `cli-configs/inav_full_backup_20261015.txt`.
