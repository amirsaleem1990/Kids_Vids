#!/usr/bin/bash

# This script will loop over videos in /home/home/Videos; move videos to their folders by keywords specified blow, and then print frequecy of words in videos not moved to any folder

echo DEPRECIATED. USE Move_videos_to_folders.py instead

exit

before=$(ls | wc -l)
func(){
	test -e $2
	if [[ $? -ne 0 ]]; then
		#echo -e "\nSorry, The folder <$2> is not found"
		#return
		mkdir "$2"
	fi
	if [[ $(ls | grep $1 | wc -l) -gt 0 ]]; then
		mv -v $(ls | grep $1) $2
	else
		echo -e "\nNo file found for the keyword <$1>"
	fi
}
func morphle_ Morphle/
func vlad_and_niki_ Vlad_and_niki/
func _peekaboo_ Peekaboo/
func chuchu_tv_ Chuchu_tv/
func scishow_kids Scishow_kids/
func chuchu_tv Chuchu_tv/
func robocar_poli Robocar/
func chuchutv Chuchu_tv/
func blippi Blippi/
func earth_to_luna  Earth_to_luna/
func alphablocks  Alphablocks/
func miss_molly  Miss_molly/
func preschool  Preschool/
func for_toddlers For_toddlers/
func _hana_ Omar_and_Hana/
func story_time Story_time/
func math_for_kids Math_for_kids/
func '_مع_زكريا' Omar_and_Hana

after=$(ls | wc -l)
echo -e "\nMoved $(bc <<< $before-$after) videos to their folders"

echo -e "\n\n"
ls *.mp4 *.mkv *.webm|
	sed 's/_/\ /g'  | 
	sed 's/\./\ /g'  | 
	xargs -n 1 |
	tr '[:upper:]' '[:lower:]' |
	sed 's/\ \{1,\}//g'> .amp
python3 <<< '
exclude_word_list = ["mp4", "mkv", "the", "how", "why", "their", "t", "do", "don", "webm", "and", "in", "all", "was", "to"]
x = open(".amp", "r").read().splitlines()
x = [i for i in x if not i in exclude_word_list]
print(*sorted( [i for i in [(i, x.count(i)) for i in set(x)] if i[1] > 1], key=lambda x:x[1], reverse=True), sep="\n")
'

