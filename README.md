# Raspberry Fan
PWM Auto adjust fan speed for Raspberry Pi

Based on [WiringPi](https://github.com/WiringPi/WiringPi-Python)

###Usage:
usage: raspberry_fan.py [-h] [-H N] [-r N] [-m N] [-d N] [-v]

optional arguments:
- [ -h ] - show this help message and exit
- [ -H ] - hysteresis, default: 5°C ( 1 < n < 10)
- [ -r ] - refresh rate, default: 5 sec ( 1 < n < 30)
- [ -m ] - maximum temperature threshold, default: 70°C (60 < n < 80)
- [ -d ] - turn off fan at, default: 47°C ( 40 < n < 55)
- [ -v ] - print output


PWM out will use **GPIO18** and **GND** pins.

###Fan Connection:
The fan must be connected via ***Logic MOSFET Transistor ONLY***!
More information on http://elinux.org/RPi_GPIO_Interface_Circuits
