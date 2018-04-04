
stty -F /dev/ttyUSB0 speed 115200 cs8 -cstopb -parenb raw
echo -ne "*" > /dev/ttyUSB0
