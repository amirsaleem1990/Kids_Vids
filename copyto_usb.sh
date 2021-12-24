#!/usr/bin/bash
cd /home/home/Videos/
sleep 1s
echo
lsblk -e7
echo 
read -p "Enter usb mount point (eg: /home/home/usb): " usb_mounted_at
echo
mv $(for i in `ls` ; do \
		if [[ $(echo $i | grep -o '\.' | wc -l) -eq 1 ]] ; then 
			echo $i
		fi
	done
	) "$usb_mounted_at" -v