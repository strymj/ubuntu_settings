#!/usr/bin/python

import subprocess
import re
import os

logfile = os.environ['HOME'] + "/.mining.log"
minerd = os.environ['HOME'] + "/Documents/cpuminer/minerd"
bright_cmd = "xrandr --verbose | grep -m 1 rightness | awk '{ print $2 }'"
minerd_pid = subprocess.check_output("ps -a | grep minerd | awk '{print $1}'", shell=True).strip()


if minerd_pid == "" :
    color = "#fff"
    status_output = "Sleeping |"
    # switch_output = ":runner:   - Start Mining | bash=rm\ -rf\ " +logfile +"\ &&\ " +minerd +"\ -a\ yescrypt\ -o\ stratum+tcp://bitzenypool.work:19666\ -u\ freesky.freesky\ -p\ 9j260a95yten9eh\ 2>\ " +logfile
    switch_output = ":runner:   - Start Mining | bash=" +minerd +"\ -a\ yescrypt\ -o\ stratum+tcp://bitzenypool.work:19666\ -u\ freesky.freesky\ -p\ 9j260a95yten9eh\ 2>\ " +logfile
else :
    switch_output = ":zzz:   - Stop Mining | bash=kill\ " +minerd_pid
    if os.path.exists(logfile) :
        status_list = subprocess.check_output("tail -n 100 "+logfile+" | grep -E yay\|retry | tail -n 1", shell=True).split(" ")
        if 3 <= len(status_list) and status_list[2] == "accepted:" :
            color = "#0f0"
            status_output = status_list[5] +" khash/s |"
        else:
            color = "#ff0"
            status_output = "Starting... |"
    else :
        status_output = "No Logfile |"
        color = "#00f"

if os.path.exists(logfile) :
    log_output = "See Logfile | bash=tail\ -n\ 100\ " +logfile
else :
    log_output = "No Logfile |"


font = "font=Ubuntu\ Mono trim=false"
print ":moneybag: | color=" +color
print "---"
print ":moneybag:   " +status_output, font
print switch_output, font, "terminal=false refresh=true"
print ":books:   - " +log_output, font
