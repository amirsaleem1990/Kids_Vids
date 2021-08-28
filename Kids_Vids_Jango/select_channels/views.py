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

def func_(vid, img, channel, upload_date, videos_to_exclude):
	upload_date = datetime.strptime(upload_date, "%Y%m%d")
	uploaded_before_days = (datetime.now() - upload_date).days
	msg = f"{uploaded_before_days} days ago"
	vid_name = vid.strip(".webm").strip(".mkv").strip(".mp4").replace("_", ' ').capitalize()
	if vid.endswith(".part"):
		return ""
	vid = f'/home/home/Videos/{vid}'
	vid = vid[::-1].split('.', 1)[-1][::-1]
	for i in ('mkv', 'mp4', 'webm'):
		vid_ = vid  + "." + i
		if os.path.exists(vid_):
			vid = vid_
			break
	else:
		return ""
	if vid in videos_to_exclude:
		return ""
	if int(list(os.popen(f"du -s -BM {vid} | cut -dM -f1"))[0].strip()) < 10:
		return ""
	if vid.endswith(".mkv"):
		  return f"""<div class="column">
				<figure class="D3Oi9">
					<video width="320" height="240" controls poster="{img}" src="{vid}"></video>
					<span class="QuG1o"><br>{vid_name}<br><b>{channel}<br></b>{msg}</span>
				</figure>
			</div>
			"""
	elif vid.endswith(".mp4"):
		return f"""<div class="column">
			<figure class="D3Oi9">
				<video width="320" height="240" controls  poster="{img}">
					<source src="{vid}" type="video/mp4">
					Your browser does not support the video tag.
				</video>
				<span class="QuG1o"><br>{vid_name}<br><b>{channel}<br></b>{msg}</span>
			</figure>
		</div>
		"""
	return f"""<div class="column">
				<figure class="D3Oi9">
					<video width="320" height="240" controls  poster="{img}">
						<source src="{vid}" type="video/webm">
						Your browser does not support the video tag.
					</video>
					<span class="QuG1o"><br>{vid_name}<br><b>{channel}<br></b>{msg}</span>
				</figure>
			</div>
			"""
				
def select_channels(request):
	print("................. select_channels.select_channels called")

	x = dict(request.POST)

	selected_channels = [k.strip() for k,v in x.items() if v == ['on']]
	if not selected_channels:
		return render(request, 'Error.html', {"error" : "No channel is selected!!!!!!"})
	channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))
	channels_mapping_flapped = {v:k for k,v in channels_mapping.items()}
	selected_channels = [channels_mapping_flapped[i] for i in selected_channels if i in channels_mapping_flapped.keys()]


	sys.path += [f'/home/{getpass.getuser()}/github/Kids_Vids']
	from get_current_channels import get_channels
	channels = get_channels()
	channels = [i for i in channels if i[0] in selected_channels]
	if not channels:
		return render(request, 'Error.html', {"error" : "No channel is selected_!!!!"})


	##############################################################################################################
	try:
		x = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))
		x = sorted(x.items(), key=lambda x: (datetime.now() - datetime.strptime(x[1]['upload_date'], "%Y%m%d")).days)
		x = {i[0] : i[1] for i in x}
		to_be_exclude = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/to_be_exclude.json", "r"))
		channels_to_exclude = to_be_exclude['channel']
		videos_to_exclude = to_be_exclude['video']

		channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))

		to_remove = []
		for k,v in x.items():
			if v['channel'] in channels_to_exclude or (k in videos_to_exclude):
				to_remove.append(k)
		if to_remove:
			for i in to_remove:
				x.pop(i)

		s = """<!DOCTYPE html><html>
		<head>
			<style>
				* {box-sizing: border-box;}
				.column {float: left;width: 20.00%; padding: 0px;}
				/* Clearfix (clear floats) */
				.row::after {content: "";clear: both;display: table;}
			</style>
		</head>
		<body>
			<center>Kids_Vids</center><br>
			<div class="row">
				"""

		df = pd.DataFrame.from_dict(x, orient='index')
		df = df[df.downloaded]
		df.upload_date = pd.to_datetime(df.upload_date)
		x = df.reset_index().rename(columns={"index" : "url"}).groupby("channel").apply(lambda x:x.sort_values("upload_date", ascending=False).iloc[:15]).reset_index(drop=True).set_index('url').sort_values("upload_date", ascending=False)
		# x = df.reset_index().rename(columns={"index" : "url"}).groupby("channel").apply(lambda x:x.sort_values("upload_date", ascending=False)).reset_index(drop=True).set_index('url').sort_values("upload_date", ascending=False)
		x.upload_date = x.upload_date.astype(str).str.replace("-", "")
		x = x.to_dict(orient="index")

		for k,v in x.items():
			s += func_(
				vid = v['video_name'], 
				# img = v['thumbnail_url'], # fatching from internet
				img = f"/home/{getpass.getuser()}/github/Kids_Vids/thumbs/{v['thumbnail_name']}", 
				channel = v['channel'],
				upload_date = v['upload_date'],
				videos_to_exclude=videos_to_exclude
				)
		s += "\n</div></body></html>"

		open("dashboard.html", 'w').write(s)
		#import webbrowser
		#webbrowser.get("chromium").open(f"/home/{getpass.getuser()}/github/Kids_Vids/dashboard.html")
		# os.system(f"chromium /home/{getpass.getuser()}/github/Kids_Vids/dashboard.html")
	except Exception as e:
		open(f"/home/{getpass.getuser()}/github/Kids_Vids/EX.txt", 'w').write(str(e))
		return render(request, 'Error.html', {"error" : e})

	##############################################################################################################

	return render(request, 'dashboard.html')
