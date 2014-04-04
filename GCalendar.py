#!/bin/env python3

import sys
import requests
import datetime
import dateutil
import re
import math
from dateutil import parser
from bs4 import BeautifulSoup

# Add Google Calendars here. This can be extraced from the feed url, or from GCal > A Calendar's settings > Private Address [XML]
feed = [] # Your email address will probably be the default/general calendar ID
visibility = [] # public/private/private-[magic_cookie]
calendars = {}
if (len(feed) == 0) or (len(visibility) == 0): 
	print("No Events")
	sys.exit(0)
	
for f, v in zip(feed, visibility):
	full_calendar_url = "https://www.google.com/calendar/feeds/{0}/{1}/full?orderby=starttime&sortorder=ascending&max-results=3&futureevents=true".format(f, v)
	events_rss = requests.get(full_calendar_url)
	if events_rss.status_code == 200:
		if len(BeautifulSoup(events_rss.content).find_all("title")) == 1: continue
		event_title = BeautifulSoup(events_rss.content).find_all("title")[1].get_text()
		event_url = BeautifulSoup(events_rss.content).find_all("link")[5].get("href")
		event_rss = requests.get(event_url)
		if not event_rss.status_code == 200: continue
		else:
			event_date = dateutil.parser.parse(BeautifulSoup(event_rss.content).find("gd:when").get("starttime"))
			seconds = math.floor((event_date.replace(tzinfo=None) - datetime.datetime.now()).total_seconds())
			minutes = math.ceil(seconds / 60)
			hours = round(seconds / 3600, 1)
			days = round(seconds / 86400, 1)
		
			duration, units = (days, "days") if days > 1 else (hours, "hrs") if hours > 1 else (minutes, "mins") if minutes > 1 else (seconds, "secs") if seconds > 0 else (0, "")
			calendars[event_date.replace(tzinfo=None)] = event_title +  ' - ' + re.sub("( @ 00:00:00|:00)$", "",  event_date.strftime("%D @ %T"))
			if (duration > 0): calendars[event_date.replace(tzinfo=None)] += " (" + str(duration) + " " + units + ")"
	else: continue
	
first_event = None
output = ""
for date, event in calendars.items():
	if (first_event is None) or (date < first_event):
		first_calendar = date
		output = event
		
print("No Events" if output == "" else output)	
