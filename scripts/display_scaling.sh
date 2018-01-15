#!/bin/bash
echo "##### display_scaling.sh #####"

main="eDP-1"
hdmi="HDMI-1"
hdmiStatus=$(xrandr | grep ${hdmi} | awk '{ print $2 }')

_help ()
{
	echo "Usage: sh display_scaling.sh [options] [args]"
	echo "-h   Show this help message."
	echo "-s <scaling ratio>"
}

# scale=1
scale=1.5
# scale=2

while getopts "s:h" OPT; do
	case ${OPT} in
		s) scale=${OPTARG};;
		h) _help && exit;;
	esac
done


if [ $# -eq 1 ]; then
	scale=$1
fi

# get_display_size <disp_name> <width|height|offset_x|offset_y>
get_display_size ()
{
	hdmiSize=$(xrandr | grep $1 | awk '{ print $3 }')
	if [ ${hdmiSize} = "primary" ]; then
		hdmiSize=$(xrandr | grep $1 | awk '{ print $4 }')
	fi
	hdmiWH=${hdmiSize%%+*}
	hdmiXY=${hdmiSize#*+}

	case $2 in
		"width")
			echo ${hdmiWH%%x*};;
		"height")
			echo ${hdmiWH##*x};;
		"offset_x")
			echo ${hdmiXY%%+*};;
		"offset_y")
			echo ${hdmiXY##*+};;
	esac
}

if [ ${hdmiStatus} = "disconnected" ]; then
	echo "HDMI disconnected."
else
	echo "HDMI connected."
	xrandr --output ${hdmi} --scale ${scale}x${scale}
	# xrandr --output ${main} --scale 1x1
	mainWidth=$(get_display_size ${main} width)
	hdmiWidth=$(get_display_size ${hdmi} width)
	hdmiHeight=$(get_display_size ${hdmi} height)
	if [ ${hdmiWidth} -gt ${mainWidth} ]; then
		hdmiOffsetX=0
		mainOffsetX=$(((${hdmiWidth}-${mainWidth})/2))
	else
		hdmiOffsetX=$(((${mainWidth}-${hdmiWidth})/2))
		mainOffsetX=0
	fi	

	sleep 1
	xrandr --output ${hdmi} --pos ${hdmiOffsetX}x0
	echo "Setting ${hdmi} pos."
	sleep 3
	xrandr --output ${main} --pos ${mainOffsetX}x${hdmiHeight##*x}
	echo "Setting ${main} pos."
	sleep 3

	echo "Scaling x${scale}"
	echo "${hdmi} offset ${hdmiOffsetX}+0"
	echo "${main} offset ${mainOffsetX}+${hdmiHeight##*x}"

fi

exit 0
