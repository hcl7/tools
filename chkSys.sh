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

if [[ $EUID -ne 0 ]]; then
    echo -e $red"You do not have admin privilegies, execute the script as root!!!"$transparent""
    exit 1
fi

#PID=()
#PID=$(ps -ej --no-headers | awk '{print $1}')
while (true); do
	nts=$(netstat -antp | awk '{print $7}' | grep '/' | sed 's/\/.*//')
	echo -e $red"Looking for PIDs!"$transparent
	for i in ${nts}
	do
		lsof -p $i | grep 'bin' &> /dev/null
		if [ $? == 0 ]; then
			echo -ne $green"[+] Result for PID $i ->"$transparent
			lsof -p $i | grep 'bin' | awk '{print $9}'
		fi
	done
	echo -e $blue"Done!!!"$transparent
	sleep 12
	tput cup 8 0 && tput ed
done

