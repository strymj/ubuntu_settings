#!/bin/bash

# ps_minerd=$(ps -a | grep -v grep | grep minerd | awk '{print $1}')
# ps_wifi=$(ps -a | grep -v grep | grep wifi_restarter | awk '{print $1}')
start_sh="${HOME}/ubuntu_settings/argos/mining/start.sh"
stop_sh="${HOME}/ubuntu_settings/argos/mining/stop.sh"
restarter_sh="${HOME}/ubuntu_settings/argos/mining/wifi_restarter.sh"
ps_util_sh="${HOME}/ubuntu_settings/argos/mining/ps_util.sh"
log_file="${HOME}/.mining.log"
old_log_file="${HOME}/.mining_old.log"
nline_log=100
minerd_status=$(${ps_util_sh} -c minerd)
restarter_status=$(${ps_util_sh} -c wifi_restarter)

pict_ready="⛑"
pict_mining="⛑"
pict_warn="⚠"
pict_pic="🔨"
pict_log="📘"
pict_wifi="🔁"
pict_sleep="💤"

thumbnail="init"

# echo $(${ps_util_sh} -c minerd)

# has not launch minerd process
if [ ${minerd_status} = "not_running" ]; then
	thumbnail="${pict_ready} zzz"
else

	# no log file
	if [ ! -f ${log_file} ]; then
		thumbnail="${pict_mining} no log"
	else

		# log file is empty
		output=$(tail -n ${nline_log} ${log_file} | grep -E yay\|retry | tail -n 1)
		if [ ${#output} -eq 0 ]; then
			thumbnail="${pict_mining} starting..."
		else

			# now mining
			result=$(echo ${output} | awk '{print $3}')
			if [ ${result} = "accepted:" ]; then
				power=$(echo ${output} | awk '{print $6}')
				thumbnail="${pict_mining} ${power} khps"
			else
				thumbnail="${pict_warn} error"
				${restart_wifi_sh}
			fi

		fi

	fi

fi

if [ ${restarter_status} != "not_running" ]; then
	thumbnail="${pict_wifi} ${thumbnail}"
fi

echo -e ${thumbnail}
echo "---"
if [ ${minerd_status} = "not_running" ]; then
	echo "${pict_pic}  start mining | bash=${start_sh} param1=${log_file} param2=6 terminal=false refresh=true"
	echo "${pict_log}  see logfile | bash=tail param1=-n param2=${nline_log} param3=${old_log_file} terminal=true"
else
	# echo "${pict_pic}  stop mining | terminal=false bash=kill param1=-SIGINT param2=${ps_minerd} reflesh=true"
	echo "${pict_pic}  stop mining | bash=${stop_sh} param1=${ps_util_sh} param2=${log_file} param3=${old_log_file} terminal=false refresh=true"
	echo "${pict_log}  see logfile | bash=tail param1=-n param2=${nline_log} param3=${log_file} terminal=true"
fi

if [ ${restarter_status} = "not_running" ]; then
	echo "${pict_wifi}  restarter sleeping | bash=${restarter_sh} param1=${log_file} param2=${nline_log} terminal=false refresh=true"
else
	echo "${pict_wifi}  restarter working | bash=${ps_util_sh} param1=-k param2=wifi_restarter terminal=false refresh=true"
fi
