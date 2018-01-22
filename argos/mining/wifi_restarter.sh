#!/bin/bash

restart_wifi_sh="${HOME}/ubuntu_settings/scripts/restart_wifi.sh"
check_interval=70

while :
do
	sleep ${check_interval}
	if [ -f $1 ]; then
		output=$(tail -n $2 $1 | grep -E yay\|retry | tail -n 1)
		# echo "file exist and output is ${output}"
		if [ ${#output} -ne 0 ]; then
			result=$(echo ${output} | awk '{print $3}')
			if [ ${result} != "accepted:" ]; then
				# echo "restarting wifi ..."
				${restart_wifi_sh}
			fi
		fi
	fi
done
