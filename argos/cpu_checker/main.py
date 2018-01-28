#!/usr/bin/python

import unicodedata
import subprocess
import re

cmd = "vmstat 1 2 | tail -n 1"
outlist = re.split(" +", subprocess.check_output(cmd, shell=True))
cpu_usr = int(outlist[13])
cpu_sys = int(outlist[14])
cpu_total = cpu_usr + cpu_sys
if 100 < cpu_total:
    cpu_total = 100

color_ratio = int(31.0 * cpu_total / 100)
color_r =15
color_g = min(15, 31 - color_ratio)
color_b = max(15 - color_ratio, 0)

color_code = "#" + format(color_r, 'x') + format(color_g, 'x') + format(color_b, 'x')

# print "color", color_r, color_g, color_b
print ":computer: | color=" + str(color_code)
print "---"
print ":computer:    Total CPU   ", cpu_total, "% | font=Ubuntu\ Mono"
print ":computer:    - Usr       ", cpu_usr,   "% | font=Ubuntu\ Mono"
print ":computer:    - System    ", cpu_sys,   "% | font=Ubuntu\ Mono"
