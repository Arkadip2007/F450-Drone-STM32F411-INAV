# Source Code Modifications (INAV 5.1.0)

This directory contains the patched C source file for the MPU-6050 gyroscope and accelerometer driver.

## File: `accgyro_mpu.c`

### What was changed:
In stock INAV 5.1.0, `mpuDetect()` validates the sensor via the `WHO_AM_I` register:

```c
// Stock INAV 5.1.0:
uint8_t whoAmI = mpuReadRegister(MPU_RA_WHO_AM_I);
if (whoAmI == 0x68) {
    return MPU_6050;
}
```

This caused modern Chinese clone MPU-6050 modules (which return `0x98` or `0x70`) to fail detection completely, displaying `GYRO=NONE, ACC=NONE`.

### Patched Implementation:
```c
// Patched in this repository:
uint8_t whoAmI = mpuReadRegister(MPU_RA_WHO_AM_I);
if (whoAmI == 0x68 || whoAmI == 0x98 || whoAmI == 0x70) {
    return MPU_6050; // Whitelist clone silicon dies
}
```

This single change allows full 6-DOF attitude tracking on counterfeit and remarked MPU-6050 sensors.
