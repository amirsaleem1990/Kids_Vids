#!/usr/bin/python3
import re
from datetime import timedelta
import get_soup_object_using_selenium
import multiprocessing.dummy
import subprocess
import os
import pickle
import json
from datetime import datetime

if not os.path.exists("/home/home/Videos/"):
    raise Exception("No directory /home/home/Videos/")

if not os.path.exists("/home/home/thumbnail/"):
    raise Exception("No directory /home/home/thumbnail/")


# if os.path.exists("mapping.pkl"):
#     mapping = pickle.load(open("mapping.pkl", 'rb'))
# else:
mapping = dict()

if os.path.exists("Error_file.pkl"):
    errors = pickle.load(open("Error_file.pkl", 'rb'))
else:
    errors = dict()

def download_thumbnails():
    global mapping
    try:
        for url, values in mapping.items():
            com = f"youtube-dl --no-playlist {url} --list-thumbnails"
            thumbnail = "http" + list(os.popen(com))[-1].split("http")[1]
            img_name = thumbnail.strip().replace('/', '_')
            mapping[url].append(img_name)
            thumbn = f"/home/home/thumbnail/{img_name}"
            if os.path.exists(thumbn):
                to_skip = [url]
                continue
            com = f"curl {thumbnail.strip()} > {thumbn}"
            os.system(com)
    except Exception as e:
        errors[url] = ["download_thumbnails",e, str(datetime.now())]
        mapping[url].append("Error")

def download_videos(x):
    print("\n---- download_videos called ........")
    try:
        url, v = x
        file_name = v[3]
        if (url in to_skip) or (file_name in iter_):
            return None
        # file_name = f'Videos/{list(os.popen(f"youtube-dl --restrict-filenames --get-filename {url}"))[0].strip()}'
        subprocess.check_call(['youtube-dl', url, '-o', file_name])
        open("downloaded.txt", "a").write(url+"\n")
    except Exception as e:
        errors[url] = ["download_videos",e, str(datetime.now())]


def gather_meta_data(u):
    print("\n---- gather_meta_data called ........")
    try:
        print(f'----------------------Extracting information about <{u}>')
        
        id_ = x['id']

        if int(x['duration']) == 0:
            to_skip.append(u)
            return None
        duration = str(timedelta(seconds=int(x['duration'])))
        if duration.split(":")[0] == "0":
            duration = "0" + duration

        # video_name = "/home/home/Videos/" + list(os.popen(f"youtube-dl --restrict-filenames --get-filename {u}"))[0].strip()
        # video_name = video_name.replace(id_, "").replace(" ", "").replace("-.", ".")
        n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyz" else "_" for i in x.get("title").lower()])
        video_name = f"{re.sub('_+', '_', n_).strip('_')}.{x['ext']}"

        if video_name in iter_:
            to_skip.append(u)
            return None

        mapping[u] = [channel, 
                      x['upload_date'], 
                      duration, 
                      video_name
                      ]
    except Exception as e:
        print(f"\n\n\nUrl: {u}\nError: {e}\n\n\n")
        errors[url] = ["faild to extract data",e, str(datetime.now())]

to_skip = []

channels = [
    ('robocar', "https://www.youtube.com/c/robocarpoli/videos"),
    ('VladandNiki', "https://www.youtube.com/c/VladandNiki/videos"),
    ('ChuchuTv', "https://www.youtube.com/c/ChuChuTVBedtimeStories/videos")
]

import itertools
iter_ = list(itertools.chain.from_iterable(list(mapping.values())))

if os.path.exists("downloaded.txt"):
    downloaded = open("downloaded.txt", 'r').read().splitlines()
else:
    downloaded = []

# to_download = []
# for i in channels:
#     channel, url = i
#     x = get_soup_object_using_selenium.get_soup_object_using_selenium(url)[0]
#     urls = ['https://www.youtube.com'+i for i in x if i.startswith("/watch?")]
#     x_2 = [i for i in urls if not i in downloaded]
#     to_download += x_2


# pickle.dump(to_download, open("to_download.pkl", 'wb'))
# print("\n\n ---------------------------- to_download saved as to_download.pkl\n\n")

to_download = pickle.load(open("to_download.pkl", 'rb'))

# def func(u): 
#     subprocess.call(['youtube-dl', '-j', u], stdout=open(f'jsons/{u.replace("/", "_")}', "w"))
#     print(f"{u}  .............................")
# import multiprocessing.dummy
# import subprocess
# p = multiprocessing.dummy.Pool()
# p.map(func, to_download)

# import time
for u in to_download:
    print(f'.............................{u}')
    com =  (f"youtube-dl -j '{u}' > jsons/\'{u.replace('/', '_')}\'")
    os.system(com)
    time.sleep(5)

# d_ = {}
# for u in to_download:
#     try:
#         d_[u] = json.loads(list(os.popen(f"youtube-dl -j  {u} 2>/dev/null"))[0])
#     except Exception as e:
#         print(f"Error\t\t\t{u}")


# open("r_.sh", 'w').write(r_)
# os.system('bash r_.sh')


# pickle.dump(d_, open("d_.pkl", 'wb'))
# print("\n\n ---------------------------- d_ saved as d_.pkl\n\n")


gather_meta_data()

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

to_del = []
for url, values in mapping.items():
    if  'Error' in values:
        to_del.append(url)
for d in to_del:
    mapping.pop(d)
pickle.dump(mapping, open("mapping.pkl", 'wb'))
# mapping = pickle.load(open("mapping.pkl", 'rb'))

if len(mapping):
    p = multiprocessing.dummy.Pool()
    print("\n---- download_thumbnails called ........")
    p.map(download_videos, list(mapping.items()))