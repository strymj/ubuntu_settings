#!/bin/bash

_help ()
{
	echo "Usage: sh redshift_brightness.sh [options] [args]"
	echo "-c   Set command."
	echo "-t   Set timeout. (default: 10[s])"
	echo "-h   Show this help message."
}

password=""
timeout=10
command=""

while getopts "c:t:h" OPT; do
	case ${OPT} in
		c) command=${OPTARG};;
		t) timeout=${OPTARG};;
		t) _help && exit 0;;
	esac
done

expect -c "
set timeout ${timeout}
spawn sudo ${command}
expect \"sudo\"
send \"${password}\n\"
"
echo "\n"

exit 0
