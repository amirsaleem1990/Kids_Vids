#!/usr/bin/bash
sleep 2s
cd /home/home/github/Kids_Vids/Kids_Vids_Jango
python3 manage.py  runserver &
chromium http://127.0.0.1:8000/

