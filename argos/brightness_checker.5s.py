#!/usr/bin/python

import subprocess
import re

brightness_step = 0.1
gamma_default = "1.0:1.0:1.0"

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

conf = "terminal=false refresh=true"
font = "font=Ubuntu\ Mono trim=false"

print ":bulb:" 
print "---"
print ":bulb:     Brightness ", float(now_brightness), "|" , font
print ":bulb:     + up   |", conf, font, "bash=redshift\ -O\ " +now_temp +"\ -b\ " +str(float(now_brightness)+brightness_step)
print ":bulb:     - down |", conf, font, "bash=redshift\ -O\ " +now_temp +"\ -b\ " +str(float(now_brightness)-brightness_step)
print "---"
print ":computer:     RedShift", rs_status, "|", conf, font, "bash=redshift\ -O\ " +target_temp +"\ -b\ " +now_brightness
print "---"
print ":repeat:     Restore Default |", conf, font, "bash=redshift\ -O\ 6500\ -b\ 1.0"
print ":bust_in_silhouette:     My Setting |", conf, font, "bash=redshift\ -O\ 5000\ -b\ 0.4"
