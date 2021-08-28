

from django.shortcuts import render
from django.http.response import HttpResponse
import getpass
import json
import shutil
import getpass
import pickle
import sys

def show_selected_channels(request):
	x = dict(request.POST)
	selected_channels = [k.strip() for k,v in x.items() if v == ['on']]
	channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))
	channels_mapping_flapped = {v:k for k,v in channels_mapping.items()}
	selected_channels = [channels_mapping_flapped[i] for i in selected_channels if i in channels_mapping_flapped.keys()]


	sys.path += [f'/home/{getpass.getuser()}/github/Kids_Vids']
	from get_current_channels import get_channels
	channels = get_channels()
	channels = [i for i in channels if i[0] in selected_channels]
	
	print("...............................................................")
	print(*channels, sep="\n")
	# return render(request, 'choose_channels.html', {"channels" : list_of_channels})
