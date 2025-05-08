import RPi.GPIO as GPIO
from pylibdmtx.pylibdmtx import decode
from guizero import App, Box, Text, PushButton, Picture
from PIL import Image
import os
import time

#------------------------------------------------------------
# GPIO Setup
GPIO.setmode(GPIO.BCM)

## 13 for PiControl, 4 for Industrial Hat
button = 4
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

## 23 for PiControl, 19 for Industrial Hat
led = 19
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, GPIO.LOW)

os.system("mkdir input")
os.system("mkdir output")


#------------------------------------------------------------
# Function -----

def scanpcb():
    bt4.text="Scanning..."
    bt2.text="Scanning..."

    # Capturing Image and Crop the Data Matrix
    os.system("sudo rm /home/pi/yolov5/output/exp/image.jpg")
    os.system("sudo rm /home/pi/yolov5/output/exp/crops/0/*")
    os.system("sudo rm /home/pi/yolov5/output/exp/crops/Data-Matrix/*")
    os.system("sudo rm fswebcam /home/pi/yolov5/input/image.jpg")
    time.sleep(0.1)
    
    os.system("rpicam-still -n --output /home/pi/yolov5/input/image.jpg --width 768 --height 768 --sharpness 2.0 autofocus-on-capture --autofocus-speed fast --autofocus-range full")
    # Uncomment the line below if using USB Camera
    #os.system("fswebcam -r 640x480 --no-banner /home/pi/yolov5/input/image.jpg")
    #os.system("fswebcam -r 640x480 --no-banner /home/pi/yolov5/input/image.jpg")

    os.system("python3 detect.py --weights best.pt --img 768 --conf 0.5 --source /home/pi/yolov5/input/image.jpg --save-crop --project /home/pi/yolov5/output --exist-ok")

    bt4.text="Scanning Done!"
    time.sleep(2)
    bt4.text="Scan PCB"

def showbigimg():
    bigimg.image = "/home/pi/yolov5/output/exp/image.jpg"
    bigimg.resize(450,450)
    bigimg.show()


# Widget and Layout -----
mainWin = App(title="Test App", height=768, width=1024)

leftSec = Box(mainWin, height=768, width=324, align="left")
rightSec = Box(mainWin, height=768, width=700, align="right")

## Left Side Layout
left1 = Box(leftSec, height=40, width=300)
listtitle = Box(leftSec, height=45, width=300)
dmlist = Text(listtitle, text="Scanned Data Matrix", align="bottom", size=17)

listbox = Box(leftSec, height=550, width=300)

## Right Side

right1 = Box(rightSec, height=40, width=600)
imgbox = Box(rightSec, height=450, width=600)
# altimg = Text(imgbox, text="PICTURE\nHERE", size=90)

spacer = Box(rightSec, height=280, width=55, align="left")
bt1 = PushButton(rightSec, height=5, width=15, align="left", text="Show Scanned\nImage", command=showbigimg)
bt2 = PushButton(rightSec, height=5, width=15, align="left")
bt3 = PushButton(rightSec, height=5, width=15, align="left")
bt4 = PushButton(rightSec, height=5, width=15, align="left", text="Scan PCB", command=scanpcb)


#------------------------------------------------------------
# App Execute -----
bigimg = Picture (imgbox)
mainWin.display()



"""
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

    # Uncomment the line below if using CSI Camera
    os.system("rpicam-still -n --output /home/pi/yolov5/input/image.jpg --width 768 --height 768 --sharpness 2.0 --autofocus-on-capture --autofocus-speed fast --autofocus-range full")
    # Uncomment the line below if using USB Camera
    #os.system("fswebcam -r 640x480 --no-banner /home/pi/yolov5/input/image.jpg")

    os.system("python3 detect.py --weights best.pt --img 768 --conf 0.5 --source /home/pi/yolov5/input/image.jpg --save-crop --project /home/pi/yolov5/output --exist-ok")


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
"""
