# INAV CLI Configuration Scripts

This directory contains the verified CLI scripts for the F450 quadcopter running INAV 5.1.0 on STM32F411 Black Pill.

## Files Description

- **`inav_full_backup_20261015.txt`**: Complete master configuration dump. Restores all motor mixers, serial ports, sensor hardware definitions, and flight modes in a single paste.
- **`inav_f450_tuning_3s_10inch.txt`**: Dedicated PID and filter tuning batch. Contains the physics-calculated gains for 1045 propellers on an F450 frame with a 3S LiPo battery.
- **`INAV_5.1.0_cli_20261015_231349.txt`**: Raw unformatted backup from initial bench testing.

## How to Apply:
1. Connect to the board in **INAV Configurator** and open the **CLI** tab.
2. Open `inav_full_backup_20261015.txt`, copy all contents, and paste into the CLI prompt.
3. Press **Enter**, type `save`, and press **Enter**.
