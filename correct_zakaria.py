import pickle
x = pickle.load(open("mapping.pkl", 'rb'))
zakaria_urls = [k for k,v in x.items() if v['channel'] == "Learn with Zakaria - تعلم مع زكريا"]
