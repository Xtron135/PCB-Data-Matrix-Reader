import RPi.GPIO as GPIO
from pylibdmtx.pylibdmtx import decode
from PIL import Image
import os
import time


GPIO.setmode(GPIO.BCM)

button = 13
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

led = 23
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

os.system("mkdir input")
os.system("mkdir output")

while True:
    print("\nWaiting for Button Press\n")
    GPIO.wait_for_edge(button, GPIO.FALLING)
    GPIO.output(led, GPIO.HIGH)
    print("\nButton Pressed\n")

    # Capturing Image and Crop the Data Matrix
    os.system("sudo rm /home/pi/yolov5/output/exp/image.jpg")
    os.system("sudo rm /home/pi/yolov5/output/exp/crops/0/*")
    os.system("sudo rm /home/pi/yolov5/output/exp/crops/Data-Matrix/*")
    os.system("sudo rm fswebcam /home/pi/yolov5/input/image.jpg")
    time.sleep(0.1)
    os.system("fswebcam -r 640x480 --no-banner /home/pi/yolov5/input/image.jpg")
    os.system("python3 detect.py --weights best.pt --img 640 --conf 0.5 --source /home/pi/yolov5/input/image.jpg --save-crop --project /home/pi/yolov5/output --exist-ok")


    # Read the Cropped Data Matrix and Store Locally
    try:
        if os.path.exists("/home/pi/yolov5/output/exp/crops/Data-Matrix/image.jpg"):
            raw = decode(Image.open('/home/pi/yolov5/output/exp/crops/Data-Matrix/image.jpg'))
        else:
            raw = decode(Image.open('/home/pi/yolov5/output/exp/crops/0/image.jpg'))

        raw2 = str(raw[0])
        raw3 = raw2.split(",")
        raw4 = raw3[0].split("'")

        output = raw4[1]
        print(output)

        file1 = open("/home/pi/yolov5/output/data.txt", "a")
        file1.write(output + "\n")
        file1.close()

        print("\n\nSUCCESS: Data Matrix Successfully Read")
        GPIO.output(led, GPIO.LOW)

    except Exception:
        print("\n\nERROR: No Data Matrix Detected")
        GPIO.output(led, GPIO.LOW)
