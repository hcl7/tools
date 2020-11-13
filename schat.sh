#!/bin/bash

#Colors
white="\033[1;37m"
grey="\033[0;37m"
purple="\033[0;35m"
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
Purple="\033[0;35m"
Cyan="\033[0;36m"
Cafe="\033[0;33m"
Fiuscha="\033[0;35m"
blue="\033[1;34m"
transparent="\e[0m"

# Design
function top(){
	clear
	sleep 0.1 && echo -e "$blue "
 		sleep 0.1 && echo -e "	 ___  _____   _____ _ __  "
		sleep 0.1 && echo -e "	/ __|/ _ \ \ / / _ \ |_ \ "
		sleep 0.1 && echo -e "	\__ \  __/\ V /  __/ | | |"
		sleep 0.1 && echo -e "	|___/\___| \_/ \___|_| |_|"
                         
        sleep 0.1 && echo -e "$transparent"
	echo
	echo
}

top

if [ $# -lt 1 ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
	echo -e $green"["$red"./server.sh <port>"$green"]"
	exit 1
fi

PORT=$1
while IFS= read -r MSG; do python progressivecipher.py -e "$MSG"; done | nc -vv -l -p "$PORT" | while IFS= read -r REC; do echo "#>: $(python progressivecipher.py -d "$REC")"; done
