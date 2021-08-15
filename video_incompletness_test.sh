#!/usr/bin/bash
file_name=/home/home/Videos/incompleted_vdieos_names.txt
counter=0

echo -e "#################################\nFollowing files are incomplete\n#################################\n" > $file_name

cd /home/home/Videos/

for i in `ls *.mp4 *.mkv *.webm 2>/dev/null`;  do 
	# ffmpeg -v error -sseof -60 -i $i -f null - 2>test.log
	# if [[ `cat test.log | wc -l` -gt 0 ]] ; then 
	if [[ `ffmpeg -v error -sseof -60 -i $i -f null - 2>&1 > /dev/null | wc -l` -gt 0 ]] ; then
		let "counter+=1"
		echo /home/home/Videos/$i >> $file_name
	fi
done

if [[ $counter -eq 0 ]]; then
	echo -e "\n-------- Tested `ls *.mp4 *.mkv *.webm 2>/dev/null | wc -l` videos, but no incomplete video found ----------\n"
else
	cat $file_name
	echo
fi