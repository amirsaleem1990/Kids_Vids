######################################################################################
#   This script will keep latest 15 videos for each channel, and remove all others.  #
######################################################################################

import pickle
import pandas as pd
import getpass
import os

def get_actual_video_name(vid_name):
	v = vid_name.strip(".mp4").strip("webm").strip(".mkv")
	for extention in ['.mkv', '.mp4', 'webm']:
		if os.path.exists(f"/home/home/Videos/{v}{extention}"):
			return  v + extention
	else:
		return None

x = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))
df = pd.DataFrame.from_dict(x, orient='index')
df = df[df.downloaded]
df.upload_date = pd.to_datetime(df.upload_date)



to_remove = df[
	~ df.index.isin(
		df.reset_index().rename(columns={"index" : "url"}).groupby("channel").apply(lambda x:x.sort_values("upload_date", ascending=False).iloc[:15]).reset_index(drop=True).set_index('url').sort_values("upload_date", ascending=False).index.to_list()
		)
	].index.to_list()
q = []
for i in to_remove:
	s = get_actual_video_name(x[i]['video_name'])
	if not s is None:
		q.append(i)
to_remove = q

vids_to_delete = []
Count_dict = {}
Size_dict = {}
for url in to_remove:
	vid = f"/home/home/Videos/{x[url]['video_name']}"
	channel = x[url]['channel']
	if os.path.exists(vid):
		Count_dict[ x[url]['channel'] ] = Count_dict.get(channel, -1) + 1
		# os.remove(vid)
		size = os.stat(vid).st_size # in bytes
		size /= 1024*1024*1024# in GB
		Size_dict[channel] = Size_dict.get(channel, 0) + size
		vids_to_delete.append((vid, channel, size))
print(f"\n\n\n{'*'*10}Videos for delete count by channel{'*'*10}")
x = sorted(Count_dict.items(), key=lambda x:x[1], reverse=True)
print("Index\tCount\tSize\tChannel")
for e, i in enumerate(x):
    print(f"{e}\t{i[1]}\t{round(Size_dict[i[0]])}\t{i[0]}")

input_ = input('''
Are you sure to DELETE ALL of these channels: 
	- yes 
	- no 
	- Enter index[es] to exclude, (delimated by comma <,>) 

	''').replace(" ", "")
if input_ == "yes":
	for e, i in enumerate(x):
		channel = i[0]
		print(f"Deleting {i[1]} videos from <{channel}> channel")
		...
elif input_ == "no":
	import sys
	sys.exit()
elif True:
	if ',' in input_:
		to_exlude_index = [int(i.strip()) for i in input_.split(",")]
	else:
		to_exlude_index  = [int(input_.strip())]
	final_to_delete_channels = [i[0] for e, i in enumerate(x) if not e in to_exlude_index]

	before=int(list(os.popen("du -sh -BM  /home/home/Videos/ | cut -dM -f1"))[0].strip())
	x = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))
	for i in to_remove:
		if x[i]['channel'] in final_to_delete_channels:
			vid_actual_name = get_actual_video_name(x[i]['video_name'])
			if vid_actual_name is None:
				continue
			print(f">> Deleting <{vid_actual_name}> from channel <{x[i]['channel']}>")
			os.remove(f"/home/home/Videos/{vid_actual_name}")
	after=int(list(os.popen("du -sh -BM  /home/home/Videos/ | cut -dM -f1"))[0].strip())
	print(f"\n\nFreed {before-after} MB | {(before-after)/1024} GB")

