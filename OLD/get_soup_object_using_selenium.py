def get_soup_object_using_selenium(url, visual=False, urls=True):
	from selenium import webdriver
	from bs4 import BeautifulSoup
	
	# url = input("Enter your url: ")
	# visusl = True if input("Visual or not? [y|n]") in ['y', 'Y'] else False

	if visual:
		browser = webdriver.Firefox(executable_path = "geckodriver")
	else:
		from selenium.webdriver.firefox.options import Options
		options = Options()
		options.add_argument("--headless")
		browser = webdriver.Firefox(executable_path = "geckodriver", options=options)

	browser.get(url)
	s = BeautifulSoup(browser.page_source, "lxml")
	extrected_urls = []
	if urls:
		for i in s.select("a"):
			try:
				l = i['href']
				extrected_urls.append(l)
			except:
				pass
		for i in s.select("source"):
			try:
				l = i['src']
				extrected_urls.append(l)
			except:
				pass
		# print(f"\nA tuple is returned, 1st vlues is urls, 2nd value is BeautifulSoup object\nThere are {len(extrected_urls)} urls\n")
		print(f"\nA tuple is returned, 1st vlues is urls, 2nd value is BeautifulSoup object\n")
	return (set(extrected_urls), s)
