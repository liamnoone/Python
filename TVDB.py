#!/usr/bin/python3
import re
import os
import requests
import sys
import Rename as r
from bs4 import BeautifulSoup


# TVDb API Key
API_KEY = "C2AA47AACAA7C7B2"
# The file types the script will work on
FILE_TYPES = ["AVI", "MP4", "MKV", "SRT"]
# Characters which aren't allowed in file names
ILLEGAL_CHARACTERS = ["/", "\\", ":", "*", "?", "\"", "<", ">", "|", "/"]
# Character to replace those characters with
REPLACE_CHAR = "_"
# Pad out the season/episode with zeros to desired length
SEASON_PADDED_ZEROS = 1
EPISODE_PADDED_ZEROS = 2
# What to filter out of the file name, the goal being to leave only the TV Show, Season # and Episode #
FILTER = r"\.|-|_|\b(S?(\d+)+?x?E?(\d+)+?)\b|(\(.+\))|(\[.+\])|(\-.+\-)|\s-.+\s*|\b(\d{4})\b| \
         480p|480i|720p|720i|1080p|1080i|HDTV|H\.264|x264|XviD|BluRay|MMI|WEB-DL|DD5\.1|AAC2\.0|DTS|INTERNAL|REPACK|PROPER|ReEnc| \
         IMMERSE|EVOLVE|YIFY|PublicHD|CTU|RED|DIMENSION|AFG|MIKY|KILLERS|IMMERSE|DeeJayAhmed|REMARKABLE|tla|2hd"
# The language to return episode data from TVDb for. English is the only tested language
LANGUAGE = "en" 

class TVShow:
    def __init__(self, tvshow):
        self.tvshow = tvshow
        self.series = 0
        self.season = 0
        self.episode = 0
        self.title = ""

    def __str__(self):
        return "{0} - {1}x{2} - {3}".format(self.tvshow, 
                                            self.season.zfill(SEASON_PADDED_ZEROS), 
                                            self.episode.zfill(EPISODE_PADDED_ZEROS), 
                                            self.title)

    def process(self):
        release = re.findall("S?(\d+)x?E?(\d+)", self.tvshow, flags=2)
        if len(release) > 0:
            self.season = release[0][0].lstrip("0") if len(re.findall("^0+$", release[0][0])) == 0 else "0"
            self.episode = release[0][1].lstrip("0") if len(re.findall("^0+$", release[0][1])) == 0 else "0"

        # Replace any fluff from the file name
        self.tvshow = re.sub(FILTER, " ", self.tvshow, flags=2).strip()

    def fetch(self):
        r = requests.get("http://thetvdb.com/api/GetSeries.php?seriesname={0}&language={1}".format(self.tvshow, LANGUAGE))
        soup = BeautifulSoup(r.content)

        self.series = soup.find("seriesid").text
        self.tvshow = soup.find("seriesname").text

    def get_episode(self):
        r = requests.get("http://thetvdb.com/api/{0}/series/{1}/default/{2}/{3}/{4}.xml"
            .format(API_KEY, self.series, str(self.season), str(self.episode), LANGUAGE))

        if r.status_code == 404: print("Error! 404: Not found")
        else: self.title = BeautifulSoup(r.content).find("episodename").text

    def replace_illegal_characters(self):
        for illegal_character in ILLEGAL_CHARACTERS:
            self.title = self.title.replace(illegal_character, REPLACE_CHAR)

        # Replace the ellipsis with three periods to prevent UnicodeError
        self.title = self.title.replace("…",  "...")


def process_files(directory):
    if os.path.isdir(directory):
        print("Processing...\n")
        for file_ in os.listdir(directory):
            split = file_.split(os.extsep)
            if split[-1].upper() in FILE_TYPES:
                tvshow = TVShow(os.extsep.join(split[0:-1]))
                tvshow.process()
                try:
                    tvshow.fetch()
                except AttributeError:
                    print("Skipped:", file_)
                    continue
                tvshow.get_episode()
                tvshow.replace_illegal_characters()
                r.rename(os.sep.join([directory, file_]), str(tvshow),
                         extension=split[-1], extensions=FILE_TYPES)

        print("\nProcessing complete.")
    else:
        raise IOError("Directory doesn't exist!")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        process_files(sys.argv[1])
    else:
        print("Missing target Directory")
