# STM32F411CEU6 (Black Pill) Custom INAV 5.1.0 Firmware & Pinout Guide

## 1. কাস্টম ফার্মওয়্যার ফাইল
- **ফার্মওয়্যার পাথ:** `stm32f411ceu6/inav_5.1.0_BLACKPILL_QUAD_SD_108_CUSTOM_MPU6050_PB6_PB7.hex`
- **বেস আর্কিটেকচার:** INAV 5.1.0 (Blackpill F411 Overclocked to 108MHz for zero I2C loop jitter)

---

## 2. কী কী পরিবর্তন করা হয়েছে?
1. **জাইরোস্কোপ WHO_AM_I ক্লোন বাইপাস (0x68 ও 0x98):**
   - অরিজিনাল InvenSense চিপের `0x68` এবং বর্তমান চাইনিজ ক্লোন চিপের `0x98`—দুটোই অ্যাক্সেপ্ট করবে।
   - ক্লোন চিপের রিভিশন চেক ফেইল হওয়ার সমস্যা বাইপাস করে সরাসরি ফুল রেজোলিউশন অ্যাক্সেল ও জাইরো মোড অন করা হয়েছে।
2. **I2C পিন পরিবর্তন (User Request):**
   - **I2C1 SCL:** `PB6`
   - **I2C1 SDA:** `PB7`
   - সব I2C সেন্সর (MPU-6050, BMP280, HMC5883L/QMC5883L) এখন প্যারালালে `PB6` এবং `PB7`-এ কানেক্ট হবে।
3. **মোটর পিন রিম্যাপিং:**
   - যেহেতু `PB6` এবং `PB7` আগে মোটর ৩ ও ৪ ছিল, সেগুলোকে এখন সেফলি `PB8` এবং `PB9`-এ স্থানান্তর করা হয়েছে (TIM4 চ্যানেল ৩ এবং ৪)।

---

## 3. সম্পূর্ণ ওয়্যারিং গাইড (Wiring Connection)

### [ক] I2C সেন্সর বাস (সবগুলো সমান্তরাল বা প্যারালাল কানেকশন)
| সেন্সর | সেন্সর পিন | STM32F411 Black Pill পিন |
| :--- | :--- | :--- |
| **MPU-6050** | SCL | **PB6** |
| **MPU-6050** | SDA | **PB7** |
| **BMP280** (HW-611) | SCL | **PB6** |
| **BMP280** (HW-611) | SDA | **PB7** |
| **GY-271 / HMC5883L** | SCL | **PB6** |
| **GY-271 / HMC5883L** | SDA | **PB7** |
| **সব সেন্সর** | VCC | **3.3V** (বা 5V যদি সেন্সরে রেগুলেটর থাকে) |
| **সব সেন্সর** | GND | **GND** |

---

### [খ] মোটর / ESC সিগন্যাল পিন
| মোটর | ESC সিগন্যাল পিন | STM32F411 Black Pill পিন | হার্ডওয়্যার টাইমার |
| :--- | :--- | :--- | :--- |
| **Motor 1** | ESC 1 Signal | **PB4** | TIM3_CH1 |
| **Motor 2** | ESC 2 Signal | **PB5** | TIM3_CH2 |
| **Motor 3** | ESC 3 Signal | **PB8** | TIM4_CH3 |
| **Motor 4** | ESC 4 Signal | **PB9** | TIM4_CH4 |

---

### [গ] GPS মডিউল (NEO-6M / GPS-6M)
| GPS মডিউল পিন | STM32 পিন | বিবরণ |
| :--- | :--- | :--- |
| GPS **TX** | **PA10** (RX1) | UART1 Receiver |
| GPS **RX** | **PA9** (TX1) | UART1 Transmitter |
| GPS **VCC** | **5V** / 3.3V | পাওয়ার |
| GPS **GND** | **GND** | গ্রাউন্ড |

---

### [ঘ] রিসিভার (RC Receiver - IBUS / SBUS / CRSF)
| রিসিভার সিগন্যাল | STM32 পিন | বিবরণ |
| :--- | :--- | :--- |
| Receiver Signal (IBUS / CRSF / SBUS) | **PA3** (RX2) | UART2 Receiver |
| Receiver VCC | **5V** / 3.3V | পাওয়ার |
| Receiver GND | **GND** | গ্রাউন্ড |

---

### [ঙ] অন্যান্য পেরিফেরালস
- **Beeper (Buzzer):** `PB2` (বা `PB1`)
- **Battery Voltage ADC (VBAT):** `PB0`
- **WS2812 LED Strip:** `PA8`
- **Onboard Status LED:** `PC13`

---

## 4. ফ্ল্যাশ করার নিয়ম (Flashing Instructions via INAV Configurator)
1. আপনার STM32F411 ব্ল্যাকপিলের **BOOT0 বাটন চেপে ধরে** USB কেবল দিয়ে কম্পিউটারে লাগান।
2. যদি উইন্ডোজে DFU ড্রাইভার না পায়, তাহলে **ImpulseRC Driver Fixer** চালু করে ড্রাইভার ঠিক করে নিন।
3. **INAV Configurator** ওপেন করুন (শীর্ষে `DFU` লেখা দেখতে পাবেন)।
4. বাম পাশের মেনু থেকে **Firmware Flasher**-এ যান।
5. নিচে ডান পাশে **Load Firmware [Local]** বাটনে ক্লিক করে নির্বাচন করুন:
   `inav_5.1.0_BLACKPILL_QUAD_SD_108_CUSTOM_MPU6050_PB6_PB7.hex`
6. **Flash Firmware** বাটনে ক্লিক করুন।
7. ফ্ল্যাশ শেষ হলে ড্রোন রিবুট হবে এবং INAV Configurator-এ কানেক্ট করতে পারবেন!
