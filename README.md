###Raspberry Fan

PWM Auto adjust fan speed for Raspberry Pi

###Dependencies

It is tested under Python 3.4

- [WiringPi](https://github.com/WiringPi/WiringPi-Python)
- [Daemonize](https://github.com/thesharp/daemonize)

You can install dependencies from Python Package Index (PyPI):

    $ pip install daemonize wiringpi

###Usage:

    usage: raspberry_fan.py [-h] [-H N] [-r N] [-m N] [-d N] [-v] [-D]
    optional arguments:
    [ -h ] - show this help message and exit
    [ -H ] - hysteresis, default: 5°C ( 1 < n < 10) 
    [ -r ] - refresh rate, default: 5 sec ( 1 < n < 30)
    [ -m ] - maximum temperature threshold, default: 70°C (60 < n < 80)
    [ -d ] - turn off fan at, default: 47°C ( 40 < n < 55) 
    [ -v ] - print output in stdout (of /var/log/r_fan.log in daemon-mode)
    [ -D ] - run as daemon


PWM out will use **GPIO18**

###Fan Connection:
Fan must be connected via ***Logic N-Channel MOSFET Transistor ONLY*** (IRL... for example)!
More information on http://elinux.org/RPi_GPIO_Interface_Circuits#Using_a_FET
