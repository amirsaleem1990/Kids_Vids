import pickle
import os
x = pickle.load(open("/home/home/github/Kids_Vids/mapping.pkl", 'rb'))
s = """<!DOCTYPE html><html><body><div id="contents">"""
def func_(vid, img):
    if 'robo' in vid.lower(): print(vid)
    img = f'/home/home/thumbnail/{img}'    
    # print(os.path.exists(vid) and os.path.exists(img))
    return f"""\n<video width="320" height="240" controls  poster="{img}"><source src="{vid}" type="video/mp4"></source></video>"""
for k,v in x.items():
    s += func_(*v[3:])
    # break

s += "\n</div></body></html>"
open("dashboard.html", 'w').write(s)