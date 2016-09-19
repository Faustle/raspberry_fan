# raspberry_fan
PWM Auto adjust fan speed for Raspberry Pi

Based on [WiringPi](https://github.com/WiringPi/WiringPi-Python)

###Usage:
usage: raspberry_fan.py [-h] [-H] [-r] [-m] [-d] [-v]
- [-H] - Hysteresis ( 1 < n < 10)
- [-r] - Refresh rate in sec ( 1 < n < 30)
- [-m] - The temperature at which the maximum fan speed (60 < n < 80)
- [-d] - The temperature at which fan will auto off ( 40 < n < 55)
- [-v] - Verbose-mode

PWM out will use **GPIO18** and **GND** pins.

###Fan Connection:
The fan must be connected via ***Logic MOSFET Transistor ONLY***!
More information on http://elinux.org/RPi_GPIO_Interface_Circuits
