# RaspberryPi
Includes all RPI functionality for the project. Utilizes python 3 development version.

## Dependencies
- Python 3 Development Version: https://www.python.org/downloads/
- ds4drv: https://github.com/chrippa/ds4drv
- picamera: https://picamera.readthedocs.io/en/release-1.13/
- pygame: https://www.pygame.org/news

## Getting Started:
1. Install Git:
```bash
apt-get install git
```
2. Clone Repository onto Raspberry Pi:
```bash
git clone https://github.com/ECEw18T01/RaspberryPi
```
3. Run configuration script:
```bash
chmod +x RaspberryPi/utilities/setup.sh
RaspberryPi/utilities/setup.sh
```

## Connecting Raspberry Pi Camera module:
1. Open RaspberryPi Configuration:
```bash
sudo raspi-config
```
2. Navigate to Peripherals and enable camera interface:
Ensure the camera module is working by running camera_preview() available in test.py.


## Connecting the Dualshock 4 Controller:
1. Run the Dualshock 4 Driver Utility Setup.
```bash
chmod +x RaspberryPi/utilities/setup.sh
RaspberryPi/utilities/setup.sh
```
2. Next start ds4drv:
```bash
sudo ds4drv
```
As daemon:
```bash
sudo ds4drv &
```
3. Pair bluetooth controller to the device:
You can test that the device is properly connected by running utilities/joystick.py

## Running the application:
1. Run drive.py from the RaspberryPi directory:
```bash
python drive.py
```
Currently the main program is broken up into two seperate processes drive.py and stream.py. These two files will be combined into the main program once testing is complete.

Has seperate master and progress branch.
