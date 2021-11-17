from django.shortcuts import render
from django.http.response import HttpResponse
import getpass
import json
import shutil
import pickle
import sys
import pandas as pd
import os
from datetime import datetime
from auth_app.views import replace_wrong_videos_names_with_correct_one

to_be_exclude = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/to_be_exclude.json", "r"))
channels_to_exclude = to_be_exclude['channel']
videos_to_exclude = to_be_exclude['video']

existing_files = os.listdir(f"/home/home/Videos")
existing_files = [i for i in existing_files if i.split(".")[-1] in ['mp4', 'mkv', 'webm']]


def func_(vid, img, channel, upload_date):
	upload_date = datetime.strptime(upload_date, "%Y%m%d")
	uploaded_before_days = (datetime.now() - upload_date).days
	msg = f"{uploaded_before_days} days ago"
	vid_name = vid.strip(".webm").strip(".mkv").strip(".mp4").replace("_", ' ').capitalize()
	if vid.endswith(".part"):
		return {}
	vid = vid[::-1].split('.', 1)[-1][::-1]
	for i in ('mkv', 'mp4', 'webm'):
		vid_ = vid  + "." + i
		if vid_ in existing_files:
			vid = vid_
			break
	else:
		return {}
	if vid in videos_to_exclude:
		return {}
	return {
		"img" : 'thumbs/' + img,
		"vid" : 'Videos/' + vid,
		"vid_name" : vid_name,
		"channel" : channel,
		"msg" : msg,
		"extention" :  '.mp4' if vid.endswith(".mp4") else '.mkv' if vid.endswith(".mkv") else '.webm'
		}

def select_channels(request):

	print("................. select_channels.select_channels called")

	x = dict(request.POST)

	selected_channels = [k.strip() for k,v in x.items() if v == ['on']]
	print("selected channels:")

	if not selected_channels:
		return render(request, 'Error.html', {"error" : "No channel is selected!!!!!!"})
	try:
		x = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))
		x = replace_wrong_videos_names_with_correct_one(x)
		x = dict(sorted(x.items(), key=lambda x: (datetime.now() - datetime.strptime(x[1]['upload_date'], "%Y%m%d")).days))

		df = pd.DataFrame.from_dict(x, orient='index')
		df = df[(df.channel.isin(selected_channels))]
		df.upload_date = pd.to_datetime(df.upload_date)
		to_ = None
		if len(df) > 200:
			to_ = 15
		x = (df.assign(upload_date=df.upload_date.astype(str).str.replace("-", ""))
			   .reset_index()
			   .rename(columns={"index" : "url"})
			   .groupby("channel")
			   .apply(lambda x:x.sort_values("upload_date", ascending=False).iloc[:to_])
			   .reset_index(drop=True)
			   .set_index('url')
			   .sort_values("upload_date", ascending=False)
			).to_dict(orient="index")

		data = []
		for k,v in x.items():
			 data.append(
			 	func_(
					vid = v['video_name'], 
					img = v['thumbnail_name'], 
					channel = v['channel'],
					upload_date = v['upload_date']
					)
			 	)
		data = [i for i in data if i]
	except Exception as e:
		open(f"/home/{getpass.getuser()}/github/Kids_Vids/EX.txt", 'w').write(str(e))
		return render(request, 'Error.html', {"error" : e})

	return render(request, 'dashboard.html', {'data' : data})
