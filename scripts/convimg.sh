#!/bin/sh

_help()
{
	echo "Usage: $0 [options] [args]"
	echo "-i <image>"
	echo "-e <filename extension>"
	echo "-q <quality>"
	echo "-h   Show this help message."
	exit 0
}

size="100%"
quality=100
image="none"
output="none"
extension="none"

while getopts "i:e:q:s:h" OPT; do
	case ${OPT} in
		i) image=${OPTARG};;
		e) extension=${OPTARG};;
		q) quality=${OPTARG};;
		s) size=${OPTARG};;
		h) _help;;
	esac
done

if [ $# -eq 0 ] || [ ${image} = "none" ]; then
	_help
fi

if [ ${extension} = "none" ];then
	output=${image}
else
	output=${image%\.*}.${extension}
fi

convert ${image} -quality ${quality} -resize ${size} ${output}
