from guizero import App, Box, Text, PushButton, Picture
from PIL import Image


# Function -----

def showbigimg():
    bigimg.image = "/home/pi/yolov5/output/exp/image.jpg"
    bigimg.resize(450,450)
    bigimg.show()


# Widget and Layout -----
mainWin = App(title="Test App", height=768, width=1024)

leftSec = Box(mainWin, height=768, width=324, align="left")
rightSec = Box(mainWin, height=768, width=700, align="right")
leftSec.bg = "blue"
rightSec.bg = "green"

## Left Side Layout
left1 = Box(leftSec, height=40, width=300)
left1.bg = "grey"
listtitle = Box(leftSec, height=45, width=300)
listtitle.bg = "yellow"
dmlist = Text(listtitle, text="Scanned Data Matrix", align="bottom", size=17)

listbox = Box(leftSec, height=550, width=300)
listbox.bg = "red"

## Right Side

right1 = Box(rightSec, height=40, width=600)
right1.bg = "grey"
imgbox = Box(rightSec, height=450, width=600)
imgbox.bg = "yellow"
# altimg = Text(imgbox, text="PICTURE\nHERE", size=90)

spacer = Box(rightSec, height=280, width=55, align="left")
spacer.bg = "red"
bt1 = PushButton(rightSec, height=5, width=15, align="left", text="Show Scanned\nImage", command=showbigimg)
bt2 = PushButton(rightSec, height=5, width=15, align="left")
bt3 = PushButton(rightSec, height=5, width=15, align="left")
bt4 = PushButton(rightSec, height=5, width=15, align="left")

# App Execute -----
bigimg = Picture (imgbox)
mainWin.display()
