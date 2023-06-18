import pandas as pd
from django.shortcuts import render
from django.http.response import HttpResponse
import getpass
import os
import shutil
import pickle
import sys
import json
from get_soup_object_using_selenium import get_soup_object_using_selenium



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
		# shutil.copy(f"/home/{getpass.getuser()}/github/Kids_Vids/dashboard.html", f"/home/{getpass.getuser()}/github/Kids_Vids/Kids_Vids_Jango_ONLINE/auth_app/templates/dashboard.html")
		# print("................ rendering dashboard.html page") 
		# return render(request, 'dashboard.html')

		sys.path += [f'/home/{getpass.getuser()}/github/Kids_Vids']
		
		# from get_current_channels import get_channels
		def get_channels():
			print("\n\n>> get_channels method is called.")
			channels_dict = json.load(open("channels.json", 'r'))
			channels_dict = {k:v for k,v in channels_dict.items() if not k.startswith("_")}
			return channels_dict

		channels_dict = get_channels()
		pickle.dump(channels_dict, open("channels_dict.pkl", 'wb'))

		channels_mapping = json.load(open("channels_mapping.json", 'r'))
		channels_dict_clean_name = {channels_mapping[k]:v for k,v in channels_dict.items()}
		pickle.dump(channels_dict_clean_name, open("channels_dict_clean_name.pkl", 'wb'))

		channels_clean_names_and_urls_count = [(k,len(v)) for k,v in channels_dict_clean_name.items()]
		return render(request, 'select_channels/choose_channels.html', {"channels_clean_names_and_urls_count" : channels_clean_names_and_urls_count})
 
	else:
		return render(request, 'Error.html', {"error" : "Wrong password"})
