import pickle
import time
import os
import sys
from functools import reduce
from moviepy.editor import VideoFileClip
from datetime import timedelta
from multiprocessing import Pool

x = pickle.load(open("mapping.pkl", 'rb'))
print("Total length of mapping.pkl:", len(x))
downloaded = {k:v for k,v in x.items() if v['downloaded']}
print("Downloaded videos count    :", len(downloaded))

videos_in_disk = os.listdir("/home/home/Videos")
print("Videos in disk             :", len(videos_in_disk))


x1 = {k:v for k,v in x.items() if v['video_name'] in videos_in_disk}

# Adding info
for k,v in x1.items():
	x1[k]['size_MB'] = os.stat(f"/home/home/Videos/{v['video_name']}").st_size/1024/1024

print("\n")
# d = {}
# for k,v in x1.items():
# 	d[v['channel']] = d.get(v['channel'], 0) + v['size_MB']

# pickle.dump(d, open("d", 'wb'))
d = pickle.load(open("d", 'rb'))

# def get_durations(tup):
# 	k,v = tup
# 	try:
# 		a = VideoFileClip(f"/home/home/Videos/{v['video_name']}").duration
# 	except:
# 		a = 0
# 	x1[k]['duration'] = a
# pool = Pool()   # Create a multiprocessing Pool
# pool.map(get_durations, list(x1.items()))

# pickle.dump(x1, open("x1", 'wb'))
x1 = pickle.load(open("x1", 'rb'))

# duration = {}
# for k,v in x1.items():
# 	qm = reduce(lambda x, y: x*60+y, [int(i) for i in (v['duration'].replace(':',',')).split(',')])
# 	duration[v['channel']] = duration.get(v['channel'], 0) + qm
# for k,v in duration.items():
# 	duration[k] = str(timedelta(seconds=v))
# pickle.dump(duration, open("duration", 'wb'))

duration = pickle.load(open("duration", 'rb'))

# d = dict(sorted(d.items(), key=lambda x: x[1]))
# for k,v in d.items():
	# print(f"{int(v)}\t{k}")


x2 = [v['channel'] for k,v in x1.items()]
x3 = sorted([(x2.count(i), i) for i in set(x2)])

lst = []
for k,v in x3:
	lst.append(
		(k, round(d[v]), v, duration[v])
		)
lst = sorted(lst, key=lambda x:x[1], reverse=True)
open('res', 'w').write("Videos|Size_GB|Duration|Channel\n------|-------|--------|-------\n")
for i in lst:
	open("res", 'a').write(f"{i[0]}|{round(i[1]/1024, 1)}|{i[3]}|{i[2]}\n")
os.system("cat res | column -t -s\|")

def deleted_videos_for_specific_channels(channel_name):
	# x = pickle.load(open("mapping.pkl", 'rb'))
	# x = {k:v  for k,v in x.items() if v['channel'] == channel_name}
	# videos_in_disk = os.listdir('/home/home/Videos')
	# for k,v in x.items():
	# 	if v['video_name'] in videos_in_disk:
	# 		x[k]['duration'] = VideoFileClip(f"/home/home/Videos/{v['video_name']}").duration
	for i in lst:
		if i[2].strip() == channel_name.strip():
			break
	else:
		print("Wrong channel name\nAborting ........ \n")
		sys.exit()
	print(f"\n--------------------------------- {channel_name} ---------------------------------\n")
	print(*[v['video_name'] for k,v in x.items() if v['channel'] == channel_name], sep="\n")
	user_input = input_ = input(f"\nAre you really need to DELETE ALL Videos for .......\nchannel       : {channel_name}\nVideos in disk: {i[0]}\nSize in GB    : {round(i[1]/1024, 1)}\nTotal duration: {i[3]}\n[y|n]: ")
	if user_input == "y":
		for i in range(2):
			if input("Are you sure TO DELTE all these videos?\n[y|n]: ") != "y":
				break
		else:
			for k,v in x.items():
				if v['channel'] == channel_name:
					print(f">>> Deleting {v['video_name']}")
					vid = f"/home/home/Videos/{v['video_name']}"
					if os.path.exists(vid):
						os.remove(vid)
						time.sleep(1)



	# print(
	# 	"Entries in mapping.pkl:", 
	# 	len(x)
	# 	)
	# print(
	# 	"Files in ~/Videos     :", 
	# 	sum([v['video_name'] in videos_in_disk for k,v in x.items()])
	# 	)
	# print(
	# 	"Total size in GB      :", 
	# 	round(sum([os.stat(f"/home/home/Videos/{v['video_name']}").st_size/1024/1024 for k,v in x.items() if v['video_name'] in videos_in_disk])/1024, 1)
	# 	)
	# print(
	# 	"Total duration        :", 
	# 	str(timedelta(
	# 		seconds=sum([v['duration'] for k,v in x.items() if v['video_name'] in videos_in_disk])
	# 		))
	# 	)

while True:
	f = input("\nEnter channel name [or press ENTER]: ")
	if f:
		deleted_videos_for_specific_channels(f)
	else:
		break



