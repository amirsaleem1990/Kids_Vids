#!/usr/bin/python3
import itertools
import re
import time
from datetime import timedelta
import get_soup_object_using_selenium
import multiprocessing.dummy
import subprocess
import os
import pickle
import json
from datetime import datetime

def download_jsons(to_download):
    print("\n---- download_jsons called ........")
    for u in to_download:
        try:
            s = time.time()
            json_name = f"jsons/\'{u.replace('/', '_')}\'"
            json_name_mapping[json_name] = json_name.replace("'", '')
            if os.path.exists(json_name_mapping[json_name]):
                print(f"############################# Json file {json_name} already exists")
                to_skip.append(u)
                continue
            com =  (f"youtube-dl -j '{u}' > {json_name}")
            os.system(com)
            print(f'.............................{u}, Sec consumed: {time.time() - s}')
            time.sleep(5)
        except:
            to_skip.append(u)
            pass

def extrect_data_from_json(to_download):
    global mapping
    print("\n---- extrect_data_from_json called ........")
    for u in to_download:
        if u in to_skip:
            continue
        json_name = f"jsons/\'{u.replace('/', '_')}\'"
        if not os.path.exists(json_name_mapping[json_name]):
            to_skip.append(u)
            continue
        try:
            x = json.load(open(json_name_mapping[json_name], 'r'))
            print(f'----------------------Extracting information about <{u}>')
            # id_ = x['id']
            if int(x['duration']) == 0:
                to_skip.append(u)
                continue
            duration = str(timedelta(seconds=int(x['duration'])))
            if duration.split(":")[0] == "0":
                duration = "0" + duration
            # video_name = "/home/home/Videos/" + list(os.popen(f"youtube-dl --restrict-filenames --get-filename {u}"))[0].strip()
            # video_name = video_name.replace(id_, "").replace(" ", "").replace("-.", ".")
            n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyz" else "_" for i in x.get("fulltitle").lower()])
            video_name = f"{re.sub('_+', '_', n_).strip('_')}.{x['ext']}"
            if video_name in iter_:
                to_skip.append(u)
                continue
            mapping[u] = [x.get("channel"), 
                          x.get('upload_date'), 
                          duration, 
                          video_name,
                          x.get("thumbnail")
                          ]
        except Exception as e:
            # print(f"\n\n\nUrl: {u}\nError: {e}\n\n\n")
            # errors[url] = ["faild to extract data",e, str(datetime.now())]
            to_skip.append(u)
            pass

def download_thumbnails(to_download):
    print(f'----------------------download_thumbnails called')
    global mapping
    try:
        for url in to_download:
            if url in to_skip:
                continue
            if mapping.get(url) is None:
                continue
            _,_,_,_,thumbnail_url = mapping[url]
            img_name = thumbnail_url.strip().replace('/', '_')
            mapping[url].append(img_name)
            # thumbn = f"/home/home/thumbnail/{img_name}"
            # if os.path.exists(thumbn):
            #     to_skip.append(url)
            #     continue
            # com = f"curl {thumbn.strip()} > {thumbn}"
            # os.system(com)
    except Exception as e:
        to_skip.append(url)
        errors[url] = ["download_thumbnails",e, str(datetime.now())]
        mapping[url].append("Error")

def download_videos(url):
    try:
        if url in to_skip:
            return None
        if mapping.get(url) is None:
            return None
        v = mapping[url]
        file_name = v[3]
        # file_name = f'Videos/{list(os.popen(f"youtube-dl --restrict-filenames --get-filename {url}"))[0].strip()}'
        subprocess.check_call(['youtube-dl', url, '-o', f'/home/home/Videos/{file_name}'])
        open("downloaded.txt", "a").write(url+"\n")
    except Exception as e:
        errors[url] = ["download_videos",e, str(datetime.now())]

if not os.path.exists("/home/home/Videos/"):
    raise Exception("No directory /home/home/Videos/")

if not os.path.exists("/home/home/thumbnail/"):
    raise Exception("No directory /home/home/thumbnail/")

if os.path.exists("downloaded.txt"):
    downloaded = open("downloaded.txt", 'r').read().splitlines()
else:
    downloaded = []

if os.path.exists("mapping.pkl"):
    mapping = pickle.load(open("mapping.pkl", 'rb'))
else:
    mapping = dict()

if os.path.exists("Error_file.pkl"):
    errors = pickle.load(open("Error_file.pkl", 'rb'))
else:
    errors = dict()

to_skip = []
json_name_mapping = {}

channels = [
    ('robocar', "https://www.youtube.com/c/robocarpoli/videos"),
    ('VladandNiki', "https://www.youtube.com/c/VladandNiki/videos"),
    ('ChuchuTv', "https://www.youtube.com/c/ChuChuTVBedtimeStories/videos")
]


iter_ = list(itertools.chain.from_iterable(list(mapping.values())))


to_download = []
for i in channels:
    try:
        channel, url = i
        x = get_soup_object_using_selenium.get_soup_object_using_selenium(url)[0]
        urls = ['https://www.youtube.com'+i for i in x if i.startswith("/watch?")]
        x_2 = [i for i in urls if not i in downloaded]
        to_download += x_2
    except:
        pass
pickle.dump(to_download, open("to_download.pkl", 'wb'))
print("\n\n ---------------------------- to_download saved as to_download.pkl\n\n")

to_download = pickle.load(open("to_download.pkl", 'rb'))

# download_jsons(to_download)

# extrect_data_from_json(to_download)

# pickle.dump(mapping, open("mapping.pkl", 'wb'))
# mapping = {
#     'https://www.youtube.com/watch?v=ebXCEB6JOtw': 
#         [
#             'ChuChuTV Bedtime Stories & Moral Stories for Kids', 
#             '20201128', 
#             '00:07:36', 
#             'chika_s_picnic_at_home_idea_chuchu_tv_storytime_good_habits_bedtime_stories_for_kids.webm', 
#             'https://i.ytimg.com/vi/ebXCEB6JOtw/maxresdefault.jpg'
#         ]
# }




download_thumbnails(to_download) 

if errors:
    pickle.dump(errors, open("Error.pkl", 'wb'))

to_del = []
for url, values in mapping.items():
    if  'Error' in values:
        to_del.append(url)

if to_del:
    for d in to_del:
        mapping.pop(d)


if len(to_download):
    p = multiprocessing.dummy.Pool()
    print("\n---- download_videos called ........")
    p.map(download_videos, to_download)