#!/bin/bash

not_running_msg="not_running"

_help ()
{
	echo "Usage: sh $0.sh [options] [args]"
	echo "-c <process name>"
	echo "     Check process is running or not."
	echo "     If the process is running, returns processID."
	echo "     Otherwise, returns \"${not_running_msg}\"."
	echo "-k <process name>"
	echo "     Kill the process."
	echo "-h   Show this help message."
}

_process_check ()
{
	psID=$(ps -a | grep $1 | awk '{print $1}')
	if [ ${#psID} -ne 0 ]; then
		echo ${psID}
	else
		echo ${not_running_msg}
	fi
}

_kill_process ()
{
	n_ps=$(ps -a | grep -c $1)
	if [ ${n_ps} -eq 1 ]; then
		psID=$(ps -a | grep $1 | awk '{print $1}')
		kill ${psID}
	else
		echo "Found multi process."
	fi
}

while getopts "k:c:h" OPT; do
	case ${OPT} in
		c) _process_check ${OPTARG};;
		k) _kill_process ${OPTARG};;
		h) _help && exit;;
	esac
done
