#!/usr/bin/python

import subprocess
import re

brightness_step = 0.1
gamma_default = "1.0:1.0:1.0"
gamma_target = "1.0:0.85:0.8"

xrandr_cmd = "xrandr --verbose"
xrandr_result = subprocess.check_output(xrandr_cmd, shell=True).split("\n")

conf = "terminal=false refresh=true"
font = "font=Ubuntu\ Mono trim=false"

disp_list = []
brightness_list = []
gamma_list = []
for i in range(len(xrandr_result)) :
    split_result = xrandr_result[i].split()
    if 2 <= len(split_result) and split_result[1] == "connected" :
        disp_list.append(split_result[0])
    if 2 <= len(split_result) and split_result[0] == "Brightness:" :
        brightness_list.append(split_result[1])
    if 2 <= len(split_result) and split_result[0] == "Gamma:" :
        gamma_list.append(split_result[1])


print ":bulb:" 
for i in range(len(disp_list)) :
    xrandr_bright = "bash=xrandr\ --output\ " +disp_list[i] +"\ --brightness\ "
    if gamma_list[i] == gamma_default :
        rs_status = "Off"
        rs_switch = "On"
        rs_target = gamma_target
    else :
        rs_status = "On"
        rs_switch = "Off"
        rs_target = gamma_default
    disp_status = disp_list[i] +"   :bulb: " +brightness_list[i] +"   :computer: " +rs_status
    print "---"
    print  disp_status, "|", conf, font, xrandr_bright +"1.0\ --gamma\ " +gamma_default
    print ":bulb:     Brightness up   |", conf, font, xrandr_bright +str(float(brightness_list[i])+brightness_step)
    print ":bulb:     Brightness down |", conf, font, xrandr_bright +str(float(brightness_list[i])-brightness_step)
    print ":bulb:     RedShift", rs_switch, "|", conf, font, xrandr_bright +brightness_list[i] +"\ --gamma\ " +rs_target

# print len(disp_list), disp_list
# print len(gamma_list), gamma_list
# print len(brightness_list), brightness_list
