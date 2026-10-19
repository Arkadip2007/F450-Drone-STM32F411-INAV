# 📸 Visual Documentation, Telemetry Screenshots & Hardware Gallery (INAV)

This directory hosts high-resolution screenshots, configurator verification captures, physical drone hardware photos, and pinout diagrams from the physical bench configuration and flight preparation of the **F450 STM32F411 Black Pill INAV Drone**.

---

## 🖼️ Gallery of Images & Tab Explanations

### A. INAV Configurator Telemetry & Navigation

#### 1. [Setup Tab & 3D Quad-X Model Preview](inav-setup-3d-model.png)
- **File:** `inav-setup-3d-model.png`
- **Configurator Tab:** `Setup`
- **What is verified:**
  - Real-time 3D Quad-X airframe rendering tracking physical board movements.
  - Heading angle, Roll/Pitch orientation values.
  - Top telemetry bar showing green status flags for Gyro, Accelerometer, Magnetometer, Barometer, and GPS.
  - Arming flag status and system health.

#### 2. [6-Point Accelerometer Calibration](inav-calibration-6point.png)
- **File:** `inav-calibration-6point.png`
- **Configurator Tab:** `Calibration`
- **What is verified:**
  - INAV's rigorous 6-step accelerometer orientation calibration (Top, Left, Right, Nose Up, Nose Down, Bottom).
  - Calibration gain and offset registers stored in non-volatile flash memory to ensure stable GPS hold, automatic Return-to-Home, and level hover without spatial drift.

#### 3. [UART & Ports Configuration](inav-ports-uart-config.png)
- **File:** `inav-ports-uart-config.png`
- **Configurator Tab:** `Ports`
- **What is verified:**
  - **USB VCP**: MSP protocol enabled for GUI communication at 115200 baud.
  - **UART1 (PA9/PA10)**: Configured for GPS module at 57600 baud with UBLOX protocol.
  - **UART2 (PA3)**: Configured for Serial RX (FlySky i-BUS receiver) with zero conflicts.

#### 4. [Receiver & i-BUS Channel Monitor](inav-receiver-ibus-channels.png)
- **File:** `inav-receiver-ibus-channels.png`
- **Configurator Tab:** `Receiver`
- **What is verified:**
  - Live serial communication over FlySky i-BUS protocol (14 channels).
  - Channel bars for Roll, Pitch, Yaw, and Throttle displaying exact microsecond ranges (1000–2000µs with 1500µs center).
  - Aux channels mapped to transmitter switches.

#### 5. [Flight Modes Configuration (ARM, ANGLE & NAV RTH)](inav-modes-flight-switches.png)
- **File:** `inav-modes-flight-switches.png`
- **Configurator Tab:** `Modes`
- **What is verified:**
  - **ARM**: Assigned to Aux 1 (2-position switch).
  - **ANGLE**: Self-leveling stabilized mode for safe takeoff and cruise.
  - **NAV RTH (Return to Home)**: Dedicated failsafe and autonomous return switch mapped to Aux switch with 20m climb altitude.
  - **NAV ALTHOLD / POSHOLD**: Barometer + GPS assisted position and altitude locking.

---

### B. Physical Drone Hardware & Bench Testing

#### 6. [Complete Drone Bench Setup & INAV Configurator Link](drone-bench-setup-laptop.jpg)
- **File:** `drone-bench-setup-laptop.jpg`
- **Description:** Complete assembled F450 quadcopter connected to laptop workstation via USB for live sensor calibration, motor direction testing, and receiver telemetry verification.

#### 7. [Custom DIY STM32F411 Flight Controller Board (Top View)](stm32f411-flight-controller-board-top.jpg)
- **File:** `stm32f411-flight-controller-board-top.jpg`
- **Description:** Close-up of custom-soldered prototyping flight controller board featuring:
  - STM32F411CEU6 Black Pill (center)
  - MPU-6050 6-DOF IMU module
  - BMP280 barometric altimeter module
  - GY-271 magnetometer compass module
  - u-blox NEO-6M GPS receiver module

#### 8. [DIY Perfboard Flight Controller — Top Component Layout](diy-perfboard-fc-top-component-layout.jpg)
- **File:** `diy-perfboard-fc-top-component-layout.jpg`
- **Description:** Top side of the home-built flight controller board on copper perfboard showing component placement:
  - Female header sockets for Black Pill MCU
  - Sensor breakout header positions (MPU-6050, BMP280, GY-271, NEO-6M GPS)
  - Filtering capacitors and power rail distribution
  - Visual blueprint for home reproduction without requiring commercial PCB fabrication

#### 9. [DIY Perfboard Flight Controller — Bottom Solder Traces & Wiring](diy-perfboard-fc-bottom-solder-wiring.jpg)
- **File:** `diy-perfboard-fc-bottom-solder-wiring.jpg`
- **Description:** Underside view of the hand-soldered perfboard showing point-to-point solder bridge connections:
  - Ground bus network and power trace distribution
  - Jumper wire routing between Black Pill GPIOs and sensor/ESC headers
  - Critical reference for manual wiring replication and schematic/EDA software capture

#### 10. [Flight Controller Installed with Active Power & Status LEDs](stm32f411-fc-installed-wiring.jpg)
- **File:** `stm32f411-fc-installed-wiring.jpg`
- **Description:** The flight controller board mounted on the central F450 plate, powered up via ESC 5V BEC with status LEDs illuminated, confirming clean power delivery and active firmware execution.

#### 11. [F450 Quadcopter Airframe Assembly](f450-frame-assembly.jpg)
- **File:** `f450-frame-assembly.jpg`
- **Description:** Mechanical assembly of the 450mm wheelbase fiberglass central plates and reinforced polyamide arms prior to electronic component installation.

#### 12. [All-Up-Weight (AUW) Measurement on Digital Scale](f450-drone-weight-scale.jpg)
- **File:** `f450-drone-weight-scale.jpg`
- **Description:** Complete quadcopter on precision digital scale validating actual All-Up-Weight (AUW) with battery and propellers (~1.1 kg), confirming the calculated ~2.5:1 thrust-to-weight ratio for stable autonomous hover and RTH climb rates.

#### 13. [FlySky FS-i6 Radio Transmitter](flysky-fs-i6-transmitter.jpg)
- **File:** `flysky-fs-i6-transmitter.jpg`
- **Description:** FlySky FS-i6 2.4GHz AFHDS 2A radio transmitter configured for Mode 2 (Throttle on left) with 14-channel i-BUS serial output enabled.

#### 14. [FlySky Transmitter Internal Power Supply Upgrade](flysky-transmitter-power-supply-mod.jpg)
- **File:** `flysky-transmitter-power-supply-mod.jpg`
- **Description:** Internal hardware modification replacing standard disposable AA batteries with a rechargeable **Lithium-Ion battery power supply**, providing extended operational battery life during extensive flight-tuning sessions.

#### 15. [Author Active Development — Hardware Assembly & Hand-Soldering](author-hardware-assembly-hand-soldering.jpg)
- **File:** `author-hardware-assembly-hand-soldering.jpg`
- **Description:** Author **Arkadip Mahapatra** actively hand-soldering and testing circuit continuity with a digital multimeter on the workshop floor, validating 100% independent DIY construction from scratch.

#### 16. [Author Active Development — Workstation Flashing & Bench Testing](author-workstation-bench-testing.jpg)
- **File:** `author-workstation-bench-testing.jpg`
- **Description:** Live firmware flashing, USB telemetry monitoring, and hardware-in-the-loop diagnostic testing at the author's computer workstation.

#### 17. [Author Active Development — Circuit Board Inspection](author-circuit-inspection.jpg)
- **File:** `author-circuit-inspection.jpg`
- **Description:** Close optical inspection of hand-soldered pin headers, cold-joint checking, and board trace verification.

---

### C. Pinout & Reference Diagrams

#### 18. [STM32F411CEU6 Black Pill Pinout Diagram](stm32f411-blackpill-pinout.png)
- **File:** `stm32f411-blackpill-pinout.png`
- **Purpose:** Full reference of MCU pins, timer channels (TIM3, TIM4), alternate functions, and power pins.

---

## 🔗 Cross-References
- [Main README](../../README.md)
- [Wiring Guide](../wiring-guide.md)
- [Master Specification](../master-specification.md)
- [Flashing Guide](../flashing-guide.md)
- [Firmware Patches Explained](../firmware-patches-explained.md)
- [Engineering Q&A Troubleshooting Journey](../engineering-qa-troubleshooting.md)
