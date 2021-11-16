
My kids watching youtube videos, but they are playing videos they want, so i wrote these scripts. 
download_new_vides.py scrap videos from sepecific channels, and open_html.py create an HTML file with all downloaded videos, and open that page in chromium.

on my home laptop i created 2 users, and at home user i desabled internet connectivity (sudo iptables -A OUTPUT -m owner --uid-owner home -j REJECT), now kids user (home) don't have internet. when laptop power-on the download_new_vides.py script start scraping (on other user), and at same time open_html.py open html file in chromium.
