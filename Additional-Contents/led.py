import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

# 13 for PiControl, 4 for Industrial Hat
button = 4
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 23 for PiControl, 19 for Industrial Hat
led = 19
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

try:
    GPIO.output(led, GPIO.HIGH)
    while True:
        pass
except KeyboardInterrupt:
    GPIO.output(led, GPIO.LOW)
