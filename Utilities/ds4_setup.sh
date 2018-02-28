sudo apt-get update

sudo apt-get -y install joystick

#Raspberry Pi 3 Requires development versions of python
sudo apt install python-dev python3-dev python-pip python3-pip

#Install Dualshock 4 drivers for python 2.7 and python 3
sudo pip3 install ds4drv
sudo pip install ds4drv

#Update rules 
#sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules -O /etc/udev/rules.d/50-ds4drv.rules

#sudo udevadm control --reload-rules

#sudo udevadm trigger