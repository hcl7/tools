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

echo -e $red"[+] Creating Profile..."
OLDUSBLIST=$(lsusb)
CAMERAPATH=$(echo /run/user/$UID/gvfs/mtp*/*/DCIM/Camera)
DOWNLOADPATH=$(echo /run/user/$UID/gvfs/mtp*/*/Download)
LOCALPATH=$(pwd)
echo -e $blue"$LOCALPATH"$default
echo -e $blue"$OLDUSBLIST"$default
echo -e $blue"$LOCALPATH"$default
echo -e $blue"$Done!!!"$default

echo -ne $red"[+] Counting Usb Devices->"
usbcount=$(lsusb | wc -l)
echo -e $blue"$usbcount"$default
newcount=$usbcount
echo -ne $red"[+] Wait Until Phone is Connected->"$default
while [ $usbcount -eq $newcount ]; do	
	newcount=$(lsusb | wc -l)
done

sudo gvfs-mount -li | awk -F= '{if(index($2,"mtp") == 1)system("gvfs-mount "$2)}'
echo -e $blue"Mouted!!!"$default

echo -ne $red"[+] Waiting Until->"$default
while [ ! -d /run/user/$UID/gvfs/mtp*/*/DCIM ]; do 
	:  > /dev/null
done
echo -e $blue"Unlocked!!!"$default
echo -e $red"[+] Navigating files..."$default
ls -aril $CAMERAPATH
ls -aril $DOWNLOADPATH
echo -e $red"[+] Copying files..."$default
mkdir $LOCALPATH/$UID
cp -R $CAMERAPATH $LOCALPATH/$UID
cp -R $DOWNLOADPATH $LOCALPATH/$UID
echo -e $blue"Done!!!"$default
