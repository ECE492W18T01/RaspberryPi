# Raspbian Lite Setup

sudo apt-get update
sudo apt-get upgrade

sudo apt install python3-dev python3-pip
pip3 install pygame

sudo apt-get -y install joystick

sudo pip3 install ds4drv

sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules -O /etc/udev/rules.d/50-ds4drv.rules
sudo udevadm control --reload-rules
sudo udevadm trigger
