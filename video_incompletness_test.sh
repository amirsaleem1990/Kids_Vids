#!/usr/bin/bash

vids_removed=0
size_removed=0
echo -e "\nMake sure that /home/amir/github/Kids_Vids/mapping.pkl is not used by ANY process\npress ANY key when you ready: "
read _

echo -e '
Select your option:
    1- Get input from user before DELETION of ANY incomplete video
    2- Use one action for all incomplete videos
option #: '
read ans_2

if [[ $ans_2 -eq 2 ]]; then
	echo -e '
Choose your action:
    1-Delete
    2-Keep
    '
	read action_
fi

cd /home/home/Videos/

for vid in `ls *.mp4 *.mkv *.webm 2>/dev/null`;  do 
	# ffmpeg -v error -sseof -60 -i $i -f null - 2>test.log
	# if [[ `cat test.log | wc -l` -gt 0 ]] ; then 
	if [[ `ffmpeg -v error -sseof -60 -i $vid -f null - 2>&1 > /dev/null | wc -l` -gt 0 ]] ; then
		# let "counter+=1"
		# echo /home/home/Videos/$i >> $file_name
		/home/amir/github/Kids_Vids/get_incompleted_vid_dict.py $vid
		if [[ $ans_2 -eq 1 ]]; then
			echo -e "


Are you need to DELETE following incomplete Video:
`du -sh $vid`
[y|n]: "
			read ans_3
			[[ $ans_3 == "y" ]] && rm -f $vid
		elif [[ $ans_2 -eq 2 ]]; then
			if [[ $action_ -eq 1 ]] ; then
				rm -f $vid 2>/dev/null 
				if [[ $? -eq 0 ]]; then
					vid_size=$(du -sh -BM $vid | cut -dM -f1)
					let "size_removed+=vid_size"
					let "vids_removed+=1"
					echo -e ">>>>> incomplete file, change its status to download=False in mapping.pkl, AND deleted: $vid"
				else
					echo -e ">>>>> incomplete file, change its status to download=False in mapping.pkl, but not deleted: $vid"
				fi
			else
				echo -e ">>>>> incomplete file, change its status to download=False in mapping.pkl, but not deleted: $vid"
			fi
		fi
	fi
done



echo -e "\n\nFreed size: $size_removed\nRemoved videos counts: $vids_removed"