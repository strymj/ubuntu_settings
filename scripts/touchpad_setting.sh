#!/bin/bash

sleep 5
synclient VertScrollDelta=-350
synclient HorizScrollDelta=-350
synclient VertEdgeScroll=false
synclient HorizEdgeScroll=false
synclient MinSpeed=1.00
synclient MaxSpeed=7.00
synclient PalmDetect=1
synclient HorizTwoFingerScroll=1
./ubuntu_settings/libinput-gestures/libinput-gestures
exit 0
