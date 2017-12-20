#!/bin/bash

_help ()
{
	echo "Usage: sh redshift_brightness.sh -r <redshift_option> -b <brightness_option>"
	echo "-r <redshift option>"
	echo "    on      --- Turn redshift on."
	echo "    off     --- Turn redshift off."
	echo "    switch  --- Switch redshift on and off."
	echo "-b <brightness option>"
	echo "    +       --- Increment brightness."
	echo "    -       --- Decrement brightness."
	echo "    default --- Default brightness(1.0)."
}

REDSHIFT_NEUTRAL_TEMP=6500
REDSHIFT_TEMP=4500
BRIGHTNESS_MAX=1.0
BRIGHTNESS_MIN=0.1
BRIGHTNESS_STEP=0.1    

# ##### now variable initialize #####
if [ -v ${REDSHIFT_NOW_TEMP} ]; then
	echo "REDSHIFT_NOW_TEMP variable has not set. Temp is set ${REDSHIFT_TEMP} ."
	REDSHIFT_NOW_TEMP=${REDSHIFT_NEUTRAL_TEMP}
fi

if [ -v ${NOW_BRIGHTNESS} ]; then
	echo "NOW_BRIGHTNESS variable has not set."
	NOW_BRIGHTNESS=1.0
fi

# ##### arg -r #####
redshift_switch ()
{
	if [ ${REDSHIFT_NOW_TEMP} -eq ${REDSHIFT_NEUTRAL_TEMP} ]; then
		REDSHIFT_NOW_TEMP=${REDSHIFT_TEMP}
	else
		REDSHIFT_NOW_TEMP=${REDSHIFT_NEUTRAL_TEMP}
	fi
}

redshift_fcn ()
{
	case $1 in
		"on")
			echo "Redshift on."
			REDSHIFT_NOW_TEMP=${REDSHIFT_TEMP};;
		"off")
			echo "Redshift off."
			REDSHIFT_NOW_TEMP=${REDSHIFT_NEUTRAL_TEMP};;
		"switch")
			echo "Redshift switch."
			redshift_switch;;
		?*)
			_help;;
	esac

	echo "Now redshift temp is ${REDSHIFT_NOW_TEMP} K."
}


brightness_range_check ()
{
	if [ `echo "${NOW_BRIGHTNESS} < ${BRIGHTNESS_MIN}" | bc` == 1 ]; then
		NOW_BRIGHTNESS=${BRIGHTNESS_MIN}
	elif [ `echo "${BRIGHTNESS_MAX} < ${NOW_BRIGHTNESS}" | bc` == 1 ]; then
		NOW_BRIGHTNESS=${BRIGHTNESS_MAX}
	fi
}

brightness_fcn ()
{
	case $1 in
		"+")
			echo "Brightness increment."
			NOW_BRIGHTNESS=$(echo "scale=1; ${NOW_BRIGHTNESS} + ${BRIGHTNESS_STEP}" | bc);;
		"-")
			echo "Brightness decrement."
			NOW_BRIGHTNESS=$(echo "scale=1; ${NOW_BRIGHTNESS} - ${BRIGHTNESS_STEP}" | bc);;
		"default")
			echo "Default brightness."
			NOW_BRIGHTNESS=${BRIGHTNESS_MAX};;
	esac
	brightness_range_check ${NOW_BRIGHTNESS}

	echo "Now brightness is ${NOW_BRIGHTNESS}."
}

# ##### check options #####
OPTIND=1
while getopts r:b: OPT
do
	case ${OPT} in
		"r") redshift_fcn ${OPTARG};;
		"b") brightness_fcn ${OPTARG};;
	esac
done

redshift -O ${REDSHIFT_NOW_TEMP} -b ${NOW_BRIGHTNESS}:${NOW_BRIGHTNESS}

