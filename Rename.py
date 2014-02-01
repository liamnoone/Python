import os
import sys

def Rename(file, new_name, extension="", extensions=[]):
	if not os.path.exists(file):
		raise FileNotFoundError("File does not exist")

	else:
		directory = os.sep.join(file.split(os.sep)[0:-1])
		file_name = os.extsep.join(file.split(os.sep)[-1].split(os.extsep)[0:-1])
		extension = file.split(os.extsep)[-1]

		# If the last word delimited by the extension seperator (usually '.') is an extension, 
		# print all but that word, otherwise print the full word (incase there isn't an extension)

		# Check if the file will actually be a different filename, rename if it will
		if file_name == new_name:
			output = "No change: " + new_name

		else: 
			os.rename(file, os.path.join(directory, os.extsep.join([new_name, extension])))
			output = (file_name if ExtensionCheck(extension, extensions) else os.extsep.join([file_name, extension])) + " -> " + new_name

		print(output)

def ExtensionCheck(string, array):
	return string.lower() in [str.lower() for str in array]

if __name__ == '__main__':
	print("Args: ", len(sys.argv))
	if len(sys.argv) == 3:
		Rename(sys.argv[1], sys.argv[2])
	elif len(sys.argv) == 4:
		Rename(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		raise AttributeError("Couldn't process. 2-3 Arguments expected:\n \
			1. File\n2. New name\n3. Optional: Seperator")
