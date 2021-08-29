from django.shortcuts import render
from django.http.response import HttpResponse
import getpass
import os
import shutil
import pickle
import sys
import json

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
		from get_current_channels import get_channels

		channels = get_channels()
		channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))
		list_of_channels = [channels_mapping[i[0]] for i in channels]

		return render(request, 'select_channels/choose_channels.html', {"channels" : list_of_channels})
 
	else:
		return render(request, 'Error.html', {"error" : "Wrong password"})
