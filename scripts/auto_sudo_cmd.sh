#!/bin/sh

_help ()
{
	echo "Usage: sh redshift_brightness.sh [options] [args]"
	echo "-c   Set command."
	echo "-t   Set timeout. (default: 10[s])"
	echo "-h   Show this help message."
}

timeout=10
command=""
password="Strymj_7290"

while getopts "c:p:t:h" OPT; do case ${OPT} in
		t) timeout=${OPTARG};;
		c) command=${OPTARG};;
		t) _help && exit 0;;
	esac
done

expect -c "
	set timeout ${timeout}
	spawn ${command}
	expect \"sudo\"
	send \"${password}\n\"
	expect \"$\"
	exit 0
"

exit 0
