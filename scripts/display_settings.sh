#!/bin/bash
echo "##### display_settings.sh #####"

brightness=$(xrandr --verbose | grep -m 1 rightness | awk '{ print $2 }')
brightness_max=1.0
brightness_min=0.1
brightness_step=0.1    
brightness_mine=0.4

redshift_on=5000
redshift_off=6500

gamma=$(xrandr --verbose | grep -m 1 amma | awk '{ print $2}')
gamma_default="1.0:1.0:1.0"
redshift=${redshift_off}
if [ ${gamma} != ${gamma_default} ]; then
	redshift=${redshift_on}
fi


_help ()
{
	echo "Usage: sh redshift_brightness.sh [options] [args]"
	echo "-v   Show current value."
	echo "-d   Default redshift and brightness value."
	echo "-m   My favorite redshift and brightness value."
	echo "-r <redshift arg>"
	echo "     on      --- Turn redshift on."
	echo "     off     --- Turn redshift off."
	echo "     switch  --- Switch redshift on and off."
	echo "-b <brightness arg>"
	echo "     [value] --- Set brightness(0.1 ~ 1.0)."
	echo "     inc, +  --- Increment brightness by ${brightness_step}."
	echo "     dec, -  --- Decrement brightness by ${brightness_step}."
	echo "     default --- Default brightness(1.0)."
	echo "-h   Show this help message."
}


show_current_value ()
{
	echo "Redshift temp : ${redshift} K"
	echo "Brightness : ${brightness}"
}


redshift_fcn ()
{
	case $1 in
		"on")
			echo "[Redshift on]"
			redshift=${redshift_on};;
		"off")
			echo "[Redshift off]"
			redshift=${redshift_off};;
		"switch")
			echo "[Redshift switch]"
			if [ ${redshift} -eq ${redshift_on} ]; then
				redshift=${redshift_off}
			else
				redshift=${redshift_on}
			fi;;
		?*)
			_help && exit;;
	esac
}


brightness_range_check ()
{
	if [ `echo "${brightness} < ${brightness_min}" | bc` -eq 1 ]; then
		brightness=${brightness_min}
	elif [ `echo "${brightness_max} < ${brightness}" | bc` -eq 1 ]; then
		brightness=${brightness_max}
	fi
}

brightness_fcn ()
{
	case $1 in
		"inc" | "+")
			echo "[Brightness increment]"
			brightness=$(echo "scale=2; ${brightness} + ${brightness_step}" | bc);;
		"dec" | "-")
			echo "[Brightness decrement]"
			brightness=$(echo "scale=2; ${brightness} - ${brightness_step}" | bc);;
		"default")
			echo "[Default brightness]"
			brightness=${brightness_max};;

		?*)
			brightness=$1;;
	esac

	brightness_range_check ${brightness}
}

set_my_value()
{
	echo "Set default brightness and redshift value."
	redshift=${redshift_on}
	brightness=${brightness_mine}
}

set_default_value()
{
	echo "Set my brightness and redshift value."
	redshift=${redshift_off}
	brightness=${brightness_max}
}

if [ $# = 0 ]; then
	_help && exit
fi

while getopts "b:r:dmhv" OPT; do
	case ${OPT} in
		r) redshift_fcn ${OPTARG};;
		b) brightness_fcn ${OPTARG};;
		d) set_default_value;;
		m) set_my_value;;
		v) show_current_value;;
		h) _help && exit;;
	esac
done

redshift -O ${redshift} -b ${brightness}:${brightness}

exit
