import os
import sys

def Rename(file, new_name, seperator=os.sep, extension="", extensions=[]):
	if not os.path.exists(file):
		raise FileNotFoundError("File does not exist")

	else:
		directory = seperator.join(file.split(seperator)[0:-1])
		file_name = file.split(seperator)[-1]
		extension = file.split(os.extsep)[-1]
		
		os.rename(file, os.path.join(directory, new_name + os.extsep + extension))
		
		# If the last word delimited by the extension seperator (usually '.'), print all but that word, otherwise print the full word (incase there isn't an extension)
		
		print(os.extsep.join(file_name.split(os.extsep)[0:-1]) if ExtensionCheck(extension, extensions) else file_name, "->", new_name)

def ExtensionCheck(string, array):
	array = [str.lower() for str in array]
	return string in array

if __name__ == '__main__':
	print("Args:", len(sys.argv))
	if len(sys.argv) == 3:
		Rename(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		Rename(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		raise AttributeError("Couldn't process. 2-3 Arguments expected:\n1. File\n2. New name\n3. Optional: Seperator")
