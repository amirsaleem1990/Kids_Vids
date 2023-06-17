import pickle
x = pickle.load(open("mapping.pkl", 'rb'))
zakaria_urls = [k for k,v in x.items() if v['channel'] == "Learn with Zakaria - تعلم مع زكريا"]


def get_info(to_download):
	try:
		ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
		with ydl:
			x = ydl.extract_info(u, download=False) # We just want to extract the info
		if x:
			duration = x['duration']
			if int(duration) == 0:
				return
			duration = str(timedelta(seconds=int(duration)))
			if duration.split(":")[0] == "0":
				duration = "0" + duration
			n_ = ''.join([i if i in "abcdefghijklmnopqrstuvwxyzاأبتثجحخدذرزسشصضطظعغفقكلمنوهيى" else "_" for i in x.get("title").lower()])
			video_name = f"{re.sub('_+', '_', n_).strip('_')}.{x['ext']}"

			thumbnail_url = x.get("thumbnail")
			if ".jpg" in thumbnail_url:
				thumbnail_url = thumbnail_url.split(".jpg")[0] + ".jpg"
			thumbnail_name = thumbnail_url.strip().replace('/', '_')
			mapping[u] = {"channel" : x.get("channel"), 
						  "upload_date" : x.get('upload_date'), 
						  "duration" : duration, 
						  "video_name" : video_name,
						  "thumbnail_url" : thumbnail_url,
						  "thumbnail_name" : thumbnail_name,
						  'downloaded' : False
						  }
						  
		print(f'.............................{u}, Sec consumed: {time.time() - s}')
		time.sleep(2)
	except Exception as e:
		to_skip.append(u)
		print('---------------------------')
		print(e)
		print()
		errors[u] = ["download_jsons fail",e, str(datetime.now())]