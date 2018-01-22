#!/bin/bash

# $1 ps_util_sh
# $2 log_file
# $3 old_log_file

# kill mining and restarter process
$1 -k minerd
$1 -k wifi_restarter

# rename log file
mv $2 $3

