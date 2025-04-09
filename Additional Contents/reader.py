from pylibdmtx.pylibdmtx import decode
from PIL import Image
import os

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
file1.close
