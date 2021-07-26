#!/usr/bin/python3
from datetime import timedelta
import get_soup_object_using_selenium
import multiprocessing.dummy
import subprocess
import os
import pickle
import json
from datetime import datetime


if os.path.exists("mapping.pkl"):
    mapping = pickle.load(open("mapping.pkl", 'rb'))
else:
    mapping = dict()

if os.path.exists("Error_file.pkl"):
    errors = pickle.load(open("Error_file.pkl", 'rb'))
else:
    errors = dict()

def download_thumbnails():
    global mapping
    print("\n---- Starting download_thumbnails ........")
    try:
        for url, values in mapping.items():
            com = f"youtube-dl --no-playlist {url} --list-thumbnails"
            thumbnail = "http" + list(os.popen(com))[-1].split("http")[1]
            img_name = thumbnail.strip().replace('/', '_')
            mapping[url].append(img_name)
            thumbn = f"/home/home/thumbnail/{img_name}"
            if os.path.exists(thumbn):
                continue
            com = f"curl {thumbnail.strip()} > {thumbn}"
            os.system(com)
    except Exception as e:
        errors[url] = ["download_thumbnails",e, str(datetime.now())]
        mapping[url].append("Error")

def download_videos(x):
    try:
        url, v = x
        file_name = v[3]
        # file_name = f'Videos/{list(os.popen(f"youtube-dl --restrict-filenames --get-filename {url}"))[0].strip()}'
        subprocess.check_call(['youtube-dl', url, '-o', file_name])
        open("downloaded.txt", "a").write(url+"\n")
    except Exception as e:
        errors[url] = ["download_videos",e, str(datetime.now())]


channels = [
    ('robocar', "https://www.youtube.com/c/robocarpoli/videos"),
    ('VladandNiki', "https://www.youtube.com/c/VladandNiki/videos"),
    ('ChuchuTv', "https://www.youtube.com/c/ChuChuTVBedtimeStories/videos")
]



def main():
    try:
        downloaded = open("downloaded.txt", 'r').read().splitlines()
        for i in channels:
            channel, url = i
            x = get_soup_object_using_selenium.get_soup_object_using_selenium(url)[0]
            urls = ['https://www.youtube.com'+i for i in x if i.startswith("/watch?")]
            x_2 = [i for i in urls if not i in downloaded]
            for u in x_2:
                x = json.loads(list(os.popen(f"youtube-dl -j  {u}"))[0])
                if int(x['duration']) == 0:
                    continue
                duration = str(timedelta(seconds=int(x['duration'])))
                if duration.split(":")[0] == "0":
                    duration = "0" + duration
                mapping[u] = [channel, 
                              x['upload_date'], 
                              duration, 
                              "/home/home/Videos/" + list(os.popen(f"youtube-dl --restrict-filenames --get-filename {u}"))[0].strip()
                              ]
    except Exception as e:
        errors[url] = ["main",e, str(datetime.now())]


main()
download_thumbnails()
pickle.dump(errors, open("Error_file.pkl", 'wb'))

# mapping = {
#     'https://www.youtube.com/watch?v=hZkbyKrJ6D8': 
#     [
#         'ChuchuTv',
#         '20201031',
#         '00:36:30',
#         'Strength in Unity, Ice Cream Truck, Little Forest Rangers - ChuChuTV Storytime Adventures Collection-hZkbyKrJ6D8.webm',
#         'https:__i.ytimg.com_vi_hZkbyKrJ6D8_maxresdefault.jpg'
#     ]
# }


for url, values in mapping.items():
    if  'Error' in values:
        mapping.pop(url)

pickle.dump(mapping, open("mapping.pkl", 'wb'))
# mapping = pickle.load(open("mapping.pkl", 'rb'))

if len(mapping):
    p = multiprocessing.dummy.Pool()
    print("\n---- Starting download_videos ........")
    p.map(download_videos, list(mapping.items()))
