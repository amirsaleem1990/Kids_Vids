#!/usr/bin/python3
import pickle
import re
import time
from datetime import timedelta
import os
from datetime import datetime
import youtube_dl
import traceback
# from download_new_vides import get_info
import getpass

mapping_2 = {}

def get_info(to_download):
	for u in to_download:
		# agar url ka data pehly fetch kya hwa h to dubara fetch nahi karo
		# if u in mapping:
			# continue
		try:
			s = time.time()
			ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'noplaylist' : True})
			with ydl:
				x = ydl.extract_info(u, download=False) # We just want to extract the info
			if x:
				duration = x['duration']
				if int(duration) == 0:
					continue
				duration = str(timedelta(seconds=int(duration)))
				if duration.split(":")[0] == "0":
					duration = "0" + duration

				n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyzاأبتثجحخدذرزسشصضطظعغفقكلمنوهيى" else "_" for i in x.get("title").lower()])
				video_name = f"{re.sub('_+', '_', n_).strip('_')}.{x['ext']}"

				thumbnail_url = x.get("thumbnail")
				if ".jpg" in thumbnail_url:
					thumbnail_url = thumbnail_url.split(".jpg")[0] + ".jpg"
				thumbnail_name = thumbnail_url.strip().replace('/', '_')

				mapping_2[u] = {"channel" : x.get("channel"), 
							  "upload_date" : x.get('upload_date'), 
							  "duration" : duration, 
							  "video_name" : video_name,
							  "thumbnail_url" : thumbnail_url,
							  "thumbnail_name" : thumbnail_name,
							  'downloaded' : False
							  }
							  
			print(f'.............................{u}, Sec consumed: {time.time() - s}')
			time.sleep(2)
		except Exception as e:
			print('---------------------------')
			print(e)
			print()
			errors[u] = ["download_jsons fail",e, str(datetime.now())]


mapping = pickle.load(open("mapping.pkl", 'rb'))
urls_file_name = input("Please type Urls file name: ")
if not os.path.exists(f"/home/{getpass.getuser()}/github/Kids_Vids/{urls_file_name}"):
	raise Exception(f"The file /home/{getpass.getuser()}/github/Kids_Vids/{urls_file_name} is not exists")
	exit()

to_download = [i for i in open (urls_file_name, 'r').read().splitlines() if i and (not i.startswith("#"))]

if not to_download:
	raise Exception("There is no url in 'to_download' variable")

errors = dict()

new_mapping_name = "mapping2.pkl"

try:
	get_info(to_download)
except:
	pickle.dump(mapping_2, open(f"/home/{getpass.getuser()}/github/Kids_Vids/{new_mapping_name}", 'wb'))
	raise Exception(str(traceback.format_exc()))

pickle.dump(mapping_2, open(f"/home/{getpass.getuser()}/github/Kids_Vids/{new_mapping_name}", 'wb'))
print(f"\n\n ---------------------------- mapping saved as /home/{getpass.getuser()}/github/Kids_Vids/{new_mapping_name}\n\n")

if errors:
	pickle.dump(errors, open(f"/home/{getpass.getuser()}/github/Kids_Vids/Error_TEMP.pkl", 'wb'))
	print(f"""Errors saved as:
/home/{getpass.getuser()}/github/Kids_Vids/Error_TEMP.pkl
""")

os.system(f"yes 'yes' | python3 /home/{getpass.getuser()}/github/Kids_Vids/Download.py {new_mapping_name}")


if errors:
	print(f"\n\n{'*'*15}ERRORS{'*'*15}")
	print(errors, sep="\n")
