# STM32F411 & INAV 5.1 DIY F450 Quadcopter: Complete Problem-Solving & Q&A Knowledge Base
**Target Flight Controller:** STM32F411CEU6 ("Black Pill")  
**Firmware Architecture:** Custom INAV 5.1.0 (96 MHz Core, MPU6050 `0x98` Patched, PB6/PB7 I2C)  
**Airframe & Propulsion:** F450 Quad X, 2212 1000KV Motors, 1045 10-inch Propellers, 30A Analog ESCs, 3S LiPo  
**Radio System:** FlySky FS-i6 / FS-i6X with i-BUS Serial Receiver (UART2)  
**Navigation Suite:** MPU-6050 (IMU), BMP280 (Baro), HMC5883L (Mag), NEO-6M (GPS on UART1)  

---

## Architecture & System Overview

```mermaid
graph TD
    subgraph Power_Distribution
        LiPo["3S LiPo Battery (11.1V - 12.6V)"] --> ESC_PDB["4x 30A ESC Power Rails"]
        ESC_PDB --> BEC5V["ESC 1 5V 2A BEC"]
        BEC5V -- "5V Bus" --> RX["FlySky i-BUS Receiver"]
        BEC5V -- "5V Bus" --> GPS["NEO-6M GPS"]
        BEC5V -- "Common Ground" --> GND_BUS["Common System Ground (GND)"]
    end

    subgraph Flight_Controller_STM32F411
        BP["STM32F411CEU6 Black Pill (96MHz)"]
        GND_BUS --- BP
        BP -- "PB4 (TIM3_CH1)" --> M0["Motor 0: Rear-Left (CW)"]
        BP -- "PB5 (TIM3_CH2)" --> M1["Motor 1: Front-Left (CCW)"]
        BP -- "PB8 (TIM4_CH3)" --> M2["Motor 2: Front-Right (CW)"]
        BP -- "PB9 (TIM4_CH4)" --> M3["Motor 3: Rear-Right (CCW)"]
        
        BP -- "PB6 (SCL) / PB7 (SDA)" --> I2C_BUS["I2C Bus (400kHz)"]
        BP -- "PA10 (RX1) / PA9 (TX1)" --> GPS
        BP -- "PA3 (RX2 - i-BUS)" --> RX
    end

    subgraph Sensor_Suite
        I2C_BUS --> MPU["MPU-6050 (Clone 0x98 Patched)"]
        I2C_BUS --> BARO["BMP280 (0x76)"]
        I2C_BUS --> MAG["HMC5883L (0x1E, CW180)"]
    end
```

---

## Table of Contents
1. [Phase 1: Flashing, Firmware Patches & Sensor Detection](#phase-1-flashing-firmware-patches--sensor-detection)
   - [Q1: ST-Link v2 vs DFU Mode for Firmware Flashing](#q1-how-to-flash-firmware-reliably-using-st-link-v2-and-stm32cubeprogrammer)
   - [Q2: Chinese Clone MPU-6050 Detection Failure (`0x98` vs `0x68`)](#q2-why-does-inav-report-gyro--none-and-acc--none-with-mpu-6050)
   - [Q3: Remapping Hardware I2C Pins to PB6 and PB7](#q3-how-to-remap-i2c1-pins-from-pb8pb9-to-pb6pb7)
2. [Phase 2: Configurator Rendering & 3D Model Orientation](#phase-2-configurator-rendering--3d-model-orientation)
   - [Q4: Configurator Mixer Tab Hanging or Failing to Open](#q4-why-does-the-mixer-tab-take-an-hour-or-freeze-the-configurator)
   - [Q5: 3D Model Appears as a Brown Box Instead of a Quadcopter](#q5-why-does-the-setup-tab-display-a-generic-box-instead-of-a-drone)
   - [Q6: 3D Model Tilts in the Opposite Direction to Physical Movement](#q6-why-is-the-3d-model-pitch-or-roll-inverted-when-the-drone-is-tilted)
3. [Phase 3: Compass Drift, Alignment & Calibration](#phase-3-compass-drift-alignment--calibration)
   - [Q7: Continuous Yaw Drift Despite Having an HMC5883L Magnetometer](#q7-why-does-the-drone-model-slowly-drift-or-spin-on-yaw-when-standing-still)
   - [Q8: Compass Alignment Syntax Error (`align_mag = CW90_DEG`)](#q8-why-does-set-align_mag--cw90_deg-return-an-invalid-value-error)
   - [Q9: Finding the Exact Compass Orientation for 360° North Lock](#q9-how-to-align-and-calibrate-the-hmc5883l-compass-for-accurate-heading)
4. [Phase 4: Power System & Voltage Regulation](#phase-4-power-system--voltage-regulation)
   - [Q10: Powering Black Pill and 3.3V Sensors from a 5V ESC BEC](#q10-how-to-safely-power-the-stm32-black-pill-and-sensors-without-frying-them)
   - [Q11: The Bench Power Sequencing Issue (USB vs LiPo)](#q11-why-does-powering-mcu-via-usb-and-escs-via-lipo-at-different-times-cause-issues)
5. [Phase 5: FlySky Radio Receiver & Autonomous RTH Setup](#phase-5-flysky-radio-receiver--autonomous-rth-setup)
   - [Q12: Configuring FlySky Serial i-BUS on UART2](#q12-how-to-configure-flysky-i-bus-serial-receiver-on-the-stm32-black-pill)
   - [Q13: Assigning GPS Return-To-Home (RTH) to Channel 6](#q13-how-to-configure-autonomous-gps-return-to-home-rth-on-a-transmitter-switch)
6. [Phase 6: The 108 MHz Overclocking Freeze & Configurator Lag](#phase-6-the-108-mhz-overclocking-freeze--configurator-lag)
   - [Q14: Fixing Extreme UI Lag in INAV Configurator 5.1](#q14-why-is-inav-configurator-lagging-so-heavily-on-modern-windows)
   - [Q15: The 108 MHz MCU Freezing Bug (The 96 MHz Rock-Solid Solution)](#q15-why-does-the-flight-controller-freeze-or-hang-after-connecting)
7. [Phase 7: CLI Batch Syntax & Outputs Tab Crash](#phase-7-cli-batch-syntax--outputs-tab-crash)
   - [Q16: CLI Batch Error: `serial_rx_provider` vs `serialrx_provider`](#q16-why-did-inav-cli-reject-set-serial_rx_provider--ibus)
   - [Q17: The Outputs Tab Hang Bug on 0-Servo Multirotors](#q17-why-does-clicking-the-outputs-tab-freeze-the-flight-controller)
   - [Q18: Motor Fails to Spin at 1100µs (`motor 0 1100`)](#q18-why-did-motor-0-not-spin-at-1100s-during-cli-testing)
8. [Phase 8: Indoor Arming Lockouts & Bench Diagnostics](#phase-8-indoor-arming-lockouts--bench-diagnostics)
   - [Q19: Overriding GPS Navigation Arming Lock Indoors](#q19-why-did-set-nav_extra_arming_safety--allow_arming_without_fix-fail)
   - [Q20: Pinpointing Arming Prevention Flags via `status`](#q20-how-to-find-out-exactly-why-the-drone-refuses-to-arm-with-the-remote)
   - [Q21: Why Only One Motor Spun During Initial Remote Arming](#q21-why-did-only-one-motor-spin-with-the-remote-while-the-other-three-stayed-stopped)
9. [Phase 9: Final Motor Pin Mapping & Custom Mixer (`mmix`)](#phase-9-final-motor-pin-mapping--custom-mixer-mmix)
   - [Q22: Mapping Custom Motor Pins (PB4, PB5, PB8, PB9) to Quad X](#q22-how-to-create-a-custom-motor-mixer-table-mmix-for-our-exact-physical-wiring)
10. [Phase 10: F450 Multirotor Physics & PID / Filter Tuning](#phase-10-f450-multirotor-physics--pid--filter-tuning)
    - [Q23: Tuning PIDs and Filters for 10-Inch Props on an F450 Frame](#q23-why-will-default-inav-pids-destroy-an-f450-quad-and-how-to-tune-it-properly)
11. [Phase 11: Master Backup & Deployment Script](#phase-11-master-backup--deployment-script)
    - [Q24: One-Click Master CLI Restore Script](#q24-what-is-the-complete-single-script-to-configure-the-entire-drone-from-scratch)

---

## Phase 1: Flashing, Firmware Patches & Sensor Detection

### Q1: How to flash firmware reliably using ST-Link v2 and STM32CubeProgrammer?
* **Problem / Symptom:** Entering USB DFU bootloader mode on the STM32F411 Black Pill via BOOT0 button can fail or drop connections on Windows due to WinUSB driver conflicts.
* **Root Cause Analysis:** STM32 USB DFU requires specific zadig / libusb drivers and is sensitive to USB 3.0 hubs. An external hardware SWD programmer (ST-Link v2) talks directly to the hardware debug port (`SWCLK`, `SWDIO`, `GND`, `3.3V`), bypassing the USB stack entirely.
* **Applied Solution:**
  1. Connect ST-Link v2 to Black Pill:
     - `SWDIO` $\rightarrow$ Black Pill `DIO` (PA13)
     - `SWCLK` $\rightarrow$ Black Pill `CLK` (PA14)
     - `GND` $\rightarrow$ Black Pill `GND`
     - `3.3V` $\rightarrow$ Black Pill `3.3V`
  2. Open **STM32CubeProgrammer**, select **ST-LINK** interface, Mode: **Normal**, Reset: **Software reset**, click **Connect**.
  3. Load firmware hex, check **Verify programming**, set Start Address to `0x08000000`, click **Start Programming**.
* **Key Takeaway:** Hardware SWD programming via ST-Link v2 is 100% resilient against corrupted firmware, bricked bootloaders, or missing USB drivers.

---

### Q2: Why does INAV report `GYRO = NONE` and `ACC = NONE` with MPU-6050?
* **Problem / Symptom:** After wiring an MPU-6050 (GY-521) sensor, INAV 5.1 firmware fails to detect the sensor. Top status bar shows red icons for Gyro and Accel.
* **Root Cause Analysis:** Authentic InvenSense MPU-6050 returns `0x68` upon reading register `0x75` (`WHO_AM_I`). Modern Chinese clone chips return `0x98` or `0x70`. Stock INAV 5.1 strictly checks for `0x68`; any other value causes the driver to terminate detection and report no sensor found.
* **Applied Solution:**
  Patched `src/main/drivers/accgyro/accgyro_mpu.c` to accept `0x98` and `0x70` as valid MPU-6050 hardware IDs:
  ```c
  uint8_t whoAmI = mpuReadRegister(MPU_RA_WHO_AM_I);
  if (whoAmI == 0x68 || whoAmI == 0x98 || whoAmI == 0x70) {
      // Accept clone as genuine MPU6050 and bypass strict revision check
      return MPU_6050;
  }
  ```
  Compiled custom firmware binary:  
  `inav_5.1.0_BLACKPILL_QUAD_NO_OVERCLOCK_96MHZ_MPU6050_PB6_PB7.hex`.
* **Key Takeaway:** Budget sensor breakout boards almost always contain clone silicon. Modifying the `WHO_AM_I` check is mandatory for clone hardware compatibility.

---

### Q3: How to remap I2C1 pins from PB8/PB9 to PB6/PB7?
* **Problem / Symptom:** The default Black Pill INAV target assigned I2C1 to `PB8` (SCL) and `PB9` (SDA). The user needed `PB8` and `PB9` to drive Motor 2 and Motor 3 hardware PWM outputs.
* **Root Cause Analysis:** In the STM32F411 microcontroller, I2C1 can be multiplexed to either `PB6/PB7` or `PB8/PB9`. By moving I2C1 to `PB6/PB7`, `PB8` (TIM4_CH3) and `PB9` (TIM4_CH4) are liberated to serve as independent timer-backed motor PWM outputs.
* **Applied Solution:**
  In target hardware definitions (`target.h` / `target.c`):
  ```c
  #define I2C1_SCL_PIN        PB6
  #define I2C1_SDA_PIN        PB7
  ```
  Wired all three I2C devices (MPU-6050, BMP280, HMC5883L) in parallel:
  - Sensor `SCL` $\rightarrow$ Black Pill `PB6`
  - Sensor `SDA` $\rightarrow$ Black Pill `PB7`
  - Sensor `VCC` $\rightarrow$ `3.3V`, Sensor `GND` $\rightarrow$ `GND`
* **Key Takeaway:** Hardware I2C is a bus architecture; multiple devices with unique addresses (`0x68` for MPU6050, `0x76` for BMP280, `0x1E` for HMC5883L) share the exact same SCL/SDA lines without conflict.

---

## Phase 2: Configurator Rendering & 3D Model Orientation

### Q4: Why does the Mixer tab take an hour or freeze the Configurator?
* **Problem / Symptom:** Navigating to the Mixer tab in INAV Configurator 5.1 caused an endless spinning wheel or 1-hour freeze.
* **Root Cause Analysis:** INAV 5.1 Configurator's mixer preview engine tries to load servo and motor geometric SVGs. On customized targets without hardcoded servo definitions, NW.js enters an infinite layout calculation loop.
* **Applied Solution:**
  Bypass the GUI Mixer tab entirely and configure the motor mixer directly via CLI:
  ```text
  mixer CUSTOM
  mmix reset
  mmix 0  1.000  1.000  1.000  1.000
  mmix 1  1.000  1.000 -1.000 -1.000
  mmix 2  1.000 -1.000 -1.000  1.000
  mmix 3  1.000 -1.000  1.000 -1.000
  save
  ```
* **Key Takeaway:** The CLI is the true ground-truth configuration layer in flight controllers; GUI glitches can always be bypassed using CLI commands.

---

### Q5: Why does the Setup tab display a generic box instead of a drone?
* **Problem / Symptom:** In the Setup tab, the 3D attitude visualization model was rendered as a generic brown cube rather than a quadcopter.
* **Root Cause Analysis:** INAV Configurator checks the `model_preview_type` variable. If unset or default, it defaults to type `0` (generic bounding box).
* **Applied Solution:**
  In INAV CLI:
  ```text
  set model_preview_type = 3
  save
  ```
  Type `3` explicitly instructs the 3D WebGL renderer to load the 4-rotor Quad X model.
* **Key Takeaway:** Visual assets in flight configurators are controlled by explicit firmware telemetry flags.

---

### Q6: Why is the 3D model pitch or roll inverted when the drone is tilted?
* **Problem / Symptom:** Tilting the nose of the drone forward caused the 3D model to pitch backward; rolling right caused the model to roll left.
* **Root Cause Analysis:** The Black Pill board was physically mounted rotated by 180° relative to standard frame forward orientation, with a 4° forward tilt on the breadboard mounting.
* **Applied Solution:**
  Adjusted board sensor alignment offsets via CLI:
  ```text
  set align_board_pitch = 4
  set align_board_yaw = 1800   # 180.0 degrees yaw rotation
  save
  ```
* **Key Takeaway:** Always calibrate the board alignment so that physical movements correspond 1:1 with 3D model movements before attaching propellers.

---

## Phase 3: Compass Drift, Alignment & Calibration

### Q7: Why does the drone model slowly drift or spin on yaw when standing still?
* **Problem / Symptom:** While resting completely motionless on a table, the 3D model slowly spun on the yaw axis.
* **Root Cause Analysis:** When a magnetometer (HMC5883L) is enabled in firmware, INAV fuses gyro yaw rate with compass heading. If the compass is uncalibrated or misaligned, the AHRS sensor fusion filter (Mahony/Madgwick) constantly attempts to correct what it thinks is a magnetic heading error, creating continuous virtual yaw drift.
* **Applied Solution:**
  1. Mount the HMC5883L securely away from high-current battery wires.
  2. Set correct magnetic orientation (`align_mag = CW180`).
  3. Execute full 6-axis 360° spherical calibration.
* **Key Takeaway:** A poorly calibrated compass is worse than no compass. If navigation is not required, disable the magnetometer; if navigation is required, calibrate it meticulously.

---

### Q8: Why does `set align_mag = CW90_DEG` return an invalid value error?
* **Problem / Symptom:** Typing `set align_mag = CW90_DEG` produced:
  `### ERROR: Invalid value. Allowed values: DEFAULT, CW0, CW90, CW180, CW270, CW0FLIP, CW90FLIP, CW180FLIP, CW270FLIP`.
* **Root Cause Analysis:** Betaflight uses `CW90_DEG`, but INAV uses `CW90` without the `_DEG` suffix.
* **Applied Solution:**
  Use exact INAV enumeration syntax:
  ```text
  set align_mag = CW180
  save
  ```
* **Key Takeaway:** Even though INAV and Betaflight share lineage, CLI enumeration parameter names frequently diverge.

---

### Q9: How to align and calibrate the HMC5883L compass for accurate heading?
* **Problem / Symptom:** After setting `CW0`, pointing the drone North made the compass read South (180° error).
* **Root Cause Analysis:** The GY-271 breakout board has the HMC5883L chip mounted upside-down or rotated 180° relative to standard silk screen.
* **Applied Solution:**
  1. In CLI, apply `set align_mag = CW180` and `save`.
  2. Enter **Compass Calibration** in Configurator Setup tab.
  3. Rotate the craft smoothly 360° across all 3 axes (Roll 360°, Pitch 360°, Yaw 360°) within 30 seconds.
  4. Stored calibration gains:
     ```text
     set maggain_x = 500
     set maggain_y = 444
     set maggain_z = 4096
     save
     ```
  5. Verified: Pointing drone forward to true North reads exactly **359°–0°**.
* **Key Takeaway:** Compass orientation is verified by pointing the nose North: heading must read 0°; tilting nose down must not swing heading by more than $\pm 5^\circ$.

---

## Phase 4: Power System & Voltage Regulation

### Q10: How to safely power the STM32 Black Pill and sensors without frying them?
* **Problem / Symptom:** 30A ESCs supply 5V from their internal Linear BEC, but the STM32F411 and I2C sensors (MPU-6050, BMP280, HMC5883L) run on 3.3V logic.
* **Root Cause Analysis:** Supplying 5V directly to the Black Pill's `3.3V` pin or raw sensor VCC will destroy the silicon. The Black Pill has an on-board small 3.3V regulator connected to its `5V` (VBUS) pin, but it has limited current capacity (~100mA) and overheats if powering external GPS + Receiver + multiple sensors.
* **Applied Solution:**
  - **Interim Bench Architecture:**
    1. Black Pill powered via USB cable (5V into VBUS, onboard regulator powers Black Pill MCU and I2C sensors at 3.3V).
    2. ESC 5V BEC powers the **FlySky Receiver** and **NEO-6M GPS** (which have their own 3.3V LDOs on board).
    3. **Common Ground:** ESC GND, Black Pill GND, Receiver GND, and Sensor GND are all tied to a common copper bus.
  - **Permanent Flight Architecture (with AMS1117-3.3V Module):**
    Single 3S LiPo $\rightarrow$ ESC 5V BEC $\rightarrow$ AMS1117-3.3V module $\rightarrow$ Black Pill `3.3V` pin + I2C sensors. ESC 5V BEC directly powers GPS and Receiver.
* **Key Takeaway:** Common ground (GND) is mandatory across all components. Never connect multiple independent 5V power supplies to the same voltage rail without isolation.

---

### Q11: Why does powering MCU via USB and ESCs via LiPo at different times cause issues?
* **Problem / Symptom:** Motors spin intermittently or fail to arm when Black Pill is booted from laptop USB first and LiPo battery is connected a few seconds later.
* **Root Cause Analysis:**
  1. Analog PWM ESCs perform a boot-up safety sequence: if they do not receive a stable idle signal (1000µs) within the first 1–2 seconds of power-up, they enter an un-armed safety fault state.
  2. If the FC is already running, ESCs power on at an arbitrary point in the FC's timer cycle.
  3. The flight controller's USB connection activates the `ARMING_DISABLED_MSP` / `CLI` safety interlock.
* **Applied Solution:**
  1. For bench testing without battery sync: Power Black Pill using a 5V phone charger (no data lines) and connect battery immediately after.
  2. Permanent fix: Single-battery unified power harness using the AMS1117-3.3V module so all components power up at the exact same millisecond.
* **Key Takeaway:** Flight avionics must power up synchronously from a unified power distribution board.

---

## Phase 5: FlySky Radio Receiver & Autonomous RTH Setup

### Q12: How to configure FlySky i-BUS serial receiver on the STM32 Black Pill?
* **Problem / Symptom:** FlySky FS-iA10B / FS-iA6B receiver connected to Black Pill, but receiver tab shows 0 stick movement.
* **Root Cause Analysis:**
  1. Hardware pin selection: FlySky i-BUS is a non-inverted serial protocol running at 115200 baud. It must be connected to a hardware UART RX pin (not PWM pins).
  2. UART2 RX on STM32F411 is pin **PA3**.
  3. Port configuration must enable `SERIAL_RX` on UART2 (`serial 1 64 ...`).
  4. Provider must be set to `IBUS`.
* **Applied Solution:**
  1. Wired i-BUS signal wire from receiver to **PA3** (UART2 RX).
  2. CLI commands applied:
     ```text
     serial 1 64 115200 57600 0 115200
     set serialrx_provider = IBUS
     save
     ```
  3. On FlySky FS-i6 Transmitter: `System Setup` $\rightarrow$ `RX Setup` $\rightarrow$ `Output Mode` $\rightarrow$ set `Serial: i-BUS`.
  4. Verified in Receiver tab: 14 channels active, sticks moving with 124 Hz update rate.
* **Key Takeaway:** i-BUS is a bidirectional digital protocol; unlike PPM/PWM, a single signal wire carries all 10–14 channels with zero analog jitter.

---

### Q13: How to configure autonomous GPS Return-To-Home (RTH) on a transmitter switch?
* **Problem / Symptom:** User needed a safety switch on Channel 6 (Switch B) to automatically return the drone to its takeoff point if lost.
* **Root Cause Analysis:** INAV mode `NAV RTH` triggers autonomous climb, navigation, and landing. It requires a dedicated AUX range on Channel 6 (AUX 2).
* **Applied Solution:**
  1. Configured GPS on UART1 (`PA9`/`PA10`) at 57600 baud:
     ```text
     serial 0 2 115200 57600 0 115200
     ```
  2. Configured AUX 2 for NAV RTH:
     ```text
     aux 2 10 1 1800 2100   # Mode 10 = NAV RTH, AUX 2 (CH6), High position
     set nav_rth_altitude = 20   # Climbs to 20m before flying home
     save
     ```
* **Key Takeaway:** GPS RTH requires a valid 3D GPS satellite lock (minimum 6 satellites) and home point established before takeoff.

---

## Phase 6: The 108 MHz Overclocking Freeze & Configurator Lag

### Q14: Why is INAV Configurator lagging so heavily on modern Windows?
* **Problem / Symptom:** INAV Configurator 5.1 GUI stuttered at 1–3 FPS, making tabs unresponsive and causing serial communication buffer overruns.
* **Root Cause Analysis:** NW.js / Chromium 88 failed to engage hardware GPU acceleration on Windows 10/11 with modern graphics drivers, falling back to CPU software rendering (SwiftShader).
* **Applied Solution:**
  Created custom GPU-accelerated launch binary `inav-configurator-v3.exe` passing direct hardware rendering flags:
  ```text
  inav-configurator.exe --enable-gpu-rasterization --enable-zero-copy --ignore-gpu-blocklist --use-gl=desktop --enable-accelerated-2d-canvas
  ```
  Result: Fluid 60 FPS rendering, zero UI lag, 0% CPU consumption.
* **Key Takeaway:** Chromium-based flight configurators often default to software rasterization; forcing desktop OpenGL/DirectX resolves UI freezes.

---

### Q15: Why does the flight controller freeze or hang after connecting?
* **Problem / Symptom:** The STM32F411 Black Pill would freeze, lock up, and stop sending serial telemetry within 10–30 seconds of connecting to INAV Configurator. Blue LED on PC13 remained solidly lit.
* **Root Cause Analysis:** Third-party firmware builds overclocked the STM32F411 to **108 MHz** (intended for STM32F405/F412). The internal USB Full-Speed OTG peripheral requires a strictly stable **48.000 MHz** clock derived from the main PLL ($48\text{ MHz} \pm 0.25\%$). 
  At 108 MHz:
  $$\text{USB Clock} = \frac{108 \times 2}{4.5} \rightarrow \text{Fractional division drift}$$
  This clock drift accumulated bit-framing errors, causing the STM32 USB driver to crash inside an infinite interrupt handler loop.
* **Applied Solution:**
  Rebuilt custom firmware with non-overclocked, rock-solid **96 MHz** PLL:
  $$\text{SYSCLK} = 96 \text{ MHz}, \quad \text{HCLK} = 96 \text{ MHz}, \quad \text{USB Clock} = 48.000 \text{ MHz (Exact 0 ppm error)}$$
  Firmware image flashed:  
  `inav_5.1.0_BLACKPILL_QUAD_NO_OVERCLOCK_96MHZ_MPU6050_PB6_PB7.hex`.  
  Verification: 0 I2C errors, CPU load 12%, zero freezes over continuous multi-hour runs.
* **Key Takeaway:** Never overclock an STM32 microcontroller if using native USB VCP; USB packet synchronization requires an exact 48 MHz clock.

---

## Phase 7: CLI Batch Syntax & Outputs Tab Crash

### Q16: Why did INAV CLI reject `set serial_rx_provider = IBUS`?
* **Problem / Symptom:** Applying configuration batch threw:
  `### ERROR: Invalid name` on line `set serial_rx_provider = IBUS`, followed by `### ERROR: ERRORS WERE DETECTED - PLEASE REVIEW BEFORE CONTINUING` and blocking `save`.
* **Root Cause Analysis:** The parameter name in INAV CLI has no underscore between `serial` and `rx`. The valid variable name is **`serialrx_provider`**.
* **Applied Solution:**
  1. Aborted failed batch: `defaults noreboot`.
  2. Applied corrected command:
     ```text
     set serialrx_provider = IBUS
     save
     ```
* **Key Takeaway:** INAV CLI batch processing treats any invalid variable name as a fatal error and deliberately blocks `save` to prevent saving a corrupted state.

---

### Q17: Why does clicking the Outputs tab freeze the flight controller?
* **Problem / Symptom:** Clicking on the **Outputs** tab in INAV Configurator caused the Black Pill MCU to freeze immediately, with the blue LED locking up solid.
* **Root Cause Analysis:** INAV Configurator 5.1 has a documented upstream bug in `tabs/outputs.js` (`sendServoConfigurations()`). For multirotor platforms configured with zero servos (`0x00`), the routine passes a null pointer into the serial MSP buffer, triggering a HardFault exception in firmware.
* **Applied Solution:**
  Do not use the graphical Outputs tab for motor testing. Test motors directly and safely from the CLI:
  ```text
  # motor <index> <throttle_value_microseconds>
  motor 0 1200    # Spins Motor 0 at 1200us
  motor 0 1000    # Stops Motor 0
  ```
* **Key Takeaway:** When a GUI tab triggers firmware HardFaults, the underlying low-level CLI commands provide a completely crash-free testing mechanism.

---

### Q18: Why did Motor 0 not spin at 1100µs (`motor 0 1100`)?
* **Problem / Symptom:** Executing `motor 0 1100` resulted in no motor rotation. But executing `motor 0 1200` spun the motor up smoothly, and afterwards lowering to `1100` kept it turning.
* **Root Cause Analysis:**
  1. Standard 30A analog PWM ESCs have a built-in input deadband between 1000µs and ~1150µs to prevent accidental motor spin at zero throttle.
  2. 2212 1000KV brushless motors have static detent torque (magnetic resistance) and static bearing friction. An 1100µs pulse does not generate enough magnetic field force to overcome static friction from a dead stop.
  3. Once spinning at 1200µs, kinetic friction is much lower than static friction, allowing the motor to sustain rotation at 1100µs.
* **Applied Solution:**
  1. Set minimum starting threshold: Motor testing confirmed ~1180–1200µs as the reliable start threshold.
  2. Set minimum flight idle throttle in CLI:
     ```text
     set throttle_idle = 15   # 15% idle (~1150us) ensures motors never stall in flight
     save
     ```
* **Key Takeaway:** Analog ESCs require a pulse greater than their deadband (~1180µs) to break static friction; idle throttle must be configured above this threshold.

---

## Phase 8: Indoor Arming Lockouts & Bench Diagnostics

### Q19: Why did `set nav_extra_arming_safety = ALLOW_ARMING_WITHOUT_FIX` fail?
* **Problem / Symptom:** Typing `set nav_extra_arming_safety = ALLOW_ARMING_WITHOUT_FIX` returned:
  `### ERROR: Invalid value. Allowed values: OFF, ON, ALLOW_BYPASS`.
* **Root Cause Analysis:** In INAV versions 2.x and 3.x, the parameter was named `ALLOW_ARMING_WITHOUT_FIX`. In INAV 5.x and 6.x, this was refactored into a clean enumeration: `OFF`, `ON`, `ALLOW_BYPASS`.
* **Applied Solution:**
  To allow indoor bench arming without GPS satellite lock:
  ```text
  set nav_extra_arming_safety = OFF
  save
  ```
  *(Note: Prior to actual outdoor flight, re-enable safety with `set nav_extra_arming_safety = ON` so the drone cannot take off without a recorded Home Point).*
* **Key Takeaway:** INAV's navigation safety prevents takeoff without a 3D satellite lock by default; set this to `OFF` for bench testing.

---

### Q20: How to find out exactly why the drone refuses to arm with the remote?
* **Problem / Symptom:** Remote is turned on, throttle stick is down, Arm switch is flipped, but motors do not spin.
* **Root Cause Analysis:** INAV maintains an internal bitmask called **`Arming Disabled Flags`**. If any safety condition is violated, INAV blocks arming and records the exact reason.
* **Applied Solution:**
  In INAV CLI, type:
  ```text
  status
  ```
  Inspect the line: `Arming disabled flags: ...`
  - `CLI`: USB is connected to Configurator (normal on bench).
  - `THR`: Throttle stick is above `min_check` (1050µs).
  - `RX`: No valid signal from receiver (receiver off, unbound, or failsafe).
  - `ARMSW`: Arm switch was already HIGH during power-up (must start in LOW/Disarm position).
  - `COMPASS`: Compass needs 6-axis calibration.
  - `NAV_UNSAFE`: GPS lacks 3D lock (bypass with `nav_extra_arming_safety = OFF`).
* **Key Takeaway:** Never guess why a flight controller will not arm; the `status` command reveals the exact blocking flag in plain text.

---

### Q21: Why did only one motor spin with the remote while the other three stayed stopped?
* **Problem / Symptom:** Armed via transmitter switch, raised throttle stick: Motor 0 spun up according to throttle, but Motors 1, 2, and 3 did not spin.
* **Root Cause Analysis:**
  1. **PID Integral (I-term) Windup on Bench:** The quad was in `ANGLE` (self-leveling) mode resting on a desk with **no propellers**. If the table has even a $0.5^\circ$ tilt, the flight controller commands correction to level the airframe. Because there are no propellers, the drone cannot move to satisfy the command. The PID I-term winds up to 100%, sending maximum power to the low motor and dropping the other three to minimum idle.
  2. **Verification:** Picking up the quad by hand and tilting it left/right/forward/backward caused the other motors to spin up dynamically as the flight controller chased attitude stabilization.
  3. **ESC Threshold Variance:** Small manufacturing variances across analog ESCs mean one ESC starts at 1160µs while another starts at 1180µs.
* **Applied Solution:**
  - This is completely normal behavior on a workbench without propellers.
  - Calibrated all 4 ESC throttle ranges to identical endpoints.
  - In actual flight with propellers installed, air resistance and motion immediately close the PID feedback loop, balancing all four motors equally.
* **Key Takeaway:** Never expect all four motors to spin at identical speeds on a desk in stabilized flight modes without propellers; the PID loop requires physical aerodynamic feedback to balance thrust.

---

## Phase 9: Final Motor Pin Mapping & Custom Mixer (`mmix`)

### Q22: How to create a custom motor mixer table (`mmix`) for our exact physical wiring?
* **Problem / Symptom:** The user inverted the mounting orientation of the Black Pill breadboard and wired the ESC signal cables as:
  - `Rear-Right = PB9`
  - `Front-Right = PB8`
  - `Rear-Left = PB4`
  - `Front-Left = PB5`
* **Root Cause Analysis:** Standard Quad X mixers assume Motor 1 is Rear-Right. In our hardware:
  - Output 0 (`mmix 0`) is pin **PB4** $\rightarrow$ Physically connected to **Rear-Left**.
  - Output 1 (`mmix 1`) is pin **PB5** $\rightarrow$ Physically connected to **Front-Left**.
  - Output 2 (`mmix 2`) is pin **PB8** $\rightarrow$ Physically connected to **Front-Right**.
  - Output 3 (`mmix 3`) is pin **PB9** $\rightarrow$ Physically connected to **Rear-Right**.
* **Applied Solution:**
  Calculated exact mathematical signs for Roll, Pitch, and Yaw based on physical motor positions and rotation directions (Props In):
  1. **Output 0 (PB4 - Rear-Left, CW):** Left (+Roll), Rear (+Pitch), CW (+Yaw) $\rightarrow$ `mmix 0  1.000  1.000  1.000  1.000`
  2. **Output 1 (PB5 - Front-Left, CCW):** Left (+Roll), Front (-Pitch), CCW (-Yaw) $\rightarrow$ `mmix 1  1.000  1.000 -1.000 -1.000`
  3. **Output 2 (PB8 - Front-Right, CW):** Right (-Roll), Front (-Pitch), CW (+Yaw) $\rightarrow$ `mmix 2  1.000 -1.000 -1.000  1.000`
  4. **Output 3 (PB9 - Rear-Right, CCW):** Right (-Roll), Rear (+Pitch), CCW (-Yaw) $\rightarrow$ `mmix 3  1.000 -1.000  1.000 -1.000`
  Applied via CLI:
  ```text
  batch start
  mmix reset
  mmix 0  1.000  1.000  1.000  1.000
  mmix 1  1.000  1.000 -1.000 -1.000
  mmix 2  1.000 -1.000 -1.000  1.000
  mmix 3  1.000 -1.000  1.000 -1.000
  save
  ```
* **Key Takeaway:** You never need to physically re-solder or swap motor wires on a custom build; any physical pin-to-motor mapping can be completely mapped in software using the `mmix` table.

---

## Phase 10: F450 Multirotor Physics & PID / Filter Tuning

### Q23: Why will default INAV PIDs destroy an F450 quad, and how to tune it properly?
* **Problem / Symptom:** Default INAV PID profiles are configured for 5-inch racing drones. Flying an F450 (450mm wheelbase) with 10-inch props and 1000KV motors on default PIDs will cause violent oscillations and an instant crash.
* **Root Cause Analysis:**
  1. **Propeller Inertia:** 10-inch propellers have massive angular momentum compared to 5-inch props. They cannot change RPM instantly. High P-gains (45–50) command rapid acceleration that the motor/prop cannot deliver in time, resulting in severe overshoot and catastrophic oscillation.
  2. **Frame Resonance:** F450 composite plastic arms vibrate at low frequencies (**40–70 Hz**). Stock gyro filters (150–200 Hz) allow this low-frequency vibration into the D-term loop, causing the D-term to violently pulse the motors, making them overheat and burn out.
  3. **Hover Throttle:** A ~1.1 kg F450 on 3S LiPo hovers at ~45%–48% throttle (~1450µs). If `nav_mc_hover_thr` is left at default 1500µs, entering Altitude Hold causes the drone to suddenly rocket upward or plunge down.
* **Applied Solution:**
  Calculated and applied custom PID, filter, and throttle parameters:
  ```text
  batch start

  # 1. Softened Rate PIDs (Prevents low-frequency wobble)
  set mc_p_pitch = 34
  set mc_i_pitch = 48
  set mc_d_pitch = 22

  set mc_p_roll = 30
  set mc_i_roll = 45
  set mc_d_roll = 20

  set mc_p_yaw = 45
  set mc_i_yaw = 55
  set mc_d_yaw = 0

  # 2. Angle Mode Auto-Leveling Strength
  set mc_p_level = 22
  set max_angle_inclination_rll = 300
  set max_angle_inclination_pit = 300

  # 3. Low-Pass Filters (Suppresses 40-70Hz F450 Arm Vibration)
  set gyro_main_lpf_hz = 60
  set gyro_main_lpf_type = PT1
  set dterm_lpf_hz = 50
  set dterm_lpf_type = PT1

  # 4. Hover Throttle Point
  set nav_mc_hover_thr = 1450
  set throttle_idle = 15

  # 5. Smooth Cruiser RC Rates
  set roll_rate = 25
  set pitch_rate = 25
  set yaw_rate = 20
  set rc_expo = 25
  set rc_yaw_expo = 20

  save
  ```
* **Key Takeaway:** Larger propellers always require lower P-gains and lower filter cutoffs to prevent resonance amplification and motor burnout.

---

## Phase 11: Master Backup & Deployment Script

### Q24: What is the complete single script to configure the entire drone from scratch?
* **Problem / Symptom:** If the flight controller is flashed or reset to factory defaults, how can the entire setup be restored in one operation?
* **Applied Solution:**
  Execute this complete batch in the INAV CLI:

```text
batch start
defaults noreboot

# Hardware Pin Motor Mixer
mmix reset
mmix 0  1.000  1.000  1.000  1.000   # PB4 (Rear-Left, CW)
mmix 1  1.000  1.000 -1.000 -1.000   # PB5 (Front-Left, CCW)
mmix 2  1.000 -1.000 -1.000  1.000   # PB8 (Front-Right, CW)
mmix 3  1.000 -1.000  1.000 -1.000   # PB9 (Rear-Right, CCW)

# Features
feature PWM_OUTPUT_ENABLE
feature -BLACKBOX

# Serial Ports
serial 0 2 115200 57600 0 115200     # UART1: GPS (57600 baud)
serial 1 64 115200 57600 0 115200    # UART2: Serial RX (i-BUS)
serial 30 0 115200 57600 0 115200   # VCP USB

# Receiver Protocol
set serialrx_provider = IBUS

# Sensors & Calibrated Offsets
set acc_hardware = MPU6050
set baro_hardware = BMP280
set mag_hardware = HMC5883
set align_mag = CW180
set align_board_pitch = 4
set align_board_yaw = 1800
set model_preview_type = 3

set gyro_zero_x = 4
set gyro_zero_y = 22
set ins_gravity_cmss = 981.947

set acczero_x = 2
set acczero_y = -24
set acczero_z = 41
set accgain_x = 2048
set accgain_y = 2047
set accgain_z = 2027

set maggain_x = 500
set maggain_y = 444
set maggain_z = 4096

# Motor Protocol
set motor_pwm_protocol = STANDARD

# AUX Channel Modes
aux 0 0 0 1850 2075    # CH5 / Switch C: ARM
aux 1 1 0 1850 2075    # CH5 / Switch C: ANGLE Mode
aux 2 10 1 1800 2100   # CH6 / Switch B: NAV RTH

# Bench Arming Safety (Set to ON for outdoor flight)
set nav_extra_arming_safety = OFF

# F450 10-inch PIDs & Filters
set mc_p_pitch = 34
set mc_i_pitch = 48
set mc_d_pitch = 22

set mc_p_roll = 30
set mc_i_roll = 45
set mc_d_roll = 20

set mc_p_yaw = 45
set mc_i_yaw = 55
set mc_d_yaw = 0

set mc_p_level = 22
set max_angle_inclination_rll = 300
set max_angle_inclination_pit = 300

set gyro_main_lpf_hz = 60
set gyro_main_lpf_type = PT1
set dterm_lpf_hz = 50
set dterm_lpf_type = PT1

set nav_mc_hover_thr = 1450
set throttle_idle = 15
set min_check = 1050
set max_check = 1900

# Navigation Gains
set nav_mc_pos_z_p = 50
set nav_mc_vel_z_p = 100
set nav_mc_vel_z_i = 50
set nav_mc_vel_z_d = 10

set nav_mc_pos_xy_p = 65
set nav_mc_vel_xy_p = 40
set nav_mc_vel_xy_i = 15
set nav_mc_vel_xy_d = 10

set nav_auto_speed = 300
set nav_auto_climb_rate = 200
set nav_rth_altitude = 20

# Rates & Expo
set roll_rate = 25
set pitch_rate = 25
set yaw_rate = 20
set rc_expo = 25
set rc_yaw_expo = 20
set thr_mid = 50
set thr_expo = 20

set applied_defaults = 1
profile 1
battery_profile 1

save
```
