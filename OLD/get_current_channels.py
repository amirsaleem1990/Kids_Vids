#!/usr/bin/python3

def get_channels():

	import getpass
	import pickle
	import json
	
	channels = [
		('robocar',                     "https://www.youtube.com/c/robocarpoli/videos"),
		('VladandNiki',                 "https://www.youtube.com/c/VladandNiki/videos"),
		('ChuchuTv',                    "https://www.youtube.com/c/ChuChuTVBedtimeStories/videos"),
		('scishowkids',                 'https://www.youtube.com/c/scishowkids/videos'), 
		('PeekabooKids',                'https://www.youtube.com/c/PeekabooKids/videos'),
		('MorphleTV',                   'https://www.youtube.com/c/MorphleTV/videos'),
		('Blippi',                      'https://www.youtube.com/c/Blippi/videos'),
		('CraftsforKids',               'https://www.youtube.com/c/CraftsforKids/videos'),
		('ClarendonLearning',           'https://www.youtube.com/c/ClarendonLearning/videos'),
		('FreeSchool',                  'https://www.youtube.com/c/FreeSchool/videos'),
		('KidsLearningTube',            'https://www.youtube.com/c/KidsLearningTube/videos'),
		('NUMBEROCKLLC',                'https://www.youtube.com/c/NUMBEROCKLLC/videos'),
		('natgeokids',                  'https://www.youtube.com/natgeokidsplaylists/videos'),
		('TheDadLab',                   'https://www.youtube.com/c/TheDadLab/videos'),
		('5MinuteCraftsPLAY',           'https://www.youtube.com/c/5MinuteCraftsPLAY/videos'),
		('KidsMadaniChannel',           'https://www.youtube.com/c/KidsMadaniChannel/videos'),
		('OmarHanaIslamicSongsforKids', 'https://www.youtube.com/c/OmarHanaIslamicSongsforKids/videos'),
		('officialalphablocks',         'https://www.youtube.com/c/officialalphablocks/videos'),
		('Numberblocks',                'https://www.youtube.com/c/Numberblocks/videos'),
		('PreschoolPrepCompany',        'https://www.youtube.com/c/PreschoolPrepCompany/videos'),
		('UCbxK6jzYms1iMkU9Kwvl0sA',    'https://www.youtube.com/channel/UCbxK6jzYms1iMkU9Kwvl0sA/videos'),
		('MissMollyLearning',           'https://www.youtube.com/c/MissMollyLearning/videos'),
		('allthingsanimaltv',           'https://www.youtube.com/c/allthingsanimaltv/videos'),
		('LearnWithZakaria',            'https://www.youtube.com/c/LearnWithZakaria/videos'),
		('EarthToLuna',                 'https://www.youtube.com/c/EarthToLuna/videos'),
		('MysteryDoug',                 'https://www.youtube.com/c/MysteryDoug/videos'),
		('HappyLearningTVKids',         'https://www.youtube.com/c/HappyLearningTVKids/videos'),
		('PeepWGBH',                    'https://www.youtube.com/user/PeepWGBH/videos'),
		('ComeOutsideTV',               'https://www.youtube.com/user/ComeOutsideTV/videos'),
		('UCPttFyZAvTlWAQzgRU4duJA',    'https://www.youtube.com/channel/UCPttFyZAvTlWAQzgRU4duJA/videos'),
		('OfficialBerenstainBears',     'https://www.youtube.com/c/OfficialBerenstainBears/videos'),
		('SmileandLearnEnglish1',       'https://www.youtube.com/c/SmileandLearnEnglish1/videos'),
		('UC4p_YSvJlJpEhAh5PMyhkiQ',    'https://www.youtube.com/channel/UC4p_YSvJlJpEhAh5PMyhkiQ/videos'),
		('LearningTimeFun',             'https://www.youtube.com/c/LearningTimeFun/videos'),
		('Toddlerfunlearning',          'https://www.youtube.com/c/Toddlerfunlearning/videos')
	]

	to_be_exclude    = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/to_be_exclude.json", "r"))
	channels_mapping = json.load(open(f"/home/{getpass.getuser()}/github/Kids_Vids/channels_mapping.txt", "r"))

	channels_to_exclude = to_be_exclude['channel']
	if channels_to_exclude:
		l =	[k  for k,v in channels_mapping.items() if v in channels_to_exclude]
		channels = [c for c in channels if not c[0] in l]

	return channels