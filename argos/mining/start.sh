#!/bin/bash

# $1 log file
# $2 number of threads (optional)

cmd="${HOME}/Documents/mining/cpuminer/minerd -a yescrypt -o stratum+tcp://bitzenypool.work:19666 -u freesky.freesky -p 9j260a95yten9eh"

# remove log file
rm $1 -rf

# start mining with log
if [ $# -ge 2 ]; then
	cmd="${cmd} -t $2"
fi

${cmd} 2> $1
