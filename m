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


to_be_exclude    = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/to_be_exclude.json", "r"))
channels_to_exclude = to_be_exclude['channel']
mapping = pickle.load(open("mapping.pkl", 'rb'))
to_download = [k for k,v in mapping.items() if not v['downloaded'] and (not v['channel'] in channels_to_exclude)]

errors = {}

try:
	if to_download:
		p = multiprocessing.dummy.Pool()
		print( "\n---- download_videos called ........")
		print(f"\n--------------------------------------------------- {len(to_download)} videos to be downloaded ..........\n\n")
		p.map(download_videos, to_download)
except:
	pickle.dump(mapping, open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'wb'))
	raise Exception(str(traceback.format_exc()))
pickle.dump(mapping, open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'wb'))
