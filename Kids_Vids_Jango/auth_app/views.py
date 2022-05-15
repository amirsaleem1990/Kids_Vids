import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse
import getpass
import os
import shutil
import pickle
import sys
import json


def replace_wrong_videos_names_with_correct_one(x : dict) -> dict:
	data_vids = pd.DataFrame.from_dict(x, orient="index").video_name.to_list()
	disk_vids = os.listdir("/home/home/Videos/")

	files_in_disk_but_not_in_data = []
	for i in disk_vids:
		if not i in data_vids:
			if not i.endswith(".part"):
				files_in_disk_but_not_in_data.append(i)
	if files_in_disk_but_not_in_data:
		df = pd.DataFrame.from_dict(x, orient="index")
		df.reset_index(drop=True, inplace=True)
		df_copy = df.copy(deep=True)
		r2 = df.video_name.reset_index(drop=True)
		for disk_value in files_in_disk_but_not_in_data:
			disk_value_without_extention = disk_value.split(".")[0]
			q = r2.str.contains(disk_value_without_extention)
			if q.sum() > 0:
				data_value = r2.iloc[q.idxmax()]
				if data_value.split(".")[0] == disk_value_without_extention:
					df.loc[df.video_name.eq(data_value), "video_name"] = disk_value
		x = df.to_dict(orient="index")
	return x

def auth_(request):
	print('................ auth_app.auth_ called')
	return render(request, 'auth.html')

#ab user peechy ja kar new items select nahi kar sakta.
from django.views.decorators.cache import cache_control
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def auth_check(request):
	print("................ auth_app.auth_check called")
	password = request.POST['user_password']
	

	# should be corrected  # amir
	if password.lower().strip() == '03323388625':
		# if True:
		# os.system(f"/home/{getpass.getuser()}/github/Kids_Vids/open_html.py")
		# shutil.copy(f"/home/{getpass.getuser()}/github/Kids_Vids/dashboard.html", f"/home/{getpass.getuser()}/github/Kids_Vids/Kids_Vids_Jango/auth_app/templates/dashboard.html")
		# print("................ rendering dashboard.html page") 
		# return render(request, 'dashboard.html')

		sys.path += [f'/home/{getpass.getuser()}/github/Kids_Vids']
		
		# from get_current_channels import get_channels
		def get_channels():
			print("\n\n>> get_channels method is called.")

			channels = pickle.load(open("/home/amir/github/Kids_Vids/channels.pkl", 'rb'))
			channels_mapping = json.load(open("/home/amir/github/Kids_Vids/channels_mapping.txt", "r"))
			to_be_exclude = json.load(open("/home/amir/github/Kids_Vids/to_be_exclude.json", "r"))

			channels_to_exclude = to_be_exclude['channel']
			if channels_to_exclude:
				l = [k  for k,v in channels_mapping.items() if v in channels_to_exclude]
				channels = [c for c in channels if not c[0] in l]
			return channels
		channels = get_channels()

		channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))
		list_of_channels = [channels_mapping[i[0]] for i in channels]

		x = pickle.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/mapping.pkl", 'rb'))
		x = replace_wrong_videos_names_with_correct_one(x)
		channels = {}
		for url, data in x.items():
			if data['channel'] in list_of_channels and (os.path.exists(f"/home/home/Videos/{data['video_name']}")):
					channels[data['channel']] = channels.get(data['channel'], 0) + 1
		channels = [(k,v) for k,v in channels.items()]

		# return render(request, 'select_channels/choose_channels.html', {"channels" : list_of_channels})
		return render(request, 'select_channels/choose_channels.html', {"channels" : channels})
 
	else:
		return render(request, 'Error.html', {"error" : "Wrong password"})
