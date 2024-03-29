#!/usr/bin/python3
import shutil
import getpass
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool
import itertools
import re
import time
from datetime import timedelta
import multiprocessing.dummy
import subprocess
import os
import pickle
import json
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import youtube_dl
import traceback

base_dir = f"/home/{getpass.getuser()}/github/Kids_Vids"

def extract_videos_from_channel_page(channel_url):
	try:
		browser.get(channel_url)
	except:
		return []
	s = BeautifulSoup(browser.page_source, "lxml")
	extrected_urls = []
	for i in s.select("a"):
		try:    
			extrected_urls.append(i['href'])
		except: 
			pass
	for i in s.select("source"):
		try:
			extrected_urls.append(i['src'])
		except:
			pass
	# print('ooooooooooooooooooooooooooooooooooooooo', len(extrected_urls))
	return list({'https://www.youtube.com'+i for i in extrected_urls if i.startswith("/watch?")})


# def get_urls_to_download(channels):
#     to_download = []
#     for i in channels:
#         try:
#             channel, url = i
#             x = get_soup_object_using_selenium.get_soup_object_using_selenium(url)[0]
#             urls = ['https://www.youtube.com'+i for i in x if i.startswith("/watch?")]
#             x_2 = [i for i in urls if not i in downloaded]
#             to_download += x_2
#         except:
#             errors[i] = ["No video in the channel",e, str(datetime.now())]
#     pickle.dump(to_download, open(f"{base_dir}/to_download.pkl", 'wb'))
#     print(f"\n\n ---------------------------- to_download saved as {base_dir}/to_download.pkl\n\n")
#     return to_download

def get_urls_to_download(c):
	global get_urls_to_download_recursive_n
	start_time_ = time.time()
	# print(f"\nExtracting urls from <{c[0]}>")
	try:
		channel, url = c
		# print(f"Channel: {channel}\tUrl: {url}")
		urls = extract_videos_from_channel_page(channel_url=url)
		print(f"\nThere are {len(urls)} in <{channel}>")
		if urls:
			for e,i in enumerate(urls):
				if '&' in i:
					urls[e] = i.split("&")[0]

			pickle.dump(urls, open(f"{base_dir}/to_download_{channels.index(c)}.pkl", 'wb'))
		else:
			if get_urls_to_download_recursive_n < 5:
				get_urls_to_download_recursive_n += 1
				print(f">>>>> No usl, another attempt for {channel}")
				get_urls_to_download(c)
		# x_2 = [i for i in urls if not i in downloaded]
		# print(f"\nThere are  {len(x_2)} urls from <{channel}> that are missing in {base_dir}/downloaded.txt file")
	except:
		e = traceback.format_exc()
		if get_urls_to_download_recursive_n < 5:
			get_urls_to_download_recursive_n += 1
			print(f"An error occured, in channel <{channel}> try #{get_urls_to_download_recursive_n} out of 5 ..........")
			get_urls_to_download(c)
		else:
			print(f"Error, No url extracted from channel <{channel}\n{e}\n\n")
			# print(e)
			# print()
			errors[c] = ["No video in the channel <{channel} for the url: <{url}>>",e, str(datetime.now())]
			return False
	print(f"................{url} consumed {time.time() - start_time_} seconds")


"""
# def download_jsons(to_download):
	print("\n---- download_jsons called ........")
	for u in to_download:
		try:
			s = time.time()
			json_name = f"jsons/\'{u.replace('/', '_')}\'"
			json_name_mapping[json_name] = json_name.replace("'", '')
			if os.path.exists(json_name_mapping[json_name]):
				print(f"############################# Json file {json_name} already exists")
				to_skip.append(u)
				continue
			com =  (f"youtube-dl -j '{u}' > {json_name}")
			os.system(com)
			print(f'.............................{u}, Sec consumed: {time.time() - s}')
			time.sleep(5)
		except Exception as e:
			print(e)
			to_skip.append(u)
			errors[u] = ["download_jsons fail",e, str(datetime.now())]

# def extrect_data_from_json(to_download):
	global mapping
	print("\n---- extrect_data_from_json called ........")
	for u in to_download:
		if u in to_skip:
			continue
		json_name = f"jsons/\'{u.replace('/', '_')}\'"
		if not os.path.exists(json_name_mapping[json_name]):
			to_skip.append(u)
			continue
		try:
			x = json.load(open(json_name_mapping[json_name], 'r'))
			print(f'----------------------Extracting information about <{u}>')
			# id_ = x['id']
			if int(x['duration']) == 0:
				to_skip.append(u)
				continue
			duration = str(timedelta(seconds=int(x['duration'])))
			if duration.split(":")[0] == "0":
				duration = "0" + duration
			# video_name = "/home/home/Videos/" + list(os.popen(f"youtube-dl --restrict-filenames --get-filename {u}"))[0].strip()
			# video_name = video_name.replace(id_, "").replace(" ", "").replace("-.", ".")
			n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyz" else "_" for i in x.get("fulltitle").lower()])
			video_name = f"{re.sub('_+', '_', n_).strip('_')}.{x['ext']}"
			# if video_name in iter_:
			#     to_skip.append(u)
			#     continue
			mapping[u] = [x.get("channel"), 
						  x.get('upload_date'), 
						  duration, 
						  video_name,
						  x.get("thumbnail")
						  ]
		except Exception as e:
			# print(f"\n\n\nUrl: {u}\nError: {e}\n\n\n")
			errors[u] = ["extrect_data_from_json fail",e, str(datetime.now())]
			print(e)
			to_skip.append(u)
			pass

# def download_thumbnails(to_download):
	print(f'----------------------download_thumbnails called')
	global mapping
	try:
		for url in to_download:
			if url in to_skip:
				continue
			if mapping.get(url) is None:
				continue
			_,_,_,_,thumbnail_url = mapping[url]
			img_name = thumbnail_url.strip().replace('/', '_')
			mapping[url].append(img_name)
			# thumbn = f"/home/home/thumbnail/{img_name}"
			# if os.path.exists(thumbn):
			#     to_skip.append(url)
			#     continue
			# com = f"curl {thumbn.strip()} > {thumbn}"
			# os.system(com)
	except Exception as e:
		to_skip.append(url)
		errors[url] = ["download_thumbnails",e, str(datetime.now())]
		mapping[url].append("Error")
"""
def get_info(to_download):
	for u in to_download:
		# agar url ka data pehly fetch kya hwa h to dubara fetch nahi karo
		if u in mapping:
			continue
		try:
			s = time.time()
			ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
			with ydl:
				x = ydl.extract_info(u, download=False) # We just want to extract the info
			if x:
				duration = x['duration']
				if int(duration) == 0:
					to_skip.append(u)
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

				# if video_name in iter_:
				#     to_skip.append(u)
				#     continue
				mapping[u] = {"channel" : x.get("channel"), 
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
			to_skip.append(u)
			print('---------------------------')
			print(e)
			print()
			errors[u] = ["download_jsons fail",e, str(datetime.now())]



# def download_videos(url):
# 	try:

# 		v = mapping[url]
# 	    # com = f"curl {v['thumbnail_url']} -o thumbs/{v['thumbnail_name']}"
# 	    # os.system(com)
# 		subprocess.check_call(['curl', v['thumbnail_url'], '-o', f"{base_dir}/thumbs/{v['thumbnail_name']}"])
# 		subprocess.check_call(['youtube-dl', url, '-o', f"/home/home/Videos/{mapping[url]['video_name']}"])
# 		# open(f"{base_dir}/downloaded.txt", "a").write(url+"\n")
# 		mapping[url]['downloaded'] = True
# 	except Exception as e:
# 		print(e)
# 		errors[url] = ["download_videos fail",e, str(datetime.now())]


if os.path.exists(f"{base_dir}/mapping.pkl"):
	try:
		mapping = pickle.load(open(f"{base_dir}/mapping.pkl", 'rb'))
		if len(mapping):
		# if input(f"We need to backup the '{base_dir}/mapping.pkl' file as '{base_dir}/mapping_BACKUP.pkl'. The '{base_dir}/mapping.pkl' file currently has {len(mapping)} items, Are you need to backup this file? [yes|no] ") == "yes":
			shutil.copyfile(f"{base_dir}/mapping.pkl", f"{base_dir}/mapping_BACKUP.pkl")
			print(f"\nThe file '{base_dir}/mapping.pkl' is succussflly saved as '{base_dir}/mapping_BACKUP.pkl'")
		else:
			raise Exception(f"\nThe file '{base_dir}/mapping.pkl' has no items\n")
			exit()
	except Exception as e:
		print(e)
		pass
else:
	mapping = dict()


if __name__ == "__main__":

	pkls = [i for i in os.listdir(base_dir+"/") if i.startswith("to_download_") and i.endswith(".pkl")]
	if pkls:
		for i in pkls:
			os.remove(i)

	if not os.path.exists("/home/home/Videos/"):
		raise Exception("No directory /home/home/Videos/")

	# if not os.path.exists("/home/home/thumbnail/"):
	if not os.path.exists(f"{base_dir}/thumbs/"):
		raise Exception(f"No directory {base_dir}/thumbs/")

	if os.path.exists("to_be_exclude.json"):
		excluded_videos = open(f"{base_dir}/to_be_exclude.json", 'r').read().splitlines()
	else:
		excluded_videos = []

	if os.path.exists(f"{base_dir}/Error_file.pkl"):
		errors = pickle.load(open(f"{base_dir}/Error_file.pkl", 'rb'))
	else:
		errors = dict()

	# if os.path.exists(f"{base_dir}/downloaded.txt"):
	# 	downloaded = open(f"{base_dir}/downloaded.txt", 'r').read().splitlines()
	# else:
	# 	downloaded = list()
	downloaded = [k for k,v in mapping.items() if v['downloaded']]

	get_urls_to_download_recursive_n = 0

	to_skip = []
	# json_name_mapping = {}


	from get_current_channels import get_channels
	channels = get_channels() 

	# iter_ = list(itertools.chain.from_iterable(list(mapping.values())))


	options = Options()
	options.add_argument("--headless")
	browser = webdriver.Firefox(executable_path = "geckodriver", options=options)

	pool = Pool()   # Create a multiprocessing Pool
	pool.map(get_urls_to_download, channels)

	browser.close()

	pkls = [i for i in os.listdir(base_dir + "/") if i.startswith("to_download_") and i.endswith(".pkl")]
	to_download = []
	for i in pkls:
		to_download += pickle.load(open(f"{base_dir}/{i}", 'rb'))
	to_download = [i for i in set(to_download) if not i in downloaded]
	pickle.dump(to_download, open(f"{base_dir}/to_download.pkl", 'wb'))
	print(f"\n\n ---------------------------- to_download saved as {base_dir}/to_download.pkl\n\n")
	# to_download = pickle.load(open(f"{base_dir}/to_download.pkl", 'rb'))

	for i in pkls:
		os.remove(f"{base_dir}/{i}")


	# # download_jsons(to_download)
	try:
		print("Out function", id(mapping))
		get_info(to_download)
	except:
		pickle.dump(mapping, open(f"{base_dir}/mapping.pkl", 'wb'))
		raise Exception(str(traceback.format_exc()))
	pickle.dump(mapping, open(f"{base_dir}/mapping.pkl", 'wb'))
	print(f"\n\n ---------------------------- mapping saved as {base_dir}/mapping.pkl\n\n")
	# mapping = pickle.load(open(f"{base_dir}/mapping.pkl", 'rb'))

	# extrect_data_from_json(to_download)
	# pickle.dump(mapping, open(f"{base_dir}/mapping.pkl", 'wb'))
	# mapping = pickle.load(open(f"{base_dir}/mapping.pkl", 'rb'))

	# download_thumbnails(to_download) 
	# pickle.dump(mapping, open(f"{base_dir}/mapping.pkl", 'wb'))
	# mapping = pickle.load(open(f"{base_dir}/mapping.pkl", 'rb'))

	if errors:
		pickle.dump(errors, open(f"{base_dir}/Error.pkl", 'wb'))

	# to_download = [i for i in to_download if not i in to_skip]
	# urls in mapping but video is not_downloaded
	# excluded_videos = open("to_be_exclude.json", 'r').read().splitlines()
	# to_download = [k for k,v in mapping.items() if not os.path.exists(f"/home/home/Videos/{v['video_name']}") and (not i in to_skip) and (not i in excluded_videos)]


	# moved to Download.py
	# try:
	# 	if to_download:
	# 		p = multiprocessing.dummy.Pool()
	# 		print( "\n---- download_videos called ........")
	# 		print(f"\n--------------------------------------------------- {len(to_download)} videos to be downloaded ..........\n\n")
	# 		p.map(download_videos, to_download)
	# except:
	# 	pickle.dump(mapping, open(f"{base_dir}/mapping.pkl", 'wb'))
	# 	raise Exception(str(traceback.format_exc()))
	# pickle.dump(mapping, open(f"{base_dir}/mapping.pkl", 'wb'))
	os.system(f"yes 'yes' | python3 {base_dir}/Download.py")


	if os.path.exists(f"{base_dir}/Error.pkl"):
		try:
			errors = pickle.load(open(f"{base_dir}/Error.pkl", 'rb'))
			if errors:
				print(f"\n\n{'*'*15}ERRORS{'*'*15}")
				print(errors, sep="\n")
		except:
			pass
