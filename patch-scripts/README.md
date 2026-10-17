# Python Binary Patch Scripts

This directory contains standalone Python tools developed to reverse-engineer, inspect, and modify compiled INAV firmware binaries and the NW.js INAV Configurator bundle.

## Tools Overview

| Script | Purpose | Usage |
| :--- | :--- | :--- |
| **`find_align.py`** | Scans binary firmware for sensor alignment structs and orientation flags. | `python find_align.py` |
| **`find_mixer.py`** | Locates motor mixer tables (`mmix`) in binary firmware offsets. | `python find_mixer.py` |
| **`find_rth.py`** | Scans for Return-to-Home parameters and altitude settings. | `python find_rth.py` |
| **`patch_model.py`** | Modifies the 3D model preview rendering in the Configurator GUI. | `python patch_model.py` |
| **`patch_record.py`** | Modifies the flight log recording behavior in INAV Configurator. | `python patch_record.py` |
| **`rebuild_exe.py`** | Rebuilds the Configurator executable with GPU rasterization flags to eliminate 1 FPS GUI lag on modern Windows. | `python rebuild_exe.py` |
| **`test_rot.py`** | Simulates and verifies 3D Euler angle rotation matrices. | `python test_rot.py` |

## Requirements
- Python 3.8+ (Standard library only; no external pip dependencies needed).
