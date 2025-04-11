# PCB-Data-Matrix-Reader


> [!WARNING]
> This project is still in development. Some planned features are still in development and not ready.
> - Currently the program only able to detect and process one Data Matrix at once. Planned to be able to scan multiple Data Matrix.
> - Currently the program saves the Data Matrix content in a txt file. Planned to be able to upload to server/cloud API.


## Overview


This project uses an Industrial Controller; [IRIV PiControl](https://my.cytron.io/p-iriv-picontrol-cm4-industrial-controller){:target="_blank"}, based on Rasberry Pi Compute Module 5 to read PCB Data Matrix using USB Camera. This repo is a simplified concept and procedure for developing this project. A detailed tutorial will be developed on the Cytron Technologies Tutorial Page.


## Hardwares


- [IRIV PiControl CM5 8GB RAM 32GB eMMC](https://my.cytron.io/p-iriv-picontrol-cm4-industrial-controller)
- [USB Camera 5MP](https://my.cytron.io/c-raspberry-pi-camera/p-usb-camera-with-housing-for-raspberry-pi-jetson)
- [A Push Button (Industrial Illuminated Push Button)(Connected to GPIO 13)](https://my.cytron.io/p-illuminated-push-push-button-24vdc-240vac)
- [An LED (Industrial Illuminated Push Button)(Connected to GPIO 23)](https://my.cytron.io/p-illuminated-push-push-button-24vdc-240vac)

> [!NOTE]
> You can also develop this project using a normal Raspberry PI 5. Modify the connection accordingly based on your wiring configuration.
> In our case, we use the [IRIV PiControl Training Kit](https://my.cytron.io/p-iriv-picontrol-industry-4p0-kit-and-workshops) and simply use the included Illuminated Push Button.


## Project Flow


A lot of processes are involved in this project. This is a rough overview of how the flow of the code works.

1. Capturing the image of the PCB board.
2. Detect and classify the existence and position of the Data Matrix on the board.
3. Crop the Data Matrix image out from the main image.
4. Read the content of the Data Matrix.
5. Store the Data Matrix content in a txt file.
6. Upload the content to online server/cloud API [Future]


## Hardware Scope and Limitation

- Maximum PCB Board size allowed to scan is around 15 x 15 cm
- Captured image resolution is 640 x 640 px
- The program should be able to read multiple Data Matrix at once. [Future]
- The distance between the camera and the PCB Board needs to be around 15 cm.

> [!IMPORTANT]
> The camera distance depends on your maximum PCB size and the resolution of your camera. For our case, to scan a 15 x 15 cm PCB and get a clear image using a 5 MP camera, the distance needs to be 15 cm.


## Procedures


## Code Explanation


## Reference

Data Matrix Dataset is from Roboflow User, tryclofus. All credits for the dataset goes to him.\
https://universe.roboflow.com/tryclofus/dtmx/dataset/1

Raspberry Pi Camera commands documentation.\
https://www.raspberrypi.com/documentation/computers/camera_software.html#use-a-usb-webcam

AI Vision Recognition using YOLO5. Train models and use YOLOV5.\
https://my.cytron.io/tutorial/worker-safety-compliance-monitoring-system-with-raspberry-pi-5

Read Data Matrix contents using 'pylibdmtx' library\
https://pypi.org/project/pylibdmtx/
