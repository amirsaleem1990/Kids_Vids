#!/usr/bin/ipython3
import sys
import pickle
import getpass

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

# live_robocar_poli_full_episodes_non_stop_rescue_episodes_robocar_poli_tv.webm
