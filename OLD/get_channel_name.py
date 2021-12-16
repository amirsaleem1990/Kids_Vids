#!/usr/bin/ipython3
import youtube_dl
import sys
try:
	url = sys.argv[1]
except:
	url = input("Enter url: ")
yt = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', 'noplaylist' : True})
info = yt.extract_info(url, download=False)

print(
	"\n\n\"" + info.get("channel") + "\"\n\n"
	)



# import youtube_dl
# url = "https://youtu.be/Krgbx4SYnVg"
# yt = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
# x = yt.extract_info(url, download=False)
# print(x.get("channel"))
