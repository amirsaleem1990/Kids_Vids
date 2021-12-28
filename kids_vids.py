#!/usr/bin/python3
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
import multiprocessing.dummy 
from datetime import datetime  
from bs4 import BeautifulSoup
from termcolor import colored
from selenium import webdriver
from datetime import timedelta
from multiprocessing import Pool  
from selenium.webdriver.firefox.options import Options
from get_soup_object_using_selenium import get_soup_object_using_selenium


class Kids_Vids:

	def __init__(self, mapping_file_name, error_file_name="Error.pkl"):
		self.to_skip = []
		self.get_urls_to_download_recursive_n = 0
		self.mapping_n = 0
		self.base_path = f"/home/{getpass.getuser()}/github/Kids_Vids/"
		self.videos_dir_path = "/home/home/Videos/"

		self.to_be_exclude = json.load(open(f"{self.base_path}to_be_exclude.json", "r"))
		self.mapping = pickle.load(open(f"{self.base_path}{mapping_file_name}", 'rb'))
	
		if mapping_file_name == 'mapping.pkl':
			shutil.copy(f"{self.base_path}{mapping_file_name}", f"{self.base_path}mapping_BACKUP.pkl")
			self.original_mapping = self.mapping
		else:
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
			subprocess.check_call(['youtube-dl', '--no-playlist', url, '-o', full_video_name])
			self.mapping[url]['downloaded'] = True
			print(colored(f"\n>>> The value 'True' is assigned to 'downloaded' for the {url}\n", 'green'))
			self.mapping_save()
		except Exception as e:
			print(e)
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
		to_lst = [
			k for k,v in self.mapping.items() if (not v['downloaded']) \
				and (not v['channel'] in channels_to_exclude) \
				and (self.duration_sec(v['duration']) > 180) \
				and (self.duration_sec(v['duration']) < 7200)
			]

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
				raise Exception("No_video_to_be_downloaded")
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
		for u in to_download:
			if u in self.mapping:
				continue
			try:
				s = time.time()
				ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
				with ydl:
					x = ydl.extract_info(u, download=False) # We just want to extract the info
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

					self.mapping[u] = {"channel" : x.get("channel"), 
								  "upload_date" : x.get('upload_date'), 
								  "duration" : duration, 
								  "video_name" : video_name,
								  "thumbnail_url" : thumbnail_url,
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
		# channels = [
		# 	('robocar',                               "https://www.youtube.com/c/robocarpoli/videos"),
		# 	('VladandNiki',                           "https://www.youtube.com/c/VladandNiki/videos"),
		# 	('ChuchuTv',                              "https://www.youtube.com/c/ChuChuTVBedtimeStories/videos"),
		# 	('scishowkids',                           'https://www.youtube.com/c/scishowkids/videos'), 
		# 	('PeekabooKids',                          'https://www.youtube.com/c/PeekabooKids/videos'),
		# 	('MorphleTV',                             'https://www.youtube.com/c/MorphleTV/videos'),
		# 	('Blippi',                                'https://www.youtube.com/c/Blippi/videos'),
		# 	('CraftsforKids',                         'https://www.youtube.com/c/CraftsforKids/videos'),
		# 	('ClarendonLearning',                     'https://www.youtube.com/c/ClarendonLearning/videos'),
		# 	('FreeSchool',                            'https://www.youtube.com/c/FreeSchool/videos'),
		# 	('KidsLearningTube',                      'https://www.youtube.com/c/KidsLearningTube/videos'),
		# 	('NUMBEROCKLLC',                          'https://www.youtube.com/c/NUMBEROCKLLC/videos'),
		# 	('natgeokids',                            'https://www.youtube.com/natgeokidsplaylists/videos'),
		# 	('TheDadLab',                             'https://www.youtube.com/c/TheDadLab/videos'),
		# 	('5MinuteCraftsPLAY',                     'https://www.youtube.com/c/5MinuteCraftsPLAY/videos'),
		# 	('KidsMadaniChannel',                     'https://www.youtube.com/c/KidsMadaniChannel/videos'),
		# 	('OmarHanaIslamicSongsforKids',           'https://www.youtube.com/c/OmarHanaIslamicSongsforKids/videos'),
		# 	('officialalphablocks',                   'https://www.youtube.com/c/officialalphablocks/videos'),
		# 	('Numberblocks',                          'https://www.youtube.com/c/Numberblocks/videos'),
		# 	('PreschoolPrepCompany',                  'https://www.youtube.com/c/PreschoolPrepCompany/videos'),
		# 	('UCbxK6jzYms1iMkU9Kwvl0sA',              'https://www.youtube.com/channel/UCbxK6jzYms1iMkU9Kwvl0sA/videos'),
		# 	('MissMollyLearning',                     'https://www.youtube.com/c/MissMollyLearning/videos'),
		# 	('allthingsanimaltv',                     'https://www.youtube.com/c/allthingsanimaltv/videos'),
		# 	('LearnWithZakaria',                      'https://www.youtube.com/c/LearnWithZakaria/videos'),
		# 	('EarthToLuna',                           'https://www.youtube.com/c/EarthToLuna/videos'),
		# 	('MysteryDoug',                           'https://www.youtube.com/c/MysteryDoug/videos'),
		# 	('HappyLearningTVKids',                   'https://www.youtube.com/c/HappyLearningTVKids/videos'),
		# 	('PeepWGBH',                              'https://www.youtube.com/user/PeepWGBH/videos'),
		# 	('ComeOutsideTV',                         'https://www.youtube.com/user/ComeOutsideTV/videos'),
		# 	('UCPttFyZAvTlWAQzgRU4duJA',              'https://www.youtube.com/channel/UCPttFyZAvTlWAQzgRU4duJA/videos'),
		# 	('OfficialBerenstainBears',               'https://www.youtube.com/c/OfficialBerenstainBears/videos'),
		# 	('SmileandLearnEnglish1',                 'https://www.youtube.com/c/SmileandLearnEnglish1/videos'),
		# 	('UC4p_YSvJlJpEhAh5PMyhkiQ',              'https://www.youtube.com/channel/UC4p_YSvJlJpEhAh5PMyhkiQ/videos'),
		# 	('LearningTimeFun',                       'https://www.youtube.com/c/LearningTimeFun/videos'),
		# 	('Toddlerfunlearning',                    'https://www.youtube.com/c/Toddlerfunlearning/videos'),
  #           ('Luqmay',                                'https://www.youtube.com/c/Luqmay/videos'), 
  #           ('KAZschool',                             'https://www.youtube.com/c/KAZschool/videos'), 
  #           ('DUAKidsEnglish',                        'https://www.youtube.com/c/DUAKidsEnglish/videos'), 
  #           ('TheMiniMuslims',                        'https://www.youtube.com/c/TheMiniMuslims/videos'), 
  #           ('SafarPublications',                     'https://www.youtube.com/c/SafarPublications/videos'), 
  #           ('IslamicKidsVideos',                     'https://www.youtube.com/c/IslamicKidsVideos/videos'), 
  #           ('IQRACARTOONNETWORK',                    'https://www.youtube.com/c/IQRACARTOONNETWORK/videos'), 
  #           ('UrduIslamicKidsVideos',                 'https://www.youtube.com/c/UrduIslamicKidsVideos/videos'), 
  #           ('TheMuslimsCartoonSeries',               'https://www.youtube.com/c/TheMuslimsCartoonSeries/videos'), 
  #           ('EnglishMoralStoriesWithTedZoe',         'https://www.youtube.com/c/EnglishMoralStoriesWithTedZoe/videos'), 
  #           ('UCCwB8hOCCRFENjEUP_U7FoQ',              'https://www.youtube.com/channel/UCCwB8hOCCRFENjEUP_U7FoQ/videos'), 
  #           ('UC3n8KIvfsdomdMjQBcmgiAA',              'https://www.youtube.com/channel/UC3n8KIvfsdomdMjQBcmgiAA/videos'), 
  #           ('EnglishProphetStoriesQuranStories',     'https://www.youtube.com/c/EnglishProphetStoriesQuranStories/videos'), 
  #           ('BillionSurpriseToys_NurseryRhymes',     'https://www.youtube.com/c/BillionSurpriseToys_NurseryRhymes/videos'), 
  #           ('HindiStoriesoftheProphetsQuranStories', 'https://www.youtube.com/c/HindiStoriesoftheProphetsQuranStories/videos')
		# ]
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
			count = list(os.popen(f"ls '{x}'/ | wc -l"))[0].strip()
			return(folder, size, count)
		folders = [i for i in os.listdir(self.videos_dir_path) if not "." in i]
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

def Only_download_new_videos_OR_Download_new_videos_and_new_info(kids_vids_obj):
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
		print("\n\nNo new information to be added to 'channels_mapping.txt' and  'channels.pkl'\nExiting.....\n")
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

if __name__ == "__main__":
	
	print("""
Select you option:
	1- Download new videos
	2- Download new info
	3- Download new videos AND new info
	4- Move videos to their folders
	5- Show distribution of present videos in the disk
	6- Add channels""")

	user_inp = input().strip()
	if not  user_inp.isnumeric():
		raise Exception ("Wrong input")
	
	kids_vids_obj = Kids_Vids(mapping_file_name = 'mapping.pkl')
	
	if user_inp in ['2', '3']:

		kids_vids_obj.main_function_of_getting_new_videos_info()

	if user_inp in ['1', '3']:
		Only_download_new_videos_OR_Download_new_videos_and_new_info(kids_vids_obj)

	if user_inp == '4':
		move_videos_to_their_folders(kids_vids_obj)

	if user_inp == '5':
		kids_vids_obj.distribution_of_the_videos_in_the_disk()
	if user_inp == '6':
		Add_channels()
	