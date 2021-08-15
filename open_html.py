#!/usr/bin/python3

import pickle
import os
import getpass
import os
import json
from datetime import datetime

def func_(vid, img, channel, upload_date):
	
	upload_date = datetime.strptime(upload_date, "%Y%m%d")
	uploaded_before_days = (datetime.now() - upload_date).days
	if uploaded_before_days < 31 or (uploaded_before_days > 365):
		msg = f"{uploaded_before_days} days ago"
	else:
		msg = f"{uploaded_before_days//31} months ago"

	vid_name = vid.strip(".webm").strip(".mkv").strip(".mp4").replace("_", ' ').capitalize()
	if vid.endswith(".part"):
		return ""
	# img = f'/home/{getpass.getuser()}/thumbnail/{img.replace("/", "_")}'
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
	# if vid.endswith(".mkv"):
		# return ""
	# print(img)
	# print(vid)
	# print() 
	# print(os.path.exists(vid) and os.path.exists(img))
	if vid.endswith(".mkv"):
		  # return f"""\n<video width="320" height="240" controls poster="{img}" src="{vid}"></video>"""
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

	# return f"""\n<video width="320" height="240" controls  poster="{img}">
	# 	<source src="{vid}" type="video/mp4">
	# 	<source src="{vid}" type="video/ogg">
	# 	<source src="{vid}" type="video/webm">
	# 	Your browser does not support the video tag.</video>"""
						# 	<source src="{vid}" type="video/mp4">
						# <source src="{vid}" type="video/ogg">
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




try:

	x = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))
	# x = sorted(x.items(), key=lambda x: x[1]['upload_date'], reverse=True) # sort by upload date 
	x = sorted(x.items(), key=lambda x: (datetime.now() - datetime.strptime(x[1]['upload_date'], "%Y%m%d")).days)
	x = {i[0] : i[1] for i in x[:150]} # only last 150 videos
	to_be_exclude = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/to_be_exclude.json", "r"))
	channels_to_exclude = to_be_exclude['channel']
	videos_to_exclude = to_be_exclude['video']

	channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))

	to_remove = []
	for k,v in x.items():
		if v['channel'] in channels_to_exclude:
			to_remove.append(k)
	if to_remove:
		for i in to_remove:
			x.pop(i)

	s = """<!DOCTYPE html><html>
	<head>
		<style>
			* {box-sizing: border-box;}
			.column {float: right;width: 20.00%; padding: 0px;}
			/* Clearfix (clear floats) */
			.row::after {content: "";clear: both;display: table;}
		</style>
	</head>
	<body>
		<div class="row">
			"""
	# c = 0
	for k,v in x.items():
		if k in videos_to_exclude:
			continue
		# c += 1
		# if c > 12:
		# 	break
		s += func_(
			vid = v['video_name'], 
			# img = v['thumbnail_url'], # fatching from internet
			img = f"/home/{getpass.getuser()}/github/Kids_Vids/thumbs/{v['thumbnail_name']}", 
			channel = v['channel'],
			upload_date = v['upload_date']
			)
		# s += f"<br><{v['video_name']}"

	s += "\n</div></body></html>"

	open(f"/home/{getpass.getuser()}/github/Kids_Vids/dashboard.html", 'w').write(s)
	import webbrowser
	webbrowser.get("chromium").open(f"/home/{getpass.getuser()}/github/Kids_Vids/dashboard.html")
	# os.system(f"chromium /home/{getpass.getuser()}/github/Kids_Vids/dashboard.html")
except Exception as e:
	print(e)
	open(f"/home/{getpass.getuser()}/github/Kids_Vids/EX.txt", 'w').write(str(e))