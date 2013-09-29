from bs4 import BeautifulSoup
import requests
import re

url = "http://timetables.itsligo.ie:81/reporting/individual;student+set;id;SG_KSDEV_07%2FF%2FY3%2F1%2F%28A%29%0D%0A?t" \
      "=student+set+individual&days=1-5&weeks=4&periods=3-20&template=student+set+individual"
data = requests.get(url)

soup = BeautifulSoup(''.join(str(data.content)))
rooms = []
classes = {}


print(soup.__iter__())
