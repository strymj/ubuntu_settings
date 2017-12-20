#!/bin/sh

_usage()
{
	echo "Error!"
	echo "Usage : $0 <image path> <extension> (quality)"
	exit 0
}

if [ $# = 2 ]; then
	convert $1 ${1%\.*}.$2
elif [ $# = 3 ]; then
	convert $1 -quality $3 ${1%\.*}.$2
else
	_usage
fi

exit 0
