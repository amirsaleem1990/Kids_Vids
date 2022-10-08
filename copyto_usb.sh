#!/usr/bin/bash
cd /home/home/Videos/
sleep 1s
echo
lsblk -e7
echo 
read -p "Enter usb mount point (eg: /home/home/usb): " usb_mounted_at
echo
read -p "Enter dev (eg: /dev/sdc): " dev_
echo 

for file in $(cat last_copied_files); do
	touch "$file"
done

rm -f last_copied_files.txt

IFS=$'\n'
for file in $(
				for i in `ls` ; do \
					if [[ $(echo $i | grep -o '\.' | wc -l) -eq 1 ]] ; then 
						echo $i
					fi
				done
			); do 
	if [[ $(df $dev_ | sed 's/\ \{2,\}/,/g' | cut -d, -f4 | cut -d\% -f1) -gt 95 ]] ; then
		exit
	fi
	cp "$file" "$usb_mounted_at" -v
	echo "$file" >> last_copied_files.txt
done