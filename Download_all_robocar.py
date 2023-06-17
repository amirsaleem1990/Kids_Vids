from bs4 import BeautifulSoup
import string
import pickle
s = BeautifulSoup(open("Robocar POLI TV - YouTube.html", 'r').read(), 'lxml')
lst = []
for q in s.select("ytd-grid-video-renderer", {"class" : "style-scope ytd-grid-renderer"}):
    for i in q.select("a"):
        try:
            name = q.find("a", {"id" : "video-title"}).text.lower()
            if all( [i in string.printable for i in name]) and (not 'korean' in name) and  (not 'song' in name) and (not 'chinese' in name) and (not 'spanish' in name) and (not 'thai' in name) and (not 'portuguese' in name):
                lst.append(i['href'])
                break
        except:
            pass
x = pickle.load(open("mapping.pkl", 'rb'))
pickle.dump(lst, open("robocar-all-links.pkl", 'wb'))
