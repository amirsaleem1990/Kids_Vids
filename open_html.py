#!/usr/bin/python3

import pickle
import os

def func_(vid, img):
	if vid.endswith(".part"):
		return ""
	# img = f'/home/home/thumbnail/{img.replace("/", "_")}'
	vid = f'/home/home/Videos/{vid}'
	vid = vid[::-1].split('.', 1)[-1][::-1]
	for i in ('mkv', 'mp4', 'webm'):
		vid_ = vid  + "." + i
		if os.path.exists(vid_):
			vid = vid_
			break
	else:
		return ""
	# if vid.endswith(".mkv"):
		# return ""
	# print(img)
	# print(vid)
	# print() 
	# print(os.path.exists(vid) and os.path.exists(img))
	if vid.endswith(".mkv"):
		  return f"""\n<video width="320" height="240" controls poster="{img}" src="{vid}"></video>"""
	return f"""\n<video width="320" height="240" controls  poster="{img}">
		<source src="{vid}" type="video/mp4">
		<source src="{vid}" type="video/ogg">
		<source src="{vid}" type="video/webm">
		Your browser does not support the video tag.</video>"""

try:

	x = pickle.load(open("/home/home/github/Kids_Vids/mapping.pkl", 'rb'))
	x = sorted(x.items(), key=lambda x: x[1]['upload_date'], reverse=True) # sort by upload date 
	x = {i[0] : i[1] for i in x}

	s = """<!DOCTYPE html><html><body><div id="contents">"""

	for k,v in x.items():
		s += func_(v['video_name'], v['thumbnail_url'])

	s += "\n</div></body></html>"
	open("/home/home/github/Kids_Vids/dashboard.html", 'w').write(s)
	os.system("chromium /home/home/github/Kids_Vids/dashboard.html")
except Exception as e:
	open("/home/home/github/Kids_Vids/EX.txt", 'w').write(str(e))