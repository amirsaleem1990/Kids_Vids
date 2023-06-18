from django.shortcuts import render
import time
from django.http.response import HttpResponse
import getpass
import json
import shutil
import pickle
import sys
import pandas as pd
import os
from datetime import datetime
from . import utils

def select_channels(request):
	print("................. select_channels called")

	x = dict(request.POST)

	selected_channels = [k.strip() for k, v in x.items() if v == ['on']]
	print("\nselected channels:")
	print(*selected_channels, sep="\n")
	print()
	if not selected_channels:
		return render(request, 'Error.html', {"error" : "No channel is selected!!!!!!"})
	# try:
	channels_mapping = json.load(open("channels_mapping.json", 'r'))
	channels_mapping_rev = {v:k for k,v in channels_mapping.items()}
	channels_dict = pickle.load(open("channels_dict.pkl", 'rb'))

	all_urls = []
	for channel_name, channel_url in channels_dict.items():
		if channels_mapping[channel_name] in selected_channels:
			urls = utils.get_urls(channel_name, channel_url)
			if not urls:
				print(f"\n>>> No urls found for the '{channel_name}' | {channel_url}")
				continue
			all_urls.append([channels_mapping[channel_name], urls])
	pickle.dump(all_urls, open("all_urls.pkl", 'wb'))

	vids_info = {}
	for i in all_urls:
		channel_name, urls = i
		for url in urls:
			vids_info[url] = utils.get_video_info(url)
			file_name = "url_info_" + url.replace("/", "_") + ".pkl"
			if not os.path.exists(file_name):
				print(f"\n>>> Writing '{file_name}' to the disk.")
				pickle.dump(vids_info[url], open(file_name, 'wb'))
				time.sleep(1)
			else:
				print(f"\n>>> The file '{file_name}' is already exist.")
				
	# except Exception as e:
	# 	return HttpResponse(e)

		# raise Exception(e)
		# open(f"/home/{getpass.getuser()}/github/Kids_Vids/EX.txt", 'w').write(str(e))
		# return render(request, 'Error.html', {"error" : e})
	# return render(request, 'dashboard.html', {'data' : all_urls})
	return HttpResponse("HI")