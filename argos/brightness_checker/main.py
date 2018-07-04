#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

usage:
    main.py [-r|--redshift <value>] [-b|--brightness <value>] [-d|--default]

options:
    -h --help                 show this help message and exit
    -b --brightness <value>   set brightness (0.1 ~ 1.0, "inc" or "dec")
    -r --redshift <value>     redshift ["on" , "off" , "toggle"]
    -d --default              restore default value (brightness : 1.0, redshift : off)

"""

import subprocess
import re, sys, os
from docopt import docopt

# print ":bulb:"
print ":computer:"
if os.environ.get( "ARGOS_MENU_OPEN" ) != "true" and len( sys.argv ) == 1:
    sys.exit(0)


gamma_default = "1.0:1.0:1.0"
gamma_target = "1.0:0.8:0.6"
n_shadow = 5
shadow_step = 0.15


xrandr_cmd = "xrandr --verbose"
xrandr_result = subprocess.check_output( xrandr_cmd, shell=True ).split("\n")

conf = "terminal=false refresh=true"
font = "font=Ubuntu\ Mono trim=false"
font = "font=Takao\ Pゴシック\ Regular trim=false"

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

    # if gamma_list[0] != gamma_default :
    #     print ":bulb: | color=#f80"
    # else :
    #     print ":bulb:"

    for i in range(len(disp_list)) :

        rs = False
        if gamma_list[i] != gamma_default :
            rs = True

        # disp_status = disp_list[i] +"   :bulb: " +bright_list[i] +"   :computer: " +getStatus(rs)
        disp_status = "<span weight='bold'>" + ":computer:   " + disp_list[i] + "</span>"
        
        current_bright_i = 0
        for bright_i in range( n_shadow ):
            if 1.0 - bright_i * shadow_step <= float( bright_list[i] ):
                current_bright_i = bright_i
                break

        print "---"
        print  disp_status, "|", conf, XRANDR +disp_list[i] +BRIGHT +"1.0" +GAMMA +gamma_default
        print "  Shadow"
        color = ""
        for bright_i in range( n_shadow ):
            show_str = "level " + str( bright_i )
            color = "color=#AAA"
            if bright_i == 0:
                show_str = "off"
            if bright_i == current_bright_i:
                color = "color=#FFF"
            print "--", show_str, "|", color, conf, XRANDR +disp_list[i] +BRIGHT +str( 1.0 - bright_i * shadow_step ) +GAMMA +getGamma(rs)
        print "  RedShift"
        if rs:
            print "-- off |", "color=#AAA", conf, XRANDR +disp_list[i] +BRIGHT +bright_list[i] +GAMMA +getGamma(not rs)
            print "-- on |" , "color=#FFF"
        else:
            print "-- off |", "color=#FFF"
            print "-- on |" , "color=#AAA", conf, XRANDR +disp_list[i] +BRIGHT +bright_list[i] +GAMMA +getGamma(not rs)


else :
    bright_value = float(bright_list[0]);
    gamma_str = getGamma(gamma_list[0] != gamma_default);

    args = docopt(__doc__)
    print( args )

    arg = args.get('--brightness')
    if len(arg) :
        if arg[0] == "inc" :
            bright_value += shadow_step
        elif arg[0] == "dec" :
            bright_value -= shadow_step
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
