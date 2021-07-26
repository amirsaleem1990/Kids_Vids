import pickle
x = pickle.load(open("/home/amir/github/temp_work/JANGO/kids_youtuebe_app/mapping.pkl", 'rb'))
s = """<!DOCTYPE html><html><body><div id="contents">"""
def func_(vid, img):
    return f"""\n<video width="320" height="240" controls  poster="{img}"><source src="{vid}" type="video/mp4"></source></video>"""
for k,v in x.items():
    s += func_(*v)

s += "\n</div></body></html>"
open("x.html", 'w').write(s)