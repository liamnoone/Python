import re
import os
import requests
import xml.etree.ElementTree as et
import sys

# TVDb API Key
API_KEY = ""
# The file types the script will work on
FILE_TYPES = ["AVI", "MP4", "MKV"]
# Characters which aren't allowed in file names
ILLEGAL_CHARACTERS = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|"]
# Character to replace those characters with
REPLACE_CHAR = "-"
SEASON_PADDED_ZEROS = 1
EPISODE_PADDED_ZEROS = 2
FILTER = 	r"\.|-|_|\b(S?(\d+)+?x?E?(\d+)+?)\b|(\(.+\))|(\[.+\])|(\-.+\-)|\s-.+\s*|\b(\d{4})\b|480p|480i|720p|720i|1080p|1080i|HDTV|H\.264|x264|XviD|BluRay|MMI|WEB-DL|DD5\.1|AAC2\.0|DTS|IMMERSE|EVOLVE|YIFY|PublicHD|CTU|RED|DIMENSION|AFG"	

class Media:
	def __init__(self, title):
		self.title = title
		self.year = 0000
		self.season = 0
		self.episode = 0

	def __str__(self):
		return "{0} - {1}x{2} - {3}".format(self.title, self.season.zfill(SEASON_PADDED_ZEROS), self.episode.zfill(EPISODE_PADDED_ZEROS), self.name)

	def Process(self):
		# Get the year (for movies)
		self.year = re.findall('[\.\-\(\[](\d{4})[\.\-\(\[]', self.title, flags=2)
		if self.year.__len__() > 0: self.year = self.year[0]
		else: self.year = 0000

		# Get the season and episode (for TV Shows)
		release = re.findall("S?(\d+)x?E?(\d+)", self.title, flags=2)
		if release.__len__() > 0:
			self.season = release[0][0].lstrip("0")
			self.episode = release[0][1].lstrip("0")

		#   Replace any fluff from the file name
		self.title = re.sub(FILTER, " ", self.title, flags=2).strip()
		return self.title, self.year, self.season, self.episode

	def TV_ID(self):
		r = requests.get("http://thetvdb.com/api/GetSeries.php?seriesname={0}&language=en".format(self.title))
		for element in et.fromstring(r.content).iter("seriesid"):
			self.seriesID = element.text
			break
		return self.seriesID or None

	def TV_Episode(self):
		r = requests.get("http://thetvdb.com/api/{0}/series/{1}/default/{2}/{3}/en.xml"
			.format(API_KEY, self.seriesID, str(self.season).lstrip("0"), str(self.episode).lstrip("0")))
		if r.status_code == 404: print("Error! 404: Not found")
		else:
			for element in et.fromstring(r.content):
				for el in element:
					if el.tag == "EpisodeName":
						self.name = el.text
						return self.name


def TV_ProcessFiles(directory):
	if os.path.exists(directory):
		print("Processing...\n")
		for file in os.listdir(directory):
			split = file.split(os.extsep)
			if split[-1].upper() in FILE_TYPES:
				media = Media(os.extsep.join(split[0:-1]))
				media.Process()
				try: media.TV_ID()
				except AttributeError:
					print("* Error, skipping:", file)
					continue
				media.TV_Episode()
				m = str(media)
				for char in ILLEGAL_CHARACTERS:	m = m.replace(char, REPLACE_CHAR)
				os.rename(directory + os.altsep + file, directory + os.altsep + m + os.extsep + split[-1].lower())
				print(os.extsep.join(split[0:-1]), "->", m)
	else: raise IOError("Directory doesn't exist!")

if __name__ == "__main__":
	di = "".join(sys.argv[1:])
	if (di):
		if not di[-1] == "\\": di += "\\"
		if os.path.exists(di) and di != "\\": TV_ProcessFiles(di)
		else: TV_ProcessFiles("D:\.TV Series")
	print("\nProcessing Complete!")