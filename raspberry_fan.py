#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

import wiringpi
import time
import argparse

''' Parsing args '''
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--hys', default=5, type=int,
                    help='change hysteresis')
parser.add_argument('-r', '--refresh', default=5, type=int,
                    help='default refresh time')
parser.add_argument('-m', '--max_temp', default=70, type=int,
                    help='maximum temperature threshold')
parser.add_argument('-d', '--disable_temp', default=47, type=int,
                    help='fan disable temp')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print output')
args = parser.parse_args()
args = vars(args)

''' Assing vars from cmdline '''
''' and test values          '''
hys = args['hys']
if hys < 1 or hys > 10:
    hys = 5
    print("Hysteresis value not valid! Use default value (5)!")

ref = args['refresh']
if ref < 1 or ref > 30:
    ref = 5
    print("Refresh rate value not valid! Use default value (5)!")

m_temp = args['max_temp']
if m_temp < 60 or m_temp > 80:
    m_temp = 70
    print("Maximum temperature threshold value not valid! Use default value (70)!")

d_temp = args['disable_temp']
if d_temp < 40 or d_temp > 55:
    d_temp = 47
    print("Disable fan value not valid! Use default value (47)!")

''' Init temperature and fan vars '''
fan_pin  = 1
temp = 0
t = 0

t_range = 640 // (m_temp-30)        # Create step speed list

''' Create table of temp and fan speed '''
temp_table = [x for x in range(30, m_temp)]
speed_table = [x for x in range(384, 1024, t_range)]
dict_table = dict(zip(temp_table, speed_table))

wiringpi.wiringPiSetup()
wiringpi.pinMode(fan_pin, 2)
wiringpi.pwmWrite(fan_pin, 0)


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

print('\nFAN CONTROL: Hysteresis: {0}\xb0C, Refresh rate: {1} sec, \
Max temperature treshold: {2}\xb0C, \
Disable fan at {3}\xb0C\n'.format(hys, ref, m_temp, d_temp))

while True:
    temp = cputemp()
    if temp >= t+hys or temp <= t-hys or t == 0:
        fan(dict_table[temp])
        t = cputemp()
    if temp <= d_temp:
        t = temp
        fan(0)
    if args['verbose']:
        print('Current = {0}\xb0C, Previus = {1}\xb0C, \
Speed value = {2}, Hyteresys = {3}\xb0C'.format(temp, t, dict_table[temp], hys))
    time.sleep(ref)
