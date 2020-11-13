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

if [[ $EUID -ne 0 ]]; then
        echo -e $red"You do not have admin privilegies, execute the script as root!!!"$default""
        exit 1
fi

# Windows and Resolution
function autoResolution {
	nx=4
	detectedresolution=$(xdpyinfo | grep -A 3 "screen #0" | grep dimensions | tr -s " " | cut -d" " -f 3)
	echo -ne $blue"[+] Screen Resolution ->"$default
	echo -e $detectedresolution
	screenwidth=${detectedresolution%x*}
	screenheight=${detectedresolution#*x}
	screenwidth=$(($screenwidth/(($nx*3))-8))
	screenheight=$(($screenheight/(($nx*5))-14))
	resolution="${screenwidth}x${screenheight}"
	TOPLEFT="-geometry $resolution+0+0"
	TOPRIGHT="-geometry $resolution-0+0"
	BOTTOMLEFT="-geometry $resolution+0-0"
	BOTTOMRIGHT="-geometry $resolution-0-0"
	MIDDLELEFT="-geometry  100x14+0+$screenheight"
	MIDDLERIGHT="-geometry 100x14-0+$screenheight"
}
autoResolution

sudo echo 1 > /proc/sys/net/ipv4/ip_forward
xterm $TOPLEFT -T HTOP -e htop &
xterm $TOPRIGHT -T SNORT -e snort -A console -q -c /etc/snort/snort.conf -i eth0 &
xterm $BOTTOMLEFT -T NETSTAT -e ./chkSys.sh &
xterm $BOTTOMRIGHT -T TCPDUMP -e tcpdump port 8080 -A &

while true; do
	echo -ne $yellow"[*] Do you want to finnish? "$default
	read WISH

	if [ $WISH = "y" ]; then
		sudo killall xterm
		echo -e $red"[+] Clean up successful..."
		echo -e $red"[+] Thank you for using Monitors.sh script, Good Bye..."
		exit
	fi
done
exit