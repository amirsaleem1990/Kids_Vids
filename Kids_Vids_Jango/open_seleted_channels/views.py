from django.shortcuts import render
from django.http.response import HttpResponse
import getpass
import json
import shutil
import getpass
import pickle
import sys

def open_seleted_channels(request):
	x = dict(request.POST)
	print("-----------------------------------------!!!!!!!!!!!!!!!!!!")
	print(x)
	# return render(request, 'choose_channels.html', {"channels" : list_of_channels})
