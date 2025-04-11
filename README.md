# PCB-Data-Matrix-Reader


> [!WARNING]
> This project is still in development. Some planned features are still in development and not ready.
> - Currently the program only able to detect and process one Data Matrix at once. Planned to be able to scan multiple Data Matrix.
> - Currently the program saves the Data Matrix content in a txt file. Planned to be able to upload to server/cloud API.


## Overview


This project uses an Industrial Controller; [IRIV PiControl](https://my.cytron.io/p-iriv-picontrol-cm4-industrial-controller), based on Rasberry Pi Compute Module 5 to read PCB Data Matrix using USB Camera. This repo is a simplified concept and procedure for developing this project. A detailed tutorial will be developed on the Cytron Technologies Tutorial Page.


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


### Libraries and dependencies

```ShellSession
pip3 install numpy -U
```
```ShellSession
pip3 install pylibdmtx
```
```ShellSession
pip3 install pillow
```
```ShellSession
sudo apt install -y python3 python3-pip git libatlas-base-dev libgtk-3-dev pkg-config libqt5gui5
```
```ShellSession
sudo apt-get install libdmtx0b
```
```ShellSession
sudo apt-get install fswebcam
```

>[!TIP]
>If you got an error about EXTERNALLY MANAGED Python Package, run this command:
>```ShellSession
>  sudo mv /usr/lib/python3.11/EXTERNALLY-MANAGED /usr/lib/python3.11/EXTERNALLY-MANAGED.old
>```


### 1. Install YOLOv5

Run this command:

```ShellSession
git clone https://github.com/ultralytics/yolov5.git
```

Enter the folder:

```ShellSession
cd yolov5
```

Install pytorch and requirements.txt:

```ShellSession
pip3 install torch torchvision
```
```ShellSession
pip3 install -r requirements.txt
```

Back to home directory:

```ShellSession
cd ~
```

### 2. Clone this repo and prepare additional files

```ShellSession
git clone https://github.com/Xtron135/PCB-Data-Matrix-Reader.git
```

Copy all contents inside the `Aditional-Contents` folder (in this repo) into `yolov5` folder:

```ShellSession
mv -r PCB-Data-Matrix-Reader/Additional-Contents/* yolov5/
```

### 3. Update path settings in experimental.py

>[!NOTE]
>This is because the models we trained, are using Windows PC. So by default, the path settings are based on the Windows environment. So, we want to run this program in Linux, we need to change the path settings to match Linux environment,

```ShellSession
sudo nano /home/pi/yolov5/models/experimental.py
```

Looks for this section:

```python
def attempt_load(weights, device=None, inplace=True, fuse=True):
  """
  Loads and fuses an ensemble or single YOLOv5 model from weights, handling device placement and model adjustments.
  Example inputs: weights=[a,b,c] or a single model weights=[a] or weights=a.
  """
  from models.yolo import Detect, Model

  model = Ensemble()
```

Add this code snippets into the code, between `from models.yolo` and `model = Ensemble()`:

```python
  import pathlib
  import sys

  if sys.platform != 'win!32:
    pathlib.WindowsPath = pathlib.PosixPath
```

Your code should look like this now:

```python
def attempt_load(weights, device=None, inplace=True, fuse=True):
  """
  Loads and fuses an ensemble or single YOLOv5 model from weights, handling device placement and model adjustments.
  Example inputs: weights=[a,b,c] or a single model weights=[a] or weights=a.
  """
  from models.yolo import Detect, Model
  import pathlib
  import sys

  if sys.platform != 'win!32:
    pathlib.WindowsPath = pathlib.PosixPath

  model = Ensemble()
```

Save your code by pressing CTRL and O on your keyboard.

Exit the code editor by pressing CTRL and X on your keyboard.

Now we are ready to run the program.


### 4. Run the program

Enter the `yolov5` folder
```ShellSession
cd yolov5
```

Try to test your USB camera to see if your camera placement, PCB placement, and the distance in between, is correct. Make sure your camera can see the PCB clearly. Adjust the focus if necessary. Run this command to test your camera view:

```ShellSession
ffplay -f v4l2 -video_size 640x480 -framerate 30 -i /dev/video0
```

>[!TIP]
>If you got an error about no camera on `video0`, try to use `video1` instead. Alternatively, you can use this command to check, how many `video` you have connected. This indicates how many cameras are detected on your USB port.
>```ShellSession
>ls /dev/video*
>```
>Normally USB Webcam will be shown as `video0` or `video1`. If you have connected your camera but don't see any `video0` or `video1`, try to check your USB port connection or this may also indicate that you have a faulty USB Webcam or faulty USB port.

Next, run this command to test the detection of your camera. Make sure your camera can detect the Data Matrix properly:

```ShellSession
python3 detect.py --weights best.pt --img 640 --conf 0.5 --source 0
```

>[!TIP]
>If you run successfully run the detection program, at a proper distance between the PCB and the camera, the program should be able to detect the Data Matrix. You should be able to see a square boundary box highlighting the Data Matrix. If the confidence level is below 0.5, you can see only the boundary box. If the its higher than 0.5, you should see the label `Data-Matrix` with the boundary box. Don't worry about the confidence level. As long as the image is clear, we will be able to read it as long as the image is clear.

Finally, if everything good, we are ready to run the main program. Run this command:

```ShellSession
python3 main.py
```

Now press the push button. Your LED should light up, indicating that the program is processing the input. When it's finished, the LED will turn off. And you can check the output.

You can check detection image in the folder `output/exp/`.

You can check the cropped Data Matrix in the folder `output/exp/crop/`. If the Data Matrix confidence level is below 0.5, the image will be in the `0` folder. Else, it will be in the `Data-Matrix` folder.

You can check the content of your Data Matrix in the text file, in the `output` folder.


## Reference

Data Matrix Dataset is from Roboflow User, tryclofus. All credits for the dataset goes to him.\
https://universe.roboflow.com/tryclofus/dtmx/dataset/1

Raspberry Pi Camera commands documentation.\
https://www.raspberrypi.com/documentation/computers/camera_software.html#use-a-usb-webcam

AI Vision Recognition using YOLO5. Train models and use YOLOV5.\
https://my.cytron.io/tutorial/worker-safety-compliance-monitoring-system-with-raspberry-pi-5

Read Data Matrix contents using 'pylibdmtx' library\
https://pypi.org/project/pylibdmtx/
