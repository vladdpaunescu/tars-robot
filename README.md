# TARS Robot

As part of the Robotics course, I developed a robot inspired by the character TARS from the movie *Interstellar*. This project was a challenge, requiring the integration of knowledge in mechanics, electronics, and computer science.

## Overview

TARS is a walking robot that replicates the rectangular monolith locomotion of its cinematic counterpart. It pivots and steps forward by coordinating three servo motors through a Raspberry Pi, controlled in real time via an Xbox gamepad.

## Hardware

| Component | Role |
| --------- | ---- |
| Raspberry Pi | Main compute unit, runs all Python code |
| PCA9685 PWM driver | Controls up to 16 servos over I2C (address `0x40`) |
| Servo — Center Lift (ch 0) | Raises and lowers the torso vertically |
| Servo — Port Drive (ch 1) | Rotates the torso to the port (left) side |
| Servo — Starboard Drive (ch 2) | Rotates the torso to the starboard (right) side |
| Xbox controller | Wireless gamepad input via `evdev` |

## Mechanics

All structural parts were designed in Fusion 360 (`cad/tars_redefined_2 v5.f3d`) and 3D-printed.

### Body

- Upper and lower chassis, upper/lower lids
- Suspension assembly: main leg mounts, suspension mounts (left/right), spring drivers, upper structure mounts, servo wheel mounts, vertical servo clips, screen support
- Axle assembly: main axle and secondary axles

### Feet

- Arms, hulls, foot pads, lids, servo clips

## Software Architecture

```text
TARS_Runner.py            ← entry point; reads Xbox controller events
    └── TARS_Servo_Abstractor3.py  ← high-level motion commands
            └── TARS_Servo_Controller3.py  ← low-level PWM sequences
```

### TARS_Runner.py

Reads gamepad events via `evdev` and dispatches motion commands:

| Input | Action |
| ----- | ------ |
| D-Pad Up | Step forward |
| D-Pad Left | Turn left |
| D-Pad Right | Turn right |
| D-Pad Down | Toggle pose / unpose |
| Button X + mode | Star main motion (plus/minus direction) |
| Button `+` / `-` | Toggle direction mode |

### TARS_Servo_Abstractor3.py

High-level gait primitives built from controller sequences:

- `stepForward()` — lift → lean forward → bump → return
- `turnLeft()` / `turnRight()` — lower → pivot → return to neutral
- `pose()` / `unpose()` — lean backward into display pose and recover

### TARS_Servo_Controller3.py

Low-level servo control using `Adafruit_PCA9685`. Manages smooth PWM transitions with configurable speed (sleep intervals between increments) and supports parallel axis movement via Python threads.

### pozitie_initiala_servo.io.ino

Arduino sketch used during calibration to set all servos to their neutral positions via the PCA9685 library.

## Repository Structure

```text
tars-robot/
├── TARS_Runner.py                  # Main controller loop
├── TARS_Servo_Abstractor3.py       # High-level motion abstraction
├── TARS_Servo_Controller3.py       # Low-level PWM servo control
├── pozitie_initiala_servo.io/      # Arduino calibration sketch
├── cad/                            # Fusion 360 source + STL files
│   ├── tars_redefined_2 v5.f3d
│   ├── BODY/
│   └── FOOTS/
└── docs/                           # Documentation, schematics, and photos
    ├── Documentation.pdf
    ├── Proiect_Robo_Paunescu_Plesu.docx
    ├── RobotTars-Copiere.pptx
    ├── 525125-Schematic__50863__42807.webp
    └── photos/
```

## Dependencies

```text
evdev
Adafruit_PCA9685
smbus
```

Install on Raspberry Pi:

```bash
pip install evdev adafruit-pca9685 smbus2
```

## Running

```bash
python3 TARS_Runner.py
```

Ensure the PCA9685 is connected on I2C bus 1 and the Xbox controller is detected at `/dev/input/event8` (adjust the path in `TARS_Runner.py` if needed).
