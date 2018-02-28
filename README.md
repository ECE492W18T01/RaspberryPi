Includes all RPI functionality for the project. Utilizes python 3 development version.

##Getting Started:
1. Install Git.
```bash
apt-get install git
```
2. Clone Repository.
```bash
git clone https://github.com/ECEw18T01/RaspberryPi
```
3. Run configuration script.
```bash
chmod +x RaspberryPi/Utilities/setup.sh
RaspberryPi/Utilities/setup.sh
```

##Enable Camera Interface:
1. Open RaspberryPi Configuration.
```bash
sudo raspi-config
```
2. Navigate to Peripherals and enable camera interface.Test camera using Utilities/camera_preview.py


##Connecting the Dualshock 4 Controller:
1. Run the Dualshock 4 Driver Utility Setup.
```bash
chmod +x RaspberryPi/Utilities/ds4_setup.sh
RaspberryPi/Utilities/ds4_setup.sh
```
2. Next start ds4drv.
```bash
sudo ds4drv
```
As daemon
```
sudo ds4drv &
```
3. Pair bluetooth controller to the device.
You can test that the device is properly connected by running Utilities/controller_test.py

##Running the application:
1. Run app.py from the RaspberryPi directory.
```bash
python app.py
```
