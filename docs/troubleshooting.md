# INAV 5.1.0 Black Pill Troubleshooting & Bench Testing Guide

## 1. Arming Prevention Flags (`status` command)

In the INAV CLI, run `status` to inspect arming lockouts:

```text
Arming disabled flags: CLI
```

| Flag | Meaning | Solution |
| :--- | :--- | :--- |
| **`CLI`** | CLI terminal is currently active | Type `exit` or disconnect to arm |
| **`NAV_SAFETY`** | Indoor arming safety active | Run `set nav_extra_arming_safety = OFF` for indoor bench testing |
| **`CALIB`** | Sensor calibration ongoing | Keep drone level and stationary after plugging battery |
| **`HW_FAIL`** | A required sensor is missing | Verify I2C bus wiring on `PB6` / `PB7` and run `status` to check sensor list |
| **`THROTTLE`** | Throttle stick is above idle | Lower throttle stick to minimum position |
| **`RX`** | No valid RC packets detected | Check UART2 RX connection (`PA3`) and transmitter power |

---

## 2. Why Only One Motor Spun During Bench Testing

When testing an assembled drone on a table without propellers in Angle mode:
1. **PID I-Term Windup:** Even a 0.5° tilt from a perfectly level plane causes the integral accumulator to build up. Because there are no propellers, the frame cannot physically level itself. The flight controller sends 100% throttle to the lower side and drops the others to idle.
2. **Verification:** Tilt the drone by hand while armed — all 4 motors will dynamically speed up and slow down to correct the tilt.

---

## 3. Compass Calibration (GY-271)

1. Mount the compass at least 5 cm away from high-current power wires and battery leads.
2. Verify orientation: `set align_mag = CW180`.
3. In INAV Configurator, click **Calibrate Magnetometer** in the Setup tab.
4. Rotate the frame 360° on all 3 axes within 30 seconds.
