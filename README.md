# PCB-Data-Matrix-Reader


## Overview


This project uses an Industrial Controller; IRIV PiControl, based on Rasberry Pi Compute Module 5 to read PCB Data Matrix using USB Camera. This repo is a simplified concept and procedure for developing this project. A detailed tutorial will be developed on Cytron Technologies Tutorial Page.


## Hardwares


- IRIV PiControl CM5 8GB RAM 32GB eMMC
- USB Camera 5MP
- A push button (Connected to GPIO 13)
- An LED (Connected to GPIO 23)

> [!NOTE]
> You can also develop this project using a normal Raspberry PI 5. Modify the connection accordingly based on your wiring configuration.


## Project Flow


A lot of processes are involved in this project. This is a rough overview on how the flow of the code works.


## Reference

Data Matrix Dataset is from Roboflow User, tryclofus. All credits for the dataset goes to him.\
https://universe.roboflow.com/tryclofus/dtmx/dataset/1

Raspberry Pi Camera commands documentation.\
https://www.raspberrypi.com/documentation/computers/camera_software.html#use-a-usb-webcam

AI Vision Recognition using YOLO5. Train models and use YOLOV5.\
https://my.cytron.io/tutorial/worker-safety-compliance-monitoring-system-with-raspberry-pi-5

Read Data Matrix contents using pylibdmtx library\
https://pypi.org/project/pylibdmtx/
