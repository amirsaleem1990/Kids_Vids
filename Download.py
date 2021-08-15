#!/usr/bin/ipython3
from multiprocessing import Pool  
import multiprocessing.dummy 
import subprocess 
import os 
import pickle 
import json 
from datetime import datetime  
import traceback 
import getpass


def download_videos(url):
	try:

		v = mapping[url]
	    # com = f"curl {v['thumbnail_url']} -o thumbs/{v['thumbnail_name']}"
	    # os.system(com)
		subprocess.check_call(['curl', v['thumbnail_url'], '-o', f"/home/{getpass.getuser()}/github/Kids_Vids/thumbs/{v['thumbnail_name']}"])
		subprocess.check_call(['youtube-dl', url, '-o', f"/home/home/Videos/{mapping[url]['video_name']}"])
		# open(f"/home/{getpass.getuser()}/github/Kids_Vids/downloaded.txt", "a").write(url+"\n")
		mapping[url]['downloaded'] = True
	except Exception as e:
		print(e)
		errors[url] = ["download_videos fail",e, str(datetime.now())]

size_before = int(list(os.popen("du -sh -BM  /home/home/Videos/"))[0].strip().split("\t")[0].strip("M"))

if os.path.exists(f"/home/{getpass.getuser()}/github/Kids_Vids/Error.pkl"):
	try:
		errors = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/Error.pkl", 'rb'))
	except:
		errors = {}
else:
	errors = {}

to_be_exclude = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/to_be_exclude.json", "r"))
channels_to_exclude = to_be_exclude['channel']
mapping = pickle.load(open("mapping.pkl", 'rb'))
to_download = [k for k,v in mapping.items() if (not v['downloaded']) and (not v['channel'] in channels_to_exclude)]


is_error = False
try:
	if to_download:
		p = multiprocessing.dummy.Pool()
		print( "\n---- download_videos called ........")
		print(f"\n--------------------------------------------------- {len(to_download)} videos to be downloaded ..........\n\n")
		p.map(download_videos, to_download)
except:
	error__ = str(traceback.format_exc())
	is_error = True
	# pickle.dump(mapping, open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'wb'))
	# if errors:
		# pickle.dump(errors, open(f"/home/{getpass.getuser()}/github/Kids_Vids/Error.pkl", 'wb'))
	# raise Exception(str(traceback.format_exc()))
	pass

if errors:
	pickle.dump(errors, open(f"/home/{getpass.getuser()}/github/Kids_Vids/Error.pkl", 'wb'))
pickle.dump(mapping, open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'wb'))


size_after = int(list(os.popen("du -sh -BM  /home/home/Videos/"))[0].strip().split("\t")[0].strip("M"))

size_downloaded = size_after - size_before

if size_downloaded > 1000:
	size_ = f'{round(size_downloaded/1000, 3)}GB'
else:
	size_ = f'{size_downloaded}MB'

print(f"\n######################################\nDownloaded {size_}\n######################################\n")


if is_error:
	raise Exception(error__)