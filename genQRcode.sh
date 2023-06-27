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

input_file=""
output_folder="qrcodes"
target_size=145

while getopts ":f:w:" opt; do
  case $opt in
    f)
      input_file="$OPTARG"
      ;;
    w)
      output_folder="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

if [ -z "$input_file" ]; then
  echo -e $red"[*] genQRcode.sh -f <input_file> -w <output_folder>!..."$default""
  exit 1
fi

mkdir -p "$output_folder"

while IFS= read -r name || [[ -n "$name" ]]; do
  clean_name=$(echo "$name" | tr -dc '[:alnum:]-_')
  output_file="$output_folder/$clean_name.png"
  qrencode -s $((target_size / 25)) -o "$output_file" -t PNG -l H -i -8 "$name"
  echo "QR code generated for '$name' successfully!"
done < "$input_file"

echo "All QR codes generated successfully!"
