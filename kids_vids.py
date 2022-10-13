#!/home/amir/github/Kids_Vids/Virtual_env/bin/python3
import re
import os 
import sys
import time
import json 
import shutil
import pickle 
import getpass
import requests
import traceback 
import itertools
import youtube_dl
import subprocess 
import pandas as pd
from functools import reduce
import multiprocessing.dummy 
from datetime import datetime  
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver
from datetime import timedelta
from multiprocessing import Pool  
from moviepy.editor import VideoFileClip
from selenium.webdriver.firefox.options import Options
if getpass.getuser() == 'amir':
	from get_soup_object_using_selenium import get_soup_object_using_selenium


class Kids_Vids:

	def __init__(self, mapping_file_name='mapping.pkl', error_file_name="Error.pkl"):
		self.user_urls = False
		self.to_skip = []
		self.get_urls_to_download_recursive_n = 0
		self.mapping_n = 0
		self.base_path = f"/home/{getpass.getuser()}/github/Kids_Vids/"
		self.videos_dir_path = "/home/home/Videos/"

		self.to_be_exclude = json.load(open(f"{self.base_path}to_be_exclude.json", "r"))
		try:
			self.mapping = pickle.load(open(f"{self.base_path}{mapping_file_name}", 'rb'))
		except EOFError:
			shutil.copy(f"{self.base_path}mapping_BACKUP.pkl", f"{self.base_path}{mapping_file_name}")
			time.sleep(2)
			self.mapping = pickle.load(open(f"{self.base_path}{mapping_file_name}", 'rb'))
		if mapping_file_name == 'mapping.pkl':
			print("\n\nCreating a backup of <{mapping_file_name}> as <mapping_BACKUP.pkl>\n")
			shutil.copy(f"{self.base_path}{mapping_file_name}", f"{self.base_path}mapping_BACKUP.pkl")
			self.original_mapping = self.mapping.copy()
		else:
			if input(f"\nYou are using {mapping_file_name}, Are you need to proceed? [yes|no] ") != 'yes':
				print("\nAborting....")
				exit()
			self.original_mapping = pickle.load(open(f"{self.base_path}mapping.pkl", 'rb'))

		if error_file_name == "Error.pkl":
			print(colored(f"\n\nYou haven't passed an error file name, so the defaul '{error_file_name}' is used\n", 'green'))
		try:
			self.errors = pickle.load(open(f"{self.base_path}{error_file_name}", 'rb'))
		except:
			self.errors = {}
		print("\n\n==== Variables ====")
		print(f"mapping:, {mapping_file_name}")
		print(f"Errors :, {error_file_name}")
		print()

	def mapping_save(self, fee_kulli_haal=False):
		if self.user_urls:
			return
		self.mapping_n += 1
		if fee_kulli_haal or (self.mapping_n % 10 == 0):
			pickle.dump( self.mapping, open(f"{self.base_path}mapping.pkl", 'wb') )
			print(colored(f"\n\n{str(datetime.now()).split()[1].split('.')[0]}: mapping is saved as {self.base_path}mapping.pkl\n", 'green'))
	
	def download_a_video(self, url):

		try:
			v = self.mapping[url]
			full_video_name = f"{self.videos_dir_path}{v['video_name']}"
			thumbnail_full_name = f"{self.base_path}thumbs/{v['thumbnail_name']}"
			if not os.path.exists(thumbnail_full_name):
				subprocess.check_call(['curl', v['thumbnail_url'], '-o', thumbnail_full_name])
			subprocess.check_call(['youtube-dl', '--no-playlist', url, '-R', '100', '-o', full_video_name])
			self.mapping[url]['downloaded'] = True
			print(colored(f"\n>>> The value 'True' is assigned to 'downloaded' for the {url}\n", 'green'))
			os.system("/amir_bin/extentions_count /home/home/Videos/")
			self.mapping_save()
		except Exception as e:
			print("\n\n\n\n",e, "\n>>>>>>>>>>\tTry again .......\n")
			self.download_a_video(url)
			# self.errors[url] = ["download_videos fail",e, str(datetime.now())]

	def duration_sec(self, x):
		h,m,s = x.split(":")
		h = int(h) if not h.startswith("0") else int(h[1])
		m = int(m) if not m.startswith("0") else int(m[1])
		s = int(s) if not s.startswith("0") else int(s[1])
		return s + m*60 + h*60*60

	def download_summary(self, size_before):
		print("\n\n>> download_summary method is called.")
		size_after = int(list(os.popen(f"du -sh -BM  {self.videos_dir_path}"))[0].strip().split("\t")[0].strip("M"))
		size_downloaded = size_after - size_before
		if size_downloaded > 1000:
			size_ = f'{round(size_downloaded/1000, 3)}GB'
		else:
			size_ = f'{size_downloaded}MB'
		print(colored(f"\n######################################\nDownloaded {size_}\n######################################\n", 'green'))
		time.sleep(2)

	def filter_videos_to_download(self):
		print("\n\n>> filter_videos_to_download method is called.")
		
		channels_to_exclude = self.to_be_exclude['channel']
		# to_lst = [
		# 	k for k,v in self.mapping.items() if (not v['downloaded']) \
		# 		and (not v['channel'] in channels_to_exclude) \
		# 		and (self.duration_sec(v['duration']) > 180) \
		# 		and (self.duration_sec(v['duration']) < 7200)\
		# 		and (not os.path.exists(f"{self.videos_dir_path}{v['video_name']}"))
		# 	]
		to_lst = []
		output = []
		for k,v in self.mapping.items():
			if v['downloaded']:
				# print(f"\n|||>>>{k} : downloaded == True")
				output.append("downloaded == True")
				continue
			elif v['channel'] in channels_to_exclude:
				# print(f"\n|||>>>{k} : in channels_to_exclude")
				output.append("in channels_to_exclude")
				continue
			elif self.duration_sec(v['duration']) < 180:
				# print(f"\n|||>>>{k} : duration is less than 180 seconds")
				output.append("duration is less than 180 seconds")
				continue
			elif self.duration_sec(v['duration']) > 7200:
				# print(f"\n|||>>>{k} : duration is greater than 7200 seconds")
				output.append("duration is greater than 7200 seconds")
				continue
			elif os.path.exists(f"{self.videos_dir_path}{v['video_name']}"):
				# print(f"\n|||>>>{k} : video name is exists")
				output.append("video name is exists")
				continue
			else:
				to_lst.append(k)

		for i in set(output):
			print(f"{i}: {output.count(i)}")

		to_download = []
		for url in to_lst:
			full_video_name = f"{self.videos_dir_path}{self.mapping[url]['video_name']}"
			if (not os.path.exists(full_video_name)) and (not full_video_name.count(".") == 2):
				to_download.append(url)
		return to_download

	def downlload_in_multithreding(self):
		print("\n\n>> downlload_in_multithreding method is called.")
		size_before = int(list(os.popen(f"du -sh -BM  {self.videos_dir_path}"))[0].strip().split("\t")[0].strip("M"))

		to_download = self.filter_videos_to_download()

		is_error = False
		try:
			if to_download:
				p = multiprocessing.dummy.Pool()
				print(colored(f"\n--------------------------------------------------- {len(to_download)} videos to be downloaded ..........\n\n", 'green'))
				p.map(self.download_a_video, to_download)
			else:
				print(colored("\n\nNo videos to be download\n", 'red'))
				# raise Exception("No_video_to_be_downloaded")
				sys.exit(0)
				# exit()
		except:
			error__ = str(traceback.format_exc())
			print("\n"*6)
			print(colored("An error occured", 'red'))
			is_error = True

		# if self.errors:
			# pickle.dump(self.errors, open(f"{self.base_path}Error.pkl", 'wb'))
		self.original_mapping.update(self.mapping)
		# print("\n\nSaving mapping.pkl ........")
		# pickle.dump(self.original_mapping, open(f"{self.base_path}mapping.pkl", 'wb'))
		self.mapping_save(fee_kulli_haal=True)

		self.download_summary(size_before)

		if is_error:
			raise Exception(error__)


	def extract_videos_from_channel_page(self, channel_url):
		try:
			self.browser.get(channel_url)
		except:
			return []
		s = BeautifulSoup(self.browser.page_source, "lxml")
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
		urls = ['https://www.youtube.com'+i for i in extrected_urls if i.startswith("/watch?")]
		urls_2 = [i for i in urls if not i in self.mapping]
		urls_3 = list(set(urls_2))
		print(f"\n{len(urls)} urls extrected from {channel_url}\n{len(urls_2)} of them exists in mapping.pkl file\n{len(urls_3)} to be downloaded\n")
		if urls and (not urls_2):
			self.all_extracted_urls_exists_in_mapping_dict = True
		return urls_3

	def get_urls_to_download(self, c):
		# print("\n\n>> get_urls_to_download method is called.")
		start_time_ = time.time()
		try:
			channel, url = c
			self.all_extracted_urls_exists_in_mapping_dict = False
			urls = self.extract_videos_from_channel_page(channel_url=url)
			print(f"\nThere are {len(urls)} videos in <{channel}>")
			if urls:
				for e,i in enumerate(urls):
					if '&' in i:
						urls[e] = i.split("&")[0]

				pickle.dump(urls, open(f"{self.base_path}to_download_{self.channels.index(c)}.pkl", 'wb'))
			else:
				if not self.all_extracted_urls_exists_in_mapping_dict:
					if self.get_urls_to_download_recursive_n < 5:
						self.get_urls_to_download_recursive_n += 1
						print(colored(f">>>>> No url found, another attempt for {channel}", 'red'))
						self.get_urls_to_download(c)
		except:
			e = traceback.format_exc()
			if self.get_urls_to_download_recursive_n < 5:
				self.get_urls_to_download_recursive_n += 1
				print(f"An error occured, in channel <{channel}> try #{self.get_urls_to_download_recursive_n} out of 5 ..........")
				self.get_urls_to_download(c)
			else:
				print(f"Error, No url extracted from channel <{channel}\n{e}\n\n")
				# self.errors[c] = ["No video in the channel <{channel} for the url: <{url}>>",e, str(datetime.now())]
				return False
		print(f"................{url} consumed {time.time() - start_time_} seconds")

	def get_info(self, to_download):
		print("\n\n>> get_info method is called.")
		if self.user_urls:
			self.mapping = {}
		for u in to_download:
			if (u in self.mapping) or (u in self.original_mapping):
				continue
			try:
				s = time.time()
				x = (
						youtube_dl
						.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'noplaylist' : True})
						.extract_info(u, download=False) # We just want to extract the info
					)
				if x:
					duration = x['duration']
					if int(duration) == 0:
						self.to_skip.append(u)
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

					self.mapping[u] = {"channel"   : x.get("channel"), 
								  "upload_date"    : x.get('upload_date'), 
								  "duration"       : duration, 
								  "video_name"     : video_name,
								  "thumbnail_url"  : thumbnail_url,
								  "thumbnail_name" : thumbnail_name,
								  'downloaded' : False
								  }
					self.mapping_save()
				print(f'.............................{u}, Sec consumed: {time.time() - s}')
				time.sleep(2)
			except Exception as e:
				self.to_skip.append(u)
				print('\n---------------------------')
				print(colored(e, 'red'))
				print()
				# self.errors[u] = ["download_jsons fail",str(e), str(datetime.now())]

	def preparetion_for_downloading_new_videos_info(self):
		print("\n\n>> preparetion_for_downloading_new_videos_info method is called.")
		pkls = [i for i in os.listdir(self.base_path) if i.startswith("to_download_") and i.endswith(".pkl")]
		if pkls:
			for i in pkls:
				os.remove(i)

		if not os.path.exists(self.videos_dir_path):
			raise Exception(f"No directory {self.videos_dir_path}")

		if not os.path.exists(f"{self.base_path}thumbs/"):
			raise Exception(f"No directory {self.base_path}thumbs/")

	def get_channels(self):
		print("\n\n>> get_channels method is called.")
		channels = pickle.load(open("channels.pkl", 'rb'))
		channels_mapping = json.load(open(f"{self.base_path}channels_mapping.txt", "r"))

		channels_to_exclude = self.to_be_exclude['channel']
		if channels_to_exclude:
			l = [k  for k,v in channels_mapping.items() if v in channels_to_exclude]
			channels = [c for c in channels if not c[0] in l]
		return channels


	def prepare_to_download_list(self):
		print("\n\n>> prepare_to_download_list method is called.")
		self.preparetion_for_downloading_new_videos_info()
		 
		options = Options()
		options.add_argument("--headless")
		self.browser = webdriver.Firefox(executable_path = "geckodriver", options=options)

		self.channels = self.get_channels()

		# pool = Pool()
		pool = multiprocessing.dummy.Pool()   # Create a multiprocessing Pool
		# import pdb
		# pdb.set_trace()
		pool.map(self.get_urls_to_download, self.channels)

		self.browser.close()
		pkls = [i for i in os.listdir(self.base_path) if i.startswith("to_download_") and i.endswith(".pkl")]
		to_download = []
		for i in pkls:
			to_download += pickle.load(open(f"{self.base_path}{i}", 'rb'))
		downloaded = [k for k,v in self.mapping.items() if v['downloaded']]
		to_download = [i for i in set(to_download) if not i in downloaded]
		if to_download:
			pickle.dump(to_download, open(f"{self.base_path}to_download.pkl", 'wb'))
			print(colored(f"\n\n ---------------------------- to_download ({len(to_download)} entries) saved as {self.base_path}to_download.pkl\n\n", 'green'))

		for i in pkls:
			os.remove(f"{self.base_path}{i}")

		return to_download

	def main_function_of_getting_new_videos_info(self):
		print("\n\n>> main_function_of_getting_new_videos_info method is called.")
		is_error = False
		if self.user_urls:
			to_download = open( input("Enter urls file name: "), 'r' ).read().splitlines()
			to_download = [i for i in to_download if i and (not i.startswith("#"))]
			if not to_download:
				raise Exception ("There is no urls to be downloaded\nAborting ...\n\n")
				exit()
		else:
			to_download = self.prepare_to_download_list()
		# to_download = pickle.load(open("/home/amir/github/Kids_Vids/to_download.pkl", 'rb'))
		try:
			self.get_info(to_download)
		except:
			error__ = traceback.format_exc()
			is_error = True

		# pickle.dump(self.mapping, open(f"{self.base_path}mapping.pkl", 'wb'))
		self.mapping_save(fee_kulli_haal=True)

		if is_error:
			raise Exception(str(error__))
		# print(f"\n\n ---------------------------- mapping saved as {self.base_path}mapping.pkl\n\n")

		if self.errors:
			try:
				pickle.dump(self.errors, open(f"{self.base_path}Error.pkl", 'wb'))
			except:
				try:
					pickle.dump(str(self.errors), open(f"{self.base_path}Error.pkl", 'wb'))
				except:
					pass


	def get_actual_video_name(self, vid_name):
		if not vid_name.split(".")[-1] in ['mp4', 'mkv', 'webm']:
			return None
		video_name_without_extention = vid_name.replace(".mp4", '').replace(".webm", '').replace(".mkv", '')
		for extention in ['.mkv', '.mp4', '.webm']:
			if f"{video_name_without_extention}{extention}" in self.saved_vids_names:
					return  f"{self.videos_dir_path}{video_name_without_extention}{extention}"
		else:
			# print(f"!! The video '{vid_name}' is not found.")
			return None

	def move_a_video_to_its_folder(self,row):
		outer_video_full_path = row.video_name
		directory_name = f"{self.videos_dir_path}{row.channel}/"
		actual_video_name = outer_video_full_path.split('/')[-1]
		inner_video_full_path = f"{directory_name}{actual_video_name}"
		# outer_video_full_path = /home/home/Videos/echo_echo_echo_full_episode_l_earth_to_luna.mkv
		# inner_video_full_path = /home/home/Videos/Earth To Luna/echo_echo_echo_full_episode_l_earth_to_luna.mkv
		# directory_name        = /home/home/Videos/Earth To Luna/
		# actual_video_name     = echo_echo_echo_full_episode_l_earth_to_luna.mkv
		if not os.path.exists(directory_name):
			os.mkdir(directory_name)
			print(f"\n>>>> Directory <{directory_name}> created.\n")
		try:
			if os.path.exists(inner_video_full_path):
				#print(colored(f"\n! The Video '{outer_video_full_path}' already exisits in '{directory_name}'", 'red'))
				outer_video_size = list(os.popen(f"du -s '{outer_video_full_path}'"))[0].strip().split("\t")[0]
				inner_video_size = list(os.popen(f"du -s '{inner_video_full_path}'"))[0].strip().split("\t")[0]
				if outer_video_size <= inner_video_size:
					os.remove(outer_video_full_path)
					return 
				else:
					os.remove(inner_video_full_path)

			shutil.move(outer_video_full_path, directory_name)
			self.d[directory_name.strip(self.videos_dir_path)] = self.d.get(directory_name.strip(self.videos_dir_path), 0) + 1
			self.files_moved += 1
		except Exception as e:
			print(e)
			self.files_error += 1

	def distribution_of_the_videos_in_the_disk(self):

		def to_mb(size):
			if size.endswith("G"):
				return float(size.rstrip("G"))*1024
			elif size.endswith("M"):
				return float(size.rstrip("M"))
			elif size.endswith("K"):
				return float(size.rstrip("K"))/1024
			else:
				return None
		def bash_func(folder):
			x = f"/home/home/Videos/{folder}"
			size = list(os.popen(f"du -sh '{x}'"))[0].split("\t")[0].strip()
			count = list(os.popen(f'ls "{x}" | wc -l'))[0].strip()
			return(folder, size, count)
		folders = [i for i in os.listdir(self.videos_dir_path) if not "." in i]
		if not folders:
			saved_vids_names = list(
					map(
						str.strip,
						os.popen(""" find /home/home/Videos/ -iname "*mp4" -o -iname "*mkv" -o -iname "*webm" """)
					)
			)

			df = pd.Series(saved_vids_names, name="full_name").to_frame()

			df['size_bytes'] = df.full_name.apply(lambda x:os.path.getsize(x))
			df = df[df.size_bytes.gt(0)]

			df['video_name'] = df.full_name.str.split("/").str[-1]

			mapping = pd.DataFrame.from_dict(pickle.load(open("mapping.pkl", 'rb')), orient="index")
			mapping = mapping.drop_duplicates(subset=["channel", "duration", "video_name"])

			# def get_actual_video_name(vid_name):
			# 	v = vid_name.strip(".mp4").strip("webm").strip(".mkv")
			# 	for extention in ['.mkv', '.mp4', 'webm']:
			# 		if os.path.exists(f"/home/home/Videos/{v}{extention}"):
			# 			return  v + extention
			# 	else:
			# 		return None
			# mapping.video_name = mapping.video_name.apply(get_actual_video_name)
			# ye apply karny k bad galat results aa rahy hen, pata nahi q. 24-apr-2022

			df = df.merge(mapping[['channel', 'video_name']], on="video_name", how="left").drop_duplicates()

			from IPython.display import display
			df = (
				df
				.assign(channel=df.channel.fillna("NaN"))
				.filter(["channel", "size_bytes"])
				.groupby("channel")
				.size_bytes
				.agg(["count", "sum"])
				.assign(
					MB=lambda x:(x['sum']/1024/1024).astype(int),
					GB=lambda x:(x['MB']/1024).astype(int)
				)
				.drop("sum", axis=1)
				.sort_values("count", ascending=False)
			)
			df.loc["Total"] = df.sum().to_list()
			display(df)
			return 
		lst = []
		for folder in folders:
			lst.append(bash_func(folder))

		df = (pd
			  .DataFrame(lst)
			  .rename(columns={0:"Name", 1:"Size", 2:"Count"}
				)
			  )

		df['MB']=df.Size.apply(to_mb)
		print(
			df
			.sort_values("MB")
			.drop("MB", axis=1)
			.reset_index(drop=True)
			.to_string()
			)


	# END of the class 'Kids_Vids'

def download_new_videos(kids_vids_obj):
	try:
		kids_vids_obj.downlload_in_multithreding()
	except KeyboardInterrupt:
		sys.exit()
		
	while [i for i in os.listdir(kids_vids_obj.videos_dir_path) if i.endswith(".part")]:
		print("\n\n\n\n=======================================================\n")
		print("There are some .part files left, retrying again......")
		try:
			kids_vids_obj.downlload_in_multithreding()
			time.sleep(60)
		except KeyboardInterrupt:
			sys.exit()

def move_videos_to_their_folders(kids_vids_obj):
	kids_vids_obj.files_moved = 0
	kids_vids_obj.files_error = 0
	kids_vids_obj.d = {}
	kids_vids_obj.saved_vids_names = os.listdir(kids_vids_obj.videos_dir_path)

	df = (pd
		  .DataFrame
		  .from_dict(kids_vids_obj.mapping, orient="index")
		  .reset_index()
		  .rename(columns={"index" : "url"})
		  .loc[:, ['channel', 'video_name']]
	)

	df.video_name = df.video_name.apply(kids_vids_obj.get_actual_video_name)
	kids_vids_obj.files_not_moved = df.video_name.isna().sum()
	df = df.dropna()

	if not len(df):
		print(colored("\n\nNo file to be moved.\n", 'red'))
		exit()

	df = df
	kids_vids_obj.to_remove = []
	df.apply(kids_vids_obj.move_a_video_to_its_folder, axis=1)

	print("\n\n")
	print("files_moved:     ", kids_vids_obj.files_moved)
	print("files_error:     ", kids_vids_obj.files_error)
	print("files_not_moved: ", kids_vids_obj.files_not_moved)

	print()

	print(json.dumps(kids_vids_obj.d, indent=4))

	if kids_vids_obj.to_remove:
		print(kids_vids_obj.to_remove)

	print()

def get_channel_name_by_url(url):
	x = get_soup_object_using_selenium(url)
	return x[1].find("div", {"id" : "text-container"}).text.strip()

def Add_channels():

	channels_mapping = json.load(open("channels_mapping.txt", 'r'))
	channels = pickle.load(open("channels.pkl", 'rb'))
	urls_in_channels = [i[1] for i in channels]
	new_channels = open("new_channels", 'r').read().splitlines()
	new_channels = [i for i in new_channels if i and (not i.startswith("#"))]

	if not new_channels:
		print("\n\nThere is no url (or urls with #)\nExiting.......\n\n")
		exit()

	d = {}
	for url in new_channels:
		if url in urls_in_channels:
			print(f"\nThe url {url} is already exists in channels.pkl, skipping........")
			continue
		key = url.split("/")[4]
		channel_name = get_channel_name_by_url(url)
		d[key] =(channel_name, url)
	if not d:
		print("\n\nNo new information to be added to 'channels_mapping.txt' and  'channels.pkl'\nAdd your new url(s) to 'new_channels' file\nExiting.....\n")

		exit()

	changings_qty = 0

	for key,value in d.items():
		channel_name, url = value
		inp = input(f"""\n\nGoing to add:\n'{key}':'{channel_name}'' to channels_mapping.txt\n{key, url} to  channels.pkl\nAre you agree? [y|n]: """)
		# inp = input(f"\nGiving this <{url}> we add this {key}:{channel_name} as a new entry in the 'to channels_mapping.txt'. Are you agree? [y|n] ")
		if inp == 'y':
			changings_qty += 1
			channels_mapping[key] = channel_name
			channels.append( (key, url) )

	if changings_qty:
		json.dump(channels_mapping, open("channels_mapping.txt", 'w'))
		pickle.dump(channels, open("channels.pkl", 'wb'))


def add_urls_to_mapping_pkl():
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


def remove_old_videos():
	if input("This option will keep latest 15 videos for each channel, and remove all others. Do you need to proceed? [yes|no] ") != "yes":
		exit()

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
	x = sorted(Count_dict.items(), key=lambda x:x[1], reverse=True)
	if not x:
		print("\n\nNo videos to remove\nAborting ........\n")
		sys.exit()
	print(f"\n\n\n{'*'*10} Videos (for delete) count by channel {'*'*10}")
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


def remove_all_Videos_for_given_channel():
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
	d = {}
	for k,v in x1.items():
		d[v['channel']] = d.get(v['channel'], 0) + v['size_MB']

	# pickle.dump(d, open("d", 'wb'))
	#d = pickle.load(open("d", 'rb'))

	def get_durations(tup):
		k,v = tup
		try:
			a = VideoFileClip(f"/home/home/Videos/{v['video_name']}").duration
		except:
			a = 0
		x1[k]['duration'] = a
	pool = Pool()   # Create a multiprocessing Pool
	pool.map(get_durations, list(x1.items()))

	# pickle.dump(x1, open("x1", 'wb'))
	# x1 = pickle.load(open("x1", 'rb'))

	duration = {}
	for k,v in x1.items():
		qm = reduce(lambda x, y: x*60+y, [int(i) for i in (v['duration'].replace(':',',')).split(',')])
		duration[v['channel']] = duration.get(v['channel'], 0) + qm
	for k,v in duration.items():
		duration[k] = str(timedelta(seconds=v))

	#pickle.dump(duration, open("duration", 'wb'))
	#duration = pickle.load(open("duration", 'rb'))

	d = dict(sorted(d.items(), key=lambda x: x[1]))
	for k,v in d.items():
		print(f"{int(v)}\t{k}")


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

def get_incompleted_vid_dict():
	print("\n\n\nSorry\n\n\n")
	sys.exit(1)
	def func(video_name):
		file_ = f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl"
		x = pickle.load(open(file_, 'rb'))
		for k,v in x.items():
			if v['video_name'] == video_name:
				v['downloaded'] = False
				break
		pickle.dump(x, open(file_, 'wb'))

	try:
		func(video_name=sys.argv[1])
	except:
		pass

def change_video_names_according_to_saved_names_in_mapping_file():
	ans = input("This function require that the 'mapping' should NOT being used from another session. Is this condition setisfied? [yes|no]")
	if ans != "yes":
	    import sys
	    sys.exit()
	vids_in_dir = list(os.popen("""IFS=$'\n'; for i in $(find /home/home/Videos/ -type f | grep -iE 'mp4|mkv|webm'); do basename "$i" ;done"""))
	vids_in_dir = list(map(str.strip, vids_in_dir))


	mapping = pickle.load(open("mapping.pkl", 'rb'))
	df = pd.DataFrame.from_dict(mapping, orient="index").rename_axis("url").reset_index()

	print(f"There are {len(set(vids_in_dir).difference(df.video_name))} files that are in /home/home/Videos/ but not in mapping.pkl")

	x = pd.Series(list(set(df.video_name).difference(vids_in_dir)))
	x2 = x[x.str.count("\.").eq(1)].reset_index(drop=True)
	lst = []
	for i in x2:
	    i_0, i_1 = i.split(".")
	    for extention in [".mp4", ".mkv", ".webm", ".MP4", ".MKV", ".WEBM"]:
	        if (i_0 + extention) in vids_in_dir:
	            lst.append(("."+i_1, extention, i_0))
	            
	x = (
		pd
		.DataFrame(lst, columns=["saved", "actual", "name"])
		.assign(
	        actual_name=lambda x:x.name + x.actual, 
	        saved_name=lambda x:x.name + x.saved
	    )
		.drop(["saved", "actual", "name"], axis=1)
	    .drop_duplicates(subset=["saved_name"], keep=False)
	)
	new_video_name = df.video_name.replace(x.set_index("saved_name").actual_name.to_dict())
	if new_video_name.eq(df.video_name).all():
		print("\nWe can not correct any name\n")
		# print("\nExiting.........\n")
		# import sys
		# sys.exit()
		# # exit()
		return
	print(f"We can correct {df.video_name.ne(new_video_name).sum()} of them.")
	df.video_name = new_video_name

	# Assing 'True' to 'downloaded' column to the changed rows. # to-do # amir

	d = df.set_index('url').T.to_dict()

	inp = input("\nAre you ready to replace mapping.pkl file? [yes|no] ")
	if inp != "yes":
		print("\nAborting......\n")
		sys.exit()
	pickle.dump(d, open("mapping.pkl", 'wb'))


if __name__ == "__main__":

	kids_vids_obj = Kids_Vids()
	# kids_vids_obj = Kids_Vids(mapping_file_name = 'mapping_from_user_urls.pkl')
	
	print("""
Select you option:
	1- Download videos
	2- Download info
	3- Download info AND videos 
	4- Move videos to their folders
	5- Show distribution of present videos in the disk
	6- Add channels
	7- Download user provided urls
	8- Add urls to mapping.pkl
	9- Remove old videos
	10- Remove all Videos for given channel/s
	11- Get incompleted vid dict
	12- Correct video names in mapping.pkl file""")

	
	user_inp = input().strip()
	assert user_inp.isnumeric(), "\nWrong input"

	actions_dict = {
		"2" : kids_vids_obj.main_function_of_getting_new_videos_info,
		"6" : Add_channels,
		"8" : add_urls_to_mapping_pkl,
		"9" : remove_old_videos,
		"10" : remove_all_Videos_for_given_channel,
		"11" : get_incompleted_vid_dict,
		"12" : change_video_names_according_to_saved_names_in_mapping_file
	}
	

	if user_inp in actions_dict:
		actions_dict[user_inp]()
	
	if user_inp == '1':
		download_new_videos(kids_vids_obj),
	
	elif user_inp == "4": 
		move_videos_to_their_folders(kids_vids_obj),
	
	elif user_inp == '3':
		kids_vids_obj.main_function_of_getting_new_videos_info()
		download_new_videos(kids_vids_obj)
		
	elif user_inp == '5':
		change_video_names_according_to_saved_names_in_mapping_file()
		kids_vids_obj.distribution_of_the_videos_in_the_disk()
	
	
	elif user_inp == '7':
		kids_vids_obj.user_urls = True
		kids_vids_obj.main_function_of_getting_new_videos_info()
		pickle.dump(
			kids_vids_obj.mapping, open(f"{kids_vids_obj.base_path}mapping_from_user_urls.pkl", 'wb')
			)
		download_new_videos(kids_vids_obj)

	else:
		raise Exception("\nWront input")

