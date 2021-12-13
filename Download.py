#!/usr/bin/ipython3
import time
from multiprocessing import Pool  
import multiprocessing.dummy 
import subprocess 
import os 
import pickle 
import json 
from datetime import datetime  
import traceback 
import getpass
import sys

def download_videos(url):
	global mapping
	global errors
	try:
		v = mapping[url]

		full_video_name = f"/home/home/Videos/{mapping[url]['video_name']}"
		if os.path.exists(full_video_name):
			print(f"\n>>. The file {full_video_name} is already exists.\n")
			mapping[url]['downloaded'] = True
			return 
		# some videos name are: .mp4..mp4, .mkv.webm ...
		if full_video_name.count(".") == 2:
			print(f"\n\nSkipping this video\t{url}\n\n")
			return

		thumbnail_full_name = f"/home/{getpass.getuser()}/github/Kids_Vids/thumbs/{v['thumbnail_name']}"
		if not os.path.exists(thumbnail_full_name):
			subprocess.check_call(['curl', v['thumbnail_url'], '-o', thumbnail_full_name])
		subprocess.check_call(['youtube-dl', '--no-playlist', url, '-o', full_video_name])
		print(f"\nThe video {full_video_name} is downloaded\n")
		mapping[url]['downloaded'] = True
	except Exception as e:
		print(e)
		errors[url] = ["download_videos fail",e, str(datetime.now())]

def duration_sec(x):
    h,m,s = x.split(":")
    h = int(h) if not h.startswith("0") else int(h[1])
    m = int(m) if not m.startswith("0") else int(m[1])
    s = int(s) if not s.startswith("0") else int(s[1])
    return s + m*60 + h*60*60

def main():
	global mapping
	global errors
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
	to_download = [k for k,v in mapping.items() if (not v['downloaded']) and (not v['channel'] in channels_to_exclude) and (duration_sec(v['duration']) > 180) and (duration_sec(v['duration']) < 7200)]
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

	if errors:
		pickle.dump(errors, open(f"/home/{getpass.getuser()}/github/Kids_Vids/Error.pkl", 'wb'))
	original_mapping.update(mapping)
	print("\n\nSaving mapping.pkl ........")
	pickle.dump(original_mapping, open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'wb'))


	size_after = int(list(os.popen("du -sh -BM  /home/home/Videos/"))[0].strip().split("\t")[0].strip("M"))

	size_downloaded = size_after - size_before

	if size_downloaded > 1000:
		size_ = f'{round(size_downloaded/1000, 3)}GB'
	else:
		size_ = f'{size_downloaded}MB'

	print(f"\n######################################\nDownloaded {size_}\n######################################\n")


	if is_error:
		raise Exception(error__)
file_name = None 
try:
	file_name = sys.argv[1]
except:
	inp = input("\nYou have to give maaping file name? Are you need to use default file 'mapping.pkl'? [yes|no] ")
	if inp != "yes":
		sys.exit()
	file_name = 'mapping.pkl'
	mapping = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/{file_name}", 'rb'))
try:
	if os.path.exists(file_name):
		mapping = pickle.load(open(file_name, 'rb'))
	else:
		mapping = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/{file_name}", 'rb'))
	inp = input(f"\nAre you need to download links in {file_name}? [yes|no]: ")
	if inp != "yes":
		sys.exit()
except:
	sys.exit()

original_mapping = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))

errors = dict()

try:
	main()
except KeyboardInterrupt:
	sys.exit()
	
while [i for i in os.listdir("/home/home/Videos/") if i.endswith(".part")]:
	print("\n\n\n\n=======================================================\n")
	print("There are some .part files left, retrying again......")
	try:
		main()
		time.sleep(60)
	except KeyboardInterrupt:
		sys.exit()