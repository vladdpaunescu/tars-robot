import evdev
import time
import TARS_Servo_Abstractor3
import TARS_Servo_Controller3
from evdev import InputDevice, categorize, ecodes
import Adafruit_PCA9685
import smbus

# Specificează manual bus-ul I2C (de obicei 1 pe Raspberry Pi)
bus = smbus.SMBus(1)

pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Setează frecvența la 60 Hz pentru servouri
pwm.set_pwm_freq(60)

# Detectează controller-ul XBOX
gamepad = InputDevice('/dev/input/event8')  # Înlocuiește cu dispozitivul corect

# Variabile de stare
toggle = True
pose = False

print(gamepad)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:  # Evenimente analogice (inclusiv D-Pad)
        if event.code == ecodes.ABS_HAT0X:  # Axa orizontală D-Pad
            if event.value == -1:
                print("D-Pad Left")
                TARS_Servo_Abstractor3.turnLeft()
            elif event.value == 1:
                print("D-Pad Right")
                TARS_Servo_Abstractor3.turnRight()
            elif event.value == 0:
                print("D-Pad Horizontal Released")
        elif event.code == ecodes.ABS_HAT0Y:  # Axa verticală D-Pad
            if event.value == -1:
                print("D-Pad Up")
                TARS_Servo_Abstractor3.stepForward()
            elif event.value == 1:
                print("D-Pad Down")
                if not pose:
                    TARS_Servo_Abstractor3.pose()
                    pose = True
                else:
                    TARS_Servo_Abstractor3.unpose()
                    pose = False
            elif event.value == 0:
                print("D-Pad Vertical Released")

    elif event.type == ecodes.EV_KEY:  # Evenimente de la alte butoane
        if event.value == 1:  # Buton apăsat
            if event.code == ecodes.BTN_WEST:  # Buton X
                print("X")
                if toggle:
                    TARS_Servo_Controller3.starMainPlus()
                else:
                    TARS_Servo_Controller3.starMainMinus()
            elif event.code == ecodes.BTN_EAST:  # Buton B
                print("B")
                # Alte funcții pentru butonul B
            elif event.code == ecodes.BTN_SELECT:  # Buton "-"
                print("Minus")
                toggle = False
            elif event.code == ecodes.BTN_START:  # Buton "+"
                print("Plus")
                toggle = True
        elif event.value == 0:  # Buton eliberat
            print("Stop")
