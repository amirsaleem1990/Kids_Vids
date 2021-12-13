#!/usr/bin/ipython3
import pickle
import pandas as pd
import os
import shutil
import json

video_path = '/home/home/Videos'

def get_actual_video_name(vid_name):
    if not vid_name.split(".")[-1] in ['mp4', 'mkv', 'webm']:
        return None
    video_name_without_extention = vid_name.replace(".mp4", '').replace(".webm", '').replace(".mkv", '')
    for extention in ['.mkv', '.mp4', '.webm']:
        if f"{video_name_without_extention}{extention}" in saved_vids_names:
                return  f"{video_path}/{video_name_without_extention}{extention}"
    else:
        print(f"!! The video '{vid_name}' is not found.")
        return None

def func(row):
    global files_moved
    global files_error
    directory_name = f"{video_path}/{row.channel}/"
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)
        print(f"\n>>>> Directory <{directory_name}> created.\n")
    try:
        if os.path.exists(row.video_name):
            print(f"\n! The Videos '{row.video_name}' already exisits in '{directory_name}'")
            return
        shutil.move(row.video_name, directory_name)
        d[directory_name.strip(f'{video_path}/')] = d.get(directory_name.strip(f'{video_path}/'), 0) + 1
        files_moved += 1
    except:
        files_error += 1

saved_vids_names = os.listdir(video_path)
x = pickle.load(open("mapping.pkl", 'rb'))
df = (pd
      .DataFrame
      .from_dict(x, orient="index")
      .reset_index()
      .rename(columns={"index" : "url"})
      .loc[:, ['channel', 'video_name']]
)

df.video_name = df.video_name.apply(get_actual_video_name)
files_not_moved = df.video_name.isna().sum()
df = df.dropna()

files_moved = 0
files_error = 0

d = {}
df.apply(func, axis=1)

print("\n\n")
print("files_moved:     ", files_moved)
print("files_error:     ", files_error)
print("files_not_moved: ", files_not_moved)

print()

print(json.dumps(d, indent=4))

print()
