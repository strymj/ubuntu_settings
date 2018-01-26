#!/bin/bash

icon_pc="🖳"
icon_graph="📈"
font="Ubuntu\ Mono"

vmstat_result=$(vmstat 1 2 | tail -n 1)

usr_cpu=$(echo ${vmstat_result} | awk '{print $13}')
sys_cpu=$(echo ${vmstat_result} | awk '{print $14}')
total_cpu=$(( ${usr_cpu} + ${sys_cpu} ))
if [ ${total_cpu} -gt 100 ]; then
	${total_cpu}=100
fi

echo "${icon_pc}  ${total_cpu} %"
echo "---"
echo "${icon_pc}     User     <span weight='bold'>${usr_cpu}</span> % | font=${font}"
echo "${icon_pc}     System   <span weight='bold'>${sys_cpu}</span> % | font=${font}"
