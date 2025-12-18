"""
Boot script for iRackPilot Pico W
Runs on startup before main.py
"""

import machine
import time

# Configure LED (if available)
try:
    led = machine.Pin("LED", machine.Pin.OUT)
    # Blink LED to indicate boot
    for _ in range(3):
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
except:
    pass

print("iRackPilot Firmware Booting...")
time.sleep(1)

