#!/usr/bin/python

import subprocess
import re

bright_step = 0.1
gamma_default = "1.0:1.0:1.0"
gamma_target = "1.8:0.8:0.6"

xrandr_cmd = "xrandr --verbose"
xrandr_result = subprocess.check_output(xrandr_cmd, shell=True).split("\n")

conf = "terminal=false refresh=true"
font = "font=Ubuntu\ Mono trim=false"

disp_list = []
bright_list = []
gamma_list = []
for i in range(len(xrandr_result)) :
    split_result = xrandr_result[i].split()
    if 2 <= len(split_result) and split_result[1] == "connected" :
        disp_list.append(split_result[0])
    if 2 <= len(split_result) and split_result[0] == "Brightness:" :
        bright_list.append(split_result[1])
    if 2 <= len(split_result) and split_result[0] == "Gamma:" :
        gamma_list.append(split_result[1])

XRANDR = "bash=xrandr\ --output\ "
BRIGHT = "\ --brightness\ "
GAMMA = "\ --gamma\ "

def getGamma(is_redshift):
    if is_redshift :
        return gamma_target
    else :
        return gamma_default

def getStatus(is_redshift) :
    if is_redshift :
        return "On"
    else :
        return "Off"


print ":bulb:" 
for i in range(len(disp_list)) :
    if gamma_list[i] == gamma_default :
        rs = False
    else :
        rs = True
    disp_status = disp_list[i] +"   :bulb: " +bright_list[i] +"   :computer: " +getStatus(rs)

    print "---"
    print  disp_status, "|", conf, font, XRANDR +disp_list[i] +BRIGHT +"1.0" +GAMMA +gamma_default
    print ":arrow_forward:   Brightness up   |", conf, font, XRANDR +disp_list[i] +BRIGHT +str(float(bright_list[i])+bright_step) +GAMMA +getGamma(rs)
    print ":arrow_forward:   Brightness down |", conf, font, XRANDR +disp_list[i] +BRIGHT +str(float(bright_list[i])-bright_step) +GAMMA +getGamma(rs)
    print ":arrow_forward:   RedShift", getStatus(not rs), "|", conf, font, XRANDR +disp_list[i] +BRIGHT +bright_list[i] +GAMMA +getGamma(not rs)

# print len(disp_list), disp_list
# print len(gamma_list), gamma_list
# print len(bright_list), bright_list
