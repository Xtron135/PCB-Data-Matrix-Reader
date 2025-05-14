import RPi.GPIO as GPIO
from pylibdmtx.pylibdmtx import decode
from guizero import App, Box, ListBox, Text, PushButton, Picture
from PIL import Image
import numpy
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

## Other Variables
light = 0
data_list = []
tdetect = 0

os.system("mkdir input")
os.system("mkdir output")


#------------------------------------------------------------
# Function -----

def scanning():
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

def showbigimg():
    bigimg.image = "/home/pi/yolov5/output/exp/image.jpg"
    bigimg.resize(450,450)
    bigimg.show()

def scanpcb():
    bt5.text="Scanning.."
    mainWin.update()

    scanning()
    showbigimg()
    decode1()
    decode2()
    bt5.text="Scanning\nDone!"
    mainWin.update()

    time.sleep(3)
    bt5.text="Scan PCB"

def lighting():
    GPIO.output(led, not GPIO.input(led))

def decode1():
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

def decode2():
    stream = os.popen("find /home/pi/yolov5/output/exp/crops -type f | wc -l")
    tdetect = stream.read().strip()
    tdetect = int(tdetect)
    print(tdetect)
    if(tdetect == 3):
        print("wei")
    else: print("no")


def reflist():
    #datalist = numpy.loadtxt('/home/pi/yolov5/output/data.txt', dtype=str)
    #datalist = datalist.tolist()
    #listbox.items = datalist
    data_array = numpy.genfromtxt("/home/pi/yolov5/output/data.txt", dtype=str, delimiter="\n")
    # Handle the possibility that the file is empty or has one line
    if data_array.ndim == 0:  
        # If there is only one line, ensure we still get a list
        data_list = [str(data_array)]
    elif data_array.size > 0:
        data_list = data_array.tolist()
    else:
        data_list = []

    print("Data: ", data_list)

    listbox.clear()

    # Append each item individually
    for item in data_list:
        listbox.append(item)


# Widget and Layout -----
mainWin = App(title="Test App", height=768, width=1024)

leftSec = Box(mainWin, height=768, width=324, align="left")
rightSec = Box(mainWin, height=768, width=700, align="right")

## Left Side Layout
left1 = Box(leftSec, height=40, width=300)
listtitle = Box(leftSec, height=45, width=300)
dmlist = Text(listtitle, text="Scanned Data Matrix", align="bottom", size=17)

listbox = ListBox(leftSec, height=550, width=300, items=["No Data Loaded"], scrollbar=True)

## Right Side

right1 = Box(rightSec, height=10, width=600)
imgbox = Box(rightSec, height=450, width=600)
# altimg = Text(imgbox, text="PICTURE\nHERE", size=90)

# status = Text(rightSec, height=40, width=600, text="test", align="top")

spacer = Box(rightSec, height=280, width=100, align="left")

bt1 = PushButton(rightSec, height=3, width=12, align="left", text="Refresh\nList", command=reflist)
bt2 = PushButton(rightSec, height=3, width=12, align="left", text="Show Scanned\nImage", command=showbigimg)
#bt3 = PushButton(rightSec, height=3, width=12, align="left", text="Show Cropped\nImages")
bt4 = PushButton(rightSec, height=3, width=12, align="left", text="Toggle\nLighting", command=lighting)
bt5 = PushButton(rightSec, height=3, width=12, align="left", text="Scan PCB", command=scanpcb)



#------------------------------------------------------------
# App Execute -----
bigimg = Picture (imgbox)
mainWin.display()

mainWin.when_closed = lambda: GPIO.cleanup()

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
