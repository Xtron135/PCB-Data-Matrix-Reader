import RPi.GPIO as GPIO
import os

button = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("waiting")

while True:
    GPIO.wait_for_edge(button, GPIO.FALLING)
    print("Button Pressed")
    os.system("fswebcam -r 640x480 --no-banner /home/pi/yolov5/input/image.jpg")
    print("image captured")
