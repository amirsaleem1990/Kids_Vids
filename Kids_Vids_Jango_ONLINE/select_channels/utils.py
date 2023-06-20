from get_soup_object_using_selenium import get_soup_object_using_selenium
import time
import pickle
import os
import youtube_dl
from datetime import timedelta
import re

def get_videos_urls_from_channel_url(channel_url):
    x = get_soup_object_using_selenium(url=channel_url)
    urls = list(map(lambda x: 'https://www.youtube.com' + x, filter(lambda y: y.startswith("/watch?v="), x[0])))
    return list(set(urls))


def duration_sec(x):
    h, m, s = x.split(":")
    h = int(h) if not h.startswith("0") else int(h[1])
    m = int(m) if not m.startswith("0") else int(m[1])
    s = int(s) if not s.startswith("0") else int(s[1])
    return s + m*60 + h*60*60


def check_if_channel_file_exist(channel_name):
    for f in os.listdir("vids_info/"):
        if channel_name == f.split("--")[0]:
            return (True, int(f.split("--")[1].replace(".pkl", "")))
    return (False,False)


def get_urls(channel_name, channel_url):
    exist, saving_time = check_if_channel_file_exist(channel_name)
    if not exist or (time.time() - saving_time) > 86400:
        urls = get_videos_urls_from_channel_url(channel_url)
        pickle.dump(urls, open(f"vids_info/{channel_name}--{int(time.time())}.pkl", 'wb'))
        if not exist:
            print(f"\n>>> Urls for '{channel_name}' doesn't exist, so we scraped them, and saved them for future use\n")
        else:
            print(f"\n>>> Urls for '{channel_name}' exist, but it's more than 24 hours old, so we scraped the new one, and saved them for future use\n")
    else:
        current_channel_files = list(filter(lambda x: x.startswith(f"{channel_name}--"), os.listdir("vids_info/")))
        if len(current_channel_files) == 1:
            urls = pickle.load(open(current_channel_files[0], 'rb'))
            print(f"\n>>> Urls for '{channel_name}' are existing\n")
        else:
            most_recent_file_name = sorted(current_channel_files, key=lambda x: int(x.split('--')[1].replace(".pkl", "")), reverse=True)[0]
            urls = pickle.load(open(most_recent_file_name, 'rb'))
            print(f"\n>>> Urls for '{channel_name}' are existing\n")
    # if not urls:
        # print(f"\n>>> No urls for the '{channel_name}'|'{channel_url}', so we retry..")
        # if exist:
        #     if len(current_channel_files) == 1:
        #         os.remove(current_channel_files[0])
        #     else:
        #         os.remove(most_recent_file_name)
        # get_urls(channel_name, channel_url)
    return urls

def get_video_info(url, file_name):

    urls_info = pickle.load(open('urls_info.pkl', 'rb'))

    if url in urls_info:
        return urls_info[url]
    if os.path.exists(file_name):
        return pickle.load(open(file_name, 'rb'))

    else: # No need for this `else`, but it's easear to understand the flow
        try:
            x = (
                    youtube_dl
                    .YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'noplaylist' : True})
                    .extract_info(url, download=False) # We just want to extract the info
                )
        except:
            print(f">>> Failed to fetch information about '{url}'")
            return
        if x:
            duration = x['duration']
            if int(duration) == 0:
                return
            duration = str(timedelta(seconds=int(duration)))
            if duration.split(":")[0] == "0":
                duration = "0" + duration

            n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyzاأبتثجحخدذرزسشصضطظعغفقكلمنوهيى" else "_" for i in x.get("title").lower()])
            video_name = f"{re.sub('_+', '_', n_).strip('_')}"

            thumbnail_url = x.get("thumbnail")
            if ".jpg" in thumbnail_url:
                thumbnail_url = thumbnail_url.split(".jpg")[0] + ".jpg"

            dict_ = {
                "channel"        : x.get("channel"), 
                "upload_date"    : x.get('upload_date'), 
                "duration"       : duration, 
                "video_name"     : video_name,
                "thumbnail_url"  : thumbnail_url
            }
            urls_info = pickle.load(open('urls_info.pkl', 'rb'))
            urls_info[url] = dict_
            pickle.dump(urls_info, open('urls_info.pkl', 'wb'))

            return dict_


def get_and_save_video_info(url, vids_info):
    try:
        file_name = "urls_info/url_info_" + url.replace("/", "_") + ".pkl"
        vids_info[url] = get_video_info(url, file_name)
        if not os.path.exists(file_name):
            print(f"\n>>> Writing '{file_name}' to the disk.")
            pickle.dump(vids_info[url], open(file_name, 'wb'))
        else:
            print(f"\n>>> The file '{file_name}' is already exist.")
    except:
        ...