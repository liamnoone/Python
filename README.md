Python
======

Various python scripts

**Anime hash checker**: Anime show files can sometimes be named *"...[8 characters]..."*, 
where those 8 characters correspond to the file's CRC32 hash. 
This script gets the provided hash code, 
calculates the file's hash and compares the two to verify the file is correct.  
**CRC32.py**: Calculates a file's hash code. Used in other scripts. [Source](http://stackoverflow.com/a/2387880/1820405).  
**Duplicate.py**: Finds duplicate files in a directory by calculating a file's CRC32 and comparing to previous files.  
**Instapaper.py**: Verify Instapaper account credentials, add URLs to Instapaper account. [Requires *Requests*](http://docs.python-requests.org/en/latest/).  
**Rename.py**: Renames a file. Used in other scripts.  
**TVDb.py**: Get TVDb metadata for a directory of files. Example file name is "TVShow.SxxExx.RELEASE".
