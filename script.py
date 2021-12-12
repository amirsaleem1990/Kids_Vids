#!/usr/bin/ipython3
import time
from multiprocessing import Pool  
import multiprocessing.dummy 
import subprocess 
import os 
import pickle 
import json 
from datetime import datetime  
import traceback 
import getpass
import sys

class Kids_Vids:
    def __init__(self, mapping_file_name, error_file_name="Error.pkl"):
        
        self.base_path = f"/home/{getpass.getuser()}/github/Kids_Vids/"
        self.videos_dir_path = "/home/home/Videos/"
        self.mapping = pickle.load(open(f"{self.base_path}{mapping_file_name}"))
        if mapping_file_name == 'mapping.pkl':
            self.original_mapping = self.mapping
        else:
            self.original_mapping = pickle.load(open(f"{self.base_path}/mapping.pkl", 'rb'))

        if error_file_name == "Error.pkl":
            print(f"\n\nYou are not passed error file name, so the defaul '{error_file_name}' is used\n")
        self.errors = pickle.load(open(f"{self.base_path}{error_file_name}", 'rb'))

    def download_a_video(self, url):
        # try:
        v = self.mapping[url]
        full_video_name = f"{self.videos_dir_path}{self.mapping[url]['video_name']}"
        if os.path.exists(full_video_name):
            print(f"\n>>. The file {full_video_name} is already exists.\n")
            return 
        # some videos name are: .mp4..mp4, .mkv.webm ...
        if full_video_name.count(".") == 2:
            print(f"\n\nSkipping this video\t{url}\n\n")
            return

        thumbnail_full_name = f"{self.base_path}thumbs/{v['thumbnail_name']}"
        if not os.path.exists(thumbnail_full_name):
            subprocess.check_call(['curl', v['thumbnail_url'], '-o', thumbnail_full_name])
        subprocess.check_call(['youtube-dl', '--no-playlist', url, '-o', full_video_name])
        print(f"\nThe video {full_video_name} is downloaded\n")
        self.mapping[url]['downloaded'] = True
        # except Exception as e:
            # print(e)
            # self.errors[url] = ["download_videos fail",e, str(datetime.now())]

    def duration_sec(self, x):
        h,m,s = x.split(":")
        h = int(h) if not h.startswith("0") else int(h[1])
        m = int(m) if not m.startswith("0") else int(m[1])
        s = int(s) if not s.startswith("0") else int(s[1])
        return s + m*60 + h*60*60

    def download_summary(self, size_before):
        size_after = int(list(os.popen(f"du -sh -BM  {self.videos_dir_path}"))[0].strip().split("\t")[0].strip("M"))
        size_downloaded = size_after - size_before
        if size_downloaded > 1000:
            size_ = f'{round(size_downloaded/1000, 3)}GB'
        else:
            size_ = f'{size_downloaded}MB'
        print(f"\n######################################\nDownloaded {size_}\n######################################\n")
        time.sleep(2)

    def downlload_in_multithreding(self):

        size_before = int(list(os.popen("du -sh -BM  {self.videos_dir_path}"))[0].strip().split("\t")[0].strip("M"))

        to_be_exclude = json.load(open(f"{self.base_path}/to_be_exclude.json", "r"))
        channels_to_exclude = to_be_exclude['channel']
        to_download = [
            k for k,v in self.mapping.items() if (not v['downloaded']) \
                and (not v['channel'] in channels_to_exclude) \
                and (duration_sec(v['duration']) > 180) \
                and (duration_sec(v['duration']) < 7200)
            ]
        is_error = False
        try:
            if to_download:
                p = multiprocessing.dummy.Pool()
                print( "\n---- download_videos called ........")
                print(f"\n--------------------------------------------------- {len(to_download)} videos to be downloaded ..........\n\n")
                p.map(download_a_video, to_download)
            else:
                print("\n\nNo videos to be download\n")
                exit()
        except:
            error__ = str(traceback.format_exc())
            print("\n"*6)
            print("An error occured")
            is_error = True

        if self.errors:
            pickle.dump(self.errors, open(f"{self.base_path}/Error.pkl", 'wb'))
        self.original_mapping.update(self.mapping)
        print("\n\nSaving mapping.pkl ........")
        pickle.dump(self.original_mapping, open(f"{self.base_path}/mapping.pkl", 'wb'))

        download_summary(size_before)

        if is_error:
            raise Exception(error__)

if __name__ == "__main__":
    mapping_file_name = input("Enter you mapping file name: \nNote: Press Enter for using defaul mapping <mapping.pkl>\n")
    if not mapping_file_name:
        mapping_file_name = 'mapping.pkl'

    kids_vids_obj = Kids_Vids(mapping_file_name, error_file_name="Error.pkl")

    try:
        kids_vids_obj.downlload_in_multithreding()
    except KeyboardInterrupt:
        sys.exit()
        
    while [i for i in os.listdir(self.videos_dir_path) if i.endswith(".part")]:
        print("\n\n\n\n=======================================================\n")
        print("There are some .part files left, retrying again......")
        try:
            kids_vids_obj.downlload_in_multithreding()
            time.sleep(60)
        except KeyboardInterrupt:
            sys.exit()