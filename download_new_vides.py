#!/usr/bin/python3
def extract_videos_from_channel_page(channel_url):
    browser.get(channel_url)
    s = BeautifulSoup(browser.page_source, "lxml")
    extrected_urls = []
    for i in s.select("a"):
        try:    
            extrected_urls.append(i['href'])
        except: 
            pass
    for i in s.select("source"):
        try:
            extrected_urls.append(i['src'])
        except:
            pass
        # print('ooooooooooooooooooooooooooooooooooooooo', len(extrected_urls))
        return list(set(extrected_urls))


# def get_urls_to_download(channels):
#     to_download = []
#     for i in channels:
#         try:
#             channel, url = i
#             x = get_soup_object_using_selenium.get_soup_object_using_selenium(url)[0]
#             urls = ['https://www.youtube.com'+i for i in x if i.startswith("/watch?")]
#             x_2 = [i for i in urls if not i in downloaded]
#             to_download += x_2
#         except:
#             errors[i] = ["No video in the channel",e, str(datetime.now())]
#     pickle.dump(to_download, open("to_download.pkl", 'wb'))
#     print("\n\n ---------------------------- to_download saved as to_download.pkl\n\n")
#     return to_download

def get_urls_to_download(c):
    start_time_ = time.time()
    # print(f"\nExtracting urls from <{c[0]}>")
    try:
        channel, url = c
        # print(f"Channel: {channel}\tUrl: {url}")
        x = extract_videos_from_channel_page(channel_url=url)
        urls = ['https://www.youtube.com'+i for i in x if i.startswith("/watch?")]
        if urls:
            for e,i in enumerate(urls):
                if '&' in i:
                    urls[e] = i.split("&")[0]

        x_2 = [i for i in urls if not i in downloaded]
        print(f"Extracted {len(x_2)} urls from {channel}")
        pickle.dump(x_2, open(f"to_download_{channels.index(c)}.pkl", 'wb'))
    except Exception as e:
        print(f"Error, No url extracted from channel <{channel}>\n")
        # print(e)
        # print()
        errors[c] = ["No video in the channel <{channel} for the url: <{url}>>",e, str(datetime.now())]
    print(f"................{url} consumed {time.time() - start_time_} seconds")


"""
# def download_jsons(to_download):
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
        except Exception as e:
            print(e)
            to_skip.append(u)
            errors[u] = ["download_jsons fail",e, str(datetime.now())]

# def extrect_data_from_json(to_download):
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
            # if video_name in iter_:
            #     to_skip.append(u)
            #     continue
            mapping[u] = [x.get("channel"), 
                          x.get('upload_date'), 
                          duration, 
                          video_name,
                          x.get("thumbnail")
                          ]
        except Exception as e:
            # print(f"\n\n\nUrl: {u}\nError: {e}\n\n\n")
            errors[u] = ["extrect_data_from_json fail",e, str(datetime.now())]
            print(e)
            to_skip.append(u)
            pass

# def download_thumbnails(to_download):
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
"""

def get_info(to_download):
    print("\n---- get_info called ........")
    for u in to_download:
        try:
            s = time.time()
            import youtube_dl
            ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
            with ydl:
                x = ydl.extract_info(u, download=False) # We just want to extract the info
            if x:
                duration = x['duration']
                if int(duration) == 0:
                    to_skip.append(u)
                    continue
                duration = str(timedelta(seconds=int(duration)))
                if duration.split(":")[0] == "0":
                    duration = "0" + duration

                n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyz" else "_" for i in x.get("title").lower()])
                video_name = f"{re.sub('_+', '_', n_).strip('_')}.{x['ext']}"

                thumbnail_url = x.get("thumbnail")
                if ".jpg" in thumbnail_url:
                    thumbnail_url = thumbnail_url.split(".jpg")[0] + ".jpg"
                thumbnail_name = thumbnail_url.strip().replace('/', '_')

                # if video_name in iter_:
                #     to_skip.append(u)
                #     continue
                mapping[u] = {"channel" : x.get("channel"), 
                              "upload_date" : x.get('upload_date'), 
                              "duration" : duration, 
                              "video_name" : video_name,
                              "thumbnail_url" : thumbnail_url,
                              "thumbnail_name" : thumbnail_name
                              }
                              
            print(f'.............................{u}, Sec consumed: {time.time() - s}')
            time.sleep(2)
        except Exception as e:
            to_skip.append(u)
            print('---------------------------')
            print(e)
            print()
            errors[u] = ["download_jsons fail",e, str(datetime.now())]



def download_videos(url):
    try:
        if mapping.get(url) is None:
            return None
        file_name = mapping[url]['video_name']
        # file_name = f'Videos/{list(os.popen(f"youtube-dl --restrict-filenames --get-filename {url}"))[0].strip()}'
        subprocess.check_call(['youtube-dl', url, '-o', f'/home/home/Videos/{file_name}'])
        open("downloaded.txt", "a").write(url+"\n")
    except Exception as e:
        print(e)
        errors[url] = ["download_videos fail",e, str(datetime.now())]




import itertools
import re
import time
from datetime import timedelta
import multiprocessing.dummy
import subprocess
import os
import pickle
import json
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup

pkls = [i for i in os.listdir() if i.startswith("to_download_") and i.endswith(".pkl")]
if pkls:
    for i in pkls:
        os.remove(i)

if not os.path.exists("/home/home/Videos/"):
    raise Exception("No directory /home/home/Videos/")

if not os.path.exists("/home/home/thumbnail/"):
    raise Exception("No directory /home/home/thumbnail/")

if os.path.exists("downloaded.txt"):
    downloaded = open("downloaded.txt", 'r').read().splitlines()
else:
    downloaded = list()

if os.path.exists("mapping.pkl"):
    mapping = pickle.load(open("mapping.pkl", 'rb'))
else:
    mapping = dict()

if os.path.exists("Error_file.pkl"):
    errors = pickle.load(open("Error_file.pkl", 'rb'))
else:
    errors = dict()

to_skip = []
# json_name_mapping = {}

channels = [
    ('robocar',           "https://www.youtube.com/c/robocarpoli/videos"),
    ('VladandNiki',       "https://www.youtube.com/c/VladandNiki/videos"),
    ('ChuchuTv',          "https://www.youtube.com/c/ChuChuTVBedtimeStories/videos"),
    ('scishowkids',       'https://www.youtube.com/c/scishowkids/videos'),
    ('PeekabooKids',      'https://www.youtube.com/c/PeekabooKids/videos'),
    ('MorphleTV',         'https://www.youtube.com/c/MorphleTV/videos'),
    ('Blippi',            'https://www.youtube.com/c/Blippi/videos'),
    ('CraftsforKids',     'https://www.youtube.com/c/CraftsforKids/videos'),
    ('ClarendonLearning', 'https://www.youtube.com/c/ClarendonLearning/videos'),
    ('FreeSchool',        'https://www.youtube.com/c/FreeSchool/videos'),
    ('KidsLearningTube',  'https://www.youtube.com/c/KidsLearningTube/videos'),
    ('NUMBEROCKLLC',      'https://www.youtube.com/c/NUMBEROCKLLC/videos'),
    ('natgeokids',        'https://www.youtube.com/natgeokidsplaylists/videos'),
    ('TheDadLab',         'https://www.youtube.com/c/TheDadLab/videos'),
    ('5MinuteCraftsPLAY', 'https://www.youtube.com/c/5MinuteCraftsPLAY/videos')

]

# iter_ = list(itertools.chain.from_iterable(list(mapping.values())))

from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("--headless")
browser = webdriver.Firefox(executable_path = "geckodriver", options=options)


from multiprocessing import Pool
pool = Pool()   # Create a multiprocessing Pool
pool.map(get_urls_to_download, channels)

browser.close()

pkls = [i for i in os.listdir() if i.startswith("to_download_") and i.endswith(".pkl")]
to_download = []
for i in pkls:
    to_download += pickle.load(open(i, 'rb'))
to_download = list(set(to_download))

for i in pkls:
    os.remove(i)


pickle.dump(to_download, open("to_download.pkl", 'wb'))
print("\n\n ---------------------------- to_download saved as to_download.pkl\n\n")

to_download = pickle.load(open("to_download.pkl", 'rb'))

# download_jsons(to_download)

get_info(to_download)
pickle.dump(mapping, open("mapping.pkl", 'wb'))
mapping = pickle.load(open("mapping.pkl", 'rb'))

# extrect_data_from_json(to_download)
# pickle.dump(mapping, open("mapping.pkl", 'wb'))
# mapping = pickle.load(open("mapping.pkl", 'rb'))

# download_thumbnails(to_download) 
# pickle.dump(mapping, open("mapping.pkl", 'wb'))
# mapping = pickle.load(open("mapping.pkl", 'rb'))

if errors:
    pickle.dump(errors, open("Error.pkl", 'wb'))

# to_del = []
# for url, values in mapping.items():
#     if  'Error' in values:
#         to_del.append(url)

# if to_del:
#     for d in to_del:
#         mapping.pop(d)

to_download = [i for i in to_download if not i in to_skip]
if to_download:
    p = multiprocessing.dummy.Pool()
    print("\n---- download_videos called ........")
    p.map(download_videos, to_download)


if errors:
  print(f"\n\n{'*'*15}ERRORS{'*'*15}")
  print(errors, sep="\n")
