from django.shortcuts import render
import time
from django.http.response import HttpResponse
import multiprocessing
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
		pool = multiprocessing.Pool()   # Create a multiprocessing Pool
		for url in urls:
			# pool.apply_async(utils.get_and_save_video_info, args=(url, vids_info))
			utils.get_and_save_video_info(url, vids_info)
	contenct = []
	for k,v in vids_info.items():
		if v is None:
			continue
		contenct.append(v)
		contenct[-1]["video_url"] = k.replace("watch?v=", "embed/")

	return render(request, 'dashboard.html', {'vids_info' : contenct})