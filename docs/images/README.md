# 📸 Visual Documentation & Configurator Screenshots (INAV)

This directory hosts high-resolution screenshots, configurator verification captures, and pinout diagrams from the physical bench configuration and flight preparation of the **F450 STM32F411 Black Pill INAV Drone**.

---

## 🖼️ Gallery of Images & Tab Explanations

### 1. [Setup Tab & 3D Quad-X Model Preview](inav-setup-3d-model.png)
- **File:** `inav-setup-3d-model.png`
- **Configurator Tab:** `Setup`
- **What is verified:**
  - Real-time 3D Quad-X airframe rendering tracking physical board movements.
  - Heading angle, Roll/Pitch orientation values.
  - Top telemetry bar showing green status flags for Gyro, Accelerometer, Magnetometer, Barometer, and GPS.
  - Arming flag status and system status.

---

### 2. [6-Point Accelerometer Calibration](inav-calibration-6point.png)
- **File:** `inav-calibration-6point.png`
- **Configurator Tab:** `Calibration`
- **What is verified:**
  - INAV's rigorous 6-point accelerometer calibration procedure.
  - Visual prompts for positioning the drone in 6 orthogonal orientations: Flat, Left side, Right side, Nose up, Nose down, and Upside down.
  - Calibration gain and offset registers stored in non-volatile flash memory to ensure stable GPS hold and level flight.

---

### 3. [UART & Ports Configuration](inav-ports-uart-config.png)
- **File:** `inav-ports-uart-config.png`
- **Configurator Tab:** `Ports`
- **What is verified:**
  - **USB VCP**: MSP protocol enabled for GUI communication at 115200 baud.
  - **UART1 (PA9/PA10)**: Configured for GPS module at 57600 baud with UBLOX protocol.
  - **UART2 (PA3)**: Configured for Serial RX (FlySky i-BUS receiver) with zero conflicts.

---

### 4. [Receiver & i-BUS Channel Monitor](inav-receiver-ibus-channels.png)
- **File:** `inav-receiver-ibus-channels.png`
- **Configurator Tab:** `Receiver`
- **What is verified:**
  - Live serial communication over FlySky i-BUS protocol (14 channels).
  - Channel bars for Roll, Pitch, Yaw, and Throttle displaying exact microsecond ranges (1000–2000µs with 1500µs center).
  - Aux channels mapped to transmitter switches.

---

### 5. [Flight Modes Configuration](inav-modes-flight-switches.png)
- **File:** `inav-modes-flight-switches.png`
- **Configurator Tab:** `Modes`
- **What is verified:**
  - **ARM**: Assigned to Aux 1 (2-position switch).
  - **ANGLE**: Self-leveling stabilized mode for safe takeoff and cruise.
  - **NAV RTH (Return to Home)**: Dedicated failsafe and autonomous return switch mapped to Aux switch with 20m climb altitude.
  - **NAV ALTHOLD / POSHOLD**: Barometer + GPS assisted position and altitude locking.

---

### 6. [STM32F411CEU6 Black Pill Pinout Diagram](stm32f411-blackpill-pinout.png)
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
