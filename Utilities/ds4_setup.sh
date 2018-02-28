sudo apt-get -y install joystick

#Install Dualshock 4 drivers for python 2.7 and python 3
sudo pip3 install ds4drv
sudo pip install ds4drv

#Update rules
#sudo wget https://raw.githubusercontent.com/chrippa/ds4drv/master/udev/50-ds4drv.rules -O /etc/udev/rules.d/50-ds4drv.rules
#sudo udevadm control --reload-rules
#sudo udevadm trigger
