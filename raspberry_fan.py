#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import wiringpi
import time
import argparse
import logging
from datetime import datetime as dt
from daemonize import Daemonize

''' Parsing args '''
parser = argparse.ArgumentParser(description='Automatic fan control with hardware PWM for Raspberry Pi')
parser.add_argument('-H', '--hys', default=5, type=int, metavar='N',
                    help='hysteresis, default: 5\xb0C')
parser.add_argument('-r', '--refresh', default=5, type=int, metavar='N',
                    help='refresh rate, default: 5 sec')
parser.add_argument('-m', '--max_temp', default=70, type=int, metavar='N',
                    help='maximum temperature threshold, default: 70\xb0C')
parser.add_argument('-d', '--turnoff', default=47, type=int, metavar='N',
                    help='turn off fan at, default: 47\xb0C')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print output or logging in daemon mode')
parser.add_argument('-D', '--daemon', action='store_true',
                    help='run as daemon')
args = parser.parse_args()
args = vars(args)

''' Assing vars from cmdline '''
''' and test values          '''
hys = args['hys']
if hys < 1 or hys > 10:
    hys = 5
    print("Hysteresis value not valid! Default value (5) will be used!")

ref = args['refresh']
if ref < 1 or ref > 30:
    ref = 5
    print("Refresh rate value not valid! Default value (5) will be used!")

m_temp = args['max_temp']
if m_temp < 60 or m_temp > 80:
    m_temp = 70
    print("Maximum temperature threshold value not valid! Default value (70) \
will be used!")

d_temp = args['turnoff']
if d_temp < 40 or d_temp > 55:
    d_temp = 47
    print("Turn off value not valid! Default value (47) will be used!")

''' Init temperature and fan vars '''
fan_pin  = 1
temp = 0
t = 0
cur_speed = 0
t_range = 640 // (m_temp-30)        # Create step speed list

''' Create table of temp and fan speed '''
temp_table = [x for x in range(30, m_temp)]
speed_table = [x for x in range(384, 1024, t_range)]
dict_table = dict(zip(temp_table, speed_table))

wiringpi.wiringPiSetup()
wiringpi.pinMode(fan_pin, 2)
wiringpi.pwmWrite(fan_pin, 0)

''' Daemon PID and logging init '''
pid = '/tmp/r_fan.pid'
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
fh = logging.FileHandler('/var/log/r_fan.log', 'w')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
keep_fds = [fh.stream.fileno()]


def fan(fan_value):
    ''' Change speed function '''
    wiringpi.pwmWrite(fan_pin, fan_value)


def cputemp():
    ''' Get temperature value function '''
    f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
    get_temp = f.read()
    get_temp = int(get_temp)//1000
    f.close()
    return get_temp

''' Initialization first variables '''
temp = cputemp()
fan(dict_table[temp])
set_out = 'Current settings: Hysteresis: {0}\xb0C, ' \
          'Refresh rate: {1} sec, ' \
          'Maximum temperature threshold: {2}\xb0C, ' \
          'Turn off fan at {3}\xb0C\n'.format(hys, ref, m_temp, d_temp)

''' Verbose out '''
print(set_out)
if args['daemon'] and args['verbose']:
    logger.debug(set_out)


def main():
    ''' Main function '''
    while True:
        global t
        temp = cputemp()
        cur_speed = dict_table[temp]

        if temp >= t+hys or temp <= t-hys or t == 0:
            fan(cur_speed)
            t = cputemp()

        if temp <= d_temp:
            t = temp
            cur_speed = 0
            fan(cur_speed)

        log_out = 'Current T = {0}\xb0C, Previus T = {1}\xb0C, ' \
                  'Speed = {2}, Hysteresis = {3}\xb0C, \u0394H = {5}\xb0C, ' \
                  'Turn off T = {4}\xb0C'.format(temp, t, cur_speed, hys,
                                                 d_temp, temp-t)
        if args['daemon'] and args['verbose']:
            logger.debug('[{0}] {1}'.format(dt.now(), log_out))
        elif args['verbose']:
            print('[{0}] {1}'.format(dt.now(), log_out))

        time.sleep(ref)

daemon = Daemonize(app='raspberry_fan', pid=pid, action=main, keep_fds=keep_fds)

if args['daemon']:
    daemon.start()
else:
    main()
