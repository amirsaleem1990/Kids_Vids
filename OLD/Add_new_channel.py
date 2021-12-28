import json
import pickle
import requests
from get_soup_object_using_selenium import get_soup_object_using_selenium
from bs4 import BeautifulSoup

# try:
	# url = sys.argv[1]
# except:
	# url = input("Enter a url:")

def get_channel_name_by_url(url):
	x = get_soup_object_using_selenium(url)
	return x[1].find("div", {"id" : "text-container"}).text.strip()

channels_mapping = json.load(open("channels_mapping.txt", 'r'))
channels = pickle.load(open("channels.pkl", 'rb'))
urls_in_channels = [i[1] for i in channels]
new_channels = open("new_channels", 'r').read().splitlines()
new_channels = [i for i in new_channels if i and (not i.startswith("#"))]


d = {}
for url in new_channels:
	if url in urls_in_channels:
		print(f"\nThe url {url} is exists in channels.pkl, skipping........")
		continue
	key = url.split("/")[4]
	channel_name = get_channel_name_by_url(url)
	d[key] =(channel_name, url)
if not d:
	print("===============================")
	exit()

changings_qty = 0

for key,value in d.items():
	channel_name, url = value
	inp = input(f"""\n\nGoing to add:\n'{key}':'{channel_name}'' to channels_mapping.txt\n{key, url} to  channels.pkl\nAre you agree? [y|n]: """)
	# inp = input(f"\nGiving this <{url}> we add this {key}:{channel_name} as a new entry in the 'to channels_mapping.txt'. Are you agree? [y|n] ")
	if inp == 'y':
		changings_qty += 1
		channels_mapping[key] = channel_name
		channels.append( (key, url) )

if changings_qty:
	json.dump(channels_mapping, open("channels_mapping.txt", 'w'))
	pickle.dump(channels, open("channels.pkl", 'wb'))