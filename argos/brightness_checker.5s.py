#!/usr/bin/python

import subprocess
import re

brightness_step = 0.1
gamma_default = "1.0:1.0:1.0"

conf1 = "terminal=false refresh=true"
conf2 = "font=Ubuntu\ Mono trim=false"

bright_cmd = "xrandr --verbose | grep -m 1 rightness | awk '{ print $2 }'"
gamma_cmd = "xrandr --verbose | grep -m 1 amma | awk '{ print $2}'"

now_brightness = subprocess.check_output(bright_cmd, shell=True)
now_gamma = subprocess.check_output(gamma_cmd, shell=True).strip()

if now_gamma == gamma_default:
    now_temp = "6500"
    target_temp = "5000"
    rs_status = "Off"
else:
    now_temp = "5000"
    target_temp = "6500"
    rs_status = "On"

print ":bulb:" 
print "---"
print ":bulb:     Brightness ", float(now_brightness), "|" , conf2
print ":bulb:     + up   |", conf1, conf2, "bash=redshift\ -O\ " +now_temp +"\ -b\ " +str(float(now_brightness)+brightness_step)
print ":bulb:     - down |", conf1, conf2, "bash=redshift\ -O\ " +now_temp +"\ -b\ " +str(float(now_brightness)-brightness_step)
print "---"
print ":computer:     RedShift", rs_status, "|", conf1, conf2, "bash=redshift\ -O\ " +target_temp +"\ -b\ " +now_brightness
