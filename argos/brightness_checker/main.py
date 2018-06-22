#!/usr/bin/python

"""Process some integers.

usage: main.py [-r|--redshift <on_off_toggle>] [-b|--brightness <value>] [-d|--default]

options:
    -h --help                 show this help message and exit
    -b --brightness <value>   set brightness (0.1 ~ 1.0, "inc" or "dec")
    -r --redshift <on_off_toggle>    redshift ("on" , "off" or "toggle")
    -d --default              restore default value (brightness : 1.0, redshift : off)
"""

import subprocess
import re
import sys
from docopt import docopt

bright_step = 0.1
gamma_default = "1.0:1.0:1.0"
gamma_target = "1.0:0.8:0.6"
n_shadow = 5
shadow_step = 0.2

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

rs = False

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


# with no args
if len(sys.argv) == 1 :

    if gamma_list[0] != gamma_default :
        print ":bulb: | color=#f80"
    else :
        print ":bulb:"

    for i in range(len(disp_list)) :

        rs = False
        if gamma_list[i] != gamma_default :
            rs = True

        disp_status = disp_list[i] +"   :bulb: " +bright_list[i] +"   :computer: " +getStatus(rs)

        print "---"
        print  disp_status, "|", conf, XRANDR +disp_list[i] +BRIGHT +"1.0" +GAMMA +gamma_default
        # print ":arrow_forward:   Brightness up   |", conf, font, XRANDR +disp_list[i] +BRIGHT +str(float(bright_list[i])+bright_step) +GAMMA +getGamma(rs)
        # print ":arrow_forward:   Brightness down |", conf, font, XRANDR +disp_list[i] +BRIGHT +str(float(bright_list[i])-bright_step) +GAMMA +getGamma(rs)
        print "  Shadow"
        for bright_i in range( n_shadow ):
            show_str = "level " + str( bright_i )
            if bright_i == 0:
                show_str = "off"
            print "--", show_str, "|", conf, XRANDR +disp_list[i] +BRIGHT +str( 1.0 - bright_i * shadow_step ) +GAMMA +getGamma(rs)
        print "  RedShift |", conf, XRANDR +disp_list[i] +BRIGHT +bright_list[i] +GAMMA +getGamma(not rs)


else :
    bright_value = float(bright_list[0]);
    gamma_str = getGamma(gamma_list[0] != gamma_default);

    args = docopt(__doc__)

    arg = args.get('--brightness')
    if len(arg) :
        if arg[0] == "inc" :
            bright_value += bright_step
        elif arg[0] == "dec" :
            bright_value -= bright_step
        else :
            bright_value = float(arg[0])

        if bright_value < 0.1 :
            bright_value = 0.1
        if 1.0 < bright_value :
            bright_value = 1.0

    arg = args.get('--redshift')
    if len(arg) :
        if arg[0] == "on" :
            gamma_str = gamma_target
        elif arg[0] == "off" :
            gamma_str = gamma_default
        elif arg[0] == "toggle" :
            gamma_str = getGamma(gamma_list[0] == gamma_default)

    if args.get('--default') :
        bright_value = 1.0
        gamma_str = gamma_default

    cmd = "xrandr --output " + disp_list[0] + " --brightness " + str(bright_value) + " --gamma " + gamma_str
    # print cmd
    subprocess.check_output(cmd, shell=True)
